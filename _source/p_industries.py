from common import *

TITLE = "Payment Solutions by Industry | Retail, Hospitality, Trades & More | DPayments"
DESC = ("Card machines and online payments set up for how your sector trades: retail, hospitality, trades, ecommerce, "
        "professional services, health and beauty, events, memberships and travel.")

inds = [
    ("retail", "store", "Retail &amp; shops",
     "Fast queues, clean reconciliation and a setup that copes with Saturdays.",
     ["Countertop or EPOS-integrated terminals", "Portable devices for queue-busting on busy days", "Payment links for click-and-collect or phone orders", "Online checkout if you sell through a web shop"],
     "Transaction volume and average basket size &mdash; interchange-plus pricing often suits shops with lots of small debit card sales."),
    ("hospitality", "cup", "Caf&eacute;s, restaurants &amp; bars",
     "Take payment at the table, handle tips fairly and turn tables faster.",
     ["Portable pay-at-table terminals", "Bill splitting and tipping with staff reporting", "EPOS integration so orders and payments match", "Deposits and pre-orders by payment link"],
     "Tip handling, Wi-Fi coverage across the floor and peak-time reliability."),
    ("trades", "tool", "Trades, builders &amp; merchants",
     "Get paid on the doorstep or over the trade counter, not 30 days later.",
     ["4G mobile terminals that work on site", "Payment links sent straight after a job", "Virtual terminal for phone payments and deposits", "Pre-authorisation for larger jobs"],
     "Signal on site, offline mode, larger trade-counter transactions, and avoiding long rental terms."),
    ("hotels", "users", "Hotels &amp; accommodation",
     "Guest payments from booking to check-out.",
     ["Pre-authorisations at check-in", "Deposits and balances by payment link", "Restaurant and bar charges via ePOS", "Online booking checkout and multi-currency for overseas guests"],
     "Pre-auth handling, no-show policies, future-dated bookings and DCC for international guests."),
    ("automotive", "car", "Automotive",
     "Garages, MOT centres, servicing and dealerships.",
     ["Countertop terminals at reception", "Payment links when the car is ready", "Higher-value transactions and deposits", "Integration with garage management software"],
     "Larger ticket sizes, deposits on parts and vehicles, and commercial card fees from fleet customers."),
    ("garden-centres", "heart", "Garden centres &amp; large retail",
     "Busy weekends, big catalogues and caf&eacute; counters.",
     ["Multiple tills with ePOS integration", "Portable terminals for outdoor areas", "Separate caf&eacute; and retail reporting", "Loyalty schemes for regulars"],
     "Seasonal peaks, Wi-Fi coverage outdoors, and running retail and hospitality side by side."),
    ("competitions", "sparkle", "Online competitions &amp; prize draws",
     "Payments for competition and prize draw sites.",
     ["Hosted checkout with 3D Secure 2", "Apple Pay and Google Pay for quick entries", "Fraud screening and spend controls", "Card payouts for cash prizes"],
     "Your legal structure (free entry route or licence), chargeback rates and partner appetite for the sector."),
    ("ecommerce", "cart", "Ecommerce",
     "A checkout that converts, with fraud and chargebacks kept in check.",
     ["Hosted checkout or platform plugins", "Apple Pay and Google Pay for mobile shoppers", "3D Secure 2 and fraud screening", "Multi-currency for international sales"],
     "Underwriting requirements for your site, chargeback rates, reserves and settlement speed."),
    ("professional", "briefcase", "Law firms &amp; professional services",
     "Solicitors, accountants, consultants, agencies and other client-based firms.",
     ["Invoice payment links and pay-now buttons", "Recurring billing for retainers", "Virtual terminal for client calls", "Integration with invoicing and accounting tools"],
     "Higher-value transactions, commercial card fees, client vs office account routing for law firms, and getting paid on time."),
    ("health-beauty", "heart", "Health, beauty &amp; wellness",
     "Salons, barbers, clinics, therapists and studios.",
     ["Countertop or portable terminals at reception", "Deposits to reduce no-shows", "Payments linked to booking software", "Packages and courses billed in instalments"],
     "No-show protection, booking integration and keeping costs low on smaller tickets."),
    ("events", "ticket", "Events &amp; markets",
     "Street food, pop-ups, festivals, fairs and market stalls.",
     ["4G mobile terminals with long battery life", "Offline mode for crowded networks", "Multiple devices on one account", "Short-term or seasonal options"],
     "Connectivity in busy venues, battery life and avoiding monthly minimums in quiet months."),
    ("memberships", "users", "Gyms, clubs &amp; memberships",
     "Sports clubs, gyms, schools, societies and subscription businesses.",
     ["Recurring card payments on a schedule", "Card updater to reduce failed payments", "Online sign-up with payment", "In-person terminals for classes, kit and bar sales"],
     "Failed payment recovery, churn and simple reporting for committees or managers."),
    ("travel", "car", "Travel &amp; transport",
     "Taxis, private hire, tour operators, coach hire and hospitality stays.",
     ["Mobile terminals for in-vehicle payment", "Deposits and balances by payment link", "Pre-authorisation for hire and damage holds", "Online booking checkout"],
     "Future-dated bookings can mean extra underwriting checks or reserves &mdash; we&rsquo;ll explain what to expect up front."),
]

