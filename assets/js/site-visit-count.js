/* Read the public site total without exposing an analytics API key. */
(() => {
  const count = document.querySelector('#site-visit-count');
  if (!count) return;
  fetch(`${count.dataset.site}/counter/TOTAL.json`)
    .then(response => response.json())
    .then(data => { count.textContent = data.count; });
})();
