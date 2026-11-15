from common import *
from template import build_page
from p_solutions import R_SETTLE, R_ORCH, R_PAYOUT

CHECK = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12.5l4.5 4.5L19 7.5"/></svg>'

ASSETS = ["USDT", "USDC", "ETH", "BNB", "TRX", "TRC20", "ERC20", "BEP20"]

HERO_ART = f'''<div class="crypto-art" aria-hidden="true">
  <div class="cx-card">
    <div class="cx-top"><span class="cx-dot"></span><small>Crypto checkout</small></div>
    <b class="cx-amt">250.00 <em>USDT</em></b>
    <div class="cx-net"><span class="on">TRC20</span><span>ERC20</span><span>BEP20</span></div>
    <div class="cx-qr">{"".join('<i></i>' if (i * 7 + i // 5) % 3 else '<i class="f"></i>' for i in range(49))}</div>
    <div class="cx-status"><span class="spin"></span> Awaiting confirmation</div>
  </div>
  <span class="mchip cx-f1">USDC</span><span class="mchip cx-f2">ETH</span><span class="mchip cx-f3">{CHECK} Settled</span>
</div>'''


def form():
    inds = ["iGaming / casino", "Sports betting", "Digital goods", "Other high-risk", "Other"]
    vols = ["Under &pound;50k", "&pound;50k &ndash; &pound;250k", "&pound;250k &ndash; &pound;1m", "Over &pound;1m"]
    return f'''<form class="form-card" action="/send.php" method="post">
  <div class="form-alert error" data-form-alert hidden role="alert"></div>
  <input type="hidden" name="source" value="crypto">
  <div class="hp" aria-hidden="true"><label for="website-hp">Leave this field empty</label><input type="text" id="website-hp" name="website" tabindex="-1" autocomplete="off"></div>
  <div class="form-row two">
    <div><label for="c-name">Full name <span class="req">*</span></label><input type="text" id="c-name" name="name" required autocomplete="name" maxlength="120"></div>
    <div><label for="c-email">Work email <span class="req">*</span></label><input type="email" id="c-email" name="email" required autocomplete="email" maxlength="160"></div>
  </div>
  <div class="form-row two">
    <div><label for="c-company">Company name <span class="req">*</span></label><input type="text" id="c-company" name="business" required autocomplete="organization" maxlength="160"></div>
    <div><label for="c-site">Website <span class="opt">(optional)</span></label><input type="text" id="c-site" name="site" maxlength="200" placeholder="https://"></div>
  </div>
  <div class="form-row two">
    <div><label for="c-ind">Industry</label><select id="c-ind" name="industry"><option value="">Choose one</option>{"".join(f"<option>{i}</option>" for i in inds)}</select></div>
    <div><label for="c-vol">Expected monthly volume</label><select id="c-vol" name="turnover"><option value="">Choose a range</option>{"".join(f"<option>{v}</option>" for v in vols)}</select></div>
  </div>
  <div class="form-row"><label for="c-notes">Anything else we should know? <span class="opt">(optional)</span></label><textarea id="c-notes" name="message" maxlength="4000" placeholder="e.g. markets, licences, chains or tokens you need"></textarea></div>
  <button class="btn btn-primary" type="submit">Submit application {ARROW}</button>
  <p class="form-note">We&rsquo;ll reply by email. Prefer to write? <a href="mailto:{EMAIL}?subject=Crypto%20payments">{EMAIL}</a></p>
</form>'''


EXTRA = f'''<section id="pricing" style="scroll-margin-top:90px">
  <div class="container split v-center">
    <div>
      <span class="eyebrow">Pricing</span>
      <h2>Pricing that scales with you.</h2>
      <p class="lede">Fees are tailored to your monthly volume &mdash; the more you process, the lower your rate. Tell us your expected volume and we&rsquo;ll come back with the tiers that apply to you.</p>
    </div>
    <div class="vol-bars reveal" aria-hidden="true">
      <div class="vb"><span style="height:90%"></span><small>Starter</small></div>
      <div class="vb"><span style="height:66%"></span><small>Growth</small></div>
      <div class="vb"><span style="height:42%"></span><small>Scale</small></div>
      <div class="vb"><span style="height:26%"></span><small>Custom</small></div>
      <em>Fee % falls as volume grows</em>
    </div>
  </div>
</section>
<section id="apply" class="section-white" style="scroll-margin-top:90px">
  <div class="container split">
    <div class="sticky">
      <span class="eyebrow">Apply</span>
      <h2>Apply for a crypto merchant account.</h2>
      <p class="lede">Share a few details about your business and expected volume. We&rsquo;ll match you with a suitable licensed gateway partner and guide you through onboarding.</p>
      {ticks(["No obligation", "Reply by email", "Help with KYB paperwork"])}
    </div>
    <div>{form()}</div>
  </div>
</section>'''

