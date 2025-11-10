document.addEventListener('click', (e) => {
  const btn = e.target.closest('[data-sb-toggle]');
  if (!btn) return;

  const sel = btn.getAttribute('data-sb-toggle');
  const panel = document.querySelector(sel);
  if (!panel) return;

  const group = btn.closest('.sb-group') || document;
  const open = !panel.classList.contains('open');

  // Close siblings within the same group only
  group.querySelectorAll('.sb-sub').forEach(s => { if (s !== panel) s.classList.remove('open'); });
  group.querySelectorAll('[data-sb-toggle][aria-expanded]').forEach(b => { if (b !== btn) b.setAttribute('aria-expanded','false'); });

  panel.classList.toggle('open', open);
  btn.setAttribute('aria-expanded', String(open));
});

document.getElementById('sbToggle')?.addEventListener('click', () => {
  document.body.classList.toggle('sb-collapsed');
});
