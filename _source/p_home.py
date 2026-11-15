from common import *

TITLE = "DPayments | Every Payment Method, All in One Place"
DESC = ("One partner for every way to get paid: card machines, online checkout, payment links, wallets, pay by bank, "
        "multi-currency, payouts, orchestration and crypto. Independent UK payments partner.")

CHECK = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12.5l4.5 4.5L19 7.5"/></svg>'

METHODS = ["Visa", "Mastercard", "American Express", "Apple Pay", "Google Pay", "Click to Pay", "PayPal",
           "Pay by bank", "Buy now, pay later", "Contactless", "Chip &amp; PIN", "Payment links", "Virtual terminal",
           "Recurring billing", "Multi-currency", "Card payouts", "Stablecoin", "Crypto"]


def chip(label, cls=""):
    return f'<span class="mchip {cls}">{label}</span>'


hero = f'''<section class="hhero">
  <div class="container hhero-grid">
    <div class="hhero-copy">
      <span class="eyebrow">All-in-one payments partner</span>
      <h1>Every payment.<br><em>One partner.</em></h1>
      <p class="lede">In store, online, by phone, across borders &mdash; we bring every way to get paid together in one place.</p>
      <div class="btn-row">
        <a class="btn btn-primary" href="/contact/">Get a quote {ARROW}</a>
        <a class="btn btn-ghost" href="/solutions/">Explore solutions</a>
      </div>
    </div>
    <div class="scene" aria-hidden="true">
      <div class="glow"></div>
      <div class="laptop">
        <div class="lp-screen">
          <div class="lp-top"><i></i><i></i><i></i></div>
          <div class="lp-body">
            <div class="lp-side"><b></b><span></span><span></span><span></span><span></span></div>
            <div class="lp-main">
              <div class="lp-kpis"><div><small>Today</small><b>&pound;18,420</b></div><div><small>Approval</small><b>97.8%</b></div><div><small>Channels</small><b>6</b></div></div>
              <div class="lp-chart">{"".join(f'<span style="height:{h}%"></span>' for h in [38,52,44,63,58,72,66,81,74,90,84,95])}</div>
              <div class="lp-rows"><span></span><span></span><span></span></div>
            </div>
          </div>
        </div>
        <div class="lp-base"></div>
      </div>
      <div class="phone">
        <div class="ph-notch"></div>
        <div class="ph-screen">
          <small>Checkout</small>
          <b>&pound;64.00</b>
          <div class="ph-btn apple">Apple Pay</div>
          <div class="ph-btn gpay">Google Pay</div>
          <div class="ph-line"></div><div class="ph-line short"></div>
          <div class="ph-btn card">Pay by card</div>
        </div>
      </div>
      <div class="mini-terminal">
        <div class="mt-screen"><small>Approved</small><b>&pound;24.60</b><span class="mt-ok">{CHECK}</span></div>
        <div class="mt-keys"><i></i><i></i><i></i><i></i><i></i><i></i><i class="r"></i><i class="y"></i><i class="g"></i></div>
      </div>
      {chip("Apple Pay", "f1")}{chip("Pay by bank", "f2")}{chip("&euro; $ &pound; &yen;", "f3")}{chip("Crypto", "f4")}{chip("PayPal", "f5")}{chip("Contactless", "f6")}
    </div>
  </div>
</section>'''

marquee_items = "".join(chip(m) for m in METHODS)
marquee = f'''<section class="marquee-wrap" aria-label="Payment methods we can enable">
  <div class="marquee"><div class="marquee-track">{marquee_items}{marquee_items}</div></div>
</section>'''


def tile(href, cls, ic, title, sub, art):
    return f'''<a class="vtile {cls} reveal" href="{href}">
  <div class="vt-art" aria-hidden="true">{art}</div>
  <div class="vt-label"><span class="vt-ic">{icon(ic, None)}</span><span><b>{title}</b><small>{sub}</small></span><span class="vt-go">&rarr;</span></div>
</a>'''


def bars(n=7):
    import random
    random.seed(n)
    return '<div class="art-bars">' + "".join(f'<span style="height:{random.randint(30, 95)}%"></span>' for _ in range(n)) + "</div>"


