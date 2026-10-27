/* Show one GitHub Discussion for each page and follow the site controls. */
(() => {
  const root = document.documentElement;
  const host = document.querySelector('.reader-comments .giscus');
  if (!host) return;

  const languages = { 'zh-Hans': 'zh-CN', en: 'en', 'zh-Hant': 'zh-TW', fr: 'fr', ar: 'ar' };
  const script = document.createElement('script');
  script.src = 'https://giscus.app/client.js';
  script.async = true;
  script.crossOrigin = 'anonymous';
  Object.assign(script.dataset, {
    repo: host.dataset.repo,
    repoId: host.dataset.repoId,
    category: host.dataset.category,
    categoryId: host.dataset.categoryId,
    mapping: 'pathname',
    strict: '1',
    reactionsEnabled: '1',
    emitMetadata: '0',
    inputPosition: 'bottom',
    loading: 'lazy',
    theme: root.dataset.theme === 'dark' ? 'dark' : 'light',
    lang: languages[root.lang] || 'en'
  });
  host.append(script);

  function updateComments() {
    const frame = host.querySelector('iframe.giscus-frame');
    if (!frame) return;
    frame.contentWindow.postMessage({ giscus: { setConfig: {
      theme: root.dataset.theme === 'dark' ? 'dark' : 'light',
      lang: languages[root.lang] || 'en'
    } } }, 'https://giscus.app');
  }

  new MutationObserver(updateComments).observe(root, { attributes: true, attributeFilter: ['lang', 'data-theme'] });
})();
