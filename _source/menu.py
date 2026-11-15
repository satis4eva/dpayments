from common import icon

CRYPTO_URL = "https://crypto.dpayments.co.uk"

MENU_SOLUTIONS = [
    ("Accept payments", [
        ("/card-machines/", "terminal", "POS &amp; card machines", "Countertop, portable, 4G and unattended"),
        ("/online-payments/", "globe", "Online payment gateway", "Checkout, links and recurring billing"),
        ("/online-payments/#virtual-terminal", "phone", "Phone payments (MOTO)", "Virtual terminal and pay-by-link"),
        ("/solutions/payment-methods/", "card", "Payment methods", "Cards, wallets, PayPal, pay later and more"),
        ("/solutions/multi-currency/", "coins", "Multi-currency &amp; DCC", "Price and accept in customers&rsquo; currencies"),
    ]),
    ("Move money", [
        ("/solutions/settlements/", "bank", "Settlements", "Multi-currency payouts to your accounts"),
        ("/solutions/settlements/#stablecoin", "sparkle", "Stablecoin settlements", "Faster cross-border settlement via partners"),
        ("/solutions/card-payouts/", "receipt", "Card payouts", "Send funds straight to customers&rsquo; cards"),
        ("/switch/", "search", "Switch &amp; save", "Free line-by-line statement review"),
    ]),
    ("Optimise &amp; protect", [
        ("/solutions/orchestration/", "refresh", "Payment orchestration", "Smart routing across multiple providers"),
        ("/solutions/risk-fraud/", "shield", "Risk, fraud &amp; security", "Screening, 3DS2, PCI and P2PE"),
        ("/solutions/risk-fraud/#network-tokens", "lock", "Network tokens", "Scheme tokens instead of raw card numbers"),
        ("/solutions/integration/", "plug", "Integration", "Plugins, hosted pages and APIs"),
    ]),
    ("Beyond payments", [
        ("/solutions/epos/", "store", "ePOS systems", "Tills for retail and hospitality, linked to payments"),
        ("/solutions/loyalty/", "heart", "Loyalty &amp; smart receipts", "Bring customers back"),
        ("/solutions/business-funding/", "chart", "Business funding", "Cash advance repaid from card sales"),
        ("/solutions/digital-wallets/", "wallet", "Apple Pay &amp; Click to Pay", "One-tap checkout"),
        ("/solutions/", "sparkle", "All solutions", "See everything we can arrange"),
    ]),
]

MENU_INDUSTRIES = [
    ("Everyday commerce", [
        ("/industries/#retail", "store", "Retail", "Shops and multi-site retail"),
        ("/industries/#hospitality", "cup", "Restaurants &amp; bars", "Pay-at-table, tips and EPOS"),
        ("/industries/#hotels", "users", "Hotels &amp; hospitality", "Pre-auths, deposits and bookings"),
        ("/industries/#ecommerce", "cart", "Ecommerce", "Checkout that converts"),
        ("/industries/#trades", "tool", "Trades &amp; builders merchants", "On site and over the counter"),
        ("/industries/#automotive", "car", "Automotive", "Garages, servicing and dealers"),
    ]),
    ("Specialist sectors", [
        ("/industries/igaming/", "ticket", "iGaming", "Casino, sportsbook and gaming operators"),
        ("/industries/forex/", "chart", "Forex &amp; CFD", "Deposits and withdrawals for brokers"),
        ("/industries/financial-brokerage/", "briefcase", "Financial brokerage", "Investment and trading platforms"),
        ("/industries/#competitions", "sparkle", "Online competitions", "Prize draws and competition sites"),
        ("/industries/#professional", "file", "Law firms &amp; professional", "Client account and invoice payments"),
        ("/industries/", "globe", "All industries", "Every sector we work with"),
    ]),
]

MENU_COMPANY = [
    ("Company", [
        ("/how-it-works/", "clipboard", "How it works", "Four steps, honest timelines"),
        ("/faq/", "file", "FAQ", "Merchant services, explained"),
        ("/partners/", "users", "Partner with us", "Referral and reseller partnerships"),
        ("/contact/", "mail", "Get a quote", "One short form, reply by email"),
    ]),
]

CUR = ' aria-current="page"'
CHEV = ('<svg class="chev" viewBox="0 0 12 12" aria-hidden="true"><path d="M3 4.5l3 3 3-3" fill="none" '
        'stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></svg>')


def menu(label, cols, current, key):
    active = any(href.split("#")[0] == current for _, items in cols for href, *_ in items)
    colhtml = ""
    for title, items in cols:
        li = "".join(
            f'<li><a href="{href}"{CUR if href == current else ""}>{icon(ic, "mi")}'
            f'<span><b>{t}</b><small>{d}</small></span></a></li>'
            for href, ic, t, d in items)
        colhtml += f'<div class="mega-col"><h5>{title}</h5><ul>{li}</ul></div>'
    act = (" is-active" if active else "") + (" wide" if len(cols) >= 3 else "")
    return (f'<li class="has-menu{act}"><button class="menu-btn" type="button" aria-expanded="false" '
            f'aria-controls="m-{key}">{label}{CHEV}</button>'
            f'<div class="mega mega-{len(cols)}" id="m-{key}">{colhtml}</div></li>')
