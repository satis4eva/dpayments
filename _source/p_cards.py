from common import *

TITLE = "Card Machines for UK Businesses | Countertop, Portable & 4G Terminals | DPayments"
DESC = ("Countertop, portable, 4G mobile, unattended, EPOS-integrated and pay-at-table card machines. "
        "We help you choose, set up and get fair contract terms. Get a quote from DPayments.")

hero = f'''<section class="page-hero with-art">
  <div class="container hero-grid">
    <div>
      <div class="crumbs"><a href="/">Home</a> / Card machines</div>
      <span class="eyebrow">In-person payments</span>
      <h1>Card machines that fit how you trade &mdash; not the other way round.</h1>
      <p class="lede">The right hardware depends on where and how you sell. We help you pick the right category, compare providers and terms, and get your terminals configured and ready to take payments from day one.</p>
      <div class="btn-row">
        <a class="btn btn-primary" href="/contact/?channel=in-person">Get a quote {ARROW}</a>
        <a class="btn btn-ghost" href="#types">Compare terminal types</a>
      </div>
    </div>
    <div class="hero-visual" aria-hidden="true">
      <div class="terminal">
        <div class="terminal-screen">
          <div class="merchant">Present card</div>
          <div class="amount">&pound;8.40</div>
          <div class="status">{icon("contactless", None)} Tap, insert or swipe</div>
        </div>
        <div class="keypad"><span></span><span></span><span></span><span></span><span></span><span></span><span class="k-red"></span><span class="k-amber"></span><span class="k-green"></span></div>
      </div>
    </div>
  </div>
</section>'''

types = [
    ("terminal", "Countertop", "Wired to power and network at a fixed till.", "Shops, reception desks, takeaways, salons with a front desk.",
     ["Most reliable connection (ethernet or broadband)", "Prints receipts on the spot", "Lowest-maintenance option"]),
    ("wifi", "Portable", "Wireless over Wi-Fi or Bluetooth, anywhere within your premises.", "Restaurants, pubs, cafés and larger retail floors.",
     ["Take the terminal to the customer", "Pairs with a base station or your Wi-Fi", "Good battery for a full service"]),
    ("signal", "Mobile &amp; 4G", "Built-in SIM with mobile data, so it works wherever there&rsquo;s signal.", "Market traders, deliveries, events, taxis and on-site trades.",
     ["No Wi-Fi or phone line needed", "Wi-Fi fallback on many models", "Offline mode for patchy signal"]),
    ("lock", "Unattended", "Ruggedised, tamper-resistant readers built into machines and kiosks.", "Vending, parking, EV charging, laundrettes and self-service.",
     ["Contactless-only or full Chip &amp; PIN", "Built to run 24/7", "Remote monitoring and reporting"]),
    ("plug", "EPOS-integrated", "Connected to your till so the amount is sent to the terminal automatically.", "Busy retail and hospitality with an existing EPOS system.",
     ["No double-keying or mistyped amounts", "Sales and payments reconcile together", "Faster checkout at peak times"]),
    ("users", "Pay-at-table &amp; tipping", "Split bills, add gratuities and take payment at the table.", "Restaurants, bars, hotels and hospitality groups.",
     ["Split by item or equal shares", "Preset or custom tip amounts", "Tip reporting for staff payouts"]),
]
type_cards = "".join(f'''<div class="card reveal">{icon(i)}<h3>{t}</h3><p>{d}</p><p><strong>Best for:</strong> {b}</p>{ticks(f)}</div>''' for i, t, d, b, f in types)

table = '''<div class="table-wrap reveal"><table>
<thead><tr><th>Type</th><th>Connection</th><th>Moves around?</th><th>Typical use</th></tr></thead>
<tbody>
<tr><td>Countertop</td><td>Ethernet / broadband</td><td>No &mdash; stays at the till</td><td>Fixed counter, reception desk</td></tr>
<tr><td>Portable</td><td>Wi-Fi or Bluetooth</td><td>Within your premises</td><td>Table service, shop floor</td></tr>
<tr><td>Mobile &amp; 4G</td><td>SIM / mobile data (+ Wi-Fi)</td><td>Anywhere with signal</td><td>Markets, deliveries, call-outs</td></tr>
<tr><td>Unattended</td><td>Ethernet, Wi-Fi or 4G</td><td>No &mdash; built in</td><td>Vending, parking, kiosks</td></tr>
<tr><td>EPOS-integrated</td><td>Linked to your till</td><td>Depends on model</td><td>Higher-volume retail &amp; hospitality</td></tr>
<tr><td>Pay-at-table</td><td>Wi-Fi</td><td>Within your premises</td><td>Restaurants and bars</td></tr>
</tbody></table></div>'''

accepts = f'''<section class="section-white section-tight">
  <div class="container">
    <div class="split v-center">
      <div>
        <span class="eyebrow">What a modern terminal handles</span>
        <h2>Every way customers want to pay in person.</h2>
        <p class="lede">Whatever terminal you choose, it should take every common payment method and make the end of the day easy.</p>
      </div>
      <div class="grid g2">
        <div>{ticks(["Contactless cards", "Chip &amp; PIN", "Apple Pay &amp; Google Pay", "Visa, Mastercard &amp; Maestro"])}</div>
        <div>{ticks(["American Express (where enabled)", "Printed, email or SMS receipts", "Refunds, voids &amp; pre-authorisations", "End-of-day reports"])}</div>
      </div>
    </div>
  </div>
</section>'''

