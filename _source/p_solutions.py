from common import *
from template import build_page
from menu import MENU_SOLUTIONS

SOL = [("/solutions/", "Solutions")]

R_GATEWAY = ("/online-payments/", "globe", "Online payment gateway", "Hosted checkout, payment links, MOTO and recurring billing.")
R_POS = ("/card-machines/", "terminal", "POS &amp; card machines", "Countertop, portable, 4G and integrated terminals.")
R_MULTI = ("/solutions/multi-currency/", "coins", "Multi-currency acceptance", "Show prices and take payments in your customers&rsquo; currencies.")
R_WALLET = ("/solutions/digital-wallets/", "wallet", "Digital wallets &amp; Click to Pay", "Apple Pay, Google Pay and one-click card checkout.")
R_SETTLE = ("/solutions/settlements/", "bank", "Settlements", "Get paid in the currencies you need, including stablecoin via partners.")
R_PAYOUT = ("/solutions/card-payouts/", "card", "Card payouts", "Send withdrawals, refunds and winnings back to cards.")
R_ORCH = ("/solutions/orchestration/", "refresh", "Payment orchestration", "Route each payment to the provider most likely to approve it.")
R_RISK = ("/solutions/risk-fraud/", "shield", "Risk &amp; fraud management", "Screening, 3DS2, network tokens and chargeback control.")
R_INT = ("/solutions/integration/", "plug", "Integration", "Plugins, hosted pages, SDKs and APIs.")


# ---------------- Overview ----------------
def overview():
    groups = ""
    for title, items in MENU_SOLUTIONS:
        cards = "".join(
            f'<a class="card reveal" href="{h}">{icon(i)}<h3>{t}</h3><p>{d}</p><span class="more">Learn more {ARROW}</span></a>'
            for h, i, t, d in items if h != "/solutions/")
        groups += f'''<div class="mt-l"><h2 style="font-size:1.5rem;margin-bottom:20px">{title}</h2><div class="grid g3">{cards}</div></div>'''
    groups += f'''<div class="mt-l"><h2 style="font-size:1.5rem;margin-bottom:20px">Crypto</h2><div class="grid g3">
      <a class="card reveal" href="https://crypto.dpayments.co.uk">{icon("sparkle")}<h3>Crypto payments</h3><p>Accept crypto from your customers through our crypto gateway partners.</p><span class="more">Visit crypto.dpayments.co.uk &#8599;</span></a></div></div>'''
    body = f'''<section class="page-hero">
  <div class="container">
    <div class="crumbs"><a href="/">Home</a> / Solutions</div>
    <span class="eyebrow">Solutions</span>
    <h1 style="max-width:900px">One partner for accepting, moving and protecting your payments.</h1>
    <p class="lede">From a single card machine to multi-currency, multi-provider setups for high-volume online businesses &mdash; we compare the market, arrange the right partners and stay on it afterwards.</p>
    <div class="btn-row"><a class="btn btn-primary" href="/contact/">Talk to us {ARROW}</a><a class="btn btn-ghost" href="/how-it-works/">How it works</a></div>
  </div>
</section>
<section class="section-white" style="padding-top:40px">
  <div class="container">{groups}</div>
</section>''' + cta_band()
    return page("/solutions/", "Payment Solutions | Gateway, POS, Payouts, Orchestration | DPayments",
                "Online payment gateway, POS, multi-currency, digital wallets, settlements, card payouts, payment orchestration and fraud management, arranged by an independent UK payments partner.",
                body, current="/solutions/")


