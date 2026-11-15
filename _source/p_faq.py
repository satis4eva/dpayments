import json, re
from common import *

TITLE = "Merchant Services, Explained | Card Payments FAQ | DPayments"
DESC = ("Plain-English answers on card payments: merchant accounts, acquirers, PCI DSS, 3D Secure, chargebacks, "
        "settlement, interchange and contracts.")

GROUPS = [
    ("getting-started", "Getting started", [
        ("What is a merchant account?", "A bank-style account that receives the money from your card sales first, before it moves into your normal business current account. It sits between the card networks and your bank, and may be bundled with a terminal or checkout, or kept separate."),
        ("What&rsquo;s the difference between an acquirer, a PSP and a gateway?", "An <strong>acquirer</strong> is licensed by the card schemes to settle transactions and carries the underwriting risk. A <strong>gateway</strong> securely passes transaction data to the acquirer. A <strong>PSP</strong> (payment service provider) packages a gateway, and sometimes acquiring, into a single product. One company can perform several of these roles."),
        ("What is a MID?", "A Merchant Identification number &mdash; a unique ID for your business in the acquirer&rsquo;s systems. It links your transactions, settlements and disputes to you. A business can have several, for example one per site or trading channel."),
        ("Can I take payments without a website?", "Yes. A virtual terminal lets you key in card details on a secure page for phone or mail-order payments, and payment links send a one-off hosted payment page by text or email. Both suit invoices, deposits and phone orders."),
        ("Can I take Apple Pay and Google Pay?", "Yes. Modern contactless terminals accept Apple Pay and Google Pay just like a contactless card, and most hosted checkouts can show them as one-tap options on mobile."),
        ("I&rsquo;m a new business with no trading history. Can I still take cards?", "Usually, yes. Providers will look more closely at your plans, and some may start you on slower settlement or hold a small reserve until you&rsquo;ve built up a history. We&rsquo;ll tell you what to expect before you apply."),
    ]),
    ("verification", "Verification and compliance", [
        ("Why am I asked for ID, bank statements and business details?", "Providers must run Know-Your-Customer (KYC) and anti-money-laundering (AML) checks. These confirm who owns and runs the business, which bank account will receive settlements, and what you sell. It&rsquo;s an industry-wide regulatory requirement &mdash; and the main factor in how quickly you can go live."),
        ("What is PCI DSS and what do I actually have to do?", "The Payment Card Industry Data Security Standard sets rules for handling card data. Most smaller merchants comply by completing an annual Self-Assessment Questionnaire (SAQ) and using compliant terminals or hosted checkouts, so raw card numbers stay off their systems. The less card data you handle, the fewer obligations you have. Lapsed compliance can trigger provider fees, so keep it current."),
        ("What is 3D Secure 2?", "3DS2 is the authentication step in online card payments, where a customer may confirm a purchase in their banking app. It shifts fraud liability on authenticated transactions to the card issuer and is generally required for most UK and EU online payments under Strong Customer Authentication rules. Good setups only challenge risky payments."),
        ("What do I need on my website to take online payments?", "Providers typically expect clear products and prices, terms and conditions, a refund and returns policy, a privacy policy, contact details and HTTPS across the site. We&rsquo;ll check these with you before applying."),
    ]),
    ("disputes", "Disputes and settlement", [
        ("What is a chargeback, and how do I fight one?", "A chargeback is when a cardholder&rsquo;s bank reverses a payment while it investigates a dispute. To defend it, you provide evidence the transaction was legitimate &mdash; receipts, proof of delivery, communications and authorisation records. Clear refund policies and fraud checks are the cheapest way to reduce chargebacks."),
        ("What does settlement in T+1 vs T+3 mean?", "It&rsquo;s how long cleared funds take to reach your bank after a sale: one business day for T+1, three for T+3. Authorisation takes about a second, but bank transfers take days. Timing depends on the acquirer, the card scheme and your account terms."),
        ("What is a rolling reserve?", "A percentage of your takings held back by the provider for a set period, to cover potential refunds or chargebacks. It&rsquo;s more common for new businesses, online sellers and those taking payment well before delivery. It should be disclosed up front, along with how and when it&rsquo;s released."),
    ]),
    ("pricing", "Pricing and fees", [
        ("What is interchange, and what is interchange++ pricing?", "Interchange is a wholesale fee set by the card networks and paid to the cardholder&rsquo;s bank &mdash; no provider can waive it. Scheme fees go to Visa and Mastercard, and the acquirer adds its own margin. Interchange++ itemises all three so you can see the cost and the markup separately. Blended pricing combines them into one rate, which is simpler but less transparent."),
        ("What&rsquo;s the difference between blended and interchange-plus pricing?", "Blended pricing applies one flat rate to all card types. Interchange-plus passes through the actual interchange and scheme fees and adds a fixed, visible margin. Blended is more predictable; interchange-plus is more transparent and can be cheaper depending on your card mix."),
        ("What is an authorisation fee?", "A small per-transaction charge for checking a card is valid and has funds, separate from the percentage rate. It applies even to low-value payments and can make a headline rate look cheaper than the true cost."),
    ]),
    ("contracts", "Contracts and card types", [
        ("What should I watch for in a card payments contract?", "Check the minimum term and auto-renewal, whether terminal rental is separate and how long it lasts, minimum monthly charges, PCI non-compliance fees and early-exit charges. These often add more cost than the headline rate, so terminal terms deserve the same scrutiny as transaction rates."),
        ("Do I need a different setup to take American Express or international cards?", "Sometimes. Amex is often priced and enabled separately from Visa and Mastercard. International and commercial cards usually carry higher interchange, so share your typical card mix when asking for a quote."),
        ("Can I switch provider if I&rsquo;m still in a contract?", "It depends on your terms. Sometimes waiting for the notice window is cheapest; sometimes the savings outweigh an exit fee. Send us your statement and agreement and we&rsquo;ll work out which applies to you."),
    ]),
]

