// Smooth expandable nested menus (any depth)
document.addEventListener('click', (e) => {
  const btn = e.target.closest('.sb__btn');
  if (!btn) return;

  e.preventDefault();

  const selector = btn.getAttribute('data-target');
  const panel = selector ? document.querySelector(selector) : btn.nextElementSibling;
  if (!panel) return;

  const willOpen = !panel.classList.contains('open');
  panel.classList.toggle('open', willOpen);
  btn.setAttribute('aria-expanded', String(willOpen));
});