# ---------------- Multi-currency ----------------
MULTI = dict(
    path="/solutions/multi-currency/", crumbs=SOL, crumb="Multi-currency",
    title="Multi-Currency Payment Acceptance | DPayments",
    desc="Accept card payments in your customers' local currencies, reduce cross-border friction and choose how and where you settle. Arranged by DPayments.",
    eyebrow="Multi-currency &amp; DCC", cta_channel="online",
    h1="Sell in your customers&rsquo; currency. Settle in yours.",
    lede="Customers buy more confidently when they see a familiar price and currency. We set you up to price and accept payments in multiple currencies, then settle in the currencies that suit your business.",
    points=["Major currencies worldwide", "Local pricing at checkout", "Settle in GBP, EUR, USD and more"],
    features_head=("What&rsquo;s included", "Built for selling across borders.", "The right setup depends on where your customers are and where your costs sit."),
    features=[
        ("globe", "Present in local currency", "Show prices and charge cards in the shopper&rsquo;s own currency, so there are no surprise conversion fees on their statement."),
        ("coins", "Multi-currency pricing", "Set your own price lists per currency, or convert automatically from a base price."),
        ("bank", "Flexible settlement", "Settle each currency to a matching account, or convert into your home currency &mdash; whichever costs you less."),
        ("chart", "FX transparency", "See the exchange rate and margin applied, rather than finding it buried in a blended rate."),
        ("card", "Local payment methods", "Add popular local methods alongside cards in the markets that use them."),
        ("receipt", "Clear reporting", "Reconcile sales and settlements by currency without spreadsheet gymnastics."),
    ],
    know_head=("Worth understanding", "Two ways to handle currency."),
    know=[
        ("coins", "Multi-currency pricing (MCP)", "You price in the customer&rsquo;s currency and the card is charged in that currency. Conversion happens on your side at settlement, so you control the rate and the customer sees a clean, local price."),
        ("refresh", "Dynamic currency conversion (DCC)", "The customer is offered the choice of paying in their home currency at the point of sale. It&rsquo;s common on terminals for tourists. It must be optional and clearly shown, and the rate is often less favourable for the customer."),
    ],
    uses_head=("Who it suits", "Common uses"),
    uses=[
        ("cart", "Ecommerce exporters", "Online shops selling into the EU, US and beyond."),
        ("car", "Travel &amp; tourism", "Hotels, tours and transport serving international visitors."),
        ("ticket", "iGaming", "Operators accepting deposits from players in several markets."),
        ("briefcase", "Brokers &amp; platforms", "Clients funding accounts in their own currency."),
    ],
    faqs=[
        ("Do I need a bank account in every currency?", "No. You can convert to your home currency at settlement. If you have costs in another currency, settling into a matching account can save you a second conversion."),
        ("Which currencies can I accept?", "It depends on the provider, but all the major currencies are widely supported. Tell us which markets you sell into and we&rsquo;ll check coverage."),
        ("Is multi-currency more expensive?", "International cards usually carry higher interchange whatever currency you charge in. What varies most between providers is the FX margin, which is why we compare it."),
    ],
    related=[R_SETTLE, R_GATEWAY, R_ORCH],
    cta=("Selling across borders?", "Tell us where your customers are and how you&rsquo;d like to be paid. We&rsquo;ll recommend a multi-currency setup and show the FX costs up front."),
)

# ---------------- Digital wallets ----------------
WALLETS = dict(
    path="/solutions/digital-wallets/", crumbs=SOL, crumb="Digital wallets",
    title="Apple Pay, Google Pay & Click to Pay for Business | DPayments",
    desc="Accept Apple Pay, Google Pay and Click to Pay in store and online. Faster checkout, fewer abandoned baskets and strong authentication built in.",
    eyebrow="Digital wallets &amp; Click to Pay", cta_channel="online",
    h1="One-tap checkout, in store and online.",
    lede="More and more customers pay with their phone or watch. Accepting Apple Pay, Google Pay and Click to Pay makes checkout faster, cuts form-filling and helps more payments go through first time.",
    points=["Apple Pay &amp; Google Pay", "Click to Pay for cards", "Works on terminals and online"],
    features_head=("What you can offer", "Every way to pay without typing a card number.", None),
    features=[
        ("wallet", "Apple Pay", "Accept payments from iPhone, Apple Watch and Mac with Face ID or Touch ID &mdash; contactless in store and one-tap on your website or app."),
        ("wallet", "Google Pay", "Let Android and Chrome users pay with saved cards in a tap, in store or online."),
        ("card", "Click to Pay", "The card schemes&rsquo; standard for online checkout. Returning shoppers pay with cards saved to their Visa, Mastercard or Amex profile &mdash; no long card form."),
        ("contactless", "Contactless in store", "Any modern terminal accepts phone and watch payments, just like a contactless card."),
        ("shield", "Stronger security", "Wallet payments use device tokens and biometric checks, so the real card number is never shared with you."),
        ("chart", "Better conversion", "Fewer fields means fewer abandoned baskets, especially on mobile."),
    ],
    steps_head=("Getting set up", "Usually the quickest win in payments.", "If you already take cards online, adding wallets is often a configuration change rather than a new project."),
    steps=[
        ("Check your provider supports it", "Most modern gateways and hosted checkouts do. If yours doesn&rsquo;t, that&rsquo;s worth knowing."),
        ("Verify your domain", "Apple Pay on the web needs a quick domain verification step; we&rsquo;ll walk you through it."),
        ("Switch on the buttons", "Wallet buttons appear automatically for customers whose device supports them."),
        ("Test and go live", "A few test payments on real devices, then you&rsquo;re done."),
    ],
    faqs=[
        ("Do wallet payments cost more than cards?", "Generally no. A wallet payment is still a card payment, priced at the underlying card&rsquo;s rate."),
        ("Do I need a new card machine?", "Not if it&rsquo;s contactless. Phone and watch payments work on any modern contactless terminal."),
        ("Is Click to Pay the same as Apple Pay?", "No. Apple Pay and Google Pay are device wallets. Click to Pay is a card-scheme service that lets shoppers use cards saved to their scheme profile on any device or browser."),
    ],
    related=[R_GATEWAY, R_POS, R_RISK],
)

