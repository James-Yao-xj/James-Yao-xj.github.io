# 姚行健的个人网站

[打开网站](https://James-Yao-xj.github.io) · [内容修改指南](docs/EDITING.md) · [课程笔记更新指南](docs/COURSE_NOTES.md)

本站使用 Jekyll，主题基于 Academic Pages / Minimal Mistakes。日常更新通常只需修改 Markdown、YAML 或图片。

## 常用文件

| 要修改的内容 | 位置 |
| --- | --- |
| 首页自我介绍 | `_pages/site/home.md` |
| 生活动态与照片 | `_news/`、`images/news/` |
| 博客文章 | `_posts/`（新文章按 `YYYY-MM-DD-title.md` 命名） |
| 项目列表 | `_data/projects.yml` |
| 论文与下载文件 | `_publications/`、`files/` |
| 教学经历 | `_teaching/` |
| 简历 | `_pages/site/cv.md` |
| 顶部导航 | `_data/navigation.yml` |
| 姓名、头像、社交链接与站点服务 | `_config.yml` |
| 五语界面与介绍译文 | `assets/js/site-translations.js` |
| Learning 入口与课程说明 | `_pages/learning/`、`_data/course_topics.json` |
| 自主学习专题 | `learning/self-study/` |

**课程笔记正文由独立的 [PKUcourseNote](https://github.com/James-Yao-xj/PKUcourseNote) 仓库生成。** `_pages/learning/school-note/`、`_data/course_notes.json` 和 `assets/course-notes/` 是生成结果。请先修改源笔记，再按[课程笔记更新指南](docs/COURSE_NOTES.md)导出网页。

`_layouts/`、`_includes/`、`_sass/` 和 `assets/css/` 控制结构与样式。`assets/js/site-ui.js` 处理导航、主题和笔记阅读交互；页面直接加载它，无需前端打包。

## 本地预览与发布

需要 Ruby 和 Bundler。在仓库根目录运行：

```bash
bundle install
bundle exec jekyll serve --livereload
```

打开 <http://localhost:4000>。修改 `_config.yml` 后要重启预览服务。提交并推送到 `main` 后，GitHub Pages 自动构建并发布网站；可在仓库的 **Actions** 页面检查结果。

发布前打开首页和本次修改的页面，检查手机宽度下的排版、图片、链接和语言切换。新增内容的示例见[内容修改指南](docs/EDITING.md)。

页脚访问次数已连接 GoatCounter。读者留言区域已预留，尚未启用；配置说明见[内容修改指南](docs/EDITING.md#访问统计与读者留言)。

站点内容归姚行健所有。主题来源与许可见 [LICENSE](LICENSE)。
