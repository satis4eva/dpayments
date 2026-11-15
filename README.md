# dpayments.co.uk

The DPayments website with its own back office at **/admin/**.

## How it works

- **Code** (this repository) is deployed by Hostinger from the `main-site` branch whenever it changes.
- **Content** (pages, blog posts, menus, settings, enquiries) lives on the server in `/content/`, and uploaded images live in `/uploads/`. Both are git-ignored, so code deploys never overwrite your edits.
- On first run, `/content/` is created from `/content-default/`.

## Back office (/admin/)

| Section | What you can do |
|---|---|
| Pages | Edit any page in place, add sections (text, cards, images, steps, FAQ, video, call to action), replace images, change SEO titles and descriptions, create new pages from templates, hide or delete pages, restore earlier versions |
| Blog | Write, schedule and publish posts with a cover image, categories and a rich-text editor |
| Menus | Edit the top menu and dropdowns, the header button, footer columns and legal links |
| Media | Upload and manage images |
| Brand & settings | Logo, footer logo, browser icon, brand colours, fonts, corner style, contact details, top bar, company details, social links, Google Analytics and Search Console |
| Enquiries | Every form submission, with CSV export |
| Account & backups | Change your username and password, download a full backup |

### First login

Go to `/admin/` and enter the one-time setup code, then choose your username and password. Once an account exists, the code stops working.

### Contact tokens

In page content, `{{email}}`, `{{phone}}`, `{{address}}`, `{{company_name}}` and `{{company_number}}` are replaced with the values from Settings, so you only change them in one place.

## Security

- `/content/`, `/content-default/` and `/core/` are blocked from public access.
- Scripts in `/uploads/` will not run.
- Only JPG, PNG, WebP, GIF and ICO uploads are accepted.
- Admin forms are CSRF-protected, and logins lock for 15 minutes after 5 failed attempts.
