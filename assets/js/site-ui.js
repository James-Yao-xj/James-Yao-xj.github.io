/* Shared controls for navigation, theme selection, and course reading. */
(() => {
  const root = document.documentElement;
  const t = window.siteI18n.translate;
  const themeButton = document.querySelector('#theme-toggle');
  const systemTheme = window.matchMedia('(prefers-color-scheme: dark)');

  /** Apply a theme and describe the next action on the theme button. */
  function applyTheme(theme) {
    if (theme === 'dark') root.dataset.theme = 'dark';
    else delete root.dataset.theme;
    themeButton.setAttribute('aria-label', t(theme === 'dark' ? '切换为浅色主题' : '切换为深色主题'));
  }

  const preference = localStorage.getItem('theme');
  applyTheme(preference === 'dark' || (preference !== 'light' && systemTheme.matches) ? 'dark' : 'light');
  themeButton.addEventListener('click', () => {
    const next = root.dataset.theme === 'dark' ? 'light' : 'dark';
    localStorage.setItem('theme', next);
    applyTheme(next);
  });
  systemTheme.addEventListener('change', () => {
    const saved = localStorage.getItem('theme');
    if (saved !== 'light' && saved !== 'dark') applyTheme(systemTheme.matches ? 'dark' : 'light');
  });

  const navigation = document.querySelector('.site-navigation');
  const menuButton = navigation.querySelector('.menu-toggle');
  const desktopNavigation = window.matchMedia('(min-width: 1280px)');
  const pageRegions = document.querySelectorAll('#main, .page__footer');

  /** Keep menu visibility, focus access, and background scrolling in sync. */
  function setMenu(open) {
    menuButton.setAttribute('aria-expanded', String(open));
    menuButton.setAttribute('aria-label', t(open ? '关闭导航菜单' : '打开导航菜单'));
    document.body.classList.toggle('navigation-open', open);
    pageRegions.forEach(region => { region.inert = open; });
  }

  menuButton.addEventListener('click', () => setMenu(menuButton.getAttribute('aria-expanded') !== 'true'));
  navigation.querySelectorAll('a').forEach(link => link.addEventListener('click', () => setMenu(false)));
  desktopNavigation.addEventListener('change', () => setMenu(false));
  document.addEventListener('keydown', event => {
    if (menuButton.getAttribute('aria-expanded') !== 'true') return;
    if (event.key === 'Escape') {
      setMenu(false);
      menuButton.focus();
    }
    if (event.key === 'Tab') {
      const controls = [...navigation.querySelectorAll('a, button, select')].filter(element => element.getClientRects().length);
      const first = controls[0];
      const last = controls[controls.length - 1];
      if (event.shiftKey && document.activeElement === first) {
        event.preventDefault();
        last.focus();
      } else if (!event.shiftKey && document.activeElement === last) {
        event.preventDefault();
        first.focus();
      }
    }
  });

  document.addEventListener('site:language', () => {
    applyTheme(root.dataset.theme === 'dark' ? 'dark' : 'light');
    setMenu(menuButton.getAttribute('aria-expanded') === 'true');
  });

  const printButton = document.querySelector('[data-print-button]');
  if (printButton) printButton.addEventListener('click', () => window.print());

  const note = document.querySelector('.course-note');
  if (!note) return;
  const toc = note.querySelector(':scope > .note-toc');
  const breadcrumb = note.querySelector(':scope > nav');
  const body = document.createElement('div');
  body.className = 'note-body';
  body.dir = 'ltr';
  body.lang = location.pathname.includes('/western-philosophy/en/') ? 'en' : 'zh-Hans';
  [...note.childNodes].forEach(child => {
    if (child !== toc && child !== breadcrumb) body.append(child);
  });
  breadcrumb.classList.add('note-breadcrumb');
  note.replaceChildren(breadcrumb, body);
  const languageNotice = document.createElement('p');
  languageNotice.className = 'note-language-notice';
  languageNotice.textContent = t('笔记正文保留原语言。');
  note.before(languageNotice);
  document.addEventListener('site:language', () => {
    languageNotice.textContent = t('笔记正文保留原语言。');
    body.querySelectorAll('.note-pagination, .note-source').forEach(element => { element.dir = root.dir; });
  });
  body.querySelectorAll('.note-pagination, .note-source').forEach(element => { element.dir = root.dir; });

  // Reuse one outline so its links and state stay consistent at all widths.
  if (toc) {
    const outline = document.createElement('aside');
    outline.className = 'note-outline';
    outline.setAttribute('aria-label', t('本页目录'));
    toc.querySelector('ul').dir = 'ltr';
    document.addEventListener('site:language', () => outline.setAttribute('aria-label', t('本页目录')));
    outline.append(toc);
    note.insertBefore(outline, body);
    const desktopReading = window.matchMedia('(min-width: 1280px)');
    const summary = toc.querySelector('summary');
    function updateOutline() {
      toc.open = desktopReading.matches;
      summary.tabIndex = desktopReading.matches ? -1 : 0;
    }
    updateOutline();
    desktopReading.addEventListener('change', updateOutline);
    const links = [...toc.querySelectorAll('a')];
    const headings = links.map(link => document.getElementById(decodeURIComponent(link.hash.slice(1))));
    links.forEach((link, index) => link.classList.toggle('toc-subsection', headings[index].tagName === 'H3'));
    const observer = new IntersectionObserver(entries => {
      const visible = entries.filter(entry => entry.isIntersecting).sort((a, b) => a.boundingClientRect.top - b.boundingClientRect.top);
      if (!visible.length) return;
      links.forEach((link, index) => {
        if (headings[index] === visible[0].target) link.setAttribute('aria-current', 'location');
        else link.removeAttribute('aria-current');
      });
    }, { rootMargin: '-96px 0px -60% 0px' });
    headings.forEach(heading => observer.observe(heading));
  }

  const backToTop = document.createElement('a');
  backToTop.className = 'back-to-top';
  backToTop.href = '#page-top';
  backToTop.textContent = t('↑ 返回顶部');
  document.addEventListener('site:language', () => { backToTop.textContent = t('↑ 返回顶部'); });
  backToTop.hidden = true;
  document.body.append(backToTop);
  const topObserver = new IntersectionObserver(entries => {
    backToTop.hidden = entries[0].isIntersecting;
  });
  topObserver.observe(document.querySelector('.page-top-sentinel'));
})();
