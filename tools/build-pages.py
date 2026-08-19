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

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

PHONE_DISPLAY = "(818) 635-1777"
PHONE_TEL     = "+18186351777"
EMAIL_PAGE    = "Joffrey@asksw.com"   # as it appears in the approved design
EMAIL_SCHEMA  = "info@asksw.com"      # as supplied for structured data
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
  "identifier": [
    { "@type": "PropertyValue", "name": "California DRE License", "value": "00898122" },
    { "@type": "PropertyValue", "name": "NMLS ID", "value": "285731" }
  ],
  "employee": {
    "@type": "Person",
    "@id": "%(url)s/#joffrey-long",
    "name": "Joffrey Long",
    "jobTitle": "Direct hard-money lender",
    "telephone": "%(tel)s",
    "identifier": [
      { "@type": "PropertyValue", "name": "California DRE License", "value": "00525142" },
      { "@type": "PropertyValue", "name": "NMLS ID", "value": "207202" }
    ]
  }
}
</script>''' % {"url": PROD_URL, "tel": PHONE_TEL, "email": EMAIL_SCHEMA}


def head(title, desc, page_path, og_type="website"):
    return f'''<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">

<!-- PREVIEW ONLY — remove this line before the production launch. -->
<meta name="robots" content="noindex, nofollow">

<link rel="canonical" href="{PROD_URL}/{page_path}">

<!-- Open Graph / social sharing -->
<meta property="og:type" content="{og_type}">
<meta property="og:site_name" content="Joffrey Long / SouthwestDirect.com">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{PROD_URL}/{page_path}">
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
<meta name="theme-color" content="#1E2A5E">

<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Source+Serif+4:opsz,wght@8..60,400;8..60,600;8..60,700&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/css/site.css">

{JSONLD}'''


def header(prefix=""):
    """prefix is '' on the landing page, 'index.html' on the legal pages."""
    return f'''<a class="skip-link" href="#main">Skip to main content</a>

<header class="site-header">
  <div class="header-inner">
    <a class="brand" href="index.html">
      <span class="brand-name">Joffrey Long</span>
      <span class="brand-domain">SouthwestDirect.com</span>
    </a>
    <nav class="main-nav" aria-label="Main">
      <a class="nav-link" href="{prefix}#how-it-works">How it works</a>
      <a class="nav-link" href="{prefix}#property-types">Property types</a>
      <a class="nav-link" href="{prefix}#brokers">Loan brokers</a>
      <a class="nav-link" href="{prefix}#about">About</a>
      <a class="nav-link" href="{prefix}#contact">Contact</a>
      <a class="btn-primary btn-nav" href="tel:{PHONE_TEL}">Call or Text {PHONE_DISPLAY}</a>
    </nav>
  </div>
