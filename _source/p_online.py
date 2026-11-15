from common import *

TITLE = "Online Payments, Payment Links & Virtual Terminal | DPayments"
DESC = ("Hosted checkout, payment links, virtual terminal (MOTO), recurring billing and digital wallets for UK businesses. "
        "Set up properly with 3D Secure 2, chargeback guidance and clear settlement terms.")

hero = f'''<section class="page-hero">
  <div class="container">
    <div class="crumbs"><a href="/">Home</a> / Online payments</div>
    <span class="eyebrow">Online, by link &amp; by phone</span>
    <h1 style="max-width:860px">Take payments online, by link, or over the phone.</h1>
    <p class="lede">Sell through a checkout, send a payment link, bill on a schedule or take card details by phone. We set up the right mix for your business and explain the parts that matter &mdash; 3D Secure, chargebacks and settlement &mdash; in plain English.</p>
    <div class="btn-row">
      <a class="btn btn-primary" href="/contact/?channel=online">Get a quote {ARROW}</a>
      <a class="btn btn-ghost" href="#ways">See the options</a>
    </div>
  </div>
</section>'''

ways = [
    ("cart", "hosted-checkout", "Hosted checkout",
     "A secure payment page hosted by the provider and connected to your website. Card data never reaches your servers, which keeps your PCI obligations to a minimum.",
     ["Branded with your logo and colours", "Cards, Apple Pay and Google Pay", "Works on mobile and desktop", "3D Secure 2 built in"],
     "Online shops, booking sites and any business selling through its own website."),
    ("link", "payment-links", "Payment links",
     "A one-off secure payment page you send by text, email or messaging app. No website needed &mdash; the customer taps the link and pays.",
     ["Create a link in seconds", "Set an amount, reference and expiry", "See when it&rsquo;s been paid", "Great for follow-ups after a call"],
     "Invoices, deposits, bookings, quotes and social-media sales."),
    ("phone", "virtual-terminal", "Virtual terminal (MOTO)",
     "A secure web page where you or your team key in card details given over the phone or by post. For businesses that sell through conversation.",
     ["Runs in any browser &mdash; no hardware", "Multiple staff logins", "Refunds and receipts from the same screen", "Option to send a link instead"],
     "Trades, travel, professional services and anyone taking telephone orders."),
    ("repeat", "recurring", "Recurring &amp; subscriptions",
     "Securely stored card details billed on a schedule you set, with authentication and automatic retries on failed payments handled for you.",
     ["Weekly, monthly or custom schedules", "Fixed or variable amounts", "Card updater to reduce failed payments", "Customer notifications"],
     "Memberships, gyms, retainers, subscription boxes and instalment plans."),
    ("plug", "integrations", "Platform integrations",
     "Ready-made plugins and connections for the major ecommerce, booking and invoicing platforms, plus developer APIs for custom builds.",
     ["Popular shop and website builders", "Invoicing and accounting tools", "Booking and scheduling software", "API and developer docs for custom sites"],
     "Businesses already using a platform who want payments to just work."),
    ("chart", "reconciliation", "One reconciliation",
     "In-person and online takings reported together, so you see the whole picture and month-end is simpler.",
     ["One dashboard for every channel", "Exports for your accountant", "Settlement reports by day", "Fewer spreadsheets"],
     "Any business taking payments in more than one way."),
]
ways_html = "".join(f'''<div class="card reveal" id="{a}">{icon(i)}<h3>{t}</h3><p>{d}</p>{ticks(f)}<p class="mt-m"><strong>Good for:</strong> {g}</p></div>''' for i, a, t, d, f, g in ways)