cards = "".join(f'''<div class="card card-lg reveal" id="{a}" style="scroll-margin-top:100px">
  <div style="display:flex;gap:16px;align-items:flex-start">{icon(i)}<div><h3 style="margin-top:4px">{t}</h3><p>{s}</p></div></div>
  <h4 class="mt-m">Typical setup</h4>
  {ticks(items)}
  <div class="callout mt-m"><p><strong>What we look at closely:</strong> {w}</p></div>
</div>''' for a, i, t, s, items, w in inds)

jump = "".join(f'<a class="pill" href="#{a}">{icon(i, None)} {t}</a>' for a, i, t, *_ in inds)

BODY = f'''<section class="page-hero">
  <div class="container">
    <div class="crumbs"><a href="/">Home</a> / Industries</div>
    <span class="eyebrow">Who we help</span>
    <h1 style="max-width:900px">Payments set up for the way your sector trades.</h1>
    <p class="lede">A caf&eacute;, a plumber and an online shop all take cards &mdash; but they need very different setups. Here&rsquo;s how we typically approach each, and what we pay close attention to.</p>
    <div class="strip mt-m">{jump}</div>
  </div>
</section>
<section class="section-white">
  <div class="container">
    <div class="grid g2">{cards}</div>
  </div>
</section>
<section>
  <div class="container">
    <div class="section-head"><span class="eyebrow">Specialist sectors</span><h2>Sectors that need specialist partners.</h2>
      <p class="lede">Some industries need acquirers with specific appetite and experience. We work with licensed and regulated businesses in these sectors.</p></div>
    <div class="grid g3">
      <a class="card reveal" href="/industries/igaming/">{icon("ticket")}<h3>iGaming</h3><p>Casino, sportsbook, lottery and competition operators: deposits, fast payouts and multi-acquirer resilience.</p><span class="more">iGaming {ARROW}</span></a>
      <a class="card reveal" href="/industries/forex/">{icon("chart")}<h3>Forex &amp; CFD</h3><p>Client deposits and withdrawals for regulated brokers, with card payouts and multi-currency settlement.</p><span class="more">Forex &amp; CFD {ARROW}</span></a>
      <a class="card reveal" href="/industries/financial-brokerage/">{icon("briefcase")}<h3>Financial brokerage</h3><p>Investment and wealth platforms: open banking, cards, payouts and compliance-ready partners.</p><span class="more">Financial brokerage {ARROW}</span></a>
    </div>
  </div>
</section>
<section class="section-tight">
  <div class="container narrow" style="max-width:820px;text-align:center">
    <h2>Don&rsquo;t see your industry?</h2>
    <p class="lede" style="margin:0 auto 24px">We work with most UK businesses that take card payments. Tell us what you do and how you sell, and we&rsquo;ll tell you honestly what we can arrange.</p>
    <a class="btn btn-primary" href="/contact/">Ask us {ARROW}</a>
  </div>
</section>''' + cta_band()


def build():
    return page("/industries/", TITLE, DESC, BODY, current="/industries/")