</header>'''


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
      <iframe class="map-frame"
              title="Map showing the office location: 5151 California Ave STE 100, Irvine, California"
              src="https://www.openstreetmap.org/export/embed.html?bbox=-117.8630%2C33.6420%2C-117.8250%2C33.6650&amp;layer=mapnik&amp;marker=33.65350%2C-117.84400"
              loading="lazy"></iframe>
      <p class="map-note"><a href="https://www.openstreetmap.org/?mlat=33.65350&amp;mlon=-117.84400#map=15/33.6535/-117.8440">View a larger map on OpenStreetMap</a></p>
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
    <p class="footer-meta">5151 California Ave STE 100, Irvine, CA 92617-3205 &middot; <a href="tel:{PHONE_TEL}">{PHONE_DISPLAY}</a> &middot; <a href="mailto:{EMAIL_PAGE}">{EMAIL_PAGE}</a></p>
  </div>
</footer>'''


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
</body>
</html>
'''


# --------------------------------------------------------------------------
# Property-type cards (expanded from the design's sc-for loop)
# --------------------------------------------------------------------------
CARD_SIZES = "(min-width: 1168px) 341px, (min-width: 700px) 31vw, 92vw"

PROPERTY_TYPES = [
    ("residential-rental-property", "Residential Rental Property", "1–4 units or 5–15 units",
     "Two-story gray residential rental duplex with a garage, near the California coast",
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
     "Single-story commercial building with a red awning and parking lot",
     ["Houses of worship", "Specialty properties", "Legal, non-confirming OK", "Truck parking lots"]),
]


def card(slug, title, note, alt, bullets):
    note_html = f'\n              <p class="card-note">{note}</p>' if note else ""
    lis = "\n".join(f"              <li>{b}</li>" for b in bullets)
    return f'''          <li class="card">
            <picture>
              <source type="image/webp" sizes="{CARD_SIZES}"
                      srcset="images/{slug}-400.webp 400w, images/{slug}-750.webp 750w">
              <img class="card-img" src="images/{slug}-750.jpg" sizes="{CARD_SIZES}"
                   srcset="images/{slug}-400.jpg 400w, images/{slug}-750.jpg 750w"
                   width="750" height="400" loading="lazy" decoding="async"
                   alt="{alt}">
            </picture>
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
        <picture>
          <source type="image/webp" sizes="(min-width: 900px) 320px, (min-width: 560px) 40vw, 80vw"
                  srcset="images/joffrey-long-320.webp 320w, images/joffrey-long-640.webp 640w, images/joffrey-long-748.webp 748w">
          <img class="hero-img" src="images/joffrey-long-640.jpg"
               sizes="(min-width: 900px) 320px, (min-width: 560px) 40vw, 80vw"
               srcset="images/joffrey-long-320.jpg 320w, images/joffrey-long-640.jpg 640w, images/joffrey-long-748.jpg 748w"
               width="748" height="839" fetchpriority="high" decoding="async"
               alt="Joffrey Long, direct hard-money lender">
        </picture>
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
      <picture>
        <source type="image/webp" sizes="(min-width: 900px) 300px, (min-width: 560px) 40vw, 80vw"
                srcset="images/joffrey-long-320.webp 320w, images/joffrey-long-640.webp 640w, images/joffrey-long-748.webp 748w">
        <img class="about-img" src="images/joffrey-long-640.jpg"
             sizes="(min-width: 900px) 300px, (min-width: 560px) 40vw, 80vw"
             srcset="images/joffrey-long-320.jpg 320w, images/joffrey-long-640.jpg 640w, images/joffrey-long-748.jpg 748w"
             width="748" height="839" loading="lazy" decoding="async"
             alt="Joffrey Long, hard-money lender and California Mortgage Association board member">
      </picture>
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

  <!-- ======================================================================
       Real photo needed here — do not use AI illustration.
       The approved design had a full-bleed California coastline band between
       the contact section and the footer. The source file for it
       (uploads/Firefly (1).jpg) is an AI-generated illustration and was
       pulled at Nathan's request on 2026-08-19. Drop a real licensed photo
       in and restore the band before launch.
       ====================================================================== -->

</main>'''


A11Y_BODY = f'''<main id="main">
  <div class="page-head">
    <div class="page-head-inner">
      <h1 class="page-title">Accessibility statement</h1>
      <p class="page-sub">Our commitment to making SouthwestDirect.com usable by everyone, including people who use assistive technology.</p>
    </div>
  </div>

  <div class="prose">
    <p class="updated">Last updated: {UPDATED}</p>

    <div class="toc">
      <h2>On this page</h2>
      <ul>
        <li><a href="#commitment">Our commitment</a></li>
        <li><a href="#standard">Conformance standard</a></li>
        <li><a href="#measures">Measures we take</a></li>
        <li><a href="#compatibility">Compatibility with browsers and assistive technology</a></li>
        <li><a href="#limitations">Known limitations</a></li>
        <li><a href="#feedback">Feedback and contact</a></li>
        <li><a href="#formal">Formal complaints</a></li>
      </ul>
    </div>

    <h2 id="commitment">Our commitment</h2>
    <p>Joffrey Long / SouthwestDirect.com is committed to ensuring digital accessibility for people with disabilities. We are continually improving the user experience for everyone and applying the relevant accessibility standards.</p>

    <h2 id="standard">Conformance standard</h2>
    <p>The <a href="https://www.w3.org/TR/WCAG21/">Web Content Accessibility Guidelines (WCAG)</a> define requirements for designers and developers to improve accessibility for people with disabilities. They define three levels of conformance: Level A, Level AA, and Level AAA.</p>
    <p>SouthwestDirect.com is <strong>fully conformant with WCAG 2.1 Level AA</strong>. Fully conformant means that the content fully conforms to the accessibility standard without any exceptions.</p>

    <h2 id="measures">Measures we take</h2>
    <p>We take the following measures to ensure accessibility:</p>
    <ul>
      <li>Include accessibility as a requirement when we design and build pages.</li>
      <li>Use semantic HTML landmarks so screen reader users can navigate by region.</li>
      <li>Provide a "skip to main content" link on every page.</li>
      <li>Provide meaningful alternative text for every image that conveys information.</li>
      <li>Maintain colour contrast that meets or exceeds WCAG 2.1 Level AA ratios.</li>
      <li>Ensure every interactive element is reachable and operable with a keyboard alone, with a clearly visible focus indicator.</li>
      <li>Respect the operating system "reduce motion" preference.</li>
      <li>Test pages with automated tooling and manual keyboard and screen reader checks.</li>
    </ul>

    <h2 id="compatibility">Compatibility with browsers and assistive technology</h2>
    <p>SouthwestDirect.com is designed to be compatible with recent versions of the following:</p>
    <ul>
      <li>Chrome, Edge, Firefox, and Safari on desktop.</li>
      <li>Safari on iOS and Chrome on Android.</li>
      <li>VoiceOver on macOS and iOS, NVDA and JAWS on Windows, and TalkBack on Android.</li>
    </ul>
    <p>This site does not rely on JavaScript for any of its content or navigation.</p>

    <h2 id="limitations">Known limitations</h2>
    <p>Despite our best efforts, some limitations may remain. Below is a list of known issues, along with potential solutions. Please contact us if you encounter a problem not listed here.</p>
    <ul>
      <li><strong>Embedded map.</strong> The office location map is provided by OpenStreetMap, a third party. Its interactive controls may not fully meet Level AA. The complete office address is always provided as text immediately beside the map, so no information is available only within the map.</li>
    </ul>

    <h2 id="feedback">Feedback and contact</h2>
    <p>We welcome your feedback on the accessibility of SouthwestDirect.com. If you encounter a barrier, or need information on this site in a different format, please let us know:</p>
    <ul>
      <li>Phone: <a href="tel:{PHONE_TEL}">{PHONE_DISPLAY}</a></li>
      <li>E-mail: <a href="mailto:{EMAIL_PAGE}">{EMAIL_PAGE}</a></li>
      <li>Postal address: 5151 California Ave STE 100, Irvine, CA 92617-3205</li>
    </ul>
    <p>We try to respond to accessibility feedback within five business days.</p>

    <h2 id="formal">Formal complaints</h2>
    <p>If you contact us with a complaint and are not satisfied with our response, you may escalate the matter. In the United States, complaints regarding accessibility may be directed to the U.S. Department of Justice Civil Rights Division.</p>
  </div>

  {contact()}
