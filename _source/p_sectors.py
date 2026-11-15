from common import *
from template import build_page
from p_solutions import R_ORCH, R_PAYOUT, R_MULTI, R_RISK, R_SETTLE, R_METHODS

IND = [("/industries/", "Industries")]

HR_NOTE = ("DPayments is an independent payments partner. We introduce merchants to regulated acquirers, PSPs and "
           "specialist partners that work with this sector. We only work with appropriately licensed businesses, "
           "and approval, pricing and reserves depend on each partner&rsquo;s underwriting.")

IGAMING = dict(
    path="/industries/igaming/", crumbs=IND, crumb="iGaming",
    title="iGaming Payment Solutions for Licensed Operators | DPayments",
    desc="Payment processing for licensed casino, sportsbook, lottery and gaming operators: deposits, fast payouts, multi-currency, orchestration and risk tools via specialist partners.",
    eyebrow="iGaming", cta_channel="online", cta_label="Talk to our gaming team",
    h1="Payments for licensed gaming operators.",
    lede="Gaming needs payment partners who understand the sector: fast deposits, faster withdrawals, multiple currencies and tight risk controls. We connect licensed operators with acquirers and PSPs that actively support gaming &mdash; and build in redundancy so you&rsquo;re never reliant on one.",
    points=["Casino, sportsbook, lottery &amp; competitions", "Fast deposits and card payouts", "Multi-acquirer resilience"],
    features_head=("What we arrange", "A payment stack built for gaming.", None),
    features=[
        ("card", "Player deposits", "Cards, wallets, open banking and local methods, with high approval rates on deposits."),
        ("receipt", "Fast withdrawals", "Card payouts and other push methods so players get winnings quickly &mdash; a big driver of loyalty."),
        ("refresh", "Orchestration &amp; routing", "Multiple acquirers behind one integration, with routing and failover to protect approval rates."),
        ("coins", "Multi-currency", "Accept and settle in the currencies of each market you&rsquo;re licensed in."),
        ("shield", "Risk &amp; responsible gaming", "Fraud screening, velocity limits and controls that support your compliance obligations."),
        ("sparkle", "Crypto options", "Crypto deposits and stablecoin settlement through partners, where your licence allows."),
    ],
    know_head=("What partners look for", "Getting approved in gaming."),
    know=[
        ("file", "A valid licence", "A gaming licence for each market you serve, such as UKGC, MGA or another recognised regulator."),
        ("users", "Strong KYC and AML", "Player verification, age checks and anti-money-laundering procedures that match your licence."),
        ("chart", "Clean history", "Processing statements and chargeback ratios, if you already take payments."),
    ],
    uses_head=("Who we work with", "Gaming verticals"),
    uses=[
        ("ticket", "Online casino", "Slots, table games and live casino."),
        ("chart", "Sportsbook", "Sports and esports betting."),
        ("sparkle", "Lottery &amp; competitions", "Prize draws and competition sites."),
        ("users", "Platforms &amp; affiliates", "B2B suppliers and platform providers."),
    ],
    faqs=[
        ("Do you work with unlicensed operators?", "No. Every partner we introduce requires a valid licence for the markets you operate in."),
        ("Why do gaming merchants need more than one acquirer?", "Acquirer appetite for gaming changes, and a single provider is a single point of failure. Orchestration across several providers protects your approval rates and keeps you trading."),
        ("Will there be a reserve?", "Often, especially for new operators. The size and duration depend on your history and the partner. We get it disclosed and negotiated up front."),
    ],
    note_text=HR_NOTE,
    related=[R_ORCH, R_PAYOUT, R_MULTI],
    cta=("Licensed operator looking for payment partners?", "Tell us your licences, markets and volumes. We&rsquo;ll come back with the partners most likely to support you."),
)

FOREX = dict(
    path="/industries/forex/", crumbs=IND, crumb="Forex &amp; CFD",
    title="Forex & CFD Broker Payment Solutions | DPayments",
    desc="Client deposits and withdrawals for regulated forex and CFD brokers: cards, open banking, card payouts, multi-currency settlement and orchestration via specialist partners.",
    eyebrow="Forex &amp; CFD", cta_channel="online", cta_label="Talk to us",
    h1="Fund accounts fast. Pay withdrawals faster.",
    lede="Traders expect to fund accounts instantly and withdraw without friction. We connect regulated forex and CFD brokers with payment partners that understand trading flows, chargeback risk and the compliance that comes with them.",
    points=["Instant client deposits", "Card payouts for withdrawals", "Multi-currency settlement"],
    features_head=("What we arrange", "Payment flows built for brokers.", None),
    features=[
        ("card", "Client deposits", "Cards, wallets and open banking with high approval rates and 3DS2."),
        ("receipt", "Withdrawals", "Card payouts and bank transfers back to the original funding source."),
        ("coins", "Multi-currency", "Accept deposits in clients&rsquo; currencies and settle where you need funds."),
        ("refresh", "Orchestration", "Several acquirers and PSPs behind one integration for resilience and better approvals."),
        ("shield", "Risk controls", "Fraud screening and chargeback prevention tuned for trading."),
        ("chart", "Reconciliation", "Reporting that ties deposits and withdrawals back to client accounts."),
    ],
    know_head=("What partners look for", "Getting approved as a broker."),
    know=[
        ("file", "Regulation", "Authorisation from a recognised regulator such as the FCA, CySEC or another major authority."),
        ("users", "KYC &amp; AML", "Robust client onboarding, source-of-funds checks and AML procedures."),
        ("chart", "Processing history", "Volumes, chargeback ratios and refund patterns if you already take payments."),
    ],
    faqs=[
        ("Can withdrawals go back to cards?", "Yes. Card payouts let you return funds to the card a client deposited with, which is often required for AML reasons."),
        ("Do you work with offshore brokers?", "We work with brokers regulated in recognised jurisdictions. Partner appetite varies, so tell us where you&rsquo;re licensed."),
    ],
    note_text=HR_NOTE,
    related=[R_PAYOUT, R_ORCH, R_SETTLE],
)

