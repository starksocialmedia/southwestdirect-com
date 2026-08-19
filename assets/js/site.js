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

  /* ----------------------------------------------------------------- map */
  /* The container ships with a static image inside it, which is what a
     no-JS visitor keeps. Leaflet only takes over once it has actually loaded. */
  var mapEl = document.getElementById("office-map");

  if (mapEl && window.L) {
    var lat = parseFloat(mapEl.dataset.lat);
    var lon = parseFloat(mapEl.dataset.lon);
    var zoom = parseInt(mapEl.dataset.zoom, 10);

    mapEl.innerHTML = "";                       // drop the static fallback
    var note = document.querySelector(".map-note");
    if (note) note.remove();                    // Leaflet renders its own attribution

    var map = L.map(mapEl, {
      center: [lat, lon],
      zoom: zoom,
      // Cooperative by default: the wheel scrolls the page until the reader
      // deliberately activates the map, and touch drag is left to the page.
      scrollWheelZoom: false,
      dragging: !L.Browser.mobile,
      tap: false
    });

    L.tileLayer("https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png", {
      maxZoom: 19,
      subdomains: "abcd",
      attribution:
        '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors ' +
        '&copy; <a href="https://carto.com/attributions">CARTO</a>'
    }).addTo(map);

    var pin = L.divIcon({
      className: "map-pin",
      iconSize: [30, 40],
      iconAnchor: [15, 38],
      popupAnchor: [0, -34],
      html:
        '<svg width="30" height="40" viewBox="0 0 30 40" aria-hidden="true" focusable="false">' +
          '<path d="M15 39C15 39 28 24.5 28 14.5A13 13 0 1 0 2 14.5C2 24.5 15 39 15 39Z" ' +
                'fill="#1E2A5E" stroke="#FAFAF7" stroke-width="2"/>' +
          '<circle cx="15" cy="14.5" r="5" fill="#B8874B"/>' +
        '</svg>'
    });

    var addr = "5151 California Ave STE 100, Irvine, CA 92617-3205";
    var marker = L.marker([lat, lon], {
      icon: pin,
      keyboard: true,
      title: "Joffrey Long / SouthwestDirect.com",
      alt: "Office location: " + addr
    }).addTo(map);

    marker.bindPopup(
      '<strong>Joffrey Long / SouthwestDirect.com</strong>' +
      '<span>5151 California Ave STE 100<br>Irvine, CA 92617-3205</span>' +
      '<a class="map-directions" target="_blank" rel="noopener noreferrer" ' +
         'href="https://maps.google.com/?q=' + encodeURIComponent(addr) + '">Get directions</a>',
      { className: "map-popup", closeButton: true, autoPanPadding: [16, 16] }
    ).openPopup();

    // Activate on deliberate interaction, stand down when the pointer leaves.
    var activate = function () {
      map.scrollWheelZoom.enable();
      if (L.Browser.mobile) map.dragging.enable();
    };
    mapEl.addEventListener("click", activate);
    mapEl.addEventListener("focusin", activate);
    mapEl.addEventListener("mouseleave", function () { map.scrollWheelZoom.disable(); });

    map.getContainer().setAttribute("aria-label",
      "Interactive map of the office at " + addr);
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
