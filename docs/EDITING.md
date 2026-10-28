# 内容修改指南

从仓库根目录按下列路径找文件。修改已有页面时保留原来的 `permalink`，以免旧链接失效。

## 新增生活动态

在 `_news/` 新建 `YYYY-MM-DD-short-name.md`：

```markdown
---
title: "周末校园散步"
date: 2026-10-28
category: "校园生活"
summary: "一句话介绍这条动态。"
photos:
  - image: /images/news/2026-10-28-walk.jpg
    alt: "照片中可见的主要内容"
---

这里写完整内容。可以使用普通 Markdown。
```

照片放在 `images/news/`，`image` 必须与实际文件名一致。动态会自动进入 News 列表；首页显示最新两条。`summary` 用于列表卡片，`alt` 是图片替代文字。没有照片时，删去整个 `photos` 字段。

## 新增博客文章

在 `_posts/` 新建 `YYYY-MM-DD-short-name.md`；目录尚无文章时可直接创建：

```markdown
---
title: "一篇新的学习记录"
date: 2026-10-28
excerpt: "在列表中显示的简短介绍。"
---

正文从这里开始。
```

文章会自动进入 Blog Posts。文件名与 `date` 使用同一天。`_config.yml` 已设置博客布局、作者资料和阅读时间。

## 更新项目、论文与教学

- **项目：** 在 `_data/projects.yml` 增加条目。`id` 用不重复的英文短名。公开仓库填写 `repository_public: true` 和 `repository: "https://github.com/..."`；私有项目保持 `repository_public: false`。`homepage` 可选。
- **论文：** 参考 `_publications/` 的现有条目新建 Markdown。`title`、`date`、`excerpt`、`permalink` 分别控制标题、顺序、摘要和链接。PDF 放在 `files/`，`paperurl` 指向 `/files/文件名.pdf`。
- **教学：** 参考 `_teaching/` 的现有条目。保留 `title`、`date`、`permalink`，需要时填写 `type`、`venue` 和 `location`。

## 修改页面、导航与外观

| 内容 | 文件 |
| --- | --- |
| 首页与简历 | `_pages/site/home.md`、`_pages/site/cv.md` |
| Learning 入口 | `_pages/learning/index.md`、`_pages/learning/school-note.md`、`_pages/learning/self-study.md` |
| 栏目介绍 | `_pages/sections/` |
| 顶部菜单 | `_data/navigation.yml` |
| 头像、姓名与社交账号 | `_config.yml` 的 `author` |
| 页面样式 | `assets/css/`；设计变量在 `tokens.css` |
| 页面交互 | `assets/js/site-ui.js`、`assets/js/site-i18n.js` |

导航栏只由 `_data/navigation.yml` 控制；增删条目时确认目标页面存在。图片链接使用网站根路径，例如 `/images/photo.jpg`。

## 五语内容

`assets/js/site-translations.js` 按栏目分组。每组依次为简体中文、英文、繁体中文、法文、阿拉伯文。修改页面介绍或新增 News 文案后，搜索原句并同步更新译文；新增句子时复制一组五语条目。简体中文和英文原句用于匹配页面文字，必须与页面里的文字一致。笔记正文保留原语言。

预览时可用 `?lang=fr`、`?lang=ar` 等参数检查对应语言；阿拉伯文还要检查从右向左的排版。

## 访问统计与读者留言

页脚访问次数已连接 GoatCounter。账号地址在 `_config.yml` 的 `visitor_stats.goatcounter_url`。更换账号时修改这里，并在新账号设置中允许网站显示访问次数。统计不能补算启用前的访问。

读者留言尚未启用。仓库已开启 GitHub Discussions；启用前需给仓库安装 [giscus GitHub App](https://github.com/apps/giscus)，再把 `_config.yml` 的 `reader_comments.enabled` 改为 `true`。SchoolNote、News 详情和博客正文末尾会按页面路径分别展示留言。

## 发布前检查

1. 运行 `bundle exec jekyll build`，确认没有构建错误。
2. 打开修改的页面，检查标题、日期、图片、链接和手机宽度下的排版。
3. 若改了界面或介绍文字，切换五种语言检查；若改了笔记，按[课程笔记更新指南](COURSE_NOTES.md)核对公式与目录。
4. 推送到 `main` 后，在 GitHub **Actions** 页面确认 Pages 构建成功，再打开线上页面复查。
