from common import *
from forms import quote_form

# ---------- Contact ----------
def contact():
    body = f'''<section class="page-hero" style="padding-bottom:96px">
  <div class="container split">
    <div class="sticky">
      <div class="crumbs"><a href="/">Home</a> / Get a quote</div>
      <span class="eyebrow">Get a quote</span>
      <h1>Tell us how you take payments.</h1>
      <p class="lede">One short form is all it takes. We&rsquo;ll come back by email with a tailored quote &mdash; whether you&rsquo;re setting up for the first time or reviewing what you already run.</p>
      <h3 class="mt-l">What happens next</h3>
      <ol class="numbered">
        <li><div><h4>We read your enquiry</h4><p>A real person reads what you send and works out what you actually need &mdash; not which product to push.</p></div></li>
        <li><div><h4>We come back by email</h4><p>With questions or a tailored quote. No phone tag, and no call unless you&rsquo;d like one.</p></div></li>
        <li><div><h4>You decide, in your time</h4><p>You get a clear recommendation with the reasoning shown. No obligation and no pressure to sign.</p></div></li>
      </ol>
      <div class="callout mt-m"><p><strong>Prefer email?</strong> Write to <a href="mailto:{EMAIL}">{EMAIL}</a> &mdash; tell us what you sell, how customers pay and roughly what you take by card each month.</p></div>
    </div>
    <div>
      <p class="muted" style="font-size:.92rem">Request a quote. Required fields are marked <span class="req">*</span>.</p>
      {quote_form("contact")}
    </div>
  </div>
</section>'''
    return page("/contact/", "Get a Quote | DPayments", "Request a tailored card payments quote or a review of what you pay today. One short form, a reply by email, no pressure.", body, current="/contact/")


def thank_you():
    body = f'''<section class="page-hero" style="padding:120px 0">
  <div class="container narrow center" style="max-width:720px">
    <div class="icon" style="margin:0 auto 24px;width:64px;height:64px;border-radius:18px">{icon("check", None)}</div>
    <h1>Thanks &mdash; we&rsquo;ve got it.</h1>
    <p class="lede" style="margin:0 auto 32px">Your enquiry is with us. A real person will read it and reply by email. If you have a recent merchant statement, keep it handy &mdash; we may ask for it.</p>
    <div class="btn-row" style="justify-content:center"><a class="btn btn-primary" href="/">Back to home</a><a class="btn btn-ghost" href="/faq/">Read the FAQ</a></div>
  </div>
</section>'''
    html = page("/thank-you/", "Thank you | DPayments", "Thanks for your enquiry. We'll reply by email.", body)
    return html.replace('<meta name="description"', '<meta name="robots" content="noindex">\n<meta name="description"', 1)


def not_found():
    body = f'''<section class="page-hero" style="padding:120px 0">
  <div class="container narrow center" style="max-width:720px">
    <span class="eyebrow">Error 404</span>
    <h1>That page has settled elsewhere.</h1>
    <p class="lede" style="margin:0 auto 32px">We couldn&rsquo;t find the page you were looking for. Try one of these instead.</p>
    <div class="strip" style="justify-content:center">
      <a class="pill" href="/">Home</a><a class="pill" href="/card-machines/">Card machines</a><a class="pill" href="/online-payments/">Online payments</a><a class="pill" href="/switch/">Switch &amp; save</a><a class="pill" href="/faq/">FAQ</a><a class="pill" href="/contact/">Get a quote</a>
    </div>
  </div>
</section>'''
    html = page("/404.html", "Page not found | DPayments", "Page not found.", body)
    return html.replace('<meta name="description"', '<meta name="robots" content="noindex">\n<meta name="description"', 1)


# ---------- Legal ----------
def legal(path, title, h1, sections, desc):
    body = f'''<section class="page-hero" style="padding-bottom:32px">
  <div class="container narrow" style="max-width:820px">
    <div class="crumbs"><a href="/">Home</a> / {h1}</div>
    <h1>{h1}</h1>
    <p class="updated muted">Effective 25 July 2026</p>
  </div>
</section>
<section style="padding-top:0">
  <div class="container narrow prose" style="max-width:820px">
    {sections}
  </div>
</section>'''
    return page(path, title, desc, body)


