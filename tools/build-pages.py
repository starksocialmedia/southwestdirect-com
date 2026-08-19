#!/usr/bin/env python3
"""
Generate the three static HTML pages from shared fragments.

The .html files in the repo root ARE the deliverable and work standalone —
this script only exists so the duplicated header/contact/footer blocks can't
drift apart while we're still on a static host. If the site later moves to a
PHP host, these fragments become the includes.

Usage:  python3 tools/build-pages.py
"""
import os
import json

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

PHONE_DISPLAY = "(818) 635-1777"
PHONE_TEL     = "+18186351777"
EMAIL_PAGE    = "info@asksw.com"      # confirmed with client 2026-08-19
EMAIL_SCHEMA = EMAIL_PAGE             # page and structured data now agree
PROD_URL      = "https://southwestdirect.com"
UPDATED       = "August 19, 2026"

# --------------------------------------------------------------------------
# Structured data — FinancialService is a subclass of LocalBusiness; both are
# declared per spec. Licence numbers use PropertyValue identifiers, which is
# the convention consumers read (schema.org has no DRE/NMLS property).
# --------------------------------------------------------------------------
JSONLD = '''<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": ["FinancialService", "LocalBusiness"],
  "@id": "%(url)s/#organization",
  "name": "Southwest Bancorp",
  "alternateName": "Joffrey Long / SouthwestDirect.com",
  "description": "Direct hard-money lender for California real estate investors. Portfolio lender funding 100%% of loans directly.",
  "url": "%(url)s",
  "telephone": "%(tel)s",
  "email": "%(email)s",
  "logo": "%(url)s/assets/icon-512.png",
  "image": "%(url)s/assets/og-image.jpg",
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "5151 California Ave STE 100",
    "addressLocality": "Irvine",
    "addressRegion": "CA",
    "postalCode": "92617-3205",
    "addressCountry": "US"
  },
  "areaServed": {
    "@type": "State",
    "name": "California"
  },
  "geo": {
    "@type": "GeoCoordinates",
    "latitude": 33.64074,
    "longitude": -117.85386
  },
  "hasMap": "https://www.openstreetmap.org/?mlat=33.64074&mlon=-117.85386",
  "identifier": [
    { "@type": "PropertyValue", "name": "California DRE License", "value": "00898122" },
    { "@type": "PropertyValue", "name": "NMLS ID", "value": "285731" }
  ],
  "founder": {
    "@type": "Person",
    "@id": "%(url)s/#joffrey-long",
    "name": "Joffrey Long",
    "jobTitle": "Owner",
    "telephone": "%(tel)s",
    "identifier": [
      { "@type": "PropertyValue", "name": "California DRE License", "value": "00525142" },
      { "@type": "PropertyValue", "name": "NMLS ID", "value": "207202" }
    ]
  }
}
</script>''' % {"url": PROD_URL, "tel": PHONE_TEL, "email": EMAIL_SCHEMA}


# --------------------------------------------------------------------------
# Responsive <picture> built from images/manifest.json, which build-images.py
# writes. Driving it from the manifest means srcset can never advertise a
# derivative that was not actually produced (Residential Rental Property has a
# 750px source, so it has no 1100w variant while the others do).
# --------------------------------------------------------------------------
with open(os.path.join(ROOT, "images", "manifest.json")) as _f:
    IMG = json.load(_f)


