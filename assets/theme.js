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
    // Open LinkedIn, X, and Facebook share pages in a small window; a new tab if pop-ups are blocked.
    document.querySelectorAll("a.share-popup").forEach(function (a) {
      a.addEventListener("click", function (e) {
        if (e.metaKey || e.ctrlKey || e.shiftKey || e.altKey || e.button !== 0) return;
        if (window.matchMedia && window.matchMedia("(max-width: 760px)").matches) return;
        var w = 620, h = 680;
        var left = Math.max(0, (window.screenX || 0) + (window.outerWidth - w) / 2);
        var top = Math.max(0, (window.screenY || 0) + (window.outerHeight - h) / 2);
        var win = window.open(a.href, "share", "popup,width=" + w + ",height=" + h + ",left=" + left + ",top=" + top);
        if (win) { try { win.opener = null; } catch (err) {} e.preventDefault(); }
      });
    });
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