def strip(s):
    return re.sub(r"<[^>]+>", "", s).replace("&rsquo;", "’").replace("&mdash;", "—").replace("&amp;", "&")

nav = "".join(f'<a class="pill" href="#{a}">{t}</a>' for a, t, _ in GROUPS)
groups = "".join(
    f'<div class="faq-group" id="{a}" style="scroll-margin-top:100px"><h2>{t}</h2>' +
    "".join(f'<details class="faq"><summary>{q}</summary><div class="answer"><p>{ans}</p></div></details>' for q, ans in qs) +
    "</div>" for a, t, qs in GROUPS)

schema_obj = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
    {"@type": "Question", "name": strip(q), "acceptedAnswer": {"@type": "Answer", "text": strip(ans)}}
    for _, _, qs in GROUPS for q, ans in qs]}
schema = '<script type="application/ld+json">' + json.dumps(schema_obj, ensure_ascii=False) + "</script>"

BODY = f'''<section class="page-hero">
  <div class="container">
    <div class="crumbs"><a href="/">Home</a> / FAQ</div>
    <span class="eyebrow">Merchant services, explained</span>
    <h1>The questions merchants actually ask.</h1>
    <p class="lede">Plain-English answers on card payments: merchant accounts, acquirers, PCI, chargebacks, settlement and pricing. Can&rsquo;t see yours? Send it to us.</p>
  </div>
</section>
<section style="padding-top:0">
  <div class="container narrow" style="max-width:860px">
    <div class="faq-nav">{nav}</div>
    {groups}
    <div class="card card-lg center">
      <h2 style="font-size:1.6rem">Still have a question? Ask a human.</h2>
      <p>Send us your question and we&rsquo;ll reply by email &mdash; no obligation, no sales script.</p>
      <div class="btn-row" style="justify-content:center"><a class="btn btn-primary" href="/contact/">Get a quote {ARROW}</a><a class="text-link" href="mailto:{EMAIL}">or email {EMAIL}</a></div>
    </div>
  </div>
</section>'''


def build():
    return page("/faq/", TITLE, DESC, BODY, current="/faq/", schema=schema)