checklist = [
    ("Connectivity", "Fixed line, Wi-Fi, Bluetooth or 4G &mdash; chosen on where you trade and how reliable the signal is there."),
    ("Battery &amp; durability", "Matters if the terminal leaves the counter, especially through a long or busy day."),
    ("Tipping &amp; gratuities", "How tips are added, split between staff and shown in reporting."),
    ("Refunds &amp; voids", "How easily staff can process them, and whether a supervisor PIN is needed."),
    ("Offline mode", "Storing transactions when the network drops, then sending them when it&rsquo;s back."),
    ("Integration", "Standalone is simpler; integrated suits larger or higher-volume operations."),
]
check_html = "".join(f'<li class="reveal"><div><h4>{h}</h4><p>{p}</p></div></li>' for h, p in checklist)

rent = f'''<section>
  <div class="container">
    <div class="section-head">
      <span class="eyebrow">Rent, buy or bundle?</span>
      <h2>How you pay for the hardware matters too.</h2>
      <p class="lede">Terminal costs are often where a &ldquo;cheap&rdquo; deal becomes expensive. We lay out the options side by side so you can choose with the full picture.</p>
    </div>
    <div class="grid g3">
      <div class="card reveal"><span class="tag">Rent</span><h3>Monthly rental</h3><p>A fixed monthly fee per terminal, usually including support and replacements.</p>{ticks(["Low upfront cost", "Swaps if a device fails"])}<p class="mt-m"><strong>Watch for:</strong> rental terms that run longer than your processing contract and are hard to exit.</p></div>
      <div class="card reveal"><span class="tag">Buy</span><h3>Outright purchase</h3><p>Pay once for the device and own it.</p>{ticks(["No ongoing hardware fee", "Often easier to switch provider later"])}<p class="mt-m"><strong>Watch for:</strong> devices that are locked to one provider and can&rsquo;t move with you.</p></div>
      <div class="card reveal"><span class="tag">Bundle</span><h3>Included in pricing</h3><p>Hardware folded into your transaction pricing or a monthly plan.</p>{ticks(["Simple single bill", "Can suit lower volumes"])}<p class="mt-m"><strong>Watch for:</strong> minimum monthly charges and higher rates that cover the hardware.</p></div>
    </div>
  </div>
</section>'''

included = f'''<section class="section-white">
  <div class="container split">
    <div class="sticky">
      <span class="eyebrow">What&rsquo;s included</span>
      <h2>From first question to first sale.</h2>
      <p class="lede">We handle the parts that usually slow businesses down, so going live is the easy part.</p>
    </div>
    <div class="steps">
      <div class="step reveal"><div class="n"></div><div><h3>Recommend the right setup</h3><p>We match terminal type, number of devices and connectivity to your premises, staff and trading pattern.</p></div></div>
      <div class="step reveal"><div class="n"></div><div><h3>Compare providers and terms</h3><p>Rates, hardware costs, contract length, rental, minimum charges and exit fees &mdash; all set out side by side.</p></div></div>
      <div class="step reveal"><div class="n"></div><div><h3>Handle the application</h3><p>We help with the application and KYC documents so underwriting isn&rsquo;t held up by missing paperwork.</p></div></div>
      <div class="step reveal"><div class="n"></div><div><h3>Configure and deliver</h3><p>Terminals set up with your business name on receipts, tipping and refund settings, and any EPOS link.</p></div></div>
      <div class="step reveal"><div class="n"></div><div><h3>Support after go-live</h3><p>Help with PCI, statements and changes as you grow &mdash; extra terminals, new sites or new channels.</p></div></div>
    </div>
  </div>
</section>'''

BODY = hero + f'''<section class="section-white" id="types">
  <div class="container">
    <div class="section-head">
      <span class="eyebrow">Terminal categories</span>
      <h2>Six types of card machine, and who each one suits.</h2>
      <p class="lede">We start with categories rather than models. Once we know which fits, we compare the specific devices and providers available to you.</p>
    </div>
    <div class="grid g3">{type_cards}</div>
  </div>
</section>
<section class="section-tight">
  <div class="container">
    <div class="section-head"><h2>At a glance</h2></div>
    {table}
  </div>
</section>''' + accepts + f'''<section>
  <div class="container split">
    <div class="sticky">
      <span class="eyebrow">Before you buy</span>
      <h2>Six things to settle first.</h2>
      <p class="lede">Get these right and the terminal will suit you for years. Get them wrong and you&rsquo;ll be fighting it every busy Saturday.</p>
    </div>
    <ol class="numbered">{check_html}</ol>
  </div>
</section>''' + included + rent + cta_band(
    title="Tell us how and where you take payments.",
    text="We&rsquo;ll email you a suitable setup and a quote &mdash; with the contract terms spelled out, not just the rate.")


def build():
    return page("/card-machines/", TITLE, DESC, BODY, current="/card-machines/")