# ---------------- Card payouts ----------------
PAYOUTS = dict(
    path="/solutions/card-payouts/", crumbs=SOL, crumb="Card payouts",
    title="Card Payouts: Send Funds to Visa & Mastercard Cards | DPayments",
    desc="Send withdrawals, winnings, refunds and disbursements directly to customers' debit and credit cards, often within minutes. Arranged through DPayments' partners.",
    eyebrow="Card payouts", cta_channel="online",
    h1="Pay money out as easily as you take it in.",
    lede="Card payouts let you send funds straight to a customer&rsquo;s Visa or Mastercard &mdash; often within minutes &mdash; using the same card they paid with. No need to collect bank details.",
    points=["Fast push-to-card transfers", "No bank details needed", "Ideal for withdrawals and winnings"],
    features_head=("How businesses use it", "Fast, simple disbursements.", None),
    features=[
        ("clock", "Fast delivery", "Push-to-card services such as Visa Direct and Mastercard Send can deliver funds in minutes to eligible cards."),
        ("card", "Use the card on file", "Pay back to the card the customer deposited with &mdash; simple for them and easier to reconcile for you."),
        ("users", "Better customer experience", "Quick withdrawals build trust, especially in gaming, trading and marketplaces."),
        ("shield", "Built-in controls", "Limits, velocity checks and verification rules to keep payouts safe."),
        ("coins", "Batch or single", "Send individual payouts in real time or process them in batches."),
        ("chart", "Full visibility", "Track every payout&rsquo;s status from request to delivery."),
    ],
    uses_head=("Common uses", "Who uses card payouts"),
    uses=[
        ("ticket", "iGaming", "Player withdrawals and winnings."),
        ("chart", "Forex &amp; trading", "Client withdrawals from trading accounts."),
        ("users", "Marketplaces &amp; gig work", "Paying sellers, drivers and freelancers."),
        ("receipt", "Refunds &amp; claims", "Insurance claims, rebates and goodwill payments."),
    ],
    faqs=[
        ("How fast are card payouts?", "Many eligible cards receive funds within minutes. Some issuers take longer; the provider can tell you what to expect by card type and country."),
        ("Can I pay out to any card?", "Most Visa and Mastercard debit cards are eligible, and many credit cards too. Coverage varies by issuer and country."),
        ("Is this the same as a refund?", "No. A refund reverses a previous payment. A payout is a new transfer, which lets you send amounts that differ from the original deposit, such as winnings or profits."),
    ],
    related=[R_SETTLE, R_ORCH, R_RISK],
)

# ---------------- Settlements ----------------
STABLE = f'''<section id="stablecoin" style="scroll-margin-top:90px">
  <div class="container split v-center">
    <div>
      <span class="eyebrow">Stablecoin settlements</span>
      <h2>Faster cross-border settlement, through partners.</h2>
      <p class="lede">For businesses with international flows, some partners can settle your card takings in regulated stablecoins such as USDC, alongside or instead of fiat. That can mean faster access to funds across borders and outside banking hours.</p>
      <p>We act as an introducer only: settlement is provided by the partner, and we never hold your funds. Stablecoins carry their own risks, and whether this is suitable depends on your business, your jurisdiction and your accounting setup.</p>
      <div class="btn-row mt-m"><a class="btn btn-primary" href="/contact/">Ask about stablecoin settlement {ARROW}</a><a class="text-link" href="https://crypto.dpayments.co.uk">Crypto payments &#8599;</a></div>
    </div>
    <div class="card card-lg reveal">
      <h3>Why businesses consider it</h3>
      {ticks(["Settlement that isn&rsquo;t tied to bank cut-off times", "Fewer intermediary banks on cross-border transfers", "Useful for businesses with costs or suppliers paid in USD-linked assets", "Can sit alongside your normal fiat settlement"])}
    </div>
  </div>
</section>'''

