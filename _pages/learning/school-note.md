---
layout: single
title: "SchoolNote"
permalink: /learning/school-note/
author_profile: true
---

[← 返回 Learning]({{ site.baseurl }}/learning/)

这里按学期整理我的学校课程笔记。点击课程进入章节目录，即可在本站阅读全文。

## 第三学期

{% for course in site.data.course_notes.courses %}{% if course.semester == 3 %}
- [{{ course.title }}]({{ site.baseurl }}{{ course.url }})（{{ course.chapters | size }} 篇笔记）
{% endif %}{% endfor %}

## 第二学期

{% for course in site.data.course_notes.courses %}{% if course.semester == 2 %}
- [{{ course.title }}]({{ site.baseurl }}{{ course.url }})（中文与 English，共 {{ course.chapters | size }} 篇笔记）
{% endif %}{% endfor %}

笔记随学习进度持续补充，欢迎阅读与交流。
