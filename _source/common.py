"""Shared layout pieces for the DPayments static site."""

SITE = "https://dpayments.co.uk"
EMAIL = "info@dpayments.co.uk"

# --- Icons (stroke, 24px) -------------------------------------------------
_P = {
    "terminal": '<rect x="6" y="2" width="12" height="20" rx="2.5"/><rect x="8.5" y="5" width="7" height="5" rx="1"/><path d="M9 14h.01M12 14h.01M15 14h.01M9 17h.01M12 17h.01M15 17h.01"/>',
    "globe": '<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3a14 14 0 0 1 0 18M12 3a14 14 0 0 0 0 18"/>',
    "phone": '<path d="M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2"/>',
    "link": '<path d="M10 13a5 5 0 0 0 7.5.5l3-3a5 5 0 0 0-7-7l-1.7 1.7"/><path d="M14 11a5 5 0 0 0-7.5-.5l-3 3a5 5 0 0 0 7 7l1.7-1.7"/>',
    "repeat": '<path d="M17 2l4 4-4 4"/><path d="M3 11V9a3 3 0 0 1 3-3h15"/><path d="M7 22l-4-4 4-4"/><path d="M21 13v2a3 3 0 0 1-3 3H3"/>',
    "cart": '<circle cx="9" cy="20" r="1.5"/><circle cx="18" cy="20" r="1.5"/><path d="M2 3h3l2.6 12.4a2 2 0 0 0 2 1.6h8.8a2 2 0 0 0 2-1.6L22 7H6"/>',
    "search": '<circle cx="11" cy="11" r="7"/><path d="M21 21l-4.3-4.3"/>',
    "scale": '<path d="M12 3v18M5 21h14M6 7h12M6 7l-3 7a3 3 0 0 0 6 0zM18 7l-3 7a3 3 0 0 0 6 0z"/>',
    "clipboard": '<rect x="5" y="4" width="14" height="18" rx="2"/><path d="M9 4V3h6v1M9 11h6M9 15h4"/>',
    "eye": '<path d="M2 12s3.5-7 10-7 10 7 10 7-3.5 7-10 7S2 12 2 12z"/><circle cx="12" cy="12" r="3"/>',
    "shield": '<path d="M12 2l8 3v6c0 5-3.5 9.5-8 11-4.5-1.5-8-6-8-11V5z"/><path d="M9 12l2 2 4-4"/>',
    "wallet": '<rect x="2" y="6" width="20" height="14" rx="2.5"/><path d="M2 10h20M16 15h2"/>',
    "plug": '<path d="M9 2v6M15 2v6M6 8h12v3a6 6 0 0 1-12 0zM12 17v5"/>',
    "wifi": '<path d="M2 8.8a15 15 0 0 1 20 0M5 12.5a10 10 0 0 1 14 0M8.5 16.1a5 5 0 0 1 7 0M12 20h.01"/>',
    "signal": '<path d="M4 20v-3M9 20v-7M14 20V9M19 20V4"/>',
    "lock": '<rect x="4" y="10" width="16" height="11" rx="2"/><path d="M8 10V7a4 4 0 0 1 8 0v3"/>',
    "coins": '<ellipse cx="9" cy="7" rx="6" ry="3"/><path d="M3 7v5c0 1.7 2.7 3 6 3s6-1.3 6-3V7"/><path d="M9 15v2c0 1.7 2.7 3 6 3s6-1.3 6-3v-5c0-1.7-2.7-3-6-3"/>',
    "users": '<circle cx="9" cy="8" r="3.5"/><path d="M2 20a7 7 0 0 1 14 0"/><path d="M16 4.5a3.5 3.5 0 0 1 0 7M22 20a7 7 0 0 0-4-6.3"/>',
    "store": '<path d="M3 9l1.5-5h15L21 9M3 9v11h18V9M3 9a3 3 0 0 0 6 0 3 3 0 0 0 6 0 3 3 0 0 0 6 0"/><path d="M10 20v-5h4v5"/>',
    "cup": '<path d="M4 8h13v5a6 6 0 0 1-6 6h-1a6 6 0 0 1-6-6z"/><path d="M17 9h1.5a2.5 2.5 0 0 1 0 5H17M7 2v3M11 2v3"/>',
    "tool": '<path d="M14.7 6.3a4 4 0 0 0 5 5L22 14l-8 8-2.3-2.3a4 4 0 0 0-5-5L2 10l8-8z"/>',
    "briefcase": '<rect x="2" y="7" width="20" height="13" rx="2"/><path d="M8 7V5a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2M2 13h20"/>',
    "heart": '<path d="M12 21s-8-5-8-11a4.5 4.5 0 0 1 8-2.8A4.5 4.5 0 0 1 20 10c0 6-8 11-8 11z"/>',
    "ticket": '<path d="M3 7a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2v3a2 2 0 0 0 0 4v3a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-3a2 2 0 0 0 0-4z"/><path d="M14 5v14" stroke-dasharray="2 2"/>',
    "car": '<path d="M5 17h14M3 13l2-6a2 2 0 0 1 2-1.5h10A2 2 0 0 1 19 7l2 6v5h-3v-1H6v1H3z"/><circle cx="7.5" cy="13.5" r="1"/><circle cx="16.5" cy="13.5" r="1"/>',
    "mail": '<rect x="2" y="4" width="20" height="16" rx="2.5"/><path d="M2 7l10 7 10-7"/>',
    "file": '<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><path d="M14 2v6h6M8 13h8M8 17h6"/>',
    "chart": '<path d="M3 3v18h18"/><path d="M7 15l4-4 3 3 5-6"/>',
    "card": '<rect x="2" y="5" width="20" height="14" rx="2.5"/><path d="M2 10h20M6 15h4"/>',
    "bank": '<path d="M3 10l9-6 9 6M5 10v8M9.5 10v8M14.5 10v8M19 10v8M3 21h18"/>',
    "check": '<path d="M5 12.5l4.5 4.5L19 7.5"/>',
    "alert": '<path d="M12 3l10 18H2z"/><path d="M12 10v4M12 17.5h.01"/>',
    "clock": '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
    "receipt": '<path d="M5 2h14v20l-3-2-2 2-2-2-2 2-2-2-3 2z"/><path d="M9 7h6M9 11h6M9 15h4"/>',
    "refresh": '<path d="M21 12a9 9 0 0 1-15.5 6.2L3 16M3 12a9 9 0 0 1 15.5-6.2L21 8"/><path d="M21 3v5h-5M3 21v-5h5"/>',
    "sparkle": '<path d="M12 3l1.8 5.2L19 10l-5.2 1.8L12 17l-1.8-5.2L5 10l5.2-1.8z"/><path d="M19 17l.8 2.2L22 20l-2.2.8L19 23l-.8-2.2L16 20l2.2-.8z"/>',
    "contactless": '<path d="M8.5 8.5a5 5 0 0 1 0 7M12 6a8.5 8.5 0 0 1 0 12M15.5 3.5a12 12 0 0 1 0 17"/>',
}