SETTLE = dict(
    path="/solutions/settlements/", crumbs=SOL, crumb="Settlements",
    title="Multi-Currency & Stablecoin Settlements | DPayments",
    desc="Choose how, when and in which currency you're paid. Fiat settlement in multiple currencies, faster payout options and stablecoin settlement through partners.",
    eyebrow="Settlements", cta_channel="online",
    h1="Get paid how, when and where you need.",
    lede="Settlement is the part of payments that hits your cash flow. We find you terms that fit &mdash; the right currencies, the right accounts and the fastest payout timing available for your business.",
    points=["Multi-currency settlement", "Next-day options with some providers", "Stablecoin settlement via partners"],
    features_head=("What we look at", "Settlement terms matter as much as rates.", "Two providers with the same rate can leave you with very different cash flow."),
    features=[
        ("bank", "Settlement currencies", "Be paid in GBP, EUR, USD and other major currencies into matching accounts, to avoid unnecessary conversions."),
        ("clock", "Payout timing", "T+1, T+2 or T+3 &mdash; and whether faster options are available once you have a trading history."),
        ("refresh", "Settlement frequency", "Daily, weekly or on demand, depending on what suits your cash flow."),
        ("shield", "Reserves", "Whether a rolling or fixed reserve applies, how much, for how long, and when it&rsquo;s released."),
        ("receipt", "Gross vs net", "Whether fees are deducted before payout or invoiced separately &mdash; it affects how you reconcile."),
        ("chart", "Reporting", "Settlement reports that tie each payout back to the transactions in it."),
    ],
    extra_html=STABLE,
    faqs=[
        ("What does T+1 mean?", "Funds reach your account one business day after the transaction date. T+2 is two days, and so on."),
        ("Why would a provider hold a reserve?", "To cover potential refunds and chargebacks. It&rsquo;s more common for new businesses, online sellers and higher-risk sectors. It should always be disclosed before you sign."),
        ("Does DPayments hold my money?", "No. Settlement is always made directly to you by the acquirer or partner. We don&rsquo;t hold or touch merchant funds."),
    ],
    related=[R_MULTI, R_PAYOUT, R_ORCH],
)

# ---------------- Risk & fraud ----------------
TOKENS = f'''<section id="network-tokens" class="section-white" style="scroll-margin-top:90px">
  <div class="container split v-center">
    <div>
      <span class="eyebrow">Network tokens</span>
      <h2>Replace stored card numbers with scheme-issued tokens.</h2>
      <p class="lede">Network tokens are issued by Visa, Mastercard and other schemes to stand in for a customer&rsquo;s real card number. They&rsquo;re tied to your business and update automatically when a card is replaced or expires.</p>
    </div>
    <div class="grid g2">
      <div class="card reveal">{icon("check")}<h4>Higher approval rates</h4><p>Issuers trust tokenised transactions more, which can lift approvals on repeat and subscription payments.</p></div>
      <div class="card reveal">{icon("refresh")}<h4>Fewer failed renewals</h4><p>Tokens update when cards are reissued, so subscriptions keep running.</p></div>
      <div class="card reveal">{icon("lock")}<h4>Less sensitive data</h4><p>A stolen token is useless outside your business, reducing breach risk.</p></div>
      <div class="card reveal">{icon("coins")}<h4>Potentially lower costs</h4><p>Some schemes and acquirers offer better pricing on tokenised transactions.</p></div>
    </div>
  </div>
</section>'''

SECURITY = f'''<section id="security" style="scroll-margin-top:90px">
  <div class="container">
    <div class="section-head"><span class="eyebrow">Security &amp; compliance</span><h2>The standards that keep card data safe.</h2>
      <p class="lede">We make sure the setup we recommend meets the standards that apply to you &mdash; and that you understand your part.</p></div>
    <div class="grid g4">
      <div class="card reveal">{icon("shield")}<h4>PCI DSS</h4><p>The card industry&rsquo;s data security standard. We help you pick the right self-assessment questionnaire and keep it current, so you avoid non-compliance fees.</p></div>
      <div class="card reveal">{icon("lock")}<h4>P2PE</h4><p>Point-to-point encryption terminals encrypt card data the moment it&rsquo;s read, which can dramatically shrink your PCI scope in store.</p></div>
      <div class="card reveal">{icon("check")}<h4>3DS v2 &amp; SCA</h4><p>Strong Customer Authentication for online payments, configured to challenge only when needed.</p></div>
      <div class="card reveal">{icon("eye")}<h4>Fraud partners</h4><p>Access to specialist fraud-prevention and chargeback-guarantee services for higher-risk or high-volume merchants.</p></div>
    </div>
  </div>
</section>'''

