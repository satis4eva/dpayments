# dpayments.co.uk

Static website for DPayments, plus a small PHP **website portal** at `/admin/` for editing pages and reading enquiries. It runs on any Hostinger shared hosting plan.

## Site map

- **Home** `/`
- **Solutions** `/solutions/`
  - Accept payments: `/card-machines/`, `/online-payments/` (gateway, links, MOTO, recurring), `/solutions/payment-methods/`, `/solutions/multi-currency/`, `/solutions/digital-wallets/`
  - Move money: `/solutions/settlements/` (including stablecoin), `/solutions/card-payouts/`, `/switch/`
  - Optimise and protect: `/solutions/orchestration/`, `/solutions/risk-fraud/` (including network tokens, PCI and P2PE), `/solutions/integration/`
  - Beyond payments: `/solutions/epos/`, `/solutions/loyalty/`, `/solutions/business-funding/`
- **Industries** `/industries/` (retail, hospitality, hotels, ecommerce, trades, automotive, garden centres, competitions, professional and law, events, memberships, travel) plus `/industries/igaming/`, `/industries/forex/` and `/industries/financial-brokerage/`
- **Crypto** links to https://crypto.dpayments.co.uk
- **Company**: `/how-it-works/`, `/faq/`, `/partners/`, `/contact/`
- Legal pages: `/privacy/`, `/terms/`, `/cookies/`

Old URLs such as `/faq` redirect automatically.

## Deploying on Hostinger from GitHub

1. Push this folder's contents to the **root** of a GitHub repo, for example `satis4eva/dpayments-site`. Keep it separate from the crypto subdomain repo.
2. In hPanel, go to **Websites → dpayments.co.uk → Advanced → Git**. Add the repo and the `main` branch, and leave the install path empty (so it deploys to `public_html`).
3. Back up the current `public_html` first. Then click **Deploy**.
4. Turn on **Auto deployment**. Copy the webhook URL and add it in GitHub under **Settings → Webhooks**. From then on, every push and every portal save goes live automatically.

## Website portal (`/admin/`)

The portal lets you:

- **Edit any page in place.** Click text and type. Alt+click a link or button to change where it goes.
- **Edit raw HTML** in the HTML tab.
- **Edit the page title and Google description** in the SEO tab.
- **Read and download enquiries.** Every form submission is also saved here.

### One-time setup

1. **Create a GitHub token.** Go to GitHub → Settings → Developer settings → **Fine-grained tokens** → Generate new token.
   - Repository access: **only** your website repo.
   - Permissions: **Contents → Read and write**.
   - Copy the token.
2. **Generate your password hash.** Visit `https://dpayments.co.uk/admin/`. While the portal isn't configured, this page shows a hash generator. Choose a strong password and copy the hash it gives you.
3. **Create `config.php`.**
   - In hPanel → File Manager, open `public_html/admin/` and copy `config.sample.php` to `config.php`.
   - Fill in `ADMIN_PASS_HASH`, `GITHUB_TOKEN`, `GITHUB_REPO` and `GITHUB_BRANCH`.
   - `config.php` is git-ignored, so it stays on the server only and deploys won't touch it.
4. Reload `/admin/` and log in (the username is `admin` unless you change it).

### How saving works

- **`STORAGE_MODE = 'github'` (recommended):** each save is committed to your repo. Hostinger's auto-deploy publishes it in about a minute. Every change appears in the repo's commit history, so you can undo anything there.
- **`STORAGE_MODE = 'local'`:** files on the server are edited directly, and a backup is kept for each save. Restore an older version from the SEO tab. Only use this if you don't deploy from GitHub, because otherwise the next deploy will overwrite your edits.

### Notes

- The header, menu and footer appear on every page and can't be edited in the portal. They are generated from the Python files in `_source/` (run `python3 _source/build.py`). Rebuilding overwrites any portal edits, so it is a developer tool only. Public access to `_source/` is blocked.
- Enquiries are stored in `admin/data/`. Public access to that folder is blocked, and it is git-ignored.
- Login locks for 15 minutes after 5 failed attempts.

## Enquiry form

Forms post to `send.php`. It emails `info@dpayments.co.uk`, saves a copy for the portal, and shows `/thank-you/`.

- `FROM_EMAIL` (`noreply@dpayments.co.uk`) should be a mailbox that exists in hPanel → Emails, so the messages don't land in spam.

## Logo

The header uses an inline SVG wordmark. To use your own logo, replace `assets/img/logo.svg` and `logo-dark.svg`, then swap the inline `<svg>` in the header and footer for an `<img>`.
