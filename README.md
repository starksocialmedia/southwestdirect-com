# SouthwestDirect.com — client preview

Static preview of the SouthwestDirect.com landing page plus two legal pages,
built from the approved Claude Design canvas. Pure HTML, CSS, and images — no
JavaScript, no build step required to deploy, no server-side dependencies.

**Preview URL:** https://starksocialmedia.github.io/southwestdirect-com/

> **This is not the live site.** Every page carries
> `<meta name="robots" content="noindex, nofollow">` so search engines skip it.
> Remove that tag from all three pages before launching to
> https://southwestdirect.com.

## Pages

| Page | File |
| --- | --- |
| Landing page | `index.html` |
| Accessibility statement | `accessibility-statement.html` |
| Privacy policy + terms of service | `privacy-terms.html` |

Header, contact, and footer markup are duplicated across all three pages by
design, as agreed for the static host. If the site later moves to PHP, those
three blocks become the includes.

## Leaving feedback

Send comments to **nathan@starksocial.com**.

Anything is fair game — wording, layout, colours, images, contact details,
licence disclosures. The most useful notes name the page and the section:

> On the landing page, in "Property types we lend on", the Mixed Use card
> should mention ground-floor retail.

Screenshots with markup are welcome. Nothing needs to be filed on GitHub.

## Viewing it locally

```bash
python3 -m http.server 8000
```

Then open http://localhost:8000. Serve it over HTTP rather than opening the
files directly — `file://` breaks the relative asset paths.

## Deployment (GitHub Pages)

Pages serves from the **`main`** branch, **`/ (root)`** folder. Pushing to
`main` republishes in a minute or two.

```bash
git add .
git commit -m "Update preview"
git push origin main
```

First-time setup on a fresh repo:

1. Push this folder to `main`.
2. **Settings → Pages → Source: Deploy from a branch.**
3. **Branch: `main`, folder: `/ (root)` → Save.**

The empty `.nojekyll` file tells Pages to serve everything as-is instead of
running it through Jekyll. Leave it in place.

Cloudflare Pages works too, with no config: point it at the repo, set the build
command to none and the output directory to `/`.

## Rebuilding

Both scripts are optional — the committed `.html` and image files work as-is.

| Command | What it does |
| --- | --- |
| `python3 tools/build-pages.py` | Regenerates the three HTML pages from the shared header/contact/footer fragments. Edit a shared block once here instead of in three files. |
| `python3 tools/build-images.py` | Rebuilds WebP + JPEG derivatives from originals in `images/_src/`. |

Requires Python 3 with Pillow (`pip3 install Pillow`).

---

## Notes for Nathan

Things I decided or could not resolve. Worth a look before this goes to Joffrey.

### 1. Images — resolved, all real

All six photographs were recovered from the bundled Design preview
(`SouthwestDirect Website.html`), which carries every asset base64-encoded in its
`<script type="__bundler/manifest">` tag. The earlier truncation was a transfer
cap on the design MCP, not a problem with the files.

Originals now live in `images/_src/`:

| File | Source | Pixels |
| --- | --- | --- |
| `joffrey-long.png` | manifest `dee75825…` | 748 × 839 |
| `Residential-Rental-Property.webp` | `ext_resources` → `ptRes` | 750 × 400 (rejected — see note 11) |
| `Automotive-Service-Centers.webp` | `ptAuto` | 2560 × 1928 |
| `Other-Property-Types.webp` | `ptOther` | 2122 × 1412 |
| `Industrial-Warehouse.webp` | `ptInd` | 2560 × 1920 |
| `Mix-Use.webp` | `ptMix` | 2560 × 1928 |

Because four sources turned out to be ~2560px wide, the card derivatives now go
to three tiers — 400 / 750 / 1100 — instead of two. Residential Rental Property
has only a 750px original, so it stops at 750 and never upscales.

`build-images.py` writes `images/manifest.json` recording which widths actually
exist per image, and `build-pages.py` builds every `srcset` from that file. The
markup therefore cannot advertise a derivative that was not produced — which is
what keeps the Residential card's shorter srcset honest.

### 2. The AI illustration is out

`uploads/Firefly (1).jpg` backed a full-bleed California coastline band between
the contact section and the footer. Per your note it has been removed, and an
HTML comment marks the spot in `index.html`:

> Real photo needed here — do not use AI illustration.

The page reads fine without it — contact now runs straight into the footer. Drop
a licensed photo in and restore the band before launch.

