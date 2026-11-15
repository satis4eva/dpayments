from common import *

TITLE = "How It Works | Four Steps to the Right Payments Setup | DPayments"
DESC = ("How DPayments works: we understand your business, compare acquirers, gateways and terminals, handle setup and "
        "onboarding, then keep an eye on your pricing. Honest timelines, no jargon.")

steps = [
    ("Understand the business", "We start with how you trade &mdash; not with a product.",
     ["How you take payments: in person, online, by phone or a mix", "Your typical card mix (debit, credit, Amex, business, international)", "Average transaction size and monthly turnover", "Your premises, staff and the software you already use", "Where you&rsquo;re growing over the next year or two"],
     "Nothing is recommended until we understand what you actually need."),
    ("Compare the market", "We weigh acquirers, gateways and terminals against your profile.",
     ["Transaction pricing: blended vs interchange-plus", "Hardware: rent, buy or bundled", "Contract length, auto-renewal and notice periods", "Minimum monthly charges, PCI fees and exit fees", "Settlement speed and any reserves"],
     "You get a recommendation with the reasoning shown &mdash; not a single take-it-or-leave-it quote."),
    ("Set up and onboard", "We handle the parts that usually slow businesses down.",
     ["Application and Know-Your-Customer (KYC) checks", "Terminal configuration, receipts, tipping and refund settings", "Online checkout, payment links or virtual terminal setup", "EPOS or platform integration", "PCI DSS self-assessment guidance"],
     "The goal is for going live to be the easy part."),
    ("Stay on it", "Payments aren&rsquo;t set-and-forget. We keep watching.",
     ["Periodic check-ins on pricing and statements", "Help with new sites, extra terminals or new channels", "Support with chargebacks and disputes", "A heads-up before contract renewal dates", "We&rsquo;ll tell you if a better option appears"],
     "You have someone on your side long after the paperwork is done."),
]
steps_html = "".join(
    f'''<div class="step reveal"><div class="n"></div><div><h3>{t}</h3><p><strong>{s}</strong></p>{ticks(items)}<p class="mt-m">{note}</p></div></div>'''
    for t, s, items, note in steps)

docs = f'''<section class="section-white">
  <div class="container split">
    <div class="sticky">
      <span class="eyebrow">How long does it take?</span>
      <h2>A straight answer: it depends on underwriting.</h2>
      <p class="lede">We won&rsquo;t promise &ldquo;live in 24 hours&rdquo;. Setup is quick for a straightforward business with documents ready, and takes longer when more due diligence is needed. We&rsquo;ll give you a realistic timeframe before you commit.</p>
      <div class="callout mt-m"><p>The biggest factor in your control is having your documents ready. Here&rsquo;s what providers typically ask for.</p></div>
    </div>
    <div class="grid g2">
      <div class="card reveal">{icon("users")}<h4>Identity</h4><p>Photo ID and proof of address for directors, owners and anyone with significant control.</p></div>
      <div class="card reveal">{icon("briefcase")}<h4>Business details</h4><p>Company number or sole-trader details, trading address, what you sell and how.</p></div>
      <div class="card reveal">{icon("bank")}<h4>Bank account</h4><p>The business account where settlements will be paid, plus recent bank statements.</p></div>
      <div class="card reveal">{icon("file")}<h4>Processing history</h4><p>If you already take cards, recent merchant statements help underwriting move faster.</p></div>
      <div class="card reveal">{icon("globe")}<h4>Website</h4><p>For online payments: a live site with terms, refund policy, privacy policy and contact details.</p></div>
      <div class="card reveal">{icon("chart")}<h4>Expected volumes</h4><p>Estimated monthly card turnover and average transaction value.</p></div>
    </div>
  </div>
</section>'''

promises = f'''<section>
  <div class="container">
    <div class="section-head center">
      <span class="eyebrow">How we work</span>
      <h2>What you can expect from us.</h2>
    </div>
    <div class="grid g4">
      <div class="card reveal">{icon("mail")}<h4>Email first</h4><p>We reply by email. No phone tag, and no call unless you&rsquo;d like one.</p></div>
      <div class="card reveal">{icon("eye")}<h4>Reasoning shown</h4><p>Every recommendation explains why &mdash; including the trade-offs.</p></div>
      <div class="card reveal">{icon("file")}<h4>Terms up front</h4><p>Contract length, rental and exit fees spelled out before you sign.</p></div>
      <div class="card reveal">{icon("check")}<h4>No obligation</h4><p>If we can&rsquo;t improve on what you have, we&rsquo;ll tell you.</p></div>
    </div>
  </div>
</section>'''

BODY = f'''<section class="page-hero">
  <div class="container">
    <div class="crumbs"><a href="/">Home</a> / How it works</div>
    <span class="eyebrow">The process, plainly</span>
    <h1>Four steps, and honest timelines.</h1>
    <p class="lede">No jargon and no promises we can&rsquo;t keep. Here&rsquo;s exactly what happens when you work with DPayments, and a straight answer on timing.</p>
    <div class="btn-row"><a class="btn btn-primary" href="/contact/">Get a quote {ARROW}</a></div>
  </div>
</section>
<section class="section-tight" style="padding-top:0">
  <div class="container narrow" style="max-width:900px">
    <div class="steps">{steps_html}</div>
  </div>
</section>''' + docs + promises + cta_band()


def build():
    return page("/how-it-works/", TITLE, DESC, BODY, current="/how-it-works/")