BROKER = dict(
    path="/industries/financial-brokerage/", crumbs=IND, crumb="Financial brokerage",
    title="Payment Solutions for Financial Brokerage & Investment Platforms | DPayments",
    desc="Secure payment acceptance and payouts for investment platforms, wealth managers and financial brokers. Open banking, cards, payouts and multi-currency via specialist partners.",
    eyebrow="Financial brokerage", cta_channel="online", cta_label="Talk to us",
    h1="Secure payments for financial platforms.",
    lede="Investment platforms, wealth apps and brokers handle larger sums and stricter compliance than most merchants. We help you find payment partners that support financial services and offer the methods your clients trust.",
    points=["Open banking for larger sums", "Cards and wallets", "Payouts and multi-currency"],
    features_head=("What we arrange", "Built for financial services.", None),
    features=[
        ("bank", "Open banking", "Fund accounts straight from the client&rsquo;s bank &mdash; ideal for larger amounts with no card chargebacks."),
        ("card", "Card funding", "Cards and wallets for convenient top-ups, with strong authentication."),
        ("receipt", "Payouts", "Return funds by card payout or bank transfer, quickly and traceably."),
        ("coins", "Multi-currency", "Support clients across markets with local currencies and settlement."),
        ("shield", "Compliance-ready", "Partners experienced with financial-services KYC, AML and audit needs."),
        ("plug", "Platform integration", "APIs and hosted options that fit your onboarding and account systems."),
    ],
    faqs=[
        ("Why open banking for investments?", "It suits larger payments: lower costs than cards on big amounts, instant confirmation and no card-style chargebacks."),
        ("Do partners work with new platforms?", "Some do, depending on your regulatory status, ownership and business plan. We&rsquo;ll tell you who is likely to support you."),
    ],
    note_text=HR_NOTE,
    related=[R_METHODS, R_PAYOUT, R_RISK],
)

PARTNERS = dict(
    path="/partners/", crumbs=[], crumb="Partner with us", current="/partners/",
    title="Partner with DPayments | Referral & Reseller Partnerships",
    desc="Accountants, ePOS and software providers, web agencies and consultants: refer clients to DPayments and earn a share. Simple referral and reseller partnerships.",
    eyebrow="Partner with us", cta_label="Become a partner", secondary_label="Who it&rsquo;s for",
    h1="Grow with us. Refer clients who take payments.",
    lede="If your clients take card payments, you can help them pay less and get set up properly &mdash; and earn from it. We handle the comparison, onboarding and support. You keep the relationship.",
    points=["Commission on referrals", "We do the legwork", "Your clients stay yours"],
    features_head=("Who partners with us", "Built for people who advise businesses.", None),
    features=[
        ("file", "Accountants &amp; bookkeepers", "Spot overpriced processing in your clients&rsquo; books and refer them for a free review."),
        ("store", "ePOS &amp; software providers", "Offer integrated payments alongside your product."),
        ("globe", "Web &amp; ecommerce agencies", "Get your clients&rsquo; checkouts live with the right gateway."),
        ("briefcase", "Consultants &amp; introducers", "Earn on introductions across retail, hospitality, ecommerce and specialist sectors."),
        ("users", "Trade associations", "Member benefits that save businesses money."),
        ("sparkle", "Gaming &amp; fintech networks", "Introduce operators and platforms to specialist payment partners."),
    ],
    steps_head=("How it works", "Simple from first referral.", None),
    steps=[
        ("Apply", "Tell us about you and your clients. We&rsquo;ll agree a simple partner arrangement."),
        ("Refer", "Send introductions by email or a referral form. We contact them promptly."),
        ("We do the work", "Statement reviews, comparisons, onboarding and ongoing support."),
        ("You earn", "Commission on clients who sign, as agreed in your partner terms."),
    ],
    note=False,
    cta=("Interested in partnering?", "Tell us who you work with and we&rsquo;ll send over partner details by email."),
)


def build_all():
    return {
        "industries/igaming/index.html": build_page(IGAMING),
        "industries/forex/index.html": build_page(FOREX),
        "industries/financial-brokerage/index.html": build_page(BROKER),
        "partners/index.html": build_page(PARTNERS),
    }