extras = f'''<section>
  <div class="container">
    <div class="section-head">
      <span class="eyebrow">Beyond the basics</span>
      <h2>Extras worth asking about.</h2>
      <p class="lede">Not every business needs these, but the ones that do usually wish they&rsquo;d set them up sooner. Availability depends on the provider we recommend.</p>
    </div>
    <div class="grid g4">
      <div class="card reveal">{icon("wallet")}<h4>Apple Pay &amp; Google Pay</h4><p>One-tap checkout on mobile, which usually means fewer abandoned baskets.</p></div>
      <div class="card reveal">{icon("bank")}<h4>Pay by bank</h4><p>Open-banking payments straight from the customer&rsquo;s bank app &mdash; useful for larger amounts.</p></div>
      <div class="card reveal">{icon("globe")}<h4>Multi-currency</h4><p>Show prices and accept payments in other currencies when you sell abroad.</p></div>
      <div class="card reveal">{icon("shield")}<h4>Fraud screening</h4><p>Rules and risk scoring that stop suspicious orders before they become chargebacks.</p></div>
      <div class="card reveal">{icon("lock")}<h4>Tokenisation</h4><p>Saved cards stored securely by the provider, so returning customers pay faster.</p></div>
      <div class="card reveal">{icon("card")}<h4>Pre-authorisation</h4><p>Hold an amount now and capture it later &mdash; for hire, hotels and deposits.</p></div>
      <div class="card reveal">{icon("receipt")}<h4>Invoicing</h4><p>Send invoices with a pay-now button and see when they&rsquo;re settled.</p></div>
      <div class="card reveal">{icon("users")}<h4>Team permissions</h4><p>Control which staff can take payments, issue refunds or see reports.</p></div>
    </div>
  </div>
</section>'''

understand = f'''<section class="section-dark">
  <div class="container">
    <div class="section-head">
      <span class="eyebrow">The parts worth understanding</span>
      <h2>Three things every online seller should know.</h2>
    </div>
    <div class="grid g3">
      <div class="card reveal">{icon("shield")}<h3>3D Secure 2</h3><p>The authentication step for online card payments, where a customer may confirm through their banking app. It&rsquo;s required for most UK and EU online payments under Strong Customer Authentication rules, and it shifts fraud liability on authenticated transactions to the card issuer. A good setup only challenges risky payments, so most customers sail through.</p></div>
      <div class="card reveal">{icon("alert")}<h3>Chargebacks</h3><p>When a cardholder disputes a payment, the amount is reversed while it&rsquo;s investigated. Receipts, proof of delivery and your communications help you win. Clear refund policies, accurate descriptions and fraud checks help prevent disputes in the first place &mdash; and that&rsquo;s always cheaper.</p></div>
      <div class="card reveal">{icon("clock")}<h3>Settlement timing</h3><p>Authorisation takes about a second, but settlement usually takes one to three business days after the sale, depending on the acquirer, the card scheme and your terms. New accounts may start on slower settlement or a reserve while a trading history builds up.</p></div>
    </div>
  </div>
</section>'''

ready = f'''<section class="section-white">
  <div class="container split">
    <div class="sticky">
      <span class="eyebrow">Getting approved</span>
      <h2>What providers look for on your website.</h2>
      <p class="lede">Underwriters review your site before approving online payments. Having these in place up front avoids delays &mdash; we&rsquo;ll check them with you before applying.</p>
    </div>
    <ol class="numbered">
      <li class="reveal"><div><h4>Clear products and prices</h4><p>What you sell, what it costs and in which currency.</p></div></li>
      <li class="reveal"><div><h4>Terms &amp; conditions</h4><p>Including how and when orders are fulfilled.</p></div></li>
      <li class="reveal"><div><h4>Refund and returns policy</h4><p>Easy to find, and consistent with consumer law.</p></div></li>
      <li class="reveal"><div><h4>Privacy policy</h4><p>How you handle customer data under UK GDPR.</p></div></li>
      <li class="reveal"><div><h4>Contact details</h4><p>A business address, email and ideally a phone number.</p></div></li>
      <li class="reveal"><div><h4>Secure site (HTTPS)</h4><p>A valid SSL certificate on every page, especially checkout.</p></div></li>
    </ol>
  </div>
</section>'''

BODY = hero + f'''<section class="section-white" id="ways">
  <div class="container">
    <div class="section-head">
      <span class="eyebrow">Ways to accept online</span>
      <h2>Pick one, or combine them.</h2>
      <p class="lede">Most businesses use two or three of these together. We&rsquo;ll recommend the mix that fits how your customers actually buy.</p>
    </div>
    <div class="grid g3">{ways_html}</div>
  </div>
</section>''' + extras + understand + ready + cta_band(
    title="Let&rsquo;s get you taking online payments, cleanly.",
    text="Tell us how you want to sell. We&rsquo;ll reply by email with a setup and quote covering checkout, links, recurring billing &mdash; or all three.")


def build():
    return page("/online-payments/", TITLE, DESC, BODY, current="/online-payments/")
