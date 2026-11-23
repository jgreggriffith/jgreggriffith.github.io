// Light/dark switch. Dark is the default; a visitor's choice is remembered in this browser.
(function () {
  var root = document.documentElement;
  function current() { return root.getAttribute("data-theme") === "light" ? "light" : "dark"; }
  function label(btn) {
    var light = current() === "light";
    btn.textContent = light ? "Dark mode" : "Light mode";
    btn.setAttribute("aria-pressed", light ? "true" : "false");
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