The bundled Design preview still contains this image (manifest `50bb048f…`,
~2.4 MB JPEG). It was deliberately **not** extracted.

**The band itself is now back** (19 Aug 2026) — see note 12. Only its photograph
is outstanding.

### 3. E-mail address — resolved

Confirmed with the client on 19 August 2026: **info@asksw.com** everywhere. It
now appears in the hero, the contact block, the footer, both legal pages, and
the Schema.org `email` field. The old personal address is gone from every page.
Page copy and structured data now agree, which is what search engines check.

### 4. The area code does not match the address

The office is in Irvine (949 / 714 territory) but the phone is an 818 number,
which is San Fernando Valley. Almost certainly a retained number, but flagging
it because name/address/phone consistency affects local search once the site is
indexed. No impact while the preview is `noindex`.

### 5. Colour change: one gold, on navy only

The brand gold `#B8874B` on the navy background measures **4.27:1**, just under
the 4.5:1 that WCAG AA requires for small text. It is used that way once — the
"FOR LOAN BROKERS" eyebrow.

I added a single lighter tint, `#C19661` (**5.04:1**), used *only* for text on
navy. The brand gold is unchanged everywhere else — buttons, rules, step
markers, separators. Visually it is a small shift on one label.

### 6. Legal pages — both final

Both pages now carry the client's final copy, placed verbatim and verified
paragraph by paragraph against the source. Wording was not changed.

The only additions are markup: phone numbers and e-mail addresses linked
(`tel:` / `mailto:`), the DRE, NMLS and ADA URLs made real links, and an
"On this page" index at the top of each. Headings map to `<h2>` for top-level
sections and `<h3>` beneath, so both pages keep a clean outline.

Both still warrant counsel review before launch — the privacy page touches
CCPA/CPRA and Gramm-Leach-Bliley, and the terms page makes licensing
representations. That is the client's call, not a blocker for the preview.

The accessibility statement claims conformance with WCAG 2.1 Level AA, which
matches what I measured on this build. If the page changes materially later,
re-check that claim.

### 7. Structured data modelling

`FinancialService` and `LocalBusiness` are declared as one node — `FinancialService`
is a subclass of `LocalBusiness`, so two separate blocks would compete. Schema.org
has no DRE or NMLS property, so all four licence numbers are `PropertyValue`
identifiers: the two company numbers on the organisation, Joffrey's two on a
nested `Person`.

Joffrey is attached as `founder` with `jobTitle: "Owner"`. `founder` is a real
schema.org property on `Organization`, so the block validates cleanly, and the
`jobTitle` carries the human-readable role. (An earlier pass used `owner`, which
is not in the vocabulary; you called that correctly.)

Deliberately omitted rather than guessed: `openingHours`, `priceRange`, `geo`,
and `sameAs`. Google likes `priceRange` on a LocalBusiness; send me a value and
I will add it.

### 8. Smaller calls I made

- **Phone links** use `tel:+18186351777` (E.164) rather than the design's bare
  `8186351777`, so they dial correctly from outside the US.
- **The brand mark is typographic**, so there was no logo file to make a favicon
  from. I built a "JL" monogram in the design's own serif on the navy field with
  the gold underline — `assets/favicon.svg` plus PNG and ICO fallbacks.
- **The Open Graph card** (`assets/og-image.jpg`, 1200×630) is generated from
  approved copy: the headline, the sub-line, the brand lockup, and credentials.
- **CSS is not minified.** It is 18 KB, around 4 KB gzipped, and readable CSS is
  more useful than a marginal saving while the design is still under review.
- **The map** is an OpenStreetMap embed, carried over from the design. It costs
  nothing and needs no API key, unlike Google Maps.
- **One small script ships.** `assets/js/site.js` (36 lines, deferred) drives the
  back-to-top control and nothing else. Every other `<script>` tag on the pages is
  the `application/ld+json` structured-data block, which is inert data. The site
  still renders and navigates completely with JavaScript disabled — the button
  simply never appears.

### 9. What the accessibility pass changed

Full audit against WCAG 2.1 AA. Fixed:

- Added `lang="en"` (was missing — 3.1.1, Level A).
- Moved `<footer>` out of `<main>`; it was nested inside.
- Converted the design canvas's `style-hover` / `style-focus` attributes into
  real CSS, so hover and focus states actually work in a browser.