CRYPTO = dict(
    path="/crypto/", crumbs=[], crumb="Crypto payments", current="/crypto/",
    title="Crypto Payments for iGaming & High-Risk Merchants | DPayments",
    desc="Accept USDT, USDC, ETH, BNB and TRX across TRC20, ERC20 and BEP20. Real-time settlement, API collections and payouts, through licensed gateway partners. Apply with DPayments.",
    eyebrow="Crypto payments", cta_label="Start your application", secondary_label="See features",
    h1="Accept crypto. Settle fast. Grow without limits.",
    lede="One gateway for stablecoins and major tokens across popular chains, with API-driven collections and payouts &mdash; backed by a UK team.",
    points=["USDT, USDC, ETH, BNB, TRX", "TRC20, ERC20, BEP20", "Collections and payouts by API"],
    features_head=("Features", "Built for merchants other providers turn away.", "Ideal for iGaming, betting, digital goods and other high-risk sectors."),
    features=[
        ("coins", "More ways to pay", "Stablecoins and major tokens on the most popular chains, so customers pay with what they already hold."),
        ("clock", "Real-time settlement", "Funds settle as payments confirm, with no mandatory holding periods."),
        ("plug", "API automation", "Run collections, transaction tracking and payouts straight from your own platform."),
        ("shield", "USDT freeze-risk protection", "Screening and controls designed to help keep your business funds safe."),
        ("chart", "No maximum limits", "No cap on deposit or withdrawal size."),
        ("users", "24/7 processing &amp; support", "Payments run around the clock, with support when you need it."),
    ],
    steps_head=("How it works", "Live in three steps.", None),
    steps=[
        ("Apply", "Share your business details and expected volume. We match you with a licensed gateway partner."),
        ("Onboard", "We help you through the partner&rsquo;s KYB checks, with pricing agreed on your monthly volume."),
        ("Go live", "Connect by API or use hosted payment links &mdash; with help if you don&rsquo;t have a platform yet."),
    ],
    extra_html=EXTRA,
    faqs=[
        ("Which coins and networks are supported?", "USDT, USDC, ETH, BNB and TRX across TRC20, ERC20 and BEP20. Ask us if you need others."),
        ("Does DPayments hold my funds?", "No. DPayments acts as an introducer only. You contract directly with the payment provider, and we never hold, receive or transfer client funds."),
        ("Can I also take card payments?", "Yes. Many merchants combine crypto with cards, wallets and open banking. See our <a href=\"/industries/igaming/\">iGaming</a> and <a href=\"/solutions/\">solutions</a> pages."),
    ],
    note_text=("DPayments acts as an introducer only. Crypto payment services are provided by our licensed gateway partners, and merchants contract directly with the payment provider. "
               "DPayments does not hold, receive or transfer client funds. Cryptoassets are high risk and unregulated in some jurisdictions; their value can go down as well as up."),
    related=[R_SETTLE, R_ORCH, R_PAYOUT],
    cta=("Ready to accept crypto?", "Apply in a couple of minutes, or email us to talk it through."),
)


def build_all():
    html = build_page(CRYPTO)
    # put the checkout illustration beside the hero copy
    html = html.replace('<section class="page-hero">\n  <div class="container">',
                        '<section class="page-hero crypto-hero">\n  <div class="container hero-grid"><div>', 1)
    html = html.replace('</ul>\n  </div>\n</section>', '</ul>\n  </div>' + HERO_ART + '</div>\n</section>', 1)
    html = html.replace('<a class="btn btn-primary" href="/contact/">Start your application',
                        '<a class="btn btn-primary" href="#apply">Start your application', 1)
    chips = "".join(f'<span class="mchip">{a}</span>' for a in ASSETS)
    html = html.replace('<section class="section-white" id="features">',
                        f'<section class="section-tight" style="padding-top:0"><div class="container"><div class="strip center-strip">{chips}</div></div></section>\n<section class="section-white" id="features">', 1)
    return {"crypto/index.html": html}