def picture(slug, cls, alt, sizes, indent, lazy=True, priority=False):
    m = IMG[slug]
    ws = m["widths"]
    w, h = m["intrinsic"]
    pad = " " * indent
    # A placeholder must not inherit the design's alt text, or a screen reader
    # would hear a description of a photograph that is not on the page.
    if m.get("placeholder"):
        alt = "Photo pending: " + m.get("label", "image")
    webp = ", ".join(f"images/{slug}-{x}.webp {x}w" for x in ws)
    jpg = ", ".join(f"images/{slug}-{x}.jpg {x}w" for x in ws)
    # <img src> is only used by browsers without srcset support, so point it at a
    # mid-size derivative rather than the largest one.
    fallback_w = ws[len(ws) // 2] if len(ws) > 1 else ws[0]
    flags = 'loading="lazy" ' if lazy else ""
    if priority:
        flags += 'fetchpriority="high" '
    return (
        f'{pad}<picture>\n'
        f'{pad}  <source type="image/webp" sizes="{sizes}"\n'
        f'{pad}          srcset="{webp}">\n'
        f'{pad}  <img class="{cls}" src="images/{slug}-{fallback_w}.jpg" sizes="{sizes}"\n'
        f'{pad}       srcset="{jpg}"\n'
        f'{pad}       width="{w}" height="{h}" {flags}decoding="async"\n'
        f'{pad}       alt="{alt}">\n'
        f'{pad}</picture>'
    )


def head(title, desc, page_path, og_type="website"):
    # index.html canonicalises to the bare root so the site has one URL, not two.
    canonical_path = "" if page_path == "index.html" else page_path
    # The hero portrait is the LCP element on the landing page; hint it early.
    hero_preload = (
        '<link rel="preload" as="image" href="images/joffrey-long-640.jpg"\n'
        '      imagesrcset="images/joffrey-long-320.jpg 320w, images/joffrey-long-640.jpg 640w, images/joffrey-long-748.jpg 748w"\n'
        '      imagesizes="(min-width: 900px) 320px, (min-width: 560px) 40vw, 80vw">'
    ) if page_path == "index.html" else ""
    return f'''<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">

<!-- PREVIEW ONLY — remove this line before the production launch. -->
<meta name="robots" content="noindex, nofollow">

<link rel="canonical" href="{PROD_URL}/{canonical_path}">

<!-- Open Graph / social sharing -->
<meta property="og:type" content="{og_type}">
<meta property="og:site_name" content="Joffrey Long / SouthwestDirect.com">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{PROD_URL}/{canonical_path}">
<meta property="og:image" content="{PROD_URL}/assets/og-image.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="Got the Deal? Get it Closed! Direct hard-money lending for California real estate investors — Joffrey Long, SouthwestDirect.com">
<meta property="og:locale" content="en_US">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{desc}">
<meta name="twitter:image" content="{PROD_URL}/assets/og-image.jpg">

<!-- Favicon -->
<link rel="icon" href="assets/favicon.svg" type="image/svg+xml">
<link rel="icon" href="assets/favicon-32.png" sizes="32x32" type="image/png">
<link rel="icon" href="assets/favicon-16.png" sizes="16x16" type="image/png">
<link rel="apple-touch-icon" href="assets/apple-touch-icon.png">
<link rel="shortcut icon" href="assets/favicon.ico">
<link rel="manifest" href="assets/site.webmanifest">
<meta name="theme-color" content="#1E2A5E">

<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Source+Serif+4:opsz,wght@8..60,400;8..60,600;8..60,700&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/css/site.css">
{hero_preload}
<script>document.documentElement.classList.add("js");</script>

{JSONLD}'''


def header(prefix=""):
    """prefix is '' on the landing page, 'index.html' on the legal pages."""
    links = [("How it works", "#how-it-works"), ("Property types", "#property-types"),
             ("Loan brokers", "#brokers"), ("About", "#about"), ("Contact", "#contact")]
    desktop = "\n".join(
        f'      <a class="nav-link" href="{prefix}{h}">{t}</a>' for t, h in links)
    drawer_links = "\n".join(
        f'      <a href="{prefix}{h}">{t}</a>' for t, h in links)
    return f'''<a class="skip-link" href="#main">Skip to main content</a>

<header class="site-header">
  <div class="header-inner">
    <a class="brand" href="index.html">
      <span class="brand-name">Joffrey Long</span>
      <span class="brand-domain">SouthwestDirect.com</span>
    </a>

    <div class="mobile-controls">
      <a class="icon-phone" href="tel:{PHONE_TEL}" aria-label="Call or text 818-635-1777">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor"
             stroke-width="2" stroke-linecap="round" stroke-linejoin="round"
             aria-hidden="true" focusable="false">
          <path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6
                   A19.79 19.79 0 0 1 2.12 4.18 2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.13.96.36 1.9.7 2.81
                   a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45
                   c.91.34 1.85.57 2.81.7A2 2 0 0 1 22 16.92z"/>
        </svg>
      </a>
      <button type="button" class="nav-toggle" aria-expanded="false"
              aria-controls="mobile-menu" aria-label="Open menu">
        <svg class="icon-open" width="20" height="20" viewBox="0 0 20 20" aria-hidden="true" focusable="false">
          <path d="M3 5h14M3 10h14M3 15h14" fill="none" stroke="currentColor"
                stroke-width="2" stroke-linecap="round"/>
        </svg>
        <svg class="icon-close" width="20" height="20" viewBox="0 0 20 20" aria-hidden="true" focusable="false">
          <path d="M4 4l12 12M16 4L4 16" fill="none" stroke="currentColor"
                stroke-width="2" stroke-linecap="round"/>
        </svg>
      </button>
    </div>

    <nav class="main-nav" aria-label="Main">
{desktop}
      <a class="btn-primary btn-nav" href="tel:{PHONE_TEL}">Call or Text {PHONE_DISPLAY}</a>
    </nav>
  </div>

</header>

  <div class="drawer-backdrop" data-drawer-close></div>

  <div id="mobile-menu" class="drawer" role="dialog" aria-modal="true" aria-label="Menu">
    <div class="drawer-head">
      <button type="button" class="drawer-close" data-drawer-close aria-label="Close menu">
        <svg width="20" height="20" viewBox="0 0 20 20" aria-hidden="true" focusable="false">
          <path d="M4 4l12 12M16 4L4 16" fill="none" stroke="currentColor"
                stroke-width="2" stroke-linecap="round"/>
        </svg>
      </button>
    </div>

    <a class="drawer-cta" href="tel:{PHONE_TEL}">Call or Text {PHONE_DISPLAY}</a>
    <a class="drawer-email" href="mailto:{EMAIL_PAGE}">Email {EMAIL_PAGE}</a>

    <hr class="drawer-divider">

    <nav class="drawer-nav" aria-label="Page sections">
{drawer_links}
    </nav>

    <ul class="drawer-trust">
      <li>43 years of lending</li>
      <li>CMA Board of Directors</li>
      <li>Direct lender</li>
      <li>DRE #00898122</li>
      <li>NMLS #285731</li>
    </ul>
  </div>'''

def contact():
    return f'''<section id="contact" class="wrap contact" aria-labelledby="contact-h">
    <div class="contact-col">
      <h2 id="contact-h" class="section-title contact-title">Talk to Joffrey</h2>
      <p class="contact-lede">No forms, no intake queue. Call, text, or e-mail — you'll reach the person who makes the decision.</p>
      <dl class="contact-dl">
        <div>
          <dt class="contact-dt">Call or text</dt>
          <dd class="contact-dd"><a class="contact-phone" href="tel:{PHONE_TEL}">{PHONE_DISPLAY}</a></dd>
        </div>
        <div>
          <dt class="contact-dt">Email</dt>
          <dd class="contact-dd"><a class="contact-email" href="mailto:{EMAIL_PAGE}">{EMAIL_PAGE}</a></dd>
        </div>
        <div>
          <dt class="contact-dt">Office</dt>
          <dd class="contact-dd contact-address">
            Joffrey Long / SouthwestDirect.com<br>
            5151 California Ave STE 100<br>
            Irvine, CA 92617-3205
          </dd>
        </div>
      </dl>
    </div>
    <div class="contact-map">
      <a class="map-link" href="https://www.openstreetmap.org/?mlat=33.64074&amp;mlon=-117.85386#map=17/33.64074/-117.85386"
         target="_blank" rel="noopener">
{picture("office-map", "map-img", "Map showing the office at 5151 California Ave STE 100, Irvine, California", "(min-width: 960px) 520px, 92vw", 8)}
        <span class="visually-hidden"> (opens OpenStreetMap in a new tab)</span>
      </a>
      <p class="map-note">Map data &copy; OpenStreetMap contributors.</p>
    </div>
  </section>'''


def footer(current=None):
    def cur(page):
        return ' aria-current="page"' if current == page else ""
    return f'''<footer class="site-footer">
  <div class="footer-inner">
    <div class="footer-top">
      <p class="footer-brand">Joffrey Long / SouthwestDirect.com</p>
      <nav class="footer-legal-nav" aria-label="Legal">
        <a href="accessibility-statement.html"{cur("a11y")}>Accessibility statement</a>
        <a href="privacy-terms.html"{cur("privacy")}>Privacy &amp; terms</a>
      </nav>
    </div>
    <div class="footer-disclosures">
      <p>Loans are primarily made (funded) and serviced by Southwest Bancorp under Calif. Dept of Real Estate Broker License no. 00898122. (<a href="https://www.dre.ca.gov">www.DRE.CA.gov</a>) Joffrey Long holds Calif. Dept. of Real Estate Broker License no. 00525142. Loans may also be arranged with entities owned by Southwest Bancorp or its owners, or with third party lenders.</p>
      <p>Investments in trust deeds secured by one or more interests in real property are subject to risk of loss. Southwest Bancorp does not make (fund) consumer purpose loans that are secured by 1-4 family residences. Those loans may be arranged with institutional lenders, under NMLS Identifier No. 285731 (Southwest Bancorp) and No. 207202 (Joffrey Long).</p>
    </div>
    <p class="footer-meta">5151 California Ave STE 100, Irvine, CA 92617-3205 &middot; <a href="tel:{PHONE_TEL}">818-635-1777</a> &middot; <a href="mailto:{EMAIL_PAGE}">{EMAIL_PAGE}</a></p>
    <p class="footer-credit">Website crafted by
      <a href="https://starksocial.com" target="_blank" rel="noopener noreferrer"
         title="Stark Social Media Agency (Santa Clarita/Los Angeles)">Stark Social</a>
    </p>
  </div>
</footer>'''


BACK_TO_TOP = """<button type="button" class="back-to-top" aria-label="Back to top">
  <svg viewBox="0 0 24 24" width="22" height="22" aria-hidden="true" focusable="false">
    <path d="M12 19V6M6 12l6-6 6 6" fill="none" stroke="currentColor"
          stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/>
  </svg>
</button>"""

def page(title, desc, path, body, current=None, prefix=""):
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
{head(title, desc, path)}
</head>
<body>
{header(prefix)}

{body}

{footer(current)}

{BACK_TO_TOP}
<script src="assets/js/site.js" defer></script>
</body>
</html>
'''


# --------------------------------------------------------------------------
# Property-type cards (expanded from the design's sc-for loop)
# --------------------------------------------------------------------------
CARD_SIZES = "(min-width: 1168px) 341px, (min-width: 700px) 31vw, 92vw"

PROPERTY_TYPES = [
    ("residential-rental-property", "Residential Rental Property", "1–4 units or 5–15 units",
     "Two-story gray residential rental duplex with twin white garage doors",
     ["Credit and income problems OK", "Damaged, incomplete properties",
      "Low rents, problem properties", "Non-confirming, zoning issues", "Purchase or cash out"]),
    ("automotive-service-centers", "Automotive / Service Centers", "",
     "Automotive brake and tire service center with roll-up bay doors",
     ["Owner-user, leased, or vacant", "Older properties accepted",
      "Credit and income problems OK", "Purchase or cash out"]),
    ("mixed-use", "Mixed Use Properties", "",
     "Street-front mixed use commercial building with large storefront windows",
     ["Leased or monthly rentals", "Stores, residential, other combos",
      "Legal, non-confirming, zoning issues OK"]),
    ("industrial-warehouse", "Industrial / Warehouse", "",
     "Industrial warehouse loading docks with roll-up doors",
     ["Mixed, warehouse/service centers", "Older and newer buildings",
      "Legal, non-confirming OK", "Leased or owner-user"]),
    ("other-property-types", "Other Property Types", "",
     "Single-story commercial building with red awning and parking lot",
     ["Houses of worship", "Specialty properties", "Legal, non-confirming OK", "Truck parking lots"]),
]


def card(slug, title, note, alt, bullets):
    note_html = f'\n              <p class="card-note">{note}</p>' if note else ""
    lis = "\n".join(f"              <li>{b}</li>" for b in bullets)
    return f'''          <li class="card">
{picture(slug, "card-img", alt, CARD_SIZES, 12)}
            <div class="card-body">
              <h3 class="card-title">{title}</h3>{note_html}
              <ul class="card-list">
{lis}
              </ul>
            </div>
          </li>'''


CARDS = "\n".join(card(*pt) for pt in PROPERTY_TYPES)

# --------------------------------------------------------------------------
INDEX_BODY = f'''<main id="main">

  <!-- HERO -->
  <section class="hero" aria-labelledby="hero-h">
    <div class="hero-inner">
      <div class="hero-copy">
        <p class="eyebrow">Direct hard-money lender &middot; California</p>
        <h1 id="hero-h" class="hero-title">Got the Deal?<br>Get it Closed!</h1>
        <p class="hero-lede">Direct hard-money lending for California real estate investors.</p>
        <div class="hero-actions">
          <a class="btn-primary btn-hero" href="tel:{PHONE_TEL}">Call or Text {PHONE_DISPLAY}</a>
          <a class="link-email" href="mailto:{EMAIL_PAGE}">{EMAIL_PAGE}</a>
        </div>
        <p class="hero-note">You'll speak with Joffrey Long — a decision-maker, not a middleman.</p>
      </div>
      <div class="hero-figure">
{picture("joffrey-long", "hero-img", "Joffrey Long, direct hard-money lender",
                   "(min-width: 900px) 320px, (min-width: 560px) 40vw, 80vw", 8,
                   lazy=False, priority=True)}
      </div>
    </div>
  </section>

  <!-- TRUST BAR -->
  <section class="trustbar" aria-label="Credentials">
    <ul class="trustbar-list">
      <li>43 years of lending</li>
      <li>CMA Board of Directors</li>
      <li>Direct lender</li>
      <li>DRE #00898122</li>
      <li>NMLS #285731</li>
    </ul>
  </section>

  <!-- HOW IT WORKS -->
  <section id="how-it-works" class="wrap section-pad" aria-labelledby="hiw-h">
    <h2 id="hiw-h" class="section-title">How it works for you</h2>
    <p class="section-lede">Three steps. No committees, no middlemen.</p>
    <ol class="steps">
      <li class="step">
        <p class="step-num">Step 1</p>
        <h3 class="step-title">Talk with Joffrey</h3>
        <p class="step-text">Talk with me, Joffrey Long. I am a decision-maker, not a middleman.</p>
      </li>
      <li class="step">
        <p class="step-num">Step 2</p>
        <h3 class="step-title">Get a clear answer</h3>
        <p class="step-text">I will ask a few quick questions, then spell out what you can get.</p>
      </li>
      <li class="step">
        <p class="step-num">Step 3</p>
        <h3 class="step-title">Close in 5–12 days</h3>
        <p class="step-text">5–12 days, if your transaction is ready.</p>
      </li>
    </ol>
  </section>

  <!-- PROPERTY TYPES -->
  <section id="property-types" class="band" aria-labelledby="pt-h">
    <div class="wrap section-pad">
      <h2 id="pt-h" class="section-title">Property types we lend on</h2>
      <p class="section-lede">Loans we make, on the properties other lenders pass over.</p>
      <ul class="cards">
{CARDS}
      </ul>
    </div>
  </section>

  <!-- TERMS -->
  <section id="terms" class="wrap section-pad terms" aria-labelledby="terms-h">
    <div class="terms-intro">
      <h2 id="terms-h" class="section-title">Custom-tailored terms from a portfolio lender</h2>
      <p>We fund 100% of all loans directly — with OUR money — so we can change or structure a loan that works.</p>
    </div>
    <ul class="terms-list">
      <li>Interest-only, 2, 4, 5, or 7 year terms</li>
      <li>Fully amortized 15 or 20 years</li>
      <li>Loans with or without early payoff fees</li>
      <li>Cross collateral for lower down payment</li>
    </ul>
  </section>

  <!-- WHAT WE DON'T DO -->
  <section class="wrap" aria-labelledby="wwdd-h" style="padding-bottom: 80px">
    <div class="exclusions">
      <h2 id="wwdd-h">What we don't do</h2>
      <p>Loans outside of California, vacant land (unless producing rental income), rural or very small communities.</p>
    </div>
  </section>

  <!-- LOAN BROKERS -->
  <section id="brokers" class="band-navy" aria-labelledby="lb-h">
    <div class="wrap section-pad">
      <p class="brokers-eyebrow">For loan brokers</p>
      <h2 id="lb-h" class="brokers-title">Get your loan funded</h2>
      <p class="brokers-lede">The borrower is YOUR client. We get that. We stay in the background and make YOU the hero.</p>
      <div class="brokers-grid">
        <div class="broker-col">
          <h3 class="broker-title">Custom tailored loans</h3>
          <p class="broker-text">We fund 100% of all loans directly — with OUR money — so we can change / structure a loan that works.</p>
        </div>
        <div class="broker-col">
          <h3 class="broker-title">Talk to the decision maker</h3>
          <p class="broker-text">I'm Joffrey. Call, text, or e-mail me. I'll be the one you work with. Get answers that work.</p>
        </div>
        <div class="broker-col">
          <h3 class="broker-title">Fees / compensation to YOU</h3>
          <p class="broker-text">Your fees paid from escrow to you, or directly from us, your choice.</p>
        </div>
      </div>
    </div>
  </section>

  <!-- ABOUT -->
  <section id="about" class="wrap about" aria-labelledby="about-h">
    <figure class="about-figure">
{picture("joffrey-long", "about-img",
                 "Portrait of Joffrey Long",
                 "(min-width: 900px) 300px, (min-width: 560px) 40vw, 80vw", 6)}
      <dl class="about-dl">
        <div class="about-row">
          <dt class="about-dt">Experience</dt>
          <dd class="about-dd">43+ years</dd>
        </div>
        <div class="about-row">
          <dt class="about-dt">DRE (Southwest Bancorp)</dt>
          <dd class="about-dd">#00898122</dd>
        </div>
        <div class="about-row">
          <dt class="about-dt">DRE (Joffrey Long)</dt>
          <dd class="about-dd">#00525142</dd>
        </div>
        <div class="about-row">
          <dt class="about-dt">NMLS</dt>
          <dd class="about-dd">#285731 / #207202</dd>
        </div>
      </dl>
    </figure>
    <div class="about-body">
      <h2 id="about-h" class="section-title">About Joffrey Long</h2>
      <div class="about-prose">
        <p>Focused on providing borrowers with "loans that work" for their real estate investment and other business needs, Joffrey has been a hard money lender for more than 43 years. He's also an investor in both real estate loans and direct real estate ownership.</p>
        <p>He serves as a member of the education committee and the board of directors of the California Mortgage Association, and is a past president and past education chair of the association.</p>
        <p>He has testified as an industry expert, providing expert witness testimony in numerous trials, depositions, and arbitration proceedings since 2006.</p>
        <p>He frequently teaches continuing education classes for loan originators and is an instructor in hard money lending topics for the California Mortgage Association. He also is a co-creator and moderator for CMA's "Private Money Basics" class, a one-day course covering eight key areas in hard money/private money lending.</p>
      </div>
      <h3 class="about-sub">How we work</h3>
      <div class="about-how">
        <p>Our borrowers are real estate investors and business owners using real estate loans to fund real estate purchases and business expansion. By directly funding our loans, we focus on getting investment buyers the loans they need, lending our own funds, providing loan brokers with the funding source for investor loans, tailoring loans to meet borrower needs, and helping property investors "get the deal" when there are other offers.</p>
        <p>We are the loan servicer for all the loans we make. We hold most loans for our own portfolio, and sell some loans to private party investors. Loans sold to private party investors are offered and sold to investors only after the initial funding and closing by our company.</p>
      </div>
    </div>
  </section>

  <!-- TESTIMONIALS -->
  <section class="band" aria-labelledby="quotes-h">
    <div class="quotes-inner">
      <h2 id="quotes-h" class="quotes-title">What borrowers say</h2>
      <div class="quotes-grid">
        <figure class="quote">
          <blockquote>"We keep coming back to Joffrey — he makes the decisions."</blockquote>
          <figcaption>Repeat borrower</figcaption>
        </figure>
        <figure class="quote">
          <blockquote>"I was not sure. But it turned out to be a great choice."</blockquote>
          <figcaption>Borrower</figcaption>
        </figure>
        <figure class="quote">
          <blockquote>"They are reasonable and they know what they are doing."</blockquote>
          <figcaption>Borrower</figcaption>
        </figure>
      </div>
    </div>
  </section>

  {contact()}

  <!-- CALIFORNIA BAND -->
  <!-- Photo pending: the design's asset for this band was an AI illustration and
       was pulled on 19 Aug 2026. Drop a licensed coastal photo at
       images/_src/california-band.jpg and re-run tools/build-images.py. The
       navy gradient that dissolves into the footer is drawn in CSS and is
       already correct. -->
  <div class="california-band">
{picture("california-band", "band-img", "", "100vw", 4)}
  </div>

</main>'''


A11Y_BODY = f'''<main id="main">
  <div class="page-head">
    <div class="page-head-inner">
      <h1 class="page-title">Accessibility Statement</h1>
    </div>
  </div>

  <div class="prose">
    <p class="updated">Last updated: {UPDATED}</p>

    <div class="toc">
      <h2>On this page</h2>
      <ul>
        <li><a href="#commitment">Our Commitment</a></li>
        <li><a href="#standards">Standards We Follow</a></li>
        <li><a href="#features">Accessibility Features</a></li>
        <li><a href="#ongoing">Ongoing Effort</a></li>
        <li><a href="#accommodations">Requesting Accommodations or Reporting Barriers</a></li>
        <li><a href="#third-party">Third-Party Content</a></li>
        <li><a href="#complaints">Formal Complaints</a></li>
      </ul>
    </div>

    <h2 id="commitment">Our Commitment</h2>
    <p>Southwest Bancorp is committed to ensuring that our website — SouthwestDirect.com — is accessible to all users, including those with disabilities. We believe that access to information and financial services should not be limited by ability, and we work continuously to meet or exceed the standards set by the Americans with Disabilities Act (ADA) and the Web Content Accessibility Guidelines (WCAG) 2.1 Level AA.</p>

    <h2 id="standards">Standards We Follow</h2>
    <p>This website has been designed and built to conform with the Web Content Accessibility Guidelines (WCAG) 2.1, Level AA, published by the World Wide Web Consortium (W3C). These guidelines explain how to make web content more accessible for people with disabilities, and more user-friendly for everyone.</p>

    <h2 id="features">Accessibility Features</h2>
    <p>The following measures have been implemented to make this site accessible:</p>
    <ul>
      <li><strong>Semantic HTML markup</strong> so screen readers and assistive technology can accurately interpret page structure</li>
      <li><strong>Keyboard navigation</strong> for all interactive elements, with visible focus indicators</li>
      <li><strong>A “Skip to main content” link</strong> that allows keyboard and screen-reader users to bypass repeated navigation</li>
      <li><strong>Descriptive alternative text</strong> for all images that convey information</li>
      <li><strong>Sufficient color contrast</strong> between text and background across every page</li>
      <li><strong>Responsive design</strong> that adapts to phones, tablets, and desktop screens without loss of functionality</li>
      <li><strong>Clear and consistent navigation</strong> across all pages</li>
      <li><strong>Descriptive link text</strong> that makes sense out of context</li>
      <li><strong>Properly structured headings</strong> to help users navigate content</li>
    </ul>

    <h2 id="ongoing">Ongoing Effort</h2>
    <p>Accessibility is an ongoing effort rather than a one-time milestone. We regularly review this site for accessibility issues and address any problems as they are identified. As we update content or add new features, we work to maintain conformance with WCAG 2.1 Level AA.</p>

    <h2 id="accommodations">Requesting Accommodations or Reporting Barriers</h2>
    <p>If you experience any difficulty accessing information or using any feature of this website, or if you have suggestions for how we can improve accessibility, please contact us. We will make every reasonable effort to provide the information you need in an alternative format and to address the issue.</p>
    <p><strong>Contact for accessibility concerns:</strong></p>
    <ul>
      <li><strong>Phone:</strong> <a href="tel:{PHONE_TEL}">{PHONE_DISPLAY}</a></li>
      <li><strong>Email:</strong> <a href="mailto:{EMAIL_PAGE}">{EMAIL_PAGE}</a></li>
      <li><strong>Mail:</strong> Southwest Bancorp, 5151 California Ave STE 100, Irvine, CA 92617-3205</li>
    </ul>
    <p>We aim to respond to accessibility inquiries within three business days.</p>

    <h2 id="third-party">Third-Party Content</h2>
    <p>While we work to ensure our own content meets accessibility standards, we cannot guarantee the accessibility of third-party content or services linked from this site (for example, external regulatory websites such as www.DRE.CA.gov). If you encounter accessibility barriers on linked sites, we encourage you to contact those providers directly.</p>

    <h2 id="complaints">Formal Complaints</h2>
    <p>If you are not satisfied with our response to an accessibility concern, you may file a complaint with the U.S. Department of Justice, Civil Rights Division, at <a href="https://www.ada.gov">ada.gov</a> or by calling <a href="tel:+18005140301">(800) 514-0301</a>.</p>
  </div>

  {contact()}
</main>'''


PRIVACY_BODY = f'''<main id="main">
  <div class="page-head">
    <div class="page-head-inner">
      <h1 class="page-title">Privacy Policy &amp; Terms of Service</h1>
    </div>
  </div>

  <div class="prose">
    <p class="updated">Last updated: {UPDATED}</p>

    <p class="lead"><em>This page combines our Privacy Policy and Terms of Service into a single document for clarity. Please read both sections carefully. By using SouthwestDirect.com, you agree to these terms.</em></p>

    <div class="toc">
      <h2>On this page</h2>
      <ul>
        <li><a href="#privacy">Privacy Policy</a></li>
        <li><a href="#terms">Terms of Service</a></li>
      </ul>
    </div>

    <h2 id="privacy">Privacy Policy</h2>

    <h3>Introduction</h3>
    <p>Southwest Bancorp (“we,” “us,” “our”) operates SouthwestDirect.com (the “Site”). This Privacy Policy explains what information we collect when you visit the Site, how we use it, and your rights regarding that information.</p>
    <p>This policy applies only to information collected through this website. It does not cover information you provide to us through other channels — telephone conversations, email correspondence, loan applications, or in-person meetings — which is governed by our lending disclosures and applicable financial-privacy laws (see “Financial Privacy” below).</p>

    <h3>Information We Collect</h3>
    <p><strong>We collect very little information through this website.</strong> SouthwestDirect.com is a static informational site. We do not use cookies, analytics tracking, advertising pixels, session recording, or any other tools that collect visitor data automatically. We do not have contact forms on this site.</p>
    <p>The only way information is transmitted to us through this website is if you choose to call, text, or email us using the contact information provided. In that case, we receive whatever information you provide in your communication — your name, phone number, email address, and the content of your message.</p>

    <h3>How We Use Information You Send Us</h3>
    <p>If you contact us via phone, text, or email using the information listed on the Site, we use that information solely to:</p>
    <ul>
      <li>Respond to your inquiry</li>
      <li>Discuss potential lending opportunities</li>
      <li>Provide requested information about our services</li>
    </ul>
    <p>We do not sell, rent, or share your contact information with third parties for marketing purposes.</p>

    <h3>Financial Privacy (Gramm-Leach-Bliley Act)</h3>
    <p>If you become a borrower or otherwise establish a customer relationship with Southwest Bancorp, we collect and use nonpublic personal information as required to originate, fund, and service your loan. Our full financial-privacy practices — including your rights under the Gramm-Leach-Bliley Act (GLBA) — are provided in the disclosures you receive as part of the loan application and closing process.</p>

    <h3>California Consumer Rights (CCPA / CPRA)</h3>
    <p>If you are a California resident, the California Consumer Privacy Act (CCPA) and California Privacy Rights Act (CPRA) provide you with certain rights regarding personal information we collect about you. These include the right to:</p>
    <ul>
      <li>Know what personal information we collect and how we use it</li>
      <li>Request deletion of your personal information (subject to legal retention requirements)</li>
      <li>Correct inaccurate personal information</li>
      <li>Opt out of the sale or sharing of personal information (note: we do not sell or share personal information)</li>
      <li>Non-discrimination for exercising your CCPA rights</li>
    </ul>
    <p>To exercise any of these rights, contact us at <a href="mailto:{EMAIL_PAGE}">{EMAIL_PAGE}</a> or <a href="tel:{PHONE_TEL}">{PHONE_DISPLAY}</a>. We will verify your identity before responding to your request and will respond within the timeframes required by law.</p>

    <h3>Information Security</h3>
    <p>We take reasonable measures to protect the information you send us. However, no method of transmission over the internet is 100% secure. Please do not send sensitive information (such as Social Security numbers, financial account numbers, or copies of identification documents) via unencrypted email. If you need to transmit sensitive information, please call us to arrange a secure method.</p>

    <h3>Children’s Privacy</h3>
    <p>This Site is not directed to children under 13, and we do not knowingly collect information from children under 13.</p>

    <h3>Changes to This Policy</h3>
    <p>We may update this Privacy Policy from time to time. When we do, we will post the updated policy on this page with a revised “Last updated” date at the top.</p>

    <h3>Contact Us About Privacy</h3>
    <p>Questions about this Privacy Policy:</p>
    <ul>
      <li><strong>Phone:</strong> <a href="tel:{PHONE_TEL}">{PHONE_DISPLAY}</a></li>
      <li><strong>Email:</strong> <a href="mailto:{EMAIL_PAGE}">{EMAIL_PAGE}</a></li>
      <li><strong>Mail:</strong> Southwest Bancorp, 5151 California Ave STE 100, Irvine, CA 92617-3205</li>
    </ul>

    <h2 id="terms">Terms of Service</h2>

    <h3>Acceptance of Terms</h3>
    <p>By accessing or using SouthwestDirect.com (the “Site”), you agree to be bound by these Terms of Service. If you do not agree, please do not use the Site.</p>

    <h3>About Southwest Bancorp</h3>
    <p>Southwest Bancorp is a licensed real estate broker and mortgage lender operating in California. Our lending activities are regulated by the California Department of Real Estate (DRE) and, where applicable, subject to the requirements of the Nationwide Multistate Licensing System (NMLS).</p>
    <ul>
      <li><strong>Southwest Bancorp:</strong> California DRE Broker License No. 00898122; NMLS ID No. 285731</li>
      <li><strong>Joffrey Long:</strong> California DRE Broker License No. 00525142; NMLS ID No. 207202</li>
    </ul>
    <p>Our license status may be verified at <a href="https://www.DRE.CA.gov">www.DRE.CA.gov</a> and <a href="https://www.nmlsconsumeraccess.org">www.nmlsconsumeraccess.org</a>.</p>

    <h3>Nature of Information Provided</h3>
    <p>The information on this Site is provided for general informational purposes only. It is not, and should not be relied upon as:</p>
    <ul>
      <li>An offer to lend or extend credit</li>
      <li>A commitment to make a loan on any specific terms</li>
      <li>Legal, tax, financial, or investment advice</li>
      <li>A guarantee of loan approval, interest rate, or loan terms</li>
    </ul>
    <p>Every lending decision depends on individual circumstances, the specific property, market conditions, and underwriting review. Any loan terms discussed will be formalized only through a written loan agreement.</p>

    <h3>What We Do</h3>
    <p>Southwest Bancorp originates and services real estate loans primarily to real estate investors and business owners for investment or business purposes. We do not fund consumer-purpose loans secured by 1-4 family residences directly; those loans, where offered, may be arranged with institutional lenders under NMLS Identifier No. 285731 (Southwest Bancorp) and No. 207202 (Joffrey Long).</p>
    <p>We lend in California only. We do not make loans on vacant land (unless producing rental income), or in rural or very small communities.</p>

    <h3>Investment Risk Disclosure</h3>
    <p>Investments in trust deeds secured by one or more interests in real property are subject to risk of loss, including loss of principal. Past performance does not guarantee future results. Any investment described or referenced on this Site is offered only to qualified investors and only after the loan has been initially funded and closed by Southwest Bancorp.</p>

    <h3>Third-Party Links</h3>
    <p>This Site may contain links to third-party websites (for example, regulatory sites such as www.DRE.CA.gov). We provide these links for convenience only. We are not responsible for the content, accuracy, privacy practices, or availability of any third-party site.</p>

    <h3>Intellectual Property</h3>
    <p>The content of this Site — including text, graphics, images, logos, and layout — is owned by or licensed to Southwest Bancorp and is protected by U.S. copyright and trademark laws. You may view and print pages of this Site for your personal, non-commercial use. Any other use — including reproduction, republication, distribution, or modification — requires our prior written consent.</p>

    <h3>Prohibited Uses</h3>
    <p>You agree not to use this Site to:</p>
    <ul>
      <li>Attempt to gain unauthorized access to any portion of the Site or its underlying systems</li>
      <li>Interfere with the Site’s operation or security</li>
      <li>Use automated tools to scrape, harvest, or extract content in violation of applicable law</li>
      <li>Submit false, misleading, or fraudulent information in any communication with us</li>
    </ul>

    <h3>Limitation of Liability</h3>
    <p>To the fullest extent permitted by law, Southwest Bancorp and its officers, directors, employees, and affiliates will not be liable for any indirect, incidental, consequential, special, or punitive damages arising out of or related to your use of this Site or your reliance on any information provided through it.</p>
    <p>The Site and its content are provided “as is” without warranties of any kind, either express or implied, including but not limited to warranties of merchantability, fitness for a particular purpose, or non-infringement.</p>

    <h3>Governing Law and Jurisdiction</h3>
    <p>These Terms are governed by the laws of the State of California, without regard to conflict-of-law principles. Any dispute arising out of or relating to these Terms or your use of the Site will be resolved exclusively in the state or federal courts located in Orange County, California, and you consent to the personal jurisdiction of those courts.</p>

    <h3>Changes to These Terms</h3>
    <p>We may update these Terms from time to time. When we do, we will post the updated Terms on this page with a revised “Last updated” date. Your continued use of the Site after changes are posted constitutes your acceptance of the revised Terms.</p>

    <h3>Contact Us About These Terms</h3>
    <p>Questions about these Terms of Service:</p>
    <ul>
      <li><strong>Phone:</strong> <a href="tel:{PHONE_TEL}">{PHONE_DISPLAY}</a></li>
      <li><strong>Email:</strong> <a href="mailto:{EMAIL_PAGE}">{EMAIL_PAGE}</a></li>
      <li><strong>Mail:</strong> Southwest Bancorp, 5151 California Ave STE 100, Irvine, CA 92617-3205</li>
    </ul>

    <p class="closing"><em>Southwest Bancorp is an equal opportunity lender.</em></p>
  </div>

  {contact()}
</main>'''


NOTFOUND_BODY = f'''<main id="main">
  <div class="page-head">
    <div class="page-head-inner">
      <p class="eyebrow">Error 404</p>
      <h1 class="page-title">That page isn\u2019t here</h1>
      <p class="page-sub">The link may be out of date, or the address mistyped. Everything on this site lives on the home page \u2014 or just call and ask.</p>
    </div>
  </div>

  <div class="prose">
    <p><a href="index.html">Back to the home page</a></p>
    <ul>
      <li><a href="index.html#how-it-works">How it works</a></li>
      <li><a href="index.html#property-types">Property types we lend on</a></li>
      <li><a href="index.html#brokers">For loan brokers</a></li>
      <li><a href="index.html#about">About Joffrey Long</a></li>
      <li><a href="index.html#contact">Contact</a></li>
    </ul>
    <p>Or reach Joffrey directly on <a href="tel:{PHONE_TEL}">{PHONE_DISPLAY}</a>
       or at <a href="mailto:{EMAIL_PAGE}">{EMAIL_PAGE}</a>.</p>
  </div>
</main>'''

PAGES = [
    ("index.html",
     "Joffrey Long | SouthwestDirect.com — Direct Hard Money Lender, California",
     "Direct hard-money lending for California real estate investors. Talk to Joffrey Long — a decision-maker, not a middleman. Close in 5–12 days.",
     INDEX_BODY, None, ""),
    ("accessibility-statement.html",
     "Accessibility Statement | Joffrey Long / SouthwestDirect.com",
     "Southwest Bancorp's commitment to WCAG 2.1 Level AA and ADA accessibility on SouthwestDirect.com, and how to report a barrier.",
     A11Y_BODY, "a11y", "index.html"),
    ("privacy-terms.html",
     "Privacy Policy & Terms of Service | Joffrey Long / SouthwestDirect.com",
     "Privacy Policy and Terms of Service for SouthwestDirect.com, operated by Southwest Bancorp. No cookies, no tracking, no contact forms.",
     PRIVACY_BODY, "privacy", "index.html"),
    ("404.html",
     "Page not found | Joffrey Long / SouthwestDirect.com",
     "That page could not be found. Return to SouthwestDirect.com, or call Joffrey Long directly on (818) 635-1777.",
     NOTFOUND_BODY, None, "index.html"),
]

for path, title, desc, body, current, prefix in PAGES:
    html = page(title, desc, path, body, current, prefix)
    with open(os.path.join(ROOT, path), "w") as f:
        f.write(html)
    print(f"  {path}  ({len(html):,} bytes)")
