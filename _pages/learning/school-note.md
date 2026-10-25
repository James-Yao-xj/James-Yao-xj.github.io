---
layout: single
title: "SchoolNote"
permalink: /learning/school-note/
author_profile: true
---

[← 返回 Learning]({{ site.baseurl }}/learning/)

<div class="section-intro"><p>把课堂上的知识慢慢整理成自己的理解。这里按学期收录课程笔记，点击课程即可选择章节在线阅读。</p></div>

{% for semester in (2..3) reversed %}
<h2>第{% if semester == 3 %}三{% else %}二{% endif %}学期</h2>
<ul class="course-list">
  {% for course in site.data.course_notes.courses %}{% if course.semester == semester %}
  <li><a class="course-entry" href="{{ site.baseurl }}{{ course.url }}">
    <span class="course-entry__text"><strong>{{ course.title }}</strong><span class="course-entry__description">{{ site.data.course_topics[course.slug].description }}</span></span>
    <span class="course-count">{{ course.chapters | size }} 篇笔记<span aria-hidden="true">→</span></span>
  </a></li>
  {% endif %}{% endfor %}
</ul>
{% endfor %}
