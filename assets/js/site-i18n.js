/* Translate site text without changing links or original note content. */
(() => {
  const languages = ['zh-Hans', 'en', 'zh-Hant', 'fr', 'ar'];
  const root = document.documentElement;
  const selector = document.querySelector('#site-language');
  const phrases = new Map();
  const normalize = text => text.trim().replace(/\s+/g, ' ').replace(/[‘’]/g, "'").replace(/[“”]/g, '"');
  window.siteTranslations.forEach(row => {
    // Both source languages occur in the existing Jekyll pages.
    phrases.set(normalize(row[0]), row);
    phrases.set(normalize(row[1]), row);
  });
  Object.entries(window.siteTranslationAliases).forEach(([source, target]) => {
    phrases.set(source, phrases.get(target));
  });
  let language = 'zh-Hans';

  /**
   * Translate a source phrase with the current site locale.
   * @param {string} source - Original interface text or a generated course label.
   * @returns {string} Translated copy, or the source when no translation exists.
   */
  function translate(source) {
    const text = normalize(source);
    const row = phrases.get(text);
    if (row) return row[languages.indexOf(language)];
    const count = text.match(/^(\d+) (门课程|篇笔记)$/);
    if (count) return translate(`{n} ${count[2]}`).replace('{n}', count[1]);
    const lecture = text.match(/^第\s*(\d+|[一二三四五六七八九十]+)\s*讲[：:]\s*(.+)$/);
    if (lecture) {
      const numbers = ['零', '一', '二', '三', '四', '五', '六', '七', '八', '九', '十', '十一'];
      const number = /^\d+$/.test(lecture[1]) ? Number(lecture[1]) : numbers.indexOf(lecture[1]);
      return translate('第 {n} 讲：').replace('{n}', number) + translate(lecture[2]);
    }
    const lesson = text.match(/^第\s*(\d+)\s*课$/);
    if (lesson) return translate('第 {n} 课').replace('{n}', lesson[1]);
    const philosopher = text.match(/^(.+)（[^）]+）$/);
    if (philosopher && phrases.has(philosopher[1])) return translate(philosopher[1]);
    for (const prefix of ['上一篇：', '下一篇：']) {
      if (text.startsWith(prefix)) return translate(prefix) + translate(text.slice(prefix.length));
    }
    if (text.includes(' · ')) return text.split(' · ').map(translate).join(' · ');
    if (text.endsWith(' 按章节选择，直接在线阅读。')) {
      return translate(text.slice(0, -' 按章节选择，直接在线阅读。'.length)) + ' ' + translate('按章节选择，直接在线阅读。');
    }
    return source;
  }

  /** Include only interface text when a note contains untranslated content. */
  function isInterface(element) {
    if (element.closest('script, style, svg, code, pre, select')) return false;
    if (element.closest('[data-original-language]') && !element.closest('.src, .next')) return false;
    if (element.closest('.course-note')) {
      return Boolean(element.closest('.note-breadcrumb, .course-note > nav, .note-toc > summary, .note-pagination, .note-source'));
    }
    return true;
  }

  // Save source nodes once so repeated switches cannot translate translated text.
  const texts = [];
  const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
  while (walker.nextNode()) {
    const node = walker.currentNode;
    if (node.textContent.trim() && isInterface(node.parentElement)) texts.push([node, node.textContent]);
  }
  const attributes = [];
  document.querySelectorAll('[aria-label], [title], img[alt]').forEach(element => {
    if (!isInterface(element)) return;
    for (const name of ['aria-label', 'title', 'alt']) {
      if (element.hasAttribute(name)) attributes.push([element, name, element.getAttribute(name)]);
    }
  });
  const originalTitle = document.title;

  /** Apply a supported locale and keep it for the next page visit. */
  function apply(next) {
    language = next;
    root.lang = language;
    root.dir = language === 'ar' ? 'rtl' : 'ltr';
    selector.value = language;
    texts.forEach(([node, source]) => {
      const translated = translate(source);
      node.textContent = source.replace(source.trim(), translated.trim());
    });
    attributes.forEach(([element, name, source]) => element.setAttribute(name, translate(source)));
    document.title = originalTitle.split(/( - | \| )/).map(translate).join('');
    try { localStorage.setItem('site-language', language); } catch (_) { /* Keep this page usable without storage. */ }
    document.dispatchEvent(new CustomEvent('site:language', { detail: { language } }));
  }

  window.siteI18n = { translate, get language() { return language; } };
  let saved;
  try { saved = localStorage.getItem('site-language'); } catch (_) { /* Use the default locale. */ }
  const requested = new URLSearchParams(location.search).get('lang');
  apply(languages.includes(requested) ? requested : languages.includes(saved) ? saved : 'zh-Hans');
  selector.addEventListener('change', () => {
    // Remove a shared language hint after the visitor makes a new choice.
    const url = new URL(location.href);
    url.searchParams.delete('lang');
    history.replaceState(null, '', url);
    apply(selector.value);
  });
})();