- Focus rings are now visible on dark sections — the design used a navy ring,
  invisible against the navy footer and brokers band. They flip to cream there.
- Skip link now works on real `:focus`, not a canvas-only attribute.
- Trust bar separators moved to CSS pseudo-elements; they were `aria-hidden`
  list items sitting inside the `<ul>` and breaking its item count.
- Fixed horizontal scrolling at 320 px (1.4.10 Reflow, AA) caused by fixed
  `min-width` values on the flex columns.
- Footer legal links pointed at `#accessibility-statement` / `#privacy-terms`
  anchors that did not exist; they now point at the real pages, with
  `aria-current="page"` on the active one.
- Added `width`/`height` to every image to stop layout shift, `scroll-margin-top`
  so anchor targets clear the sticky header, and a visible `:focus-visible`
  fallback chain.

Verified: one `<h1>` per page and no heading-level skips, every image has
meaningful alt text, all landmarks and `<nav>`s labelled, no duplicate IDs, no
broken in-page anchors, the map `<iframe>` titled, and no horizontal overflow
from 280 px to 1440 px on all three pages.

### 10. Design fidelity — verified against the bundled preview

I rendered the approved bundle and this build side by side at 1440px and compared
them programmatically rather than by eye.

**Typography and colour:** 122 text nodes in our build, 119 aligned positionally
against the bundle. For each I compared font family, size, weight, colour,
text-transform, letter-spacing and line-height. **One** difference: the "For loan
brokers" eyebrow, which is the deliberate contrast fix in note 5. The three
unaligned nodes are the three `info@asksw.com` changes.

**Geometry:** every section — header, hero, trust bar, how-it-works, property
types, terms, brokers, about, contact, footer — now matches the bundle exactly on
top offset, height and width. Total document height differs by 320px, which is
precisely the removed Firefly band.

**Alt text:** every image alt now matches the design string for string.

Two real divergences were found and fixed:

1. **The content column was 48px narrow.** The design's containers are
   `max-width: 1120px` under the browser default `content-box`, so they render
   1168px wide including their 24px gutters. This build sets `box-sizing:
   border-box` globally, which made 1120px the *outer* width and squeezed the
   text column to 1072px. Every section was affected. `--wrap` is now 1168px, so
   the content column measures 1120px as designed.

2. **Two fixed heights lost a border.** Same root cause: `.card-img` (180px +
   1px bottom border) and `.map-frame` (380px + 1px top and bottom) are
   content-box in the design. Under border-box they came out 1px and 2px short,
   which compounded into a 2px drift for every section below the property cards.
   Both now declare the design's total height.

Three copy edits I had made were reverted to match the approved design: the
footer phone reads `818-635-1777` again (not the parenthesised form), the map
link reads "View larger map", and three alt strings are back to the design's
wording.

Two intentional differences remain, both visually identical to the design: the
trust-bar `·` separators and the terms-list `—` markers are drawn with CSS
`::before` instead of `aria-hidden` elements in the DOM. They were decorative and
`aria-hidden` in the design, so this is equivalent — and it stops the separators
from being counted as list items by screen readers. The geometry check confirms
both sections match the design to the pixel.

### 11. Residential Rental Property photo — fixed by v2

In v1 this asset was **two unrelated photographs composited side by side** with a
hard vertical seam; I had it rendering a "PHOTO PENDING" placeholder.

**v2 replaces it.** The new asset (`ptRes`, 3,297,418 bytes, 5216 × 3248 JPEG) is
a single coherent photograph of a gray two-story house with twin white garage
doors. It is the only image whose content actually changed between v1 and v2.

The placeholder is gone and `FORCE_PLACEHOLDER` is now empty. The source moved
from `.webp` to `.jpg` in `images/_src/`, matching what v2 ships.

Its alt text is now *"Two-story gray residential rental duplex with twin white
garage doors."* The design's string still ends *"near the coast"*, which the new
photograph does not show — alt has to describe the image that is actually there,
so I trimmed it.

### 12. The coastal band above the footer — built, with a caveat

The band is a full-bleed 320px image with an `aria-hidden` gradient over its
lower half — `linear-gradient(to bottom, rgba(30,42,94,0), rgba(30,42,94,0.55)
60%, #1E2A5E)` — dissolving into the navy footer. Geometry, gradient stops and
the `bottom: -1px` seam guard all match the design exactly. The gradient is drawn
via `.california-band::after`.