RISK = dict(
    path="/solutions/risk-fraud/", crumbs=SOL, crumb="Risk &amp; fraud",
    title="Risk, Fraud & Security: 3D Secure, PCI, P2PE & Network Tokens | DPayments",
    desc="Stop fraud before it becomes a chargeback. Fraud screening, 3D Secure 2, network tokens, chargeback alerts and dispute support, arranged by DPayments.",
    eyebrow="Risk &amp; fraud management", cta_channel="online",
    h1="Stop fraud without stopping good customers.",
    lede="Too little protection and you pay for fraud and chargebacks. Too much and you turn away genuine customers. We help you put the right tools in place for your sector and your risk level.",
    points=["Fraud screening and rules", "3D Secure 2 done properly", "Chargeback prevention"],
    features_head=("The toolkit", "Layered protection, tuned to your business.", None),
    features=[
        ("search", "Fraud screening", "Real-time risk scoring using device, location, velocity and behaviour signals to flag or block suspicious payments."),
        ("clipboard", "Custom rules", "Set your own limits, block lists and review queues for your products and markets."),
        ("shield", "3D Secure 2", "Strong Customer Authentication that challenges only risky payments and shifts fraud liability to the card issuer."),
        ("lock", "Tokenisation", "Keep raw card numbers off your systems with gateway and network tokens."),
        ("alert", "Chargeback alerts", "Early-warning services that let you refund a disputed payment before it becomes a chargeback."),
        ("file", "Dispute support", "Help gathering the right evidence and responding to chargebacks on time."),
    ],
    know_head=("Why it matters", "The real cost of fraud is more than the sale."),
    know=[
        ("receipt", "Chargeback fees", "Each dispute usually carries a fee on top of the lost sale and the goods or service already delivered."),
        ("chart", "Monitoring programmes", "Card schemes monitor chargeback and fraud ratios. Exceeding thresholds can mean fines, reserves or losing your account."),
        ("users", "False declines", "Over-blocking turns away genuine customers. Good fraud tools protect revenue as well as reduce losses."),
    ],
    extra_html=TOKENS + SECURITY,
    faqs=[
        ("Does 3D Secure hurt conversion?", "Older versions did. 3DS2 uses risk data so most customers are approved without a challenge, and those who are challenged usually confirm in their banking app."),
        ("What chargeback rate is too high?", "Thresholds vary by scheme and change over time, but as a rule of thumb, staying well below 1% of transactions is important. Specialist sectors are watched more closely."),
        ("Can you help if I already have a chargeback problem?", "Yes. We&rsquo;ll look at where disputes are coming from and recommend fixes &mdash; from descriptors and refund policy to screening rules and alerts."),
    ],
    related=[R_ORCH, R_WALLET, R_GATEWAY],
)

# ---------------- Orchestration ----------------
ORCH_EXTRA = f'''<section id="routing" class="section-white" style="scroll-margin-top:90px">
  <div class="container">
    <div class="section-head"><span class="eyebrow">How smart routing works</span><h2>The right provider for every payment.</h2>
      <p class="lede">Instead of sending every transaction to one acquirer, an orchestration layer decides in real time where each payment should go.</p></div>
    <div class="grid g4">
      <div class="card reveal"><span class="tag">1</span><h4>Payment arrives</h4><p>Card type, country, currency, amount and risk score are read instantly.</p></div>
      <div class="card reveal"><span class="tag">2</span><h4>Rules are applied</h4><p>Route by cost, approval rate, currency or region &mdash; or let performance data decide.</p></div>
      <div class="card reveal"><span class="tag">3</span><h4>Best provider chosen</h4><p>The payment goes to the acquirer most likely to approve it at the best cost.</p></div>
      <div class="card reveal"><span class="tag">4</span><h4>Automatic retry</h4><p>If a soft decline comes back, it can be retried through another provider in milliseconds.</p></div>
    </div>
  </div>
</section>'''

ORCH = dict(
    path="/solutions/orchestration/", crumbs=SOL, crumb="Payment orchestration",
    title="Payment Orchestration & Smart Routing | DPayments",
    desc="Connect multiple acquirers and payment methods through one integration. Smart routing, failover, tokenisation and unified reporting to lift approvals and cut costs.",
    eyebrow="Payment orchestration", cta_channel="online",
    h1="Many providers. One integration. Better results.",
    lede="As you grow, relying on a single acquirer becomes a risk. Payment orchestration connects several providers and payment methods behind one integration, routing each payment where it&rsquo;s most likely to succeed at the lowest cost.",
    points=["Smart routing and failover", "Connect multiple PSPs and acquirers", "One view of performance"],
    features_head=("What orchestration gives you", "Control, resilience and insight.", None),
    features=[
        ("refresh", "Smart routing", "Rules and performance data send each payment to the best provider by cost, approval rate, currency or region."),
        ("plug", "Connections", "Add acquirers, PSPs and alternative payment methods without rebuilding your checkout each time."),
        ("shield", "Failover", "If one provider has an outage, traffic moves to another automatically, so you keep taking payments."),
        ("lock", "Provider-agnostic tokenisation", "Store cards once in a vault you control and use them with any connected provider &mdash; no lock-in."),
        ("chart", "Reporting &amp; analytics", "Approval rates, decline reasons and costs compared across every provider in one dashboard."),
        ("coins", "Cost optimisation", "Route to the cheapest suitable provider and negotiate from a position of strength."),
    ],
    extra_html=ORCH_EXTRA,
    uses_head=("Who it suits", "When orchestration makes sense"),
    uses=[
        ("chart", "Growing volume", "Online businesses processing significant monthly volume."),
        ("globe", "Multiple markets", "Selling in several countries or currencies."),
        ("ticket", "Specialist sectors", "iGaming, forex and brokerage, where provider capacity and resilience matter."),
        ("alert", "Single-provider risk", "Anyone who can&rsquo;t afford a day without payments."),
    ],
    faqs=[
        ("Do I need orchestration?", "Not always. For a single shop or modest online volume, one good provider is simpler. Orchestration pays off as volume, markets and the cost of downtime grow. We&rsquo;ll tell you honestly which camp you&rsquo;re in."),
        ("Will I need to rebuild my checkout?", "Usually you integrate once with the orchestration platform, and adding providers afterwards is configuration rather than development."),
        ("Does orchestration replace my acquirer?", "No. It sits in front of your acquirers and PSPs. You still need merchant accounts with the providers it routes to &mdash; which we can help arrange."),
    ],
    related=[R_RISK, R_MULTI, R_INT],
    cta=("Outgrowing a single provider?", "Tell us your volumes, markets and current setup. We&rsquo;ll tell you whether orchestration makes sense and what it would take."),
)

