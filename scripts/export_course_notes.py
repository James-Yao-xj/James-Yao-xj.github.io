"""Export PKUcourseNote sources as static pages in the site's shared layout.

Requires Typst 0.15.1 and lxml. The input is a local source checkout. The
revision argument records the exact source commit in the generated catalog.
"""

import argparse
import base64
import hashlib
import html as html_text
import json
import re
import shutil
import subprocess
import tempfile
from pathlib import Path
from urllib.parse import quote

from lxml import etree, html

SITE = Path(__file__).resolve().parents[1]
READING_ROOT = '/learning/school-note/'
SOURCE_REPO = 'https://github.com/James-Yao-xj/PKUcourseNote'
COURSE_TOPICS = json.loads((SITE / '_data/course_topics.json').read_text())
COURSES = [
    ('Semester3/ICS', 'ics', '计算机系统导论', 3),
    ('Semester3/DataStructureAlgorithm', 'data-structures', '数据结构与算法', 3),
    ('Semester3/IDM', 'discrete-mathematics', '离散数学基础', 3),
    ('Semester3/ProbabilityTheoryAndStatistics', 'probability', '信息学中的概率统计', 3),
    ('Semester3/PrinciplesOfEconomics', 'economics', '经济学原理', 3),
    ('Semester3/SetTheoryAndGraphTheory', 'set-theory', '集合论与图论', 3),
    ('Semester2/WesternModernPhi', 'western-philosophy', '西方现代哲学', 2),
]
PHILOSOPHERS = [
    ('Nietzsche', 'Nietzsche', '尼采'), ('Frege', 'Frege', '弗雷格'),
    ('Russell', 'Russell', '罗素'), ('Wittgenstein', 'Wittgenstein', '维特根斯坦'),
    ('Heidegger', 'Heidegger', '海德格尔'), ('Langer', 'Langer', '朗格'),
    ('Gödel', 'Godel', '哥德尔'), ('Arendt', 'Arendt', '阿伦特'),
    ('Quine', 'Quine', '奎因'), ('Turing', 'Turing', '图灵'),
    ('Murdoch', 'Murdoch', '默多克'), ('Kuhn', 'Kuhn', '库恩'),
    ('Kripke', 'Kripke', '克里普克'),
]
ICS_TITLES = {
    'Lec1': ('small-class-1', '小班课第一讲'),
    'Lesson1': ('lesson-1', '第一讲：计算机系统漫游'),
    'Lesson2': ('lesson-2', '第二讲：位、字节与整数'),
    'Lesson3': ('lesson-3', '第三讲：浮点数'),
    'Lesson4': ('lesson-4', '第四讲：机器级程序基础'),
    'Lesson5': ('lesson-5', '第五讲：控制'),
    'Lesson6': ('lesson-6', '第六讲：过程'),
    'Lesson7': ('lesson-7', '第七讲：数组、结构体与浮点指令'),
    'Lesson8': ('lesson-8', '第八讲：联合体、地址空间与缓冲区溢出'),
    'Lesson9': ('lesson-9', '第九讲：处理器架构与逻辑设计'),
    'Lesson10': ('lesson-10', '第十讲：SEQ 顺序实现'),
    'Lesson11': ('lesson-11', '第十一讲：流水线与冒险处理'),
    'LabGuide': ('lab-guide', '实验与浮点讨论课'),
    'BombLab': ('bomb-lab', 'Bomb Lab：汇编分析与调试'),
    'ICS_知识重点总结': ('summary', 'ICS 知识重点总结'),
}
SUPPLEMENTS = {
    ('data-structures', 'DevEnvironment'): ('development-environment', '开发环境与上机基础', 100),
    ('discrete-mathematics', 'NumberTheory'): ('number-theory', '初等数论', 100),
    ('economics', 'Optimization'): ('optimization', '习题课：约束优化与 KKT', 100),
    # Keep these handwritten topics after Lesson4, as in the source main.typ.
    ('set-theory', 'RelationClosure'): ('relation-closure', '关系闭包', 4.1),
    ('set-theory', 'EquivalenceAndOrder'): ('equivalence-and-order', '等价关系、划分与偏序', 4.2),
    ('set-theory', 'Functions'): ('functions', '函数的基本概念', 4.3),
}

