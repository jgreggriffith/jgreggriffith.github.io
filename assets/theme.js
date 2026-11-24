// Color switch (a half-filled circle). Dark is the default; a visitor's choice is remembered in this browser.
(function () {
  var root = document.documentElement;
  function current() { return root.getAttribute("data-theme") === "light" ? "light" : "dark"; }
  function label(btn) {
    btn.setAttribute("aria-pressed", current() === "light" ? "true" : "false");
  }
  document.addEventListener("DOMContentLoaded", function () {
    var btn = document.querySelector(".theme-toggle");
    if (!btn) return;
    btn.hidden = false;
    label(btn);
    btn.addEventListener("click", function () {
      var next = current() === "light" ? "dark" : "light";
      if (next === "light") root.setAttribute("data-theme", "light");
      else root.removeAttribute("data-theme");
      try { localStorage.setItem("theme", next); } catch (e) {}
      label(btn);
    });
  });
})();

// Sticky header: show a hairline under it once the page has scrolled.
(function () {
  var root = document.documentElement, ticking = false;
  function update() { root.classList.toggle("scrolled", window.scrollY > 8); ticking = false; }
  window.addEventListener("scroll", function () {
    if (!ticking) { ticking = true; window.requestAnimationFrame(update); }
  }, { passive: true });
  update();
})();