# ---------------- Integration ----------------
INT = dict(
    path="/solutions/integration/", crumbs=SOL, crumb="Integration",
    title="Payment Integration: Plugins, Hosted Pages & APIs | DPayments",
    desc="Connect payments to your website, app or software the way that suits you: no-code payment links, ecommerce plugins, hosted payment pages, SDKs or full APIs.",
    eyebrow="Integration", cta_channel="online",
    h1="Connect payments the way that suits your team.",
    lede="Whether you have no developers or a full engineering team, there&rsquo;s an integration route that fits. We match you with providers whose integration options suit your platform and resources.",
    points=["No-code to full API", "Major ecommerce platforms", "Sandbox testing"],
    features_head=("Integration options", "From zero code to full control.", "Ordered roughly from least to most technical effort."),
    features=[
        ("link", "Payment links &amp; virtual terminal", "No integration at all. Create links or key payments in from a browser."),
        ("cart", "Ecommerce plugins", "Ready-made plugins for popular shop and website platforms. Install, add your keys, go live."),
        ("globe", "Hosted payment page", "Redirect customers to a secure, branded page. Minimal code and the lightest PCI burden."),
        ("card", "Embedded fields &amp; drop-in", "Payment fields embedded in your own checkout while card data still goes straight to the provider."),
        ("phone", "Mobile SDKs", "Native iOS and Android components, including Apple Pay and Google Pay."),
        ("plug", "Server-to-server API", "Full control for custom platforms and orchestration. Brings greater PCI responsibility."),
    ],
    steps_head=("How we help", "Smoother from sandbox to live.", None),
    steps=[
        ("Understand your stack", "Your platform, your team and how much control you need."),
        ("Shortlist suitable providers", "Only those with solid integrations for your setup."),
        ("Sandbox access", "Test credentials so your team or developer can build and test before going live."),
        ("Go-live checks", "Webhooks, 3DS2, refunds and reconciliation tested before real money flows."),
    ],
    faqs=[
        ("Which integration has the least PCI work?", "Payment links and hosted payment pages, because card data never touches your systems. A full server-to-server API carries the most responsibility."),
        ("Can you build the integration for us?", "Our team at DBS Group builds websites and apps, so if you need development help we can scope it with you."),
        ("Do I need a developer for a plugin?", "Usually not. Most ecommerce plugins can be installed and configured by anyone comfortable with their store&rsquo;s admin panel."),
    ],
    related=[R_GATEWAY, R_ORCH, R_WALLET],
)


R_EPOS = ("/solutions/epos/", "store", "ePOS systems", "Tills and back-office linked to your card payments.")
R_METHODS = ("/solutions/payment-methods/", "card", "Payment methods", "Cards, wallets, PayPal, pay later and open banking.")
R_LOYAL = ("/solutions/loyalty/", "heart", "Loyalty &amp; smart receipts", "Rewards and digital receipts that bring customers back.")