# Preserve content that the HTML exporter does not yet handle by default.
# Only equations use SVG. Prose, code, lists, and tables remain HTML.
PRELUDE = '''#show align: it => it.body
#show pad: it => it.body
#show grid: it => table(columns: it.columns, ..it.children.map(cell => cell.body))
#show math.equation: it => {
  if it.block {
    html.elem("div", attrs: (class: "note-equation", role: "math", "aria-label": repr(it.body)), html.frame(it))
  } else {
    html.elem("span", attrs: (class: "note-math", role: "math", "aria-label": repr(it.body)), html.frame(box(it)))
  }
}
'''


def write_page(path, title, url, body, reader=False):
    """Write a Jekyll page with the existing site layout and a fixed URL."""
    fields = {'layout': 'single', 'title': title, 'permalink': url,
              'author_profile': True, 'course_note': reader}
    frontmatter = '\n'.join(f'{key}: {json.dumps(value, ensure_ascii=False)}'
                            for key, value in fields.items())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(f'---\n{frontmatter}\n---\n\n{body}\n', encoding='utf-8')


def link(url, label):
    """Return a site link that also works with a Jekyll base URL."""
    prefix = '' if url.startswith('#') else '{{ site.baseurl }}'
    return f'<a href="{prefix}{url}">{html_text.escape(label)}</a>'


def chapter_metadata(path, course):
    """Return the stable URL, display title, and reading order for a source."""
    if course == 'western-philosophy':
        order, item = next((i, p) for i, p in enumerate(PHILOSOPHERS) if p[0] == path.stem)
        language = 'en' if path.parent.name == 'EnglishVersion' else 'zh'
        title = item[0] if language == 'en' else f'{item[2]}（{item[0]}）'
        return f'{language}/{item[1].lower()}', title, (language, order)
    if course == 'ics':
        slug, title = ICS_TITLES[path.stem]
        number = re.search(r'\d+', path.stem)
        return slug, title, (int(number[0]) if number else 100, path.stem)
    if (course, path.stem) in SUPPLEMENTS:
        slug, title, position = SUPPLEMENTS[(course, path.stem)]
        return slug, title, (position, path.stem)
    number = int(re.search(r'\d+', path.stem)[0])
    slug = f'lesson-{number}'
    topic = COURSE_TOPICS[course]['topics'][slug]
    return slug, f'第 {number} 讲：{topic}', (number, path.stem)


def prepare_sources(source, staging):
    """Copy content and assets, then remove only the PDF template import."""
    shutil.copytree(source, staging, ignore=shutil.ignore_patterns('.git', '.DS_Store', '.*export*'))
    template = ('#import "@preview/ctyp:0.3.0": ctyp\n'
                '#let (ctypset, cjk) = ctyp()\n'
                '#let (song, hei, kai, fang) = cjk\n#show: ctypset')
    for path in staging.rglob('*.typ'):
        path.write_text(path.read_text(encoding='utf-8').replace(template, ''), encoding='utf-8')


def clean_html(document, image_assets):
    """Keep semantic content and deduplicate repeated equation glyphs.

    Args:
        document: Standalone HTML produced by Typst.
        image_assets: Map from site asset paths to decoded image bytes.

    Returns:
        A body fragment and a linked section outline.
    """
    body = html.fromstring(document).xpath('//body')[0]
    symbols = {}
    for definitions in body.xpath('.//svg/defs'):
        for symbol in definitions:
            symbols[symbol.attrib['id']] = etree.tostring(symbol, encoding='unicode', method='html')
        definitions.getparent().remove(definitions)
    for node in body.xpath('.//svg//*[@fill="#000000"]'):
        node.attrib['fill'] = 'currentColor'
    for node in body.xpath('.//svg//*[@stroke="#000000"]'):
        node.attrib['stroke'] = 'currentColor'
    for image in body.xpath('.//img'):
        header, encoded = image.attrib['src'].split(',', 1)
        content = base64.b64decode(encoded)
        extension = 'svg' if 'svg+xml' in header else header.split('/')[1].split(';')[0]
        asset = f'assets/course-notes/{hashlib.sha256(content).hexdigest()[:20]}.{extension}'
        image_assets[asset] = content
        image.attrib.update({'src': '{{ site.baseurl }}/' + asset,
                             'alt': '课程笔记中的原始插图', 'loading': 'lazy'})
        image.attrib.pop('style', None)
    # Wide tables scroll within the article instead of widening the page.
    for table in body.xpath('.//table'):
        wrapper = etree.Element('div', {'class': 'note-table', 'tabindex': '0', 'role': 'region', 'aria-label': '课程笔记表格'})
        table.addprevious(wrapper)
        wrapper.append(table)
    outline = []
    for index, heading in enumerate(body.xpath('.//h1|.//h2|.//h3|.//h4|.//h5|.//h6'), 1):
        if 'id' not in heading.attrib:
            heading.attrib['id'] = f'section-{index}'
        if heading.tag in ('h1', 'h2', 'h3'):
            label = heading.text_content()
            outline.append(f'<li>{link("#" + heading.attrib["id"], label)}</li>')
    result = (body.text or '') + ''.join(etree.tostring(node, encoding='unicode', method='html') for node in body)
    result = result.replace('{{%20site.baseurl%20}}', '{{ site.baseurl }}')
    if symbols:
        definitions = ''.join(symbols.values()).replace('fill="#000000"', 'fill="currentColor"').replace('stroke="#000000"', 'stroke="currentColor"')
        result += '<svg class="note-symbols" aria-hidden="true" xmlns="http://www.w3.org/2000/svg"><defs>' + definitions + '</defs></svg>'
    return result, ''.join(outline)


