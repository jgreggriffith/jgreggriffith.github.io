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

// Share row: copy link everywhere; the phone's own share sheet where it exists.
(function () {
  document.addEventListener("DOMContentLoaded", function () {
    var status = document.querySelector(".share-status");
    function say(msg) { if (!status) return; status.textContent = msg; setTimeout(function () { status.textContent = ""; }, 2500); }
    var copy = document.querySelector(".copy-link");
    if (copy && navigator.clipboard) {
      copy.parentNode.hidden = false;
      copy.addEventListener("click", function () {
        navigator.clipboard.writeText(copy.getAttribute("data-url")).then(function () { say("Link copied."); },
          function () { say("Couldn\u2019t copy. The address is in your browser\u2019s address bar."); });
      });
    }
    var share = document.querySelector(".native-share");
    var touch = window.matchMedia && window.matchMedia("(pointer: coarse)").matches;
    if (share && navigator.share && touch) {
      share.parentNode.hidden = false;
      share.addEventListener("click", function () {
        navigator.share({ title: share.getAttribute("data-title"), url: share.getAttribute("data-url") }).catch(function () {});
      });
    }
  });
})();