def icon(name, cls="icon"):
    svg = f'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{_P[name]}</svg>'
    return f'<div class="{cls}">{svg}</div>' if cls else svg


TICK = '<span class="tick"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12.5l4.5 4.5L19 7.5"/></svg></span>'
ARROW = '<span class="arrow" aria-hidden="true">&rarr;</span>'


def ticks(items):
    return '<ul class="feature-list">' + "".join(f"<li>{TICK}<span>{i}</span></li>" for i in items) + "</ul>"


LOGO_MARK = ('<rect x="0" y="2" width="32" height="32" rx="9" fill="#0e9c74"/>'
             '<path d="M10 10h6.2c5 0 8.3 3.1 8.3 8s-3.3 8-8.3 8H10z" fill="none" stroke="#fff" stroke-width="3"/>'
             '<path d="M14.5 15.2a4 4 0 0 1 0 5.6" fill="none" stroke="#fff" stroke-width="2" stroke-linecap="round"/>')


def logo(color="#0d1b26"):
    return (f'<svg viewBox="0 0 176 36" height="30" role="img" aria-label="DPayments">{LOGO_MARK}'
            f'<text x="42" y="26" font-family="Manrope, Inter, Arial, sans-serif" font-size="22" font-weight="800" letter-spacing="-0.6" fill="{color}">DPayments</text></svg>')


TAGLINE = ("Independent UK payments partner. We help businesses take card payments in person, "
           "online and over the phone &mdash; and help existing merchants cut what they pay.")