METHODS = dict(
    path="/solutions/payment-methods/", crumbs=SOL, crumb="Payment methods",
    title="Payment Methods: Cards, Apple Pay, PayPal, Klarna & Open Banking | DPayments",
    desc="Accept the payment methods your customers prefer: Visa, Mastercard, Amex, Apple Pay, Google Pay, PayPal, buy now pay later, open banking and local methods.",
    eyebrow="Payment methods", cta_channel="online",
    h1="Let customers pay the way they prefer.",
    lede="Every payment method you don&rsquo;t offer is a reason for someone to leave. We help you add the methods that matter for your customers &mdash; without cluttering checkout with ones that don&rsquo;t.",
    points=["Cards and wallets", "PayPal and pay later", "Open banking and local methods"],
    features_head=("What you can accept", "The methods UK and European customers use.", "Availability depends on the provider and your sector."),
    features_cols="g4",
    features=[
        ("card", "Visa &amp; Mastercard", "Debit, credit and commercial cards &mdash; the backbone of every setup."),
        ("card", "American Express", "Often enabled and priced separately. Worth it if your customers carry it."),
        ("wallet", "Apple Pay &amp; Google Pay", "One-tap payments in store, online and in app."),
        ("check", "Click to Pay", "Saved scheme cards for a faster online checkout."),
        ("globe", "PayPal", "Familiar and trusted, especially for first-time online customers."),
        ("clock", "Buy now, pay later", "Let customers spread the cost with providers such as Klarna. You&rsquo;re paid upfront; the BNPL provider takes the credit risk."),
        ("bank", "Open banking (pay by bank)", "Payments straight from the customer&rsquo;s bank app &mdash; good for larger amounts and no chargebacks in the card sense."),
        ("coins", "Local methods", "Popular regional methods for selling into European markets."),
    ],
    steps_head=("Choosing well", "More methods isn&rsquo;t always better.", None),
    steps=[
        ("Look at who your customers are", "Age, country, device and basket size all change which methods they reach for."),
        ("Weigh the cost", "Each method has its own fees. Some lift sales enough to justify them; some don&rsquo;t."),
        ("Keep checkout clean", "Show the most-used methods first, with the rest one tap away."),
        ("Measure and adjust", "Track usage and conversion, and drop what isn&rsquo;t pulling its weight."),
    ],
    faqs=[
        ("Does offering buy now, pay later cost more?", "BNPL providers usually charge the merchant a higher fee than cards, in exchange for paying you upfront and carrying the repayment risk. It can pay off on higher-value items."),
        ("Can I take PayPal through my card provider?", "Many gateways offer PayPal as an option on the same checkout and reporting, so you don&rsquo;t need a separate integration."),
        ("Is open banking cheaper than cards?", "Often, yes, especially for larger payments. But not every customer is comfortable with it yet, so it works best alongside cards."),
    ],
    related=[R_WALLET, R_GATEWAY, R_MULTI],
)

EPOS = dict(
    path="/solutions/epos/", crumbs=SOL, crumb="ePOS systems",
    title="ePOS Systems for Retail & Hospitality, Integrated with Card Payments | DPayments",
    desc="Till systems for shops, restaurants, bars and hotels, integrated with your card machines. Stock, tables, staff and reporting in one place. Compared and arranged by DPayments.",
    eyebrow="ePOS systems", cta_channel="in-person",
    h1="A till system that talks to your card machines.",
    lede="When your ePOS and payments are linked, amounts go straight to the terminal, sales reconcile automatically and you stop keying the same number twice. We help you choose an ePOS that suits your venue and connects cleanly to your payments.",
    points=["Retail and hospitality ePOS", "Integrated card payments", "Stock, staff and reporting"],
    features_head=("What a good ePOS does", "Run the business, not just the till.", None),
    features=[
        ("plug", "Integrated payments", "Amounts sent to the terminal automatically, with tips and split bills flowing back into the sale."),
        ("clipboard", "Stock &amp; menus", "Track stock, manage menus and modifiers, and update prices across sites."),
        ("cup", "Tables &amp; orders", "Table plans, kitchen screens or printers, and order-at-table for hospitality."),
        ("users", "Staff management", "Logins, permissions, clock-in and tip allocation."),
        ("chart", "Reporting", "Sales by product, hour, staff member and site, in real time."),
        ("globe", "Online ordering", "Click-and-collect, delivery and booking integrations feeding the same system."),
    ],
    uses_head=("Who it suits", "Built for different venues"),
    uses=[
        ("cup", "Restaurants &amp; bars", "Table service, kitchen flow and tipping."),
        ("users", "Hotels", "Restaurant, bar and room charges in one place."),
        ("store", "Retail", "Barcode scanning, stock and multi-site retail."),
        ("tool", "Garden centres &amp; merchants", "Large catalogues, trade accounts and weighed items."),
    ],
    faqs=[
        ("Can I keep my existing ePOS?", "Often, yes. Many ePOS systems integrate with several payment providers. We check which providers your system supports before recommending anything."),
        ("Is ePOS hardware bought or rented?", "Both models exist, and software is usually a monthly subscription. As with card machines, we set out the full cost and contract terms."),
        ("Do I need integrated payments?", "For busy venues, it saves time and errors. For a small shop with one till, a standalone card machine can be simpler and cheaper."),
    ],
    related=[R_POS, R_LOYAL, R_METHODS],
)

