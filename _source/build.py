import os, sys
sys.path.insert(0, os.path.dirname(__file__))
import p_home, p_cards, p_online, p_switch, p_how, p_industries, p_faq, p_misc, p_solutions, p_sectors, p_crypto
from common import SITE

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")

pages = {
    "index.html": p_home.build(),
    "card-machines/index.html": p_cards.build(),
    "online-payments/index.html": p_online.build(),
    "switch/index.html": p_switch.build(),
    "how-it-works/index.html": p_how.build(),
    "industries/index.html": p_industries.build(),
    "faq/index.html": p_faq.build(),
    "contact/index.html": p_misc.contact(),
    "thank-you/index.html": p_misc.thank_you(),
    "privacy/index.html": p_misc.privacy(),
    "terms/index.html": p_misc.terms(),
    "cookies/index.html": p_misc.cookies(),
    "404.html": p_misc.not_found(),
}
pages.update(p_solutions.build_all())
pages.update(p_sectors.build_all())
pages.update(p_crypto.build_all())

for rel, html in pages.items():
    path = os.path.join(OUT, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)

urls = ["/" + k[:-10] if k.endswith("index.html") else None for k in pages]
urls = [u for u in urls if u and "thank-you" not in u]
with open(os.path.join(OUT, "sitemap.xml"), "w") as f:
    f.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n')
    for u in urls:
        f.write(f"  <url><loc>{SITE}{u}</loc></url>\n")
    f.write("</urlset>\n")

print("built", len(pages), "pages")
