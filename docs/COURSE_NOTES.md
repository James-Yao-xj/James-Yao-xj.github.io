# 课程笔记更新指南

网站中的笔记来自独立仓库 [PKUcourseNote](https://github.com/James-Yao-xj/PKUcourseNote)。网页正文、目录、公式资源和课程清单由 `scripts/export_course_notes.py` 生成。

| 文件 | 用途 | 修改方式 |
| --- | --- | --- |
| PKUcourseNote 中的 `.typ` | 笔记正文原稿 | 在源仓库编辑 |
| `_data/course_topics.json` | 课程简介和部分章节主题 | 导出前编辑 |
| `scripts/export_course_notes.py` | 课程路径和特殊章节映射 | 新增课程或特殊章节时编辑 |
| `_pages/learning/school-note/` | HTML 页面 | 自动生成，不直接编辑 |
| `_data/course_notes.json` | 课程与章节索引 | 自动生成，不直接编辑 |
| `assets/course-notes/` | 公式等资源 | 自动生成，不直接编辑 |

## 导出步骤

准备 PKUcourseNote 的本地副本、Typst 0.15.1 和 Python 依赖。在网站仓库根目录运行：

```bash
python3 -m pip install -r scripts/requirements-course-notes.txt
git -C ../PKUcourseNote rev-parse HEAD
python3 scripts/export_course_notes.py ../PKUcourseNote --revision <上一行显示的提交 SHA>
bundle exec jekyll build
```

如果源仓库不在 `../PKUcourseNote`，将两处路径换成实际位置。`--revision` 会写进课程索引和“查看原始笔记”链接，应填写本次导出所用源仓库的准确提交。

Typst 的 HTML 导出仍处于实验阶段。导出后查看 `local/course-note-export.log`，打开受影响的章节，核对公式、代码、表格、插图、页内目录和上下篇链接。`local/` 是本机日志目录，不会提交。确认后一起提交生成的页面、资源和索引。

网站发布只需要 Jekyll；读者浏览器不需要 Typst。
