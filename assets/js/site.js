/* SouthwestDirect.com — the only script on the site.
   1. Mobile navigation panel (v2 design)
   2. Floating "back to top" control
   Neither is required to read the site; both are progressive enhancements. */
(function () {
  "use strict";

  var root = document.documentElement;
  var reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)");

  /* ---------------------------------------------------------------- menu */
  var toggle = document.querySelector(".nav-toggle");
  var menu = document.getElementById("mobile-menu");

  if (toggle && menu) {
    var isOpen = function () { return toggle.getAttribute("aria-expanded") === "true"; };

    var setMenu = function (open, returnFocus) {
      toggle.setAttribute("aria-expanded", String(open));
      toggle.setAttribute("aria-label", open ? "Close menu" : "Open menu");
      menu.hidden = !open;
      root.classList.toggle("menu-open", open);   // freezes the page behind the panel
      if (open) {
        var first = menu.querySelector("a[href]");
        if (first) first.focus();
      } else if (returnFocus) {
        toggle.focus();
      }
    };

    toggle.addEventListener("click", function () { setMenu(!isOpen(), true); });

    // Any link in the panel navigates to a section, so close behind it.
    menu.addEventListener("click", function (e) {
      if (e.target.closest("a[href]")) setMenu(false, false);
    });

    document.addEventListener("keydown", function (e) {
      if (!isOpen()) return;

      if (e.key === "Escape") { setMenu(false, true); return; }

      // Keep Tab inside the panel while it covers the page.
      if (e.key !== "Tab") return;
      var items = [toggle].concat(Array.prototype.slice.call(menu.querySelectorAll("a[href]")));
      var i = items.indexOf(document.activeElement);
      if (i === -1) return;
      var next = e.shiftKey ? i - 1 : i + 1;
      if (next < 0) next = items.length - 1;
      if (next >= items.length) next = 0;
      e.preventDefault();
      items[next].focus();
    });

    // Growing past the breakpoint hides the toggle, so drop the panel with it.
    var desktop = window.matchMedia("(min-width: 820px)");
    var onBreakpoint = function () { if (desktop.matches && isOpen()) setMenu(false, false); };
    if (desktop.addEventListener) desktop.addEventListener("change", onBreakpoint);
    else if (desktop.addListener) desktop.addListener(onBreakpoint);

    setMenu(false, false);
  }

  /* -------------------------------------------------------- back to top */
  var btn = document.querySelector(".back-to-top");
  if (!btn) return;

  var shown = null;

  function update() {
    // "past the hero" — the hero fills roughly one viewport height.
    var show = window.scrollY > window.innerHeight;
    if (show === shown) return;          // only touch the DOM on a real change
    shown = show;
    btn.classList.toggle("is-visible", show);
  }

  // Called directly rather than through requestAnimationFrame: the work is a
  // single cheap comparison, and a rAF latch can stall while a tab is throttled.
  window.addEventListener("scroll", update, { passive: true });
  window.addEventListener("resize", update, { passive: true });
  window.addEventListener("pageshow", update);
  document.addEventListener("visibilitychange", update);

  btn.addEventListener("click", function () {
    window.scrollTo({ top: 0, behavior: reduceMotion.matches ? "auto" : "smooth" });
    // The button hides once we reach the top, which would drop focus to <body>.
    // Hand it to the first control at the top of the page instead.
    var brand = document.querySelector(".brand");
    if (brand) brand.focus({ preventScroll: true });
  });

  update();
})();
