/* SouthwestDirect.com — the only script on the site.
   1. Mobile navigation panel (v2 design)
   2. Floating "back to top" control
   Neither is required to read the site; both are progressive enhancements. */
(function () {
  "use strict";

  var root = document.documentElement;
  var reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)");

  /* -------------------------------------------------------------- drawer */
  var toggle = document.querySelector(".nav-toggle");
  var drawer = document.getElementById("mobile-menu");
  var backdrop = document.querySelector(".drawer-backdrop");

  if (toggle && drawer && backdrop) {
    var isOpen = function () { return toggle.getAttribute("aria-expanded") === "true"; };

    // Everything the focus trap should cycle through, in visual order.
    var focusables = function () {
      return Array.prototype.slice.call(
        drawer.querySelectorAll("button, a[href]")
      ).filter(function (el) { return el.offsetParent !== null; });
    };

    var setDrawer = function (open, returnFocus) {
      toggle.setAttribute("aria-expanded", String(open));
      toggle.setAttribute("aria-label", open ? "Close menu" : "Open menu");
      drawer.classList.toggle("is-open", open);
      backdrop.classList.toggle("is-open", open);
      root.classList.toggle("menu-open", open);   // freezes the page behind it
      if (open) {
        var first = focusables()[0];
        if (first) first.focus();
      } else if (returnFocus) {
        toggle.focus();
      }
    };

    toggle.addEventListener("click", function () { setDrawer(!isOpen(), true); });

    // Backdrop and the close button both carry data-drawer-close.
    document.addEventListener("click", function (e) {
      if (e.target.closest("[data-drawer-close]")) setDrawer(false, true);
    });

    // Nav links scroll to a section, so close behind them (focus follows the link).
    drawer.addEventListener("click", function (e) {
      var link = e.target.closest(".drawer-nav a[href], .drawer-cta, .drawer-email");
      if (link) setDrawer(false, false);
    });

    document.addEventListener("keydown", function (e) {
      if (!isOpen()) return;

      if (e.key === "Escape") { setDrawer(false, true); return; }

      if (e.key !== "Tab") return;
      var items = focusables();
      if (!items.length) return;
      var i = items.indexOf(document.activeElement);
      if (i === -1) { e.preventDefault(); items[0].focus(); return; }
      var next = e.shiftKey ? i - 1 : i + 1;
      if (next < 0) next = items.length - 1;
      if (next >= items.length) next = 0;
      e.preventDefault();
      items[next].focus();
    });

    // Growing past the breakpoint hides the toggle, so drop the drawer with it.
    // 960px matches the width at which the full desktop nav fits on one row.
    var desktop = window.matchMedia("(min-width: 960px)");
    var onBreakpoint = function () { if (desktop.matches && isOpen()) setDrawer(false, false); };
    if (desktop.addEventListener) desktop.addEventListener("change", onBreakpoint);
    else if (desktop.addListener) desktop.addListener(onBreakpoint);

    setDrawer(false, false);
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
