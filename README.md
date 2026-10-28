# 姚行健（James Yao）的个人网站

这是 [James-Yao-xj.github.io](https://James-Yao-xj.github.io) 的源代码仓库。站点使用 Jekyll 构建，主题基于 [Academic Pages](https://github.com/academicpages/academicpages.github.io)。

## 常用内容在哪里

| 想修改的内容 | 文件或目录 |
| --- | --- |
| 姓名、简介、头像、社交链接、站点设置 | `_config.yml` |
| 顶部导航 | `_data/navigation.yml` |
| 项目介绍与仓库入口 | `_data/projects.yml`、`_pages/sections/project.html` |
| 主页 | `_pages/site/home.md` |
| 中英文简历 | `_pages/site/cv.md` |
| 简历样式 | `assets/css/cv-layout.scss`、`tokens.css` |
| 学习入口和课程笔记入口 | `_pages/learning/` |
| 长篇自主学习内容 | `learning/` |
| 博客文章 | `_posts/` |
| 生活动态 | `_news/`、`_pages/sections/news.html` |
| 文章 / 出版物 | `_publications/` |
| 教学 | `_teaching/` |
| PDF 等下载文件 | `files/` |
| 头像、主页图片、站点图标 | `images/` |

更多人工修改示例见 [`docs/EDITING.md`](docs/EDITING.md)；课程笔记更新步骤见 [`docs/COURSE_NOTES.md`](docs/COURSE_NOTES.md)。

## 内容目录约定

```text
_pages/
├── site/       # 首页、404、CV 等站点核心页面
├── learning/   # Learning、SchoolNote、SelfStudy 入口
├── sections/   # Publications、Teaching、Project 栏目入口
└── archives/   # 博客年份、分类、标签归档

_posts/         # 博客正文，文件名格式 YYYY-MM-DD-title.md
_news/          # News 动态，按 front matter 中的 date 倒序展示
_publications/  # 文章与论文条目
_teaching/      # 教学条目
```

这些页面都使用固定的 `permalink`，整理源文件位置不会改变站点上的公开网址。

## 本地预览

需要 Ruby 和 Bundler：

```bash
bundle install
bundle exec jekyll serve -l -H localhost
```

浏览器打开 <http://localhost:4000>。修改 `_config.yml` 后需要重启 Jekyll；修改 Markdown、HTML 或样式时通常会自动重建。

全站导航与阅读交互直接使用 `assets/js/site-ui.js`，修改后不需要重新打包前端脚本。

News 页面按日期展示 `_news/` 下的摘要卡片；点击卡片进入动态详情，首页也会链接最新两条。每条至少填写 `title`、`date` 和 `summary`；如需照片，可填写 `photos` 列表，每张照片包含 `image`（以 `/images/` 开头的网站路径）和 `alt`。完整正文写在 front matter 后。新动态中的文字若需五语切换，请在 `assets/js/site-translations.js` 添加对应译文。

## 访问统计与读者留言

全站页脚已连接 GoatCounter 访问次数；SchoolNote 正文、News 详情和博客正文末尾已预留读者留言。留言目前显示准备状态。配置方式：

1. GoatCounter 站点地址已填写在 `_config.yml` 的 `visitor_stats.goatcounter_url`。如需更换站点，在新账号中启用网站上显示计数的选项，再更新此地址。计数不能补算启用前的访问。
2. GitHub Discussions 已在本站仓库启用。为该仓库安装 [giscus GitHub App](https://github.com/apps/giscus)，然后将 `_config.yml` 的 `reader_comments.enabled` 改为 `true`。仓库与 Announcements 分类的标识已填好；评论按页面路径分别保存。

## 发布

推送到 GitHub 后由 GitHub Pages 自动构建。提交前建议至少检查：首页、Learning、Publications、Teaching、Blog Posts 和 CV。

## 许可与来源

站点内容归姚行健所有。主题代码来自 Academic Pages / Minimal Mistakes，相关许可见 `LICENSE`。

## 课程笔记网页版

SchoolNote 的课程和章节都在本站阅读，页面继续使用统一的 `single` 布局。正文由 PKUcourseNote 的 Typst 源文件生成，公式用 SVG 保留符号，文字、代码和表格保留为 HTML；原始笔记链接位于文末。

更新时准备 PKUcourseNote 的本地副本，安装 Typst 0.15.1 和 Python 依赖，再运行：

```bash
python3 -m pip install -r scripts/requirements-course-notes.txt
python3 scripts/export_course_notes.py ../PKUcourseNote --revision <源仓库提交SHA>
```

脚本会更新 `_pages/learning/school-note/`、`assets/course-notes/` 和 `_data/course_notes.json`，保留来源版本。Typst 的 HTML 导出仍在实验阶段，更新后需核对导出日志 `local/course-note-export.log`，并检查公式、表格、代码、插图、目录和章节链接，再提交发布。网站发布只需 Jekyll，不需要在访客浏览器中运行 Typst。

## 导航与阅读界面

全站交互使用 `assets/js/site-ui.js`，样式使用 `assets/css/interface.css`；保留原有主题变量和 `theme` 偏好。导航在窄屏下完整展开，支持键盘关闭和焦点循环。笔记的同一份页内目录在桌面显示为侧栏，在窄屏显示为折叠目录。

课程简介和章节主题统一保存在 `_data/course_topics.json`，更新章节主题后重新导出笔记即可同步目录、标题及章节切换链接。

### Site languages

The header language control supports Simplified Chinese, English, Traditional Chinese,
French, and Arabic. The selection is saved as `site-language` in local storage;
`?lang=fr` (or another supported locale) opens a page in a specific language.
Arabic uses right to left interface layout. Notes keep their original language and
left to right article layout, including formulas and code.

`assets/js/site-translations.js` contains five strings per row, in the order
`zh-Hans`, `en`, `zh-Hant`, `fr`, `ar`. Chinese and English source phrases identify
existing text nodes. `siteTranslationAliases` handles older section names.
Keep the original phrase when editing a translation, or update its matching source
text as well. Course lecture numbers and note counts use shared label templates.
New interface or introduction copy needs a translation row. Original note content
is excluded by `.course-note` or `data-original-language`.
