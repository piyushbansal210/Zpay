function toggleMenu(id, btn) {
  const submenu = document.getElementById(id);
  const expanded = btn.getAttribute("aria-expanded") === "true";
  btn.setAttribute("aria-expanded", !expanded);
  submenu.classList.toggle("show", !expanded);
}