tiles = "".join([
    tile("/card-machines/", "t-green big", "terminal", "In store", "Card machines &amp; ePOS",
         '<div class="art-terminal"><div class="s"><b>&pound;8.40</b><small>Tap to pay</small></div><div class="k"><i></i><i></i><i></i><i></i><i></i><i></i></div></div>'
         '<div class="art-wave">' + icon("contactless", None) + '</div>'),
    tile("/online-payments/", "t-blue", "globe", "Online", "Checkout &amp; gateway",
         '<div class="art-browser"><div class="bb"><i></i><i></i><i></i></div><div class="bf"><span></span><span></span><span class="cta">Pay &pound;64</span></div></div>'),
    tile("/online-payments/#payment-links", "t-violet", "link", "Payment links", "Text, email, WhatsApp",
         '<div class="art-bubble"><span>Here&rsquo;s your link to pay &pound;120</span><b>pay.link/x7Q2</b></div>'),
    tile("/solutions/payment-methods/", "t-amber", "wallet", "Wallets &amp; more", "Apple Pay, PayPal, pay later",
         '<div class="art-chips">' + chip("Apple Pay") + chip("Google Pay") + chip("PayPal") + chip("Pay later") + chip("Pay by bank") + '</div>'),
    tile("/solutions/multi-currency/", "t-teal", "coins", "Multi-currency", "Sell globally, settle locally",
         '<div class="art-fx"><span>&pound;</span><span>&euro;</span><span>$</span><span>&yen;</span></div>'),
    tile("/solutions/card-payouts/", "t-rose big", "receipt", "Payouts", "Straight to cards",
         '<div class="art-payout"><div class="pc"><small>Payout sent</small><b>&pound;250.00</b><i>' + CHECK + '</i></div></div>'),
    tile("/solutions/orchestration/", "t-ink big", "refresh", "Orchestration", "Smart routing, many providers",
         '<div class="art-route"><span class="src">Payment</span><svg viewBox="0 0 200 120" preserveAspectRatio="none"><path d="M10 60 C80 60 90 15 190 15"/><path d="M10 60 C80 60 90 60 190 60"/><path d="M10 60 C80 60 90 105 190 105"/></svg>'
         '<span class="dst d1">Acquirer A</span><span class="dst d2 on">Acquirer B &#10003;</span><span class="dst d3">Acquirer C</span></div>'),
    tile("/crypto/", "t-gold big", "sparkle", "Crypto", "Crypto &amp; stablecoin",
         '<div class="art-coin"><span>&#8383;</span><span class="c2">&#926;</span><span class="c3">$</span></div>'),
])

all_in_one = f'''<section class="section-white">
  <div class="container">
    <div class="section-head center">
      <span class="eyebrow">All in one place</span>
      <h2>Everything you need to get paid.</h2>
    </div>
    <div class="vgrid">{tiles}</div>
    <div class="center mt-m"><a class="btn btn-ghost" href="/solutions/">See all solutions {ARROW}</a></div>
  </div>
</section>'''

one_view = f'''<section class="section-dark">
  <div class="container split v-center">
    <div>
      <span class="eyebrow">One view</span>
      <h2>Every channel. One picture.</h2>
      <ul class="big-ticks">
        <li>{TICK} In-store, online and phone sales together</li>
        <li>{TICK} Settlement in the currencies you need</li>
        <li>{TICK} Routing and fraud tools that protect approvals</li>
      </ul>
      <a class="btn btn-light mt-m" href="/how-it-works/">How it works {ARROW}</a>
    </div>
    <div class="dash reveal" aria-hidden="true">
      <div class="dash-head"><b>Overview</b><span>This month</span></div>
      <div class="dash-kpis">
        <div><small>Volume</small><b>&pound;412k</b><em>+18%</em></div>
        <div><small>Transactions</small><b>9,284</b><em>+11%</em></div>
        <div><small>Approval</small><b>97.6%</b><em>+1.4%</em></div>
      </div>
      <div class="dash-body">
        <div class="donut"><svg viewBox="0 0 42 42"><circle r="15.9" cx="21" cy="21" fill="none" stroke="rgba(255,255,255,.08)" stroke-width="6"/>
          <circle r="15.9" cx="21" cy="21" fill="none" stroke="#1fc39a" stroke-width="6" stroke-dasharray="46 54" stroke-dashoffset="25"/>
          <circle r="15.9" cx="21" cy="21" fill="none" stroke="#5aa9ff" stroke-width="6" stroke-dasharray="30 70" stroke-dashoffset="-21"/>
          <circle r="15.9" cx="21" cy="21" fill="none" stroke="#f5b84a" stroke-width="6" stroke-dasharray="16 84" stroke-dashoffset="-51"/>
          <circle r="15.9" cx="21" cy="21" fill="none" stroke="#c48bff" stroke-width="6" stroke-dasharray="8 92" stroke-dashoffset="-67"/></svg>
          <ul><li><i style="background:#1fc39a"></i>In store</li><li><i style="background:#5aa9ff"></i>Online</li><li><i style="background:#f5b84a"></i>Links &amp; phone</li><li><i style="background:#c48bff"></i>Wallets</li></ul>
        </div>
        {bars(12)}
      </div>
    </div>
  </div>
</section>'''