Photo: `images/_src/california-band.jpg`, derivatives at 768 / 1280 / 1920 in
WebP and JPEG, served `100vw` through `<picture>` exactly like the property
cards. `alt=""` — the band is decorative, so screen readers skip it.

**Caveat worth re-reading.** The photo is `~/Downloads/Firefly (1).jpg`, which is
**byte-identical** (sha256 `ecbf78e4a6c4…`, 4800 × 1976) to the band image
embedded in *both* the v1 and v2 bundles — the same file pulled on 19 Aug as "an
AI-generated illustration that shouldn't ship." It was later reinstated on the
understanding that it is a Firefly-*enhanced photograph* rather than generated
art, and that it is a different file. It is not a different file. Nathan asked
for it twice with its dimensions quoted correctly, so it ships — but if the
no-AI-imagery rule still applies to this asset, this is the thing to revisit.

### 13. Back to top

A floating control, on every page. `assets/js/site.js` adds a single class once
`window.scrollY` passes one viewport height; everything else is CSS.

- 48px navy square with a 4px radius and a 1px `rgba(250,250,247,0.3)` border,
  matching v2's treatment; cream up-arrow drawn as inline SVG (v2 used a bare `↑`
  text glyph, which renders inconsistently across fonts)
- `right`/`bottom: calc(20px + env(safe-area-inset-*))` — v2 specifies 20px, and
  `env()` keeps it clear of the iOS home indicator
- `<button type="button" aria-label="Back to top">`, with the SVG marked
  `aria-hidden` and `focusable="false"`
- Hidden with `visibility: hidden`, which also takes it out of the tab order —
  verified: it is not focusable until it appears
- Smooth scroll, or instant under `prefers-reduced-motion`; the fade/slide
  transition is also disabled there
- On click, focus moves to the brand link at the top of the page, so a keyboard
  user is not dropped on `<body>` when the button hides
- Focus ring is a cream outline inside a navy halo, so it stays visible whether
  the button is floating over the cream page or the navy footer
- `@media print { display: none !important; }`

Measured contrast: cream icon on navy 12.97:1, the button's edge ring against the
navy footer 4.98:1, navy fill against the cream page 12.97:1 — all well past the
3:1 that WCAG 1.4.11 asks of non-text UI.

### 14. v2 integration (19 Aug 2026)

Diffed the v1 and v2 bundles at template level. Most of the raw diff is noise —
every embedded font file got a fresh UUID on re-export. Filtering that out leaves
a 30-added / 4-removed line diff against 272 lines of markup.

**Unchanged between v1 and v2:** all 12 sections, all 17 headings, every line of
body copy, every colour, every font size, and the entire layout. No restructuring.

**Genuinely new in v2:**

1. **Mobile navigation** (the headline change) — below 820px the desktop nav is
   replaced by a compact "Call / Text" button plus a 44 × 44 toggle, opening a
   full-height navy panel with 28px serif links, a call CTA and a credentials
   line.
2. **A back-to-top control** — which I had already built to Nathan's spec the day
   before. Retuned to v2's visual treatment; see note 13.
3. **A new Residential Rental Property photo** — see note 11. The only image whose
   content changed; the portrait and coastal band got new UUIDs but identical
   bytes.

**Accessibility work added on top of v2's mobile menu.** The design's markup gets
the basics right — `aria-expanded`, `aria-controls`, a labelled toggle, a real
`<button>` — but a full-screen panel needs more than that, so this build adds:

- a focus trap, so Tab cycles inside the panel instead of reaching the page
  underneath it (verified: the cycle wraps through all five links, the CTA and the
  toggle)
- `Escape` to close, returning focus to the toggle
- focus moved to the first link on open
- `overflow: hidden` on the root while open, so the page behind does not scroll
- the breakpoint swap done in **CSS**, not JS state as the design does it, so the
  right header renders before any script runs
- the toggle revealed only once a `js` class is set on `<html>`, so with
  JavaScript disabled there is no dead control — mobile users just get the call
  button

Panel height is `calc(100dvh - 100%)`, where `100%` resolves to the header's own
height. That avoids the design's hardcoded `100vh - 75px` and stays correct as
mobile browser chrome collapses. Measured at 390 × 760: header 130 + panel 630 =
760 exactly.

Contrast re-checked on every new element — nine pairs, all passing, worst case
4.27:1 on the gold link hover, which clears the 3:1 that 28px semibold needs.
Reflow re-checked across 29 width/page combinations from 320px to 1440px,
including with the menu open. No horizontal scrolling anywhere.

