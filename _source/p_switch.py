from common import *
from forms import quote_form

TITLE = "Switch & Save: Free Merchant Statement Review | DPayments"
DESC = ("Already taking card payments? Send us a recent statement and we'll explain every line, separate real costs from "
        "provider margin, and tell you plainly whether you could pay less.")

hero = f'''<section class="page-hero">
  <div class="container">
    <div class="crumbs"><a href="/">Home</a> / Switch &amp; save</div>
    <span class="eyebrow">Already taking payments?</span>
    <h1 style="max-width:900px">Send us a recent statement. We&rsquo;ll tell you what it actually says.</h1>
    <p class="lede">Merchant statements are built to be hard to read. Send one in and we&rsquo;ll go through it line by line, separate genuine costs from provider margin, and flag what you could stop paying.</p>
    <div class="btn-row">
      <a class="btn btn-primary" href="#review">Get your statement read {ARROW}</a>
      <a class="text-link" href="mailto:{EMAIL}?subject=Statement%20review">or email {EMAIL}</a>
    </div>
  </div>
</section>'''

lines = [
    ("Merchant service charge", "Margin + cost", "The headline percentage on your card turnover. It&rsquo;s the figure most often quoted, but on its own it says very little about what you really pay."),
    ("Interchange", "Cost", "A wholesale fee set by the card networks and paid to your customer&rsquo;s bank. No provider can waive it. Transparent statements show it separately; blended ones hide it."),
    ("Scheme fees", "Cost", "Per-transaction fees paid to Visa and Mastercard. Small individually, significant in total, and a pass-through cost rather than provider margin."),
    ("Acquirer margin", "Margin", "What your provider keeps. Interchange-plus pricing shows it as a fixed figure; blended pricing folds it into the headline rate."),
    ("Authorisation fees", "Margin", "A small charge on every authorisation request &mdash; including the smallest sales, which is where it hurts most."),
    ("PCI fees", "Margin", "Charges for data-security compliance, plus a monthly non-compliance fee if your annual self-assessment lapses."),
    ("Minimum monthly service charge", "Margin", "A monthly floor charged regardless of turnover, so quiet months can cost more than the rate suggests."),
    ("Terminal rental", "Margin", "A separate, often longer agreement that can outlast everything else on your statement and wipe out the savings of a cheap processing deal."),
]
lines_html = "".join(
    f'<li class="reveal"><div><h4>{h} <span class="tag {"tag-warn" if k == "Margin" else ""}" style="margin:0 0 0 8px;vertical-align:middle">{k}</span></h4><p>{p}</p></div></li>'
    for h, k, p in lines)

savings = f'''<section>
  <div class="container">
    <div class="section-head">
      <span class="eyebrow">Where savings usually come from</span>
      <h2>It&rsquo;s rarely just the rate.</h2>
      <p class="lede">When merchants are overpaying, it&rsquo;s usually down to a few familiar causes. These are the first things we look for.</p>
    </div>
    <div class="grid g3">
      <div class="card reveal">{icon("coins")}<h3>Pricing model</h3><p>Moving from blended to interchange-plus pricing can cut costs significantly if most of your customers pay with UK consumer debit cards.</p></div>
      <div class="card reveal">{icon("receipt")}<h3>Fees you don&rsquo;t need</h3><p>PCI non-compliance fees, duplicate service charges, statement fees and minimums that no longer match your turnover.</p></div>
      <div class="card reveal">{icon("terminal")}<h3>Hardware costs</h3><p>Paying rental on more terminals than you use, or on devices you&rsquo;ve long since paid for several times over.</p></div>
      <div class="card reveal">{icon("card")}<h3>Card mix</h3><p>Premium, commercial and international cards cost more. Pricing that reflects your real mix can make a real difference.</p></div>
      <div class="card reveal">{icon("chart")}<h3>Outgrown pricing</h3><p>Rates agreed when you were smaller. As turnover grows, your pricing should improve too &mdash; it often doesn&rsquo;t unless you ask.</p></div>
      <div class="card reveal">{icon("file")}<h3>Contract timing</h3><p>Knowing when your term and notice window end, so you can switch without exit fees &mdash; or negotiate with your current provider.</p></div>
    </div>
  </div>
</section>'''

what_send = f'''<section class="section-white section-tight">
  <div class="container split v-center">
    <div>
      <span class="eyebrow">What to send</span>
      <h2>Have these to hand.</h2>
      <p class="lede">We&rsquo;ll ask for them by email once we&rsquo;ve heard from you &mdash; you don&rsquo;t need to attach anything to the form.</p>
    </div>
    <div class="card card-lg reveal">
      {ticks(["One or two recent monthly merchant statements (all pages)", "Your terminal rental or hardware agreement, if separate", "Your contract start date and term, if you know it", "Roughly how your customers pay &mdash; in person, online, by phone"])}
      <div class="callout mt-m"><p>Please don&rsquo;t email full card numbers or passwords. Statements are fine &mdash; they don&rsquo;t contain your customers&rsquo; card details.</p></div>
    </div>
  </div>
</section>'''

review = f'''<section id="review">
  <div class="container split">
    <div class="sticky">
      <span class="eyebrow">Statement review</span>
      <h2>Get a straight read on what you pay.</h2>
      <p class="lede">Fill in a few details and we&rsquo;ll follow up by email &mdash; send your statement when we reply. It&rsquo;s free, there&rsquo;s no obligation, and no sales call unless you ask for one.</p>
      <ol class="numbered mt-m">
        <li><div><h4>We read your statement</h4><p>And separate the genuine costs from the margin.</p></div></li>
        <li><div><h4>We tell you plainly</h4><p>Whether you could do better, and by roughly how much.</p></div></li>
        <li><div><h4>If you could, we quote it</h4><p>If you couldn&rsquo;t, we&rsquo;ll say so. Either way, you&rsquo;ll know.</p></div></li>
      </ol>
    </div>
    <div>{quote_form("switch", "Request a review", "Anything we should know?", "e.g. current provider, how long you&rsquo;ve been with them, anything on the statement you don&rsquo;t understand")}</div>
  </div>
</section>'''

BODY = hero + f'''<section class="section-white">
  <div class="container split">
    <div class="sticky">
      <span class="eyebrow">Anatomy of a statement</span>
      <h2>Every line, in plain English.</h2>
      <p class="lede">Once each charge has a name, it&rsquo;s much easier to judge whether it&rsquo;s fair. Here&rsquo;s how the typical lines split between genuine <strong>cost</strong> and provider <strong>margin</strong>.</p>
    </div>
    <ol class="numbered">{lines_html}</ol>
  </div>
</section>''' + savings + what_send + review


def build():
    return page("/switch/", TITLE, DESC, BODY, current="/switch/")
