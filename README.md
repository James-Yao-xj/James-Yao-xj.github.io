# 姚行健（James Yao）的个人网站

这是 [James-Yao-xj.github.io](https://James-Yao-xj.github.io) 的源代码仓库。站点使用 Jekyll 构建，主题基于 [Academic Pages](https://github.com/academicpages/academicpages.github.io)。

## 常用内容在哪里

| 想修改的内容 | 文件或目录 |
| --- | --- |
| 姓名、简介、头像、社交链接、站点设置 | `_config.yml` |
| 顶部导航 | `_data/navigation.yml` |
| 主页 | `_pages/site/home.md` |
| 中英文简历 | `_pages/site/cv.md` |
| 简历样式 | `assets/css/cv-layout.scss`、`tokens.css` |
| 学习入口和课程笔记入口 | `_pages/learning/` |
| 长篇自主学习内容 | `learning/` |
| 博客文章 | `_posts/` |
| 文章 / 出版物 | `_publications/` |
| 教学 | `_teaching/` |
| PDF 等下载文件 | `files/` |
| 头像、主页图片、站点图标 | `images/` |

## 内容目录约定

```text
_pages/
├── site/       # 首页、404、CV 等站点核心页面
├── learning/   # Learning、SchoolNote、SelfStudy 入口
├── sections/   # Publications、Teaching 栏目入口
└── archives/   # 博客年份、分类、标签归档

_posts/         # 博客正文，文件名格式 YYYY-MM-DD-title.md
_publications/  # 文章与论文条目
_teaching/      # 教学条目
```

这些页面都使用固定的 `permalink`，整理源文件位置不会改变站点上的公开网址。

## 本地预览

需要 Ruby、Bundler 和 Node.js：

```bash
bundle install
bundle exec jekyll serve -l -H localhost
```

浏览器打开 <http://localhost:4000>。修改 `_config.yml` 后需要重启 Jekyll；修改 Markdown、HTML 或样式时通常会自动重建。

如需重新生成压缩后的前端脚本：

```bash
npm install
npm run build:js
```

## 发布

推送到 GitHub 后由 GitHub Pages 自动构建。提交前建议至少检查：首页、Learning、Publications、Teaching、Blog Posts 和 CV。

## 许可与来源

站点内容归姚行健所有。主题代码来自 Academic Pages / Minimal Mistakes，相关许可见 `LICENSE`。