def itile(anchor, img, title, ic, cls):
    return (f'<a class="itile {cls} reveal" href="{anchor}" style="--img:url(/assets/img/industries/{img}.jpg)">'
            f'<span class="it-bg" aria-hidden="true">{icon(ic, None)}</span>'
            f'<span class="it-ic">{icon(ic, None)}</span><b>{title}</b></a>')


industries = f'''<section>
  <div class="container">
    <div class="section-head center">
      <span class="eyebrow">Who we work with</span>
      <h2>Built for every kind of business.</h2>
    </div>
    <div class="igrid">
      {itile("/industries/#retail", "retail", "Retail", "store", "c1 wide")}
      {itile("/industries/#hospitality", "hospitality", "Restaurants &amp; bars", "cup", "c2")}
      {itile("/industries/#hotels", "hotels", "Hotels", "users", "c3")}
      {itile("/industries/#ecommerce", "ecommerce", "Ecommerce", "cart", "c4")}
      {itile("/industries/igaming/", "igaming", "iGaming", "ticket", "c5")}
      {itile("/industries/forex/", "forex", "Forex &amp; trading", "chart", "c6 wide")}
      {itile("/industries/#trades", "trades", "Trades", "tool", "c7")}
      {itile("/industries/#automotive", "automotive", "Automotive", "car", "c8")}
      {itile("/industries/#professional", "professional", "Professional services", "briefcase", "c9")}
      {itile("/industries/", "all", "All industries &rarr;", "globe", "c10")}
    </div>
  </div>
</section>'''

steps = f'''<section class="section-white section-tight">
  <div class="container">
    <div class="isteps">
      <div class="istep reveal">{icon("search")}<b>Tell us how you sell</b></div>
      <span class="iarrow" aria-hidden="true">&rarr;</span>
      <div class="istep reveal">{icon("scale")}<b>We compare the market</b></div>
      <span class="iarrow" aria-hidden="true">&rarr;</span>
      <div class="istep reveal">{icon("check")}<b>We set it all up</b></div>
      <span class="iarrow" aria-hidden="true">&rarr;</span>
      <div class="istep reveal">{icon("refresh")}<b>We stay on it</b></div>
    </div>
  </div>
</section>'''

switch = f'''<section class="section-tight">
  <div class="container">
    <a class="switch-band reveal" href="/switch/">
      <div class="sb-art" aria-hidden="true">
        <div class="stmt"><div class="l"><span></span><em>Interchange</em></div><div class="l"><span></span><em>Scheme fees</em></div><div class="l warn"><span></span><em>Hidden margin</em></div><div class="l warn"><span></span><em>PCI fee</em></div></div>
      </div>
      <div><span class="eyebrow">Already taking payments?</span><h2>Free statement review.</h2><p>See what you really pay &mdash; line by line.</p></div>
      <span class="btn btn-primary">Get your statement read {ARROW}</span>
    </a>
  </div>
</section>'''

schema = '''<script type="application/ld+json">{"@context":"https://schema.org","@type":"Organization","name":"DPayments","url":"https://dpayments.co.uk","email":"info@dpayments.co.uk","logo":"https://dpayments.co.uk/assets/img/logo.svg","description":"Independent UK payments partner: every payment method, all in one place.","areaServed":["GB","EU"]}</script>'''

BODY = hero + marquee + all_in_one + one_view + industries + steps + switch + cta_band(
    title="Every way to get paid. One conversation.",
    text="Tell us how you sell today and where you want to go. We&rsquo;ll put the right payment mix together.")


def build():
    return page("/", TITLE, DESC, BODY, current=None, schema=schema)
