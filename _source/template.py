"""Generic data-driven page template for solution and industry pages."""
import json, re
from common import *

PARTNER_NOTE = ("DPayments is an independent payments partner. We arrange these services through regulated "
                "acquirers, payment service providers and specialist partners; availability, pricing and approval "
                "depend on your business, sector and the partner&rsquo;s underwriting.")


def _strip(s):
    return (re.sub(r"<[^>]+>", "", s).replace("&rsquo;", "’").replace("&mdash;", "—")
            .replace("&amp;", "&").replace("&ndash;", "–"))


def build_page(d):
    """d keys: path, title, desc, crumbs[(href,label)], eyebrow, h1, lede, cta_channel,
    features_head(eyebrow,h2,lede), features[(icon,title,text)],
    steps_head(eyebrow,h2,lede), steps[(title,text)],
    know_head(eyebrow,h2), know[(icon,title,text)],
    uses_head(h2), uses[(icon,title,text)],
    extra_html, faqs[(q,a)], related[(href,icon,title,text)], cta(title,text), current, note"""
    crumbs = " / ".join([f'<a href="{h}">{l}</a>' for h, l in d.get("crumbs", [])] + [d.get("crumb", d["eyebrow"])])
    chan = d.get("cta_channel")
    qhref = "/contact/" + (f"?channel={chan}" if chan else "")
    out = f'''<section class="page-hero">
  <div class="container">
    <div class="crumbs"><a href="/">Home</a> / {crumbs}</div>
    <span class="eyebrow">{d["eyebrow"]}</span>
    <h1 style="max-width:900px">{d["h1"]}</h1>
    <p class="lede">{d["lede"]}</p>
    <div class="btn-row">
      <a class="btn btn-primary" href="{qhref}">{d.get("cta_label", "Talk to us")} {ARROW}</a>
      <a class="btn btn-ghost" href="#features">{d.get("secondary_label", "See what&rsquo;s included")}</a>
    </div>
    {('<ul class="hero-points">' + "".join(f"<li>{TICK} {p}</li>" for p in d["points"]) + "</ul>") if d.get("points") else ""}
  </div>
</section>'''

    if d.get("features"):
        e, h, l = d["features_head"]
        cols = d.get("features_cols", "g3")
        cards = "".join(f'<div class="card reveal">{icon(i)}<h3>{t}</h3><p>{x}</p></div>' for i, t, x in d["features"])
        out += f'''<section class="section-white" id="features">
  <div class="container">
    <div class="section-head"><span class="eyebrow">{e}</span><h2>{h}</h2>{f'<p class="lede">{l}</p>' if l else ""}</div>
    <div class="grid {cols}">{cards}</div>
  </div>
</section>'''

    if d.get("steps"):
        e, h, l = d["steps_head"]
        steps = "".join(f'<div class="step reveal"><div class="n"></div><div><h3>{t}</h3><p>{x}</p></div></div>' for t, x in d["steps"])
        out += f'''<section>
  <div class="container split">
    <div class="sticky"><span class="eyebrow">{e}</span><h2>{h}</h2>{f'<p class="lede">{l}</p>' if l else ""}</div>
    <div class="steps">{steps}</div>
  </div>
</section>'''

    if d.get("know"):
        e, h = d["know_head"]
        cards = "".join(f'<div class="card reveal">{icon(i)}<h3>{t}</h3><p>{x}</p></div>' for i, t, x in d["know"])
        cols = "g3" if len(d["know"]) % 3 == 0 else "g2"
        out += f'''<section class="section-dark">
  <div class="container">
    <div class="section-head"><span class="eyebrow">{e}</span><h2>{h}</h2></div>
    <div class="grid {cols}">{cards}</div>
  </div>
</section>'''

    out += d.get("extra_html", "")

    if d.get("uses"):
        cards = "".join(f'<div class="card reveal">{icon(i)}<h4>{t}</h4><p>{x}</p></div>' for i, t, x in d["uses"])
        out += f'''<section class="section-white">
  <div class="container">
    <div class="section-head"><span class="eyebrow">{d["uses_head"][0]}</span><h2>{d["uses_head"][1]}</h2></div>
    <div class="grid g4">{cards}</div>
  </div>
</section>'''

    schema = ""
    if d.get("faqs"):
        faqs = "".join(f'<details class="faq"><summary>{q}</summary><div class="answer"><p>{a}</p></div></details>' for q, a in d["faqs"])
        out += f'''<section>
  <div class="container split">
    <div class="sticky"><span class="eyebrow">Questions</span><h2>Good to know.</h2>
      <p class="lede">More answers in our <a href="/faq/">full FAQ</a>, or just ask us.</p></div>
    <div>{faqs}</div>
  </div>
</section>'''
        schema = '<script type="application/ld+json">' + json.dumps({
            "@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
                {"@type": "Question", "name": _strip(q), "acceptedAnswer": {"@type": "Answer", "text": _strip(a)}}
                for q, a in d["faqs"]]}, ensure_ascii=False) + "</script>"

    if d.get("note", True):
        out += f'''<section class="section-tight" style="padding-top:0">
  <div class="container"><div class="callout"><p>{d.get("note_text", PARTNER_NOTE)}</p></div></div>
</section>'''

    if d.get("related"):
        cards = "".join(f'<a class="card reveal" href="{h}">{icon(i)}<h4>{t}</h4><p>{x}</p><span class="more">Learn more {ARROW}</span></a>'
                        for h, i, t, x in d["related"])
        out += f'''<section class="section-white section-tight">
  <div class="container">
    <div class="section-head"><span class="eyebrow">Related</span><h2>Works well with</h2></div>
    <div class="grid g3">{cards}</div>
  </div>
</section>'''

    t, x = d.get("cta", ("Tell us how you take payments. We&rsquo;ll do the rest.",
                         "Send a few details and we&rsquo;ll come back by email with a tailored recommendation."))
    out += cta_band(t, x)
    return page(d["path"], d["title"], d["desc"], out, current=d.get("current", d["path"]), schema=schema)