PRIVACY = f'''
<p>This notice explains how DPayments handles the information you share with us through dpayments.co.uk. We aim to collect as little as possible and to be clear about how we use it.</p>
<h2>Who we are</h2>
<p>DPayments operates this website and provides payments consultancy and setup services for UK businesses. You can contact us about anything in this notice at <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>
<h2>What we collect</h2>
<p>We only collect information you choose to give us, mainly when you send an enquiry or request a quote:</p>
<ul>
<li>Your name and email address</li>
<li>Your business name, phone number, type of business and approximate card turnover, if you provide them</li>
<li>How your business takes payments and what you&rsquo;d like a quote for</li>
<li>Anything you include in your message, or in documents (such as merchant statements) you send us by email</li>
</ul>
<p>We never ask for card numbers or payment credentials through this site. Please don&rsquo;t send them to us by email.</p>
<h2>Why we use it</h2>
<p>We use your information to respond to your enquiry, prepare a quote or statement review, and continue the conversation you started with us.</p>
<h2>Our lawful basis</h2>
<p>Under UK GDPR, we rely on our legitimate interest in responding to enquiries about our services. Where relevant, we also process your information to take steps at your request before entering into a contract.</p>
<h2>Who we share it with</h2>
<p>We use trusted third-party providers for website hosting, storing enquiry details and delivering email. They process data on our behalf, under contract, and only as needed to provide their service. If you ask us to arrange a payments service for you, we will share relevant details with the provider(s) you choose, with your agreement.</p>
<h2>How long we keep it</h2>
<p>We keep enquiry information only for as long as we need it to handle your enquiry and for a reasonable period afterwards, then delete it. You can ask us to delete it sooner.</p>
<h2>Cookies</h2>
<p>See our <a href="/cookies/">cookie policy</a>. In short, we only use strictly necessary cookies.</p>
<h2>Your rights</h2>
<p>You can ask to access, correct, delete or restrict your personal data, and you can object to certain processing. Email <a href="mailto:{EMAIL}">{EMAIL}</a>. If you&rsquo;re unhappy with how we&rsquo;ve handled your data, you can complain to the Information Commissioner&rsquo;s Office at <a href="https://ico.org.uk" rel="noopener">ico.org.uk</a>.</p>
<h2>Changes to this notice</h2>
<p>We may update this notice from time to time. The effective date at the top shows when it last changed.</p>
'''

TERMS = f'''
<p>These terms apply to your use of dpayments.co.uk, operated by DPayments. By using the site you agree to them.</p>
<h2>About this website</h2>
<p>This site provides general information about DPayments&rsquo; payments consultancy and setup services. It&rsquo;s a starting point for a conversation &mdash; not a binding offer, and not financial, legal or tax advice. Any quote or recommendation we give you will be provided separately, in writing, on its own terms.</p>
<h2>Information is general</h2>
<p>We work to keep the content accurate and current, but it isn&rsquo;t advice for your particular situation. Examples of fees, timings and industries are illustrative and are not guarantees about your account. Pricing, features and approval always depend on the provider and on underwriting.</p>
<h2>Acceptable use</h2>
<p>You must not use the site unlawfully or fraudulently, attempt to gain unauthorised access to the site or its systems, or disrupt the site or misuse the enquiry form (for example, by sending spam).</p>
<h2>Intellectual property</h2>
<p>The content, branding and design of this site belong to DPayments. You may view and share it for your own reference, but you may not reuse it commercially without our permission.</p>
<h2>Links to other sites</h2>
<p>Links to third-party sites are provided for convenience. We don&rsquo;t control those sites and aren&rsquo;t responsible for their content.</p>
<h2>Liability</h2>
<p>To the extent permitted by law, DPayments is not liable for any loss arising from your use of, or reliance on, this website. Nothing in these terms limits liability that cannot legally be limited.</p>
<h2>Governing law</h2>
<p>These terms are governed by the laws of England and Wales, and the courts of England and Wales have exclusive jurisdiction.</p>
<h2>Contact</h2>
<p>Questions about these terms: <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>
'''

COOKIES = f'''
<div class="callout"><p><strong>The short version:</strong> we don&rsquo;t currently set any advertising or analytics cookies, and we don&rsquo;t track you across other websites. If that changes, we&rsquo;ll update this policy and ask for your consent where the law requires it.</p></div>
<h2>What cookies are</h2>
<p>Cookies are small text files a website stores on your device. They can help a site work, remember your preferences or measure how it&rsquo;s used.</p>
<h2>What we use</h2>
<p>We only use strictly necessary cookies that keep the site secure and working properly. These are essential and don&rsquo;t require consent under UK rules. We do not use analytics, advertising or social-media tracking cookies. Our pages load fonts from Google Fonts, which may receive your IP address when your browser requests them; no cookies are set for this.</p>
<h2>Managing cookies</h2>
<p>You can delete or block cookies through your browser settings. Because we don&rsquo;t use non-essential cookies, blocking them won&rsquo;t stop you reading the site or sending an enquiry.</p>
<h2>Contact</h2>
<p>Questions about cookies: <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>
'''


def privacy():
    return legal("/privacy/", "Privacy Notice | DPayments", "Privacy notice", PRIVACY, "How DPayments handles the information you share through dpayments.co.uk.")


def terms():
    return legal("/terms/", "Terms of Use | DPayments", "Terms of use", TERMS, "Terms of use for dpayments.co.uk.")


def cookies():
    return legal("/cookies/", "Cookie Policy | DPayments", "Cookie policy", COOKIES, "Cookies used on dpayments.co.uk.")
