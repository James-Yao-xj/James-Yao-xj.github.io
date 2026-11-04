---
title: "高等数学 C 小班课"
collection: teaching
type: "小班课"
permalink: /teaching/advanced-mathematics-c/
venue: "北京大学政府管理学院"
date: 2026-11-04
location: "北京"
excerpt: "面向北京大学政府管理学院的高等数学 C 小班课，提供前三章讲义与配套解析。"
# Add each new handout here. The Teaching index and this page use the same list.
materials:
  - title: "前三章课堂讲义"
    short_label: "讲义 PDF"
    description: "函数、极限与连续；微商与微分；微分中值定理及其应用。"
    url: "https://github.com/James-Yao-xj/advanced-mathematics-c-tutorial/blob/main/handouts/高等数学BC-前三章讲义.pdf"
  - title: "前三章配套解析"
    short_label: "解析 PDF"
    description: "按题号整理课堂例题与课后习题的解答。"
    url: "https://github.com/James-Yao-xj/advanced-mathematics-c-tutorial/blob/main/handouts/高等数学BC-前三章配套解析.pdf"
  - title: "课程仓库与 Typst 源文件"
    short_label: "查看仓库"
    description: "查看可编辑的讲义和解析源文件。"
    url: "https://github.com/James-Yao-xj/advanced-mathematics-c-tutorial"
---

这门小班课围绕函数、极限与连续，导数与微分，以及微分中值定理及其应用展开。讲义收录 55 道课堂真题例题和 12 道课后习题；配套解析按原题号整理，方便课后复习。

## 课程资料

<ul class="teaching-resources">
{% for material in page.materials %}
  <li>
    <strong>{{ material.title }}</strong>
    <p>{{ material.description }}</p>
    <a href="{{ material.url }}">{{ material.short_label }} <span aria-hidden="true">↗</span></a>
  </li>
{% endfor %}
</ul>

<p><a href="{{ '/teaching/' | relative_url }}">← 返回教学页面</a></p>
