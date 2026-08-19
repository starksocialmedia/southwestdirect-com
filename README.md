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

### 1. Five images are placeholders — real files needed

The design canvas exposes files through a transfer capped at 192 KB, and six of
the seven source images are larger than that, so they arrived truncated and
would not decode. Only **Residential Rental Property** came through intact and
is the real photo on the page.

These five currently render as a hatched "PHOTO PENDING" panel at the correct
aspect ratio:

- `joffrey-long` — the portrait, used in **two** places (hero and About)
- `automotive-service-centers`
- `mixed-use`
- `industrial-warehouse`
- `other-property-types`

To fix: drop the full-size originals into `images/_src/` using the filenames
listed in `tools/build-images.py`, then run `python3 tools/build-images.py`.
Every derivative and the `<picture>` markup is already wired up, so the real
photos appear with no HTML edits.

### 2. The AI illustration is out

`uploads/Firefly (1).jpg` backed a full-bleed California coastline band between
the contact section and the footer. Per your note it has been removed, and an
HTML comment marks the spot in `index.html`:

> Real photo needed here — do not use AI illustration.

The page reads fine without it — contact now runs straight into the footer. Drop
a licensed photo in and restore the band before launch.

### 3. Two different e-mail addresses

The approved design shows **Joffrey@asksw.com** in the hero, contact block, and
footer. The business details you sent list **info@asksw.com**.

I kept `Joffrey@asksw.com` everywhere it is visible on the page, because the
design is approved and the copy leans on reaching Joffrey personally. I used
`info@asksw.com` in the Schema.org block, as specified.

**That inconsistency should be resolved before launch** — search engines compare
the structured data against what is on the page. Tell me which one wins and it
is a one-line change in `tools/build-pages.py`.

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

### 6. The legal pages are templates, not reviewed copy

`accessibility-statement.html` and `privacy-terms.html` follow standard WCAG 2.1
AA and privacy/ToS structures and are populated with the real business details,
licence numbers, and disclosure language from the design. They are **not legal
advice and have not been reviewed by an attorney.**

For a licensed lender that matters more than usual — the privacy section touches
CCPA and Gramm-Leach-Bliley, and the terms section makes representations about
licensing and lending. **Have counsel review both before launch.**

Also note the accessibility statement claims *"fully conformant with WCAG 2.1
Level AA"*, which is the standard template wording and matches what I measured.
If anything on the page changes materially, that claim needs re-checking.

### 7. Structured data modelling

`FinancialService` and `LocalBusiness` are declared as one node — `FinancialService`
is a subclass of `LocalBusiness`, so two separate blocks would compete. Schema.org
has no DRE or NMLS property, so all four licence numbers are `PropertyValue`
identifiers: the two company numbers on the organisation, Joffrey's two on a
nested `Person`.

I set his role to `employee` with `jobTitle: "Direct hard-money lender"`. Given
the branding he is more likely owner or broker of record — **tell me the correct
role** and I will change it.

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