def header(current):
    from menu import menu, MENU_SOLUTIONS, MENU_INDUSTRIES, MENU_COMPANY, CRYPTO_URL
    sw = ' aria-current="page"' if current == "/switch/" else ""
    return f"""<a class="skip" href="#main">Skip to content</a>
<header class="site-header">
  <div class="container nav">
    <a class="logo" href="/" aria-label="DPayments home">{logo()}</a>
    <button class="menu-toggle" type="button" aria-label="Menu" aria-expanded="false" aria-controls="nav-links"><span></span></button>
    <ul class="nav-links" id="nav-links">
      {menu("Solutions", MENU_SOLUTIONS, current, "sol")}
      {menu("Industries", MENU_INDUSTRIES, current, "ind")}
      <li><a class="top-link" href="{CRYPTO_URL}">Crypto <span class="ext" aria-hidden="true">&#8599;</span></a></li>
      <li><a class="top-link" href="/switch/"{sw}>Switch &amp; save</a></li>
      {menu("Company", MENU_COMPANY, current, "co")}
      <li class="nav-cta"><a class="btn btn-primary btn-sm" href="/contact/">Get a quote</a></li>
    </ul>
  </div>
</header>"""


def cta_band(title="Tell us how you take payments. We&rsquo;ll do the rest.",
             text="Send a few details and we&rsquo;ll come back by email with a tailored quote &mdash; or a plain-English review of what you pay today.",
             subject=None):
    mail = f"mailto:{EMAIL}" + (f"?subject={subject}" if subject else "")
    return f'''<section class="section-tight">
  <div class="container">
    <div class="cta-band reveal">
      <div>
        <h2>{title}</h2>
        <p>{text}</p>
      </div>
      <div class="btn-row">
        <a class="btn btn-accent" href="/contact/">Get a quote {ARROW}</a>
        <a class="email-link" href="{mail}">or email {EMAIL}</a>
      </div>
    </div>
  </div>
</section>'''


def footer():
    return f'''<footer class="site-footer">
  <div class="container">
    <div class="footer-grid">
      <div class="footer-brand">
        <a href="/" aria-label="DPayments home">{logo("#ffffff")}</a>
        <p style="margin-top:18px">{TAGLINE}</p>
        <p><a href="mailto:{EMAIL}">{EMAIL}</a></p>
      </div>
      <div>
        <h4>Solutions</h4>
        <ul>
          <li><a href="/online-payments/">Online payment gateway</a></li>
          <li><a href="/card-machines/">POS &amp; card machines</a></li>
          <li><a href="/solutions/multi-currency/">Multi-currency</a></li>
          <li><a href="/solutions/settlements/">Settlements</a></li>
          <li><a href="/solutions/orchestration/">Payment orchestration</a></li>
          <li><a href="/solutions/risk-fraud/">Risk &amp; fraud</a></li>
          <li><a href="https://crypto.dpayments.co.uk">Crypto payments</a></li>
        </ul>
      </div>
      <div>
        <h4>Who we help</h4>
        <ul>
          <li><a href="/industries/#retail">Retail</a></li>
          <li><a href="/industries/#hospitality">Restaurants &amp; bars</a></li>
          <li><a href="/industries/#ecommerce">Ecommerce</a></li>
          <li><a href="/industries/igaming/">iGaming</a></li>
          <li><a href="/industries/forex/">Forex &amp; CFD</a></li>
          <li><a href="/industries/financial-brokerage/">Financial brokerage</a></li>
          <li><a href="/industries/">All industries</a></li>
        </ul>
      </div>
      <div>
        <h4>Company</h4>
        <ul>
          <li><a href="/how-it-works/">How it works</a></li>
          <li><a href="/faq/">FAQ</a></li>
          <li><a href="/switch/">Switch &amp; save</a></li>
          <li><a href="/contact/">Get a quote</a></li>
        </ul>
      </div>
    </div>
    <div class="footer-bottom">
      <span>&copy; <span data-year>2026</span> DPayments. Payments partner for UK business.</span>
      <ul>
        <li><a href="/privacy/">Privacy</a></li>
        <li><a href="/terms/">Terms</a></li>
        <li><a href="/cookies/">Cookies</a></li>
      </ul>
    </div>
  </div>
</footer>'''


def page(path, title, description, body, current=None, schema=""):
    canonical = SITE + path
    return f'''<!doctype html>
<html lang="en-GB">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{description}">
<link rel="canonical" href="{canonical}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="DPayments">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{description}">
<meta property="og:url" content="{canonical}">
<meta name="theme-color" content="#0d1b26">
<link rel="icon" href="/assets/img/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Manrope:wght@600;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/css/style.css">
{schema}
</head>
<body>
{header(current)}
<main id="main">
{body}
</main>
{footer()}
<script src="/assets/js/main.js" defer></script>
</body>
</html>
'''