### 15. Mobile header — single row, and a breakpoint correction

The header is now one row at every width, with three tiers:

| Width | Header |
| --- | --- |
| < 330px | brand + hamburger |
| 330 – 959px | brand + phone icon + hamburger |
| >= 960px | full desktop nav + "Call or Text" button |

The text "Call / Text" button was replaced by a 44 x 44 circular phone control —
inline Feather-style SVG, navy on cream, `aria-label="Call or text
818-635-1777"`, `href="tel:+18186351777"`, with the SVG marked `aria-hidden`. It
sits 12px from the hamburger, both centred against the two-line brand. DOM order
is brand -> phone -> hamburger -> desktop nav, so the tab order reads the way it
looks. Below 330px the phone icon is dropped so the wordmark keeps its room; the
drawer still carries a prominent Call or Text button.

**The desktop breakpoint moved from 820px to 960px.** Measured: the desktop
header needs **959px** to fit on one row — brand 170 + nav 716 + 24 gap + 48
gutters. v2's own 819px breakpoint therefore produced a *wrapped two-row desktop
header* between 820px and 958px. Raising the switch to 960px means the compact
controls cover that band instead, and the header is never a wrapped block.

That does mean mobile-style controls appear at 768px, which is a tablet width.
Fitting the real desktop nav there would need the type shrunk and the phone
number dropped from the CTA — a visible change to approved design. Raising the
breakpoint keeps the design intact; say the word if you would rather shrink the
nav instead.

Verified across 38 width/page combinations (320 – 1440px, all three pages, menu
open and closed): correct tier, single row, and no horizontal scrolling in every
one. Focus rings on both icons use the same dual-tone ring as the back-to-top
control. One bug fixed on the way: the global focus rule forces `border-radius:
2px`, which squared off the circular phone button the moment it was tabbed to —
each control now keeps its own shape while focused.

### 16. Contact map — static image instead of an embed

The OpenStreetMap iframe captured the scroll wheel whenever the cursor crossed
it. Replaced with a static map image that links out to OpenStreetMap in a new
tab, which is the simpler of the two options and right for a single location:
nothing to explore on the page, and no JavaScript involved.

`tools/build-map.py` renders it by stitching 20 OSM tiles at zoom 15 around the
office coordinate, drawing a brand-navy pin and burning in the required
attribution. It is committed, so the map can be regenerated or re-centred without
hunting for a screenshot. Output goes to `images/_src/office-map.png` and through
the normal pipeline to WebP + JPEG at 520 and 1040.

The image keeps the old frame's exact footprint (382px tall, `object-fit: cover`)
so the Contact layout is unchanged. Its alt text names the office address, the
link carries a visually-hidden "(opens OpenStreetMap in a new tab)" so the
new-tab behaviour is announced, `rel="noopener"` is set, and the attribution is
repeated as real page text beneath the map.

**There are now no iframes anywhere on the site.**

### 17. Mobile drawer

The v2 full-screen panel is replaced by a slide-in drawer, call-first:

- Slides from the right, 85% viewport width capped at 320px, full height,
  250ms ease-out (no transition under `prefers-reduced-motion`)
- Backdrop at `rgba(30,42,94,0.3)`; clicking it closes
- Order: close button, "Call or Text" CTA, email link, divider, five nav links,
  credentials at the bottom
- Cream panel rather than v2's navy one, because the spec calls for a navy CTA
  with cream text and a navy backdrop — both need a light surface to read against
- `role="dialog"`, `aria-modal="true"`, `aria-label="Menu"`; `aria-expanded` and
  the label ("Open menu" / "Close menu") tracked on the hamburger
- Focus moves to the close button on open and returns to the hamburger on close
- Focus trap verified cycling close -> CTA -> email -> five links -> wrap
- Closes on Escape, backdrop click, the close button, and any nav link
- Page behind is scroll-locked while open

Two bugs found and fixed while building it:

1. **The drawer was 72px tall, not full height.** It was nested inside
   `<header>`, and the header's `backdrop-filter: blur(8px)` establishes a
   containing block for `position: fixed` descendants — so `top: 0; bottom: 0`
   resolved against the 72px header instead of the viewport. The drawer and its
   backdrop now sit outside `<header>`.