def compile_source(staging, source, output, image_assets):
    """Compile one source and return its HTML body and section outline."""
    wrapper = staging / '.export.typ'
    wrapper.write_text(PRELUDE + '#include ' + json.dumps('/' + source, ensure_ascii=False))
    result = subprocess.run(['typst', 'compile', '--features', 'html', '--root', str(staging),
                             str(wrapper), str(output), '--diagnostic-format', 'short'],
                            capture_output=True, text=True)
    with (SITE / 'local/course-note-export.log').open('a', encoding='utf-8') as stream:
        stream.write(source + '\n' + result.stderr + '\n')
    result.check_returncode()
    return clean_html(output.read_text(), image_assets)


def link_slide_map(content, catalog, aliases):
    """Link note paths within each course section of the slide index.

    Course context is required because several courses use Lesson1.typ.
    """
    document = html.fragment_fromstring(content, create_parent='div')
    routes_by_title = {}
    for folder, course, title, semester in COURSES:
        chapters = next(item['chapters'] for item in catalog if item['slug'] == course)
        routes = {chapter['source'][len(folder) + 1:]: chapter['url'] for chapter in chapters}
        targets = {chapter['source']: chapter['url'] for chapter in chapters}
        for alias, target in aliases.items():
            if target in targets:
                routes[alias[len(folder) + 1:]] = targets[target]
        routes_by_title[title] = routes
    routes = {}
    for child in list(document):
        if child.tag == 'h2':
            title = re.sub(r'^\d+\.\s*', '', child.text_content())
            routes = routes_by_title.get(title, {})
        elif child.tag == 'p' and routes and not child.xpath('.//a'):
            pattern = '|'.join(re.escape(path) for path in sorted(routes, key=len, reverse=True))
            pattern = r'(?<![\w./])(?:' + pattern + r')(?![\w./])'
            paragraph = etree.tostring(child, encoding='unicode', method='html')
            linked = re.sub(pattern, lambda match: link(routes[match[0]], match[0]), paragraph)
            document.replace(child, html.fragment_fromstring(linked))
    return ''.join(etree.tostring(child, encoding='unicode', method='html') for child in document).replace('{{%20site.baseurl%20}}', '{{ site.baseurl }}')