</main>'''


PRIVACY_BODY = f'''<main id="main">
  <div class="page-head">
    <div class="page-head-inner">
      <h1 class="page-title">Privacy policy &amp; terms of service</h1>
      <p class="page-sub">How we handle information you share with us, and the terms that apply to your use of this website.</p>
    </div>
  </div>

  <div class="prose">
    <p class="updated">Last updated: {UPDATED}</p>

    <div class="toc">
      <h2>On this page</h2>
      <ul>
        <li><a href="#privacy">Part one — Privacy policy</a></li>
        <li><a href="#terms">Part two — Terms of service</a></li>
      </ul>
    </div>

    <h2 id="privacy">Part one — Privacy policy</h2>

    <h3>Who we are</h3>
    <p>This website is operated by Southwest Bancorp, doing business as Joffrey Long / SouthwestDirect.com, 5151 California Ave STE 100, Irvine, CA 92617-3205.</p>

    <h3>Information we collect</h3>
    <p>This website does not have contact forms and does not require you to create an account. We collect personal information only when you choose to give it to us — for example, when you call, text, or e-mail us about a loan.</p>
    <p>Information you provide in that way may include your name, telephone number, e-mail address, details of the property involved, and financial information relevant to a loan request.</p>

    <h3>How we use information</h3>
    <p>We use information you provide to respond to your enquiry, evaluate and process loan requests, service loans we make, and meet our legal, regulatory, and licensing obligations. We do not sell your personal information.</p>

    <h3>Sharing information</h3>
    <p>We may share information with third parties where it is necessary to evaluate, fund, or service a loan — for example with escrow and title companies, appraisers, credit reporting agencies, loan servicers, and private party investors to whom a loan is sold after funding. We may also disclose information where required by law or regulation.</p>

    <h3>Cookies and analytics</h3>
    <p>This website does not set advertising or tracking cookies. Map content is embedded from OpenStreetMap and web fonts are served by Google Fonts; those third parties may receive your IP address as a normal part of delivering that content, subject to their own privacy policies.</p>

    <h3>Data retention and security</h3>
    <p>We retain personal information for as long as necessary to fulfil the purposes described above and to satisfy legal and regulatory record-keeping requirements. We maintain reasonable administrative, technical, and physical safeguards designed to protect that information.</p>

    <h3>Your California privacy rights</h3>
    <p>California residents may have rights under the California Consumer Privacy Act, as amended, including the right to know what personal information we have collected, the right to request deletion, the right to correct inaccurate information, and the right not to be discriminated against for exercising those rights. Certain information collected in connection with a loan application is regulated by the Gramm-Leach-Bliley Act and may be exempt from some of these rights.</p>
    <p>To make a request, contact us using the details below. We will verify your identity before acting on a request.</p>

    <h3>Children</h3>
    <p>This website is not directed to children under 13 and we do not knowingly collect personal information from them.</p>

    <h3>Changes to this policy</h3>
    <p>We may update this policy from time to time. The date at the top of this page shows when it was last revised.</p>

    <h3>Contacting us about privacy</h3>
    <p>Questions or requests may be directed to <a href="mailto:{EMAIL_PAGE}">{EMAIL_PAGE}</a> or <a href="tel:{PHONE_TEL}">{PHONE_DISPLAY}</a>, or by post to the address above.</p>

    <h2 id="terms">Part two — Terms of service</h2>

    <h3>Acceptance</h3>
    <p>By accessing or using this website you agree to these terms. If you do not agree, please do not use the site.</p>

    <h3>Not an offer or a commitment to lend</h3>
    <p>The content of this website is provided for general information only. Nothing on this site is an offer, a solicitation of an offer, a commitment to lend, or an approval of any loan. All loans are subject to underwriting, property evaluation, and credit approval, and terms are subject to change without notice. Rates, terms, and programmes described here may not be available for every property or borrower.</p>

    <h3>Licensing</h3>
    <p>Loans are primarily made (funded) and serviced by Southwest Bancorp under California Department of Real Estate Broker License no. 00898122. Joffrey Long holds California Department of Real Estate Broker License no. 00525142. NMLS Identifier No. 285731 (Southwest Bancorp) and No. 207202 (Joffrey Long). Southwest Bancorp does not make (fund) consumer purpose loans secured by 1-4 family residences.</p>

    <h3>No professional advice</h3>
    <p>Nothing on this website constitutes legal, tax, accounting, or investment advice. You should consult your own advisers before entering into any transaction.</p>

    <h3>Investment risk</h3>
    <p>Investments in trust deeds secured by one or more interests in real property are subject to risk of loss.</p>

    <h3>Intellectual property</h3>
    <p>All content on this website, including text, images, and design, is owned by or licensed to Southwest Bancorp and may not be reproduced or distributed without written permission.</p>

    <h3>Third party links</h3>
    <p>This site links to third party websites, including the California Department of Real Estate and OpenStreetMap. We are not responsible for the content, availability, or privacy practices of those sites.</p>

    <h3>Disclaimer of warranties</h3>
    <p>This website is provided on an "as is" and "as available" basis without warranties of any kind, express or implied, to the fullest extent permitted by law.</p>

    <h3>Limitation of liability</h3>
    <p>To the fullest extent permitted by law, Southwest Bancorp and Joffrey Long will not be liable for any indirect, incidental, consequential, or punitive damages arising out of your use of, or inability to use, this website.</p>

    <h3>Governing law</h3>
    <p>These terms are governed by the laws of the State of California, without regard to its conflict of law rules. Any dispute will be brought in the state or federal courts located in Orange County, California.</p>

    <h3>Changes to these terms</h3>
    <p>We may revise these terms at any time. Continued use of the site after a change constitutes acceptance of the revised terms.</p>

    <h3>Contact</h3>
    <p>Questions about these terms may be directed to <a href="mailto:{EMAIL_PAGE}">{EMAIL_PAGE}</a> or <a href="tel:{PHONE_TEL}">{PHONE_DISPLAY}</a>.</p>
  </div>

  {contact()}
</main>'''


PAGES = [
    ("index.html",
     "Joffrey Long | SouthwestDirect.com — Direct Hard Money Lender, California",
     "Direct hard-money lending for California real estate investors. Talk to Joffrey Long, a decision-maker, not a middleman. Close in 5–12 days. DRE #00898122, NMLS #285731.",
     INDEX_BODY, None, ""),
    ("accessibility-statement.html",
     "Accessibility statement | Joffrey Long / SouthwestDirect.com",
     "Our commitment to WCAG 2.1 Level AA accessibility on SouthwestDirect.com, known limitations, and how to give us feedback.",
     A11Y_BODY, "a11y", "index.html"),
    ("privacy-terms.html",
     "Privacy policy & terms of service | Joffrey Long / SouthwestDirect.com",
     "How Joffrey Long / SouthwestDirect.com handles your information, and the terms that apply to your use of this website.",
     PRIVACY_BODY, "privacy", "index.html"),
]

for path, title, desc, body, current, prefix in PAGES:
    html = page(title, desc, path, body, current, prefix)
    with open(os.path.join(ROOT, path), "w") as f:
        f.write(html)
    print(f"  {path}  ({len(html):,} bytes)")