2. **Focus landed on the skip link instead of the drawer.** `visibility` was
   being transitioned over 250ms, so the panel was still hidden — and therefore
   unfocusable — at the moment focus was moved into it. Visibility now flips
   instantly on open and only waits for the slide on close.

Verified across 18 width/state combinations: correct header tier, single row and
no horizontal scrolling at every width, drawer open and closed.

### 18. Audit pass (19 Aug 2026)

**WCAG 2.1 AA.** Every text node on all four pages was measured against its
resolved background (walking up through transparent ancestors and compositing
alpha), with the large-text rule applied at 24px, or 18.66px when bold:

| Page | Nodes checked | Failures |
| --- | --- | --- |
| index.html | 125 | 0 |
| index.html (drawer open) | 137 | 0 |
| accessibility-statement.html | 88 | 0 |
| privacy-terms.html | 134 | 0 |
| 404.html | 36 | 0 |

Hover and focus states were checked separately, since computed styles only show
the resting state. **One real failure found and fixed:** `.btn-primary:hover`
darkened the gold to `#A6793F`, dropping the button label to **4.24:1**. The
hover gold is now `#AF7F45` (**4.65:1**), still visibly darker than the resting
`#B8874B`. Lowest passing value anywhere is now 4.65:1.

Also verified: `lang="en"` and a unique `<title>` on all four pages; one `h1`
each with no skipped levels; the skip link first in tab order; one `<main>` per
page with the footer outside it; every `<nav>` and `<section>` labelled; every
image carrying alt text or an intentional `alt=""`; every inline SVG
`aria-hidden`; no positive `tabindex`; no forms (so no label requirement); and
`prefers-reduced-motion` honoured on smooth scroll, the back-to-top scroll, the
drawer slide and the backdrop fade.

**Bug found:** the 404 page was missing its closing `</main>`, which made the
footer parse as nested inside `<main>`. All four pages now have balanced tags.