def export(source, revision):
    """Compile all chapters, then write course indexes and the source catalog."""
    pages = SITE / '_pages/learning/school-note'
    assets = {}
    catalog = []
    aliases = {}
    log = SITE / 'local/course-note-export.log'
    log.parent.mkdir(exist_ok=True)
    log.write_text('')
    with tempfile.TemporaryDirectory(prefix='course-html-') as temporary:
        staging = Path(temporary) / 'source'
        prepare_sources(source, staging)
        for folder, course, name, semester in COURSES:
            chapters = []
            for path in (staging / folder).rglob('*.typ'):
                if path.name == 'main.typ':
                    continue
                # A forwarding source must not create a second chapter URL.
                forwarded = re.fullmatch(r'\s*#include\s+"([^"]+)"\s*', path.read_text())
                if forwarded:
                    target = (path.parent / forwarded[1]).resolve().relative_to(staging.resolve())
                    aliases[path.relative_to(staging).as_posix()] = target.as_posix()
                    continue
                slug, title, order = chapter_metadata(path, course)
                chapters.append({'slug': slug, 'title': title, 'order': order,
                                 'source': path.relative_to(staging).as_posix()})
            chapters.sort(key=lambda item: item['order'])
            course_url = READING_ROOT + course + '/'
            for index, chapter in enumerate(chapters):
                output = Path(temporary) / 'chapter.html'
                content, outline = compile_source(staging, chapter['source'], output, assets)
                url = course_url + chapter['slug'] + '/'
                chapter['url'] = url
                crumb = '<nav aria-label="笔记导航">' + link(READING_ROOT, 'SchoolNote') + ' · ' + link(course_url, name) + '</nav>'
                toc = '<details class="note-toc"><summary>本页目录</summary><ul>' + outline + '</ul></details>' if outline else ''
                neighbors = []
                for offset, label in [(-1, '上一篇：'), (1, '下一篇：')]:
                    position = index + offset
                    if 0 <= position < len(chapters):
                        neighbor = chapters[position]
                        if course != 'western-philosophy' or neighbor['slug'][:2] == chapter['slug'][:2]:
                            neighbors.append(link(course_url + neighbor['slug'] + '/', label + neighbor['title']))
                bottom = '<nav class="note-pagination" aria-label="章节导航">' + '<br>'.join(neighbors) + '</nav>'
                source_url = SOURCE_REPO + '/blob/' + revision + '/' + quote(chapter['source'])
                source_link = '<p class="note-source"><a href="' + source_url + '">查看原始笔记</a></p>'
                body = '<div class="course-note">' + crumb + toc + content + bottom + source_link + '</div>'
                # Raw guards keep code samples containing Liquid syntax unchanged.
                body = '{% raw %}' + body + '{% endraw %}'
                body = body.replace('{{ site.baseurl }}', '{% endraw %}{{ site.baseurl }}{% raw %}')
                write_page(pages / course / (chapter['slug'] + '.html'), name + ' · ' + chapter['title'], url, body, True)
                print(f'Exported {name} / {chapter["title"]}', flush=True)
            index_body = link(READING_ROOT, '← 返回 SchoolNote') + '<p class="section-intro">' + COURSE_TOPICS[course]['description'] + ' 按章节选择，直接在线阅读。</p>'
            if course == 'western-philosophy':
                for language, label in [('zh', '中文笔记'), ('en', 'English notes')]:
                    index_body += '<h2>' + label + '</h2><ol class="chapter-list">' + ''.join('<li>' + link(c['url'], c['title']) + '</li>' for c in chapters if c['slug'].startswith(language + '/')) + '</ol>'
            else:
                index_body += '<ol class="chapter-list">' + ''.join('<li>' + link(c['url'], c['title']) + '</li>' for c in chapters) + '</ol>'
            write_page(pages / course / 'index.html', name, course_url, index_body)
            catalog.append({'slug': course, 'title': name, 'semester': semester, 'url': course_url,
                            'chapters': [{k: v for k, v in c.items() if k != 'order'} for c in chapters]})
        resource = {'slug': 'slide-map', 'title': '课件与笔记对应表',
                    'source': 'Semester3/课件对应表.typ', 'url': READING_ROOT + 'slide-map/'}
        content, outline = compile_source(staging, resource['source'], Path(temporary) / 'slide-map.html', assets)
        breadcrumb = '<nav aria-label="笔记导航">' + link(READING_ROOT, 'SchoolNote') + ' · 课件与笔记对应表</nav>'
        toc = '<details class="note-toc"><summary>本页目录</summary><ul>' + outline + '</ul></details>'
        content = link_slide_map(content, catalog, aliases)
        source_link = '<p class="note-source"><a href="' + SOURCE_REPO + '/blob/' + revision + '/' + quote(resource['source']) + '">查看原始笔记</a></p>'
        body = '<div class="course-note">' + breadcrumb + toc + content + source_link + '</div>'
        body = '{% raw %}' + body + '{% endraw %}'
        body = body.replace('{{ site.baseurl }}', '{% endraw %}{{ site.baseurl }}{% raw %}')
        write_page(pages / 'slide-map.html', resource['title'], resource['url'], body, True)
    for path, content in assets.items():
        target = SITE / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(content)
    data = {'repository': SOURCE_REPO, 'revision': revision, 'courses': catalog,
            'aliases': aliases, 'resources': [resource]}
    (SITE / '_data/course_notes.json').write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')
    print(f'Exported {sum(len(c["chapters"]) for c in catalog)} chapters in {len(catalog)} courses.', flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source', type=Path, help='Local PKUcourseNote checkout')
    parser.add_argument('--revision', required=True, help='Exact PKUcourseNote commit SHA')
    arguments = parser.parse_args()
    export(arguments.source.resolve(), arguments.revision)
