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
| `Residential-Rental-Property.webp` | `ext_resources` → `ptRes` | 750 × 400 |
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
~2.4 MB JPEG). It was deliberately **not** extracted. That 320px band is the
only reason our page is shorter than the approved design.

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
- **No JavaScript ships with this site.** The only `<script>` tag on any page is
  the `application/ld+json` structured-data block, which is inert data. There is
  no `.js` file in the repo.

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