LOYAL = dict(
    path="/solutions/loyalty/", crumbs=SOL, crumb="Loyalty &amp; smart receipts",
    title="Loyalty, Rewards & Smart Receipts for Card Payments | DPayments",
    desc="Card-linked loyalty, digital rewards and smart receipts that turn payments into repeat visits. Options compared and arranged by DPayments.",
    eyebrow="Loyalty &amp; smart receipts", cta_channel="in-person",
    h1="Turn every payment into a reason to come back.",
    lede="Your card terminal already knows when a customer returns. Loyalty and engagement tools use that moment to reward them, collect feedback and bring them back again &mdash; without paper stamp cards.",
    points=["Card-linked rewards", "Digital &amp; smart receipts", "Feedback and offers"],
    features_head=("What you can offer", "Simple tools that drive repeat business.", None),
    features=[
        ("card", "Card-linked loyalty", "Customers earn rewards just by paying with their usual card &mdash; no app or card to carry."),
        ("heart", "Points &amp; stamps", "Digital stamp cards and points schemes your customers actually use."),
        ("receipt", "Smart receipts", "Branded email or SMS receipts with offers, reviews and links to your socials."),
        ("users", "Feedback", "Collect ratings straight after a visit, while it&rsquo;s fresh."),
        ("mail", "Targeted offers", "Reward regulars and win back lapsed customers with timely offers."),
        ("chart", "Customer insight", "See visit frequency and spend so you know what&rsquo;s working."),
    ],
    faqs=[
        ("Do customers need to download an app?", "Not with card-linked loyalty. They&rsquo;re recognised by the card they pay with, once they&rsquo;ve opted in."),
        ("Is this GDPR-friendly?", "Good schemes are opt-in and transparent about what&rsquo;s collected. We only recommend providers that handle consent properly."),
    ],
    related=[R_EPOS, R_POS, R_METHODS],
)

FUND = dict(
    path="/solutions/business-funding/", crumbs=SOL, crumb="Business funding",
    title="Merchant Cash Advance & Business Funding | DPayments",
    desc="Business funding repaid as a percentage of your card sales. Introduced through specialist funding partners. Subject to status and eligibility.",
    eyebrow="Business funding", cta_channel="in-person",
    h1="Funding that flexes with your card sales.",
    lede="A merchant cash advance gives you a lump sum upfront, repaid automatically as a small percentage of your future card takings. Busy months repay faster; quiet months repay less. We introduce you to specialist funding partners.",
    points=["Repaid from card sales", "No fixed monthly repayments", "Introduced via funding partners"],
    features_head=("How it works", "Simple, sales-linked funding.", None),
    features=[
        ("coins", "Upfront funds", "A lump sum based on your card turnover history, to use for stock, refits, equipment or cash flow."),
        ("refresh", "Repaid as you trade", "An agreed percentage of each day&rsquo;s card takings goes towards repayment."),
        ("clock", "Fixed total cost", "You agree one fixed fee upfront, so you know exactly what you&rsquo;ll repay."),
        ("chart", "Flexes with your sales", "Repayments rise and fall with turnover, easing pressure in quiet periods."),
    ],
    features_cols="g4",
    faqs=[
        ("Who is eligible?", "Typically UK businesses that have taken card payments for several months with consistent turnover. Each funding partner sets its own criteria."),
        ("Is DPayments the lender?", "No. Funding is provided by third-party funders, subject to status, affordability and their terms. We may receive a commission for introductions."),
        ("Is a cash advance a loan?", "A merchant cash advance is usually structured as the purchase of a share of your future card sales rather than a loan, but read each funder&rsquo;s terms carefully and take independent advice if unsure."),
    ],
    note_text="DPayments is not a lender and does not provide financial advice. Funding is offered by third-party providers, subject to status, eligibility and their terms and conditions. We may receive a commission from funding partners for introductions.",
    related=[R_POS, R_SETTLE, ("/switch/", "search", "Switch &amp; save", "Free line-by-line statement review.")],
)


def build_all():
    return {
        "solutions/index.html": overview(),
        "solutions/multi-currency/index.html": build_page(MULTI),
        "solutions/digital-wallets/index.html": build_page(WALLETS),
        "solutions/card-payouts/index.html": build_page(PAYOUTS),
        "solutions/settlements/index.html": build_page(SETTLE),
        "solutions/risk-fraud/index.html": build_page(RISK),
        "solutions/orchestration/index.html": build_page(ORCH),
        "solutions/integration/index.html": build_page(INT),
        "solutions/payment-methods/index.html": build_page(METHODS),
        "solutions/epos/index.html": build_page(EPOS),
        "solutions/loyalty/index.html": build_page(LOYAL),
        "solutions/business-funding/index.html": build_page(FUND),
    }