**Schema.org.** Validates clean: JSON-LD parses, no unrecognised properties on
either the organisation or the `Person` node, all four required properties
present, and the licence numbers correctly split (company DRE + NMLS on the org,
Joffrey's on the nested `founder`). `geo` and `hasMap` were added — see note 19
for the coordinate correction that came out of this.

**Performance.** Lighthouse itself could not be run — there is no Node on this
machine, so there is no score to report. The underlying signals were measured
directly instead: 28 KB document, 234 KB total across 10 requests, DOM ready at
51ms and load at 75ms on localhost. All 9 images use `<picture>` with a WebP
source and a JPEG fallback, all carry explicit `width`/`height`, 8 of 9 are
lazy-loaded with only the hero eager, the single script is deferred, and the
console is clean. Google Fonts already requests `display=swap`. Added a
`preload` hint for the hero portrait, which is the LCP element.

**SEO.** Two issues fixed: the landing page description was 169 characters (now
141), and its canonical pointed at `/index.html` rather than the bare root — the
site now has one canonical URL, not two. Added `robots.txt` and `sitemap.xml`,
both written for launch rather than for the preview.

### 19. The map pin was in the wrong place

Geocoding "5151 California Ave, Irvine, CA 92617" against OSM Nominatim returned
**33.64074, -117.85386**. The marker inherited from the design sat at 33.65350,
-117.84400 — **1.68 km away**. The map has been re-centred on the geocoded
address (and zoomed from 15 to 16 for a closer view), the "view larger map" link
updated, and the same coordinates used for the `geo` property.

Worth a sanity check from your end: the geocoder places 5151 California Avenue on
the UC Irvine campus, which is consistent with the 92617 postcode, but it is
worth confirming the suite number and building are right before launch.

### 20. Additions

- **`404.html`** — branded, links back to the home page and to each section,
  with the phone number and e-mail inline. GitHub Pages serves it automatically.
- **Print stylesheet** — drops the header, drawer, back-to-top, coastal band,
  map and legal nav; flattens the reversed-out navy sections to black on white
  so they do not flood a printer; spells out non-obvious link destinations; and
  sets sensible page-break rules.
- **`forced-colors` support** — Windows High Contrast strips background fills,
  which would erase the phone, hamburger and back-to-top controls entirely since
  their shape *is* the fill. They now keep a `ButtonText` border under
  `forced-colors: active`.
- **PWA icons** — `icon-192.png` added alongside the existing 512, plus
  `site.webmanifest`.
- **Footer credit** — "Website crafted by Stark Social", muted, right-aligned on
  desktop and centred on mobile.
- **Hero plate on mobile** — the decorative navy offset behind the portrait is
  hidden below 768px, where it crowded the stacked layout. The portrait itself
  is unchanged.

Deliberately **not** added:

- **`CNAME`** — adding it before DNS points at GitHub would break the
  `github.io` preview URL. It should land as part of the launch cutover.
- **`_headers`** — GitHub Pages cannot set custom headers, so the file would do
  nothing here. For Cloudflare Pages the recommended starting set is
  `X-Content-Type-Options: nosniff`, `Referrer-Policy: strict-origin-when-cross-origin`,
  `X-Frame-Options: DENY`, and a CSP of roughly
  `default-src 'self'; img-src 'self' data:; style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; font-src https://fonts.gstatic.com; script-src 'self' 'unsafe-inline'` —
  the `unsafe-inline` on scripts is only needed for the one-line `js` class flag
  in `<head>`, which could be moved to a hashed inline script at launch.
- **`BreadcrumbList`** — not applicable. This is a one-page site with two legal
  pages; there is no hierarchy to describe.

### 21. Interactive map (styled OSM, no API key)

Replaces the static PNG with a real Leaflet map, on Nathan's call. Google Maps
was ruled out explicitly.

**Tiles: CARTO Positron** (`basemaps.cartocdn.com/light_all`) — the muted,
desaturated style, no API key and no account. I tested the alternatives:
Stadia now returns **401** without a key, so it was out; CARTO Voyager and
`light_nolabels` both work if a different look is ever wanted.

**Leaflet 1.9.4 is vendored** into `assets/vendor/leaflet/` rather than pulled
from a CDN — no third-party script at runtime, nothing to break if a CDN
changes. That is +158 KB of assets, the one real cost of going interactive.
Its sprite images (`marker-icon.png`, `layers.png`) are never requested,
because the marker is a `divIcon` and there is no layers control; verified zero
failed requests.

**Scroll hijacking is handled cooperatively**, which was the whole reason the
map went static in the first place. Measured on real wheel events:

| State | Wheel over the map |
| --- | --- |
| On load | not intercepted — the page scrolls |
| After a click on the map | intercepted — the map zooms |
| After the pointer leaves | not intercepted again |

Touch drag is left to the page on mobile (`dragging: !L.Browser.mobile`) and
enabled on first tap, so a one-finger swipe scrolls the page rather than
trapping in the map.

**Marker and popup.** A navy `#1E2A5E` pin with a gold `#B8874B` centre and a
cream outline, drawn as inline SVG in a `divIcon` — not the default blue
Leaflet marker. It opens a popup on load and re-opens on click; verified the pin
has `pointer-events: auto` and is not covered by anything. The popup is cream
with a navy left rule and carries the address plus a "Get directions" link to
`maps.google.com/?q=…`, which iOS hands to Apple Maps. Dismissible via its close
button or by clicking the map.

**Progressive enhancement.** The container still ships with the static PNG and
its OpenStreetMap link inside it. Leaflet clears that only once it has actually
loaded, so with JavaScript disabled the map is exactly what it was before.
Attribution is required either way: the static fallback keeps the text note, and
Leaflet renders its own control once live.

The map is keyboard focusable with an `aria-label` naming the office address,
and the zoom controls and popup close button all take the site focus ring.

### 22. vCard moved below the contact stack

It now sits after the whole `<dl>` rather than inside the e-mail entry, with a
26px gap, reading as a "save all of this" action after the individual contact
methods. Placing it outside the `<dl>` also keeps the markup valid — a bare link
between `<div>` groups inside a definition list would not be.

### 23. Contact map fills the row

Above 904px the map stretches to match the height of the contact details beside
it (measured: both 441px, zero difference). Below that the columns stack and the
map keeps its own 382px height rather than stretching to match a tall list.

904px is not arbitrary: flex wraps on flex-basis, not min-width, so the two
columns pair up at 380 + 420 + 56 gap + 48 gutters. Verified the switch lands
exactly there — stacked at 903px, side by side at 904px.

### 24. Footer: licensing, legal links, CCPA

Two premises worth correcting, because neither was actually broken:

* **The licence numbers were already on every page.** All four (DRE 00898122 /
  00525142, NMLS 285731 / 207202) appeared in the footer disclosure paragraphs
  on all four pages, including 404. The site was not out of compliance with BPC
  10140.6 or 10235.5. What the new block adds is *scannability* — the numbers
  were buried in prose, and now they are a labelled two-column list.
* **The Privacy Policy was already linked** in the footer, as "Privacy &
  terms". Relabelling it to explicit "Privacy Policy" and "Terms of Service"
  links is still an improvement for discoverability.

Added to the footer on all four pages:

* A licensing block, two columns on desktop and stacked on mobile, with
  "Equal Opportunity Lender" beneath it, separated by a rule.
* Legal links: Privacy Policy, Terms of Service (deep-linked to `#terms`),
  Accessibility Statement, and Do Not Sell or Share My Personal Information
  (deep-linked to `#do-not-sell`).
* A copyright line.

Contrast on the navy footer: names at 8.42:1, detail lines and copyright at
5.37:1, both clear of AA.

**Do Not Sell section** added to the privacy page. One judgement call on
heading level: it was specified as `##`, but it belongs *inside* the Privacy
Policy section, before Introduction. Making it a sibling `h2` of "Privacy
Policy" would have implied it sits outside the policy. It is an `h3` alongside
Introduction, with the GPC subsection as `h4`, which keeps the outline
skip-free — verified no heading skips on the page.

**GPC detection** added to `site.js`: sets `data-gpc="true"` on `<html>` when
`navigator.globalPrivacyControl` is true. A no-op by design, since the site
neither sells nor shares — it exists as a hook and as evidence of awareness.

### 25. Footer tightened into three rows

The disclosures used to run full width beneath the credentials, which left the
right of the credentials row empty. Restructured:

| Row | Left | Right |
| --- | --- | --- |
| 1 | Brand mark | Legal links |
| 2 | Credentials (both entities, stacked) + Equal Opportunity Lender | Both disclosure paragraphs |
| 3 | Contact line | Copyright + Stark Social credit |

Row 2 pairs from **720px** so tablet widths use both columns rather than
stacking; row 3 sits on one line once there is room for it. Below 720px
everything collapses to a single column in the same logical order.

Vertical rhythm tightened about 28%: the inner padding went from `56px / 40px`
to `40px / 28px` and the row gap from 32px to 22px. Measured footer height at
1440px is now 371px.

The copyright and the Stark Social credit were separate blocks and are now one
line, keeping the earlier wording ("Website crafted by") rather than the
shorthand in the layout sketch.

### 26. Drawer refinements and map nudge

Matched to the Claude Design reference:

* A **Menu** label sits top-left of the drawer, opposite the close button. The
  dialog is now `aria-labelledby` that heading rather than carrying a duplicate
  `aria-label`, so the visible and accessible names are the same string.
* The e-mail is the bare address, `info@asksw.com`, with no "Email" prefix.
* Nav item padding went from 14px to 19px, about 36% more space between items.
* The credentials line reads `DRE #00898122 · NMLS #285731` on one line
  instead of two.

**On the e-mail:** the reference mockup shows `Joffrey@asksw.com`, but the site
standardised on `info@asksw.com` earlier. The drawer uses `info@`, and there are
zero occurrences of the old address anywhere in the repo.

**Map height.** It already matched the contact column exactly, so rather than
setting a taller fixed height I added 14px of bottom padding to the column,
which grows the flex row and takes the map with it. The two boxes stay equal and
the map now finishes 14px below the column's last line of text, which is what
reads as balanced when solid boxes sit beside text ending on a baseline. Doing
it this way keeps the relationship content-relative rather than pinning a magic
pixel value that would drift if the contact copy changes.

### 27. Accessibility statement corrected

The statement listed a "Skip to main content" link among its implemented
features. That link was removed in `916f6d0`, which left the published
statement claiming something the site no longer did — the one item on it that
was not true.

Replaced with a bullet describing what actually provides the bypass now:

> **Landmark regions** — header, navigation, main and footer — that let
> assistive technology jump straight to the main content without stepping
> through the menu.

Not the suggested "Semantic HTML landmarks…" wording, because bullet 1 of the
same list already says "Semantic HTML markup so screen readers and assistive
technology can accurately interpret page structure" — the two would have read
as duplicates sitting next to each other. This version is specifically about
bypassing repeated navigation, which is the function the skip link served and
the WCAG 2.4.1 technique the site now relies on.

Verified the claim before publishing it: every page has one `header`, one
`main`, one `footer` and three `nav` elements, all three navs labelled. The
other eight bullets were re-checked too — 16 focus-visible rules, zero images
without alt text, zero heading-level skips.

