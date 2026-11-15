<?php
/**
 * DPayments CMS core: content storage, settings, menus and page rendering.
 * Content lives in /content (server only, git-ignored). It is seeded from
 * /content-default on first run, so code deploys never overwrite your edits.
 */
declare(strict_types=1);

define('SITE_ROOT', dirname(__DIR__));
define('CONTENT_DIR', SITE_ROOT . '/content');
define('DEFAULT_DIR', SITE_ROOT . '/content-default');
define('UPLOAD_DIR', SITE_ROOT . '/uploads');

// ---------------------------------------------------------------- storage
function copy_tree(string $src, string $dst): void {
    if (!is_dir($dst)) mkdir($dst, 0755, true);
    foreach (scandir($src) ?: [] as $f) {
        if ($f === '.' || $f === '..') continue;
        $s = "$src/$f"; $d = "$dst/$f";
        if (is_dir($s)) copy_tree($s, $d);
        elseif (!file_exists($d)) copy($s, $d);
    }
}

function ensure_content(): void {
    if (is_file(CONTENT_DIR . '/settings.json')) return;
    copy_tree(DEFAULT_DIR, CONTENT_DIR);
    file_put_contents(CONTENT_DIR . '/.htaccess', "Require all denied\n");
    foreach (['_backups', 'data'] as $d) if (!is_dir(CONTENT_DIR . "/$d")) mkdir(CONTENT_DIR . "/$d", 0750, true);
    if (!is_dir(UPLOAD_DIR)) mkdir(UPLOAD_DIR, 0755, true);
}

function content_path(string $rel): string { return CONTENT_DIR . '/' . ltrim($rel, '/'); }

function read_json(string $rel, $default = []) {
    $p = content_path($rel);
    if (!is_file($p)) return $default;
    $d = json_decode((string)file_get_contents($p), true);
    return is_array($d) ? $d : $default;
}

function backup_file(string $rel): void {
    $p = content_path($rel);
    if (!is_file($p)) return;
    $dir = CONTENT_DIR . '/_backups';
    if (!is_dir($dir)) mkdir($dir, 0750, true);
    copy($p, $dir . '/' . str_replace('/', '__', $rel) . '.' . date('Ymd-His') . '.bak');
    // keep the 15 most recent backups per file
    $all = glob($dir . '/' . str_replace('/', '__', $rel) . '.*.bak') ?: [];
    rsort($all);
    foreach (array_slice($all, 15) as $old) @unlink($old);
}

function write_file(string $rel, string $data): void {
    $p = content_path($rel);
    if (!is_dir(dirname($p))) mkdir(dirname($p), 0755, true);
    backup_file($rel);
    $tmp = $p . '.tmp' . bin2hex(random_bytes(3));
    if (file_put_contents($tmp, $data, LOCK_EX) === false || !rename($tmp, $p)) {
        @unlink($tmp);
        throw new RuntimeException('Could not save ' . $rel);
    }
}

function write_json(string $rel, $data): void {
    write_file($rel, json_encode($data, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES));
}

function settings(): array {
    static $s = null;
    if ($s === null) $s = read_json('settings.json');
    return $s;
}
function menus(): array { static $m = null; if ($m === null) $m = read_json('menus.json'); return $m; }
function pages(): array { static $p = null; if ($p === null) $p = read_json('pages.json'); return $p; }
function posts(): array { static $p = null; if ($p === null) $p = read_json('posts.json'); return $p; }

function slug_file(string $slug): string { return str_replace('/', '__', $slug) . '.html'; }
function page_body(string $slug): string {
    $p = content_path('pages/' . slug_file($slug));
    return is_file($p) ? (string)file_get_contents($p) : '';
}
function post_body(string $slug): string {
    $p = content_path('posts/' . $slug . '.html');
    return is_file($p) ? (string)file_get_contents($p) : '';
}
function page_url(string $slug): string { return $slug === 'home' ? '/' : '/' . $slug . '/'; }

function valid_slug(string $s): bool {
    return (bool)preg_match('~^[a-z0-9]+(-[a-z0-9]+)*(/[a-z0-9]+(-[a-z0-9]+)*)?$~', $s) && strlen($s) <= 80;
}
function slugify(string $s): string {
    $s = strtolower(trim(preg_replace('~[^A-Za-z0-9]+~', '-', $s), '-'));
    return substr($s, 0, 70) ?: 'page';
}

function e($s): string { return htmlspecialchars((string)$s, ENT_QUOTES | ENT_SUBSTITUTE, 'UTF-8'); }

// ---------------------------------------------------------------- theme
function hex_rgb(string $hex): array {
    $hex = ltrim($hex, '#');
    if (strlen($hex) === 3) $hex = $hex[0] . $hex[0] . $hex[1] . $hex[1] . $hex[2] . $hex[2];
    if (!preg_match('~^[0-9a-fA-F]{6}$~', $hex)) return [14, 156, 116];
    return [hexdec(substr($hex, 0, 2)), hexdec(substr($hex, 2, 2)), hexdec(substr($hex, 4, 2))];
}
function mix(string $hex, string $with, float $amount): string {
    [$r, $g, $b] = hex_rgb($hex); [$r2, $g2, $b2] = hex_rgb($with);
    return sprintf('#%02x%02x%02x', (int)round($r + ($r2 - $r) * $amount), (int)round($g + ($g2 - $g) * $amount), (int)round($b + ($b2 - $b) * $amount));
}
function safe_color(?string $c, string $fallback): string {
    return ($c && preg_match('~^#[0-9a-fA-F]{6}$~', $c)) ? $c : $fallback;
}

const FONTS = ['Inter', 'Manrope', 'Poppins', 'Montserrat', 'DM Sans', 'Plus Jakarta Sans', 'Outfit', 'Lato',
    'Roboto', 'Open Sans', 'Nunito Sans', 'Work Sans', 'Raleway', 'Playfair Display', 'Merriweather', 'Lora'];

function theme_css(): string {
    $t = settings()['theme'] ?? [];
    $accent = safe_color($t['accent'] ?? null, '#0e9c74');
    $accentDark = safe_color($t['accent_dark'] ?? null, mix($accent, '#000000', .35));
    $ink = safe_color($t['ink'] ?? null, '#0d1b26');
    $bg = safe_color($t['bg'] ?? null, '#f6f7f4');
    $hf = in_array($t['heading_font'] ?? '', FONTS, true) ? $t['heading_font'] : 'Manrope';
    $bf = in_array($t['body_font'] ?? '', FONTS, true) ? $t['body_font'] : 'Inter';
    $radius = max(0, min(30, (int)($t['radius'] ?? 14)));
    return ':root{--accent:' . $accent . ';--accent-ink:' . $accentDark . ';--accent-soft:' . mix($accent, '#ffffff', .88)
        . ';--accent-light:' . mix($accent, '#ffffff', .5) . ';--ink:' . $ink . ';--dark:' . $ink . ';--dark-2:' . mix($ink, '#ffffff', .06)
        . ';--bg:' . $bg . ';--radius:' . $radius . 'px;--radius-lg:' . ($radius + 8) . 'px'
        . ';--font-head:"' . $hf . '",system-ui,sans-serif;--font-body:"' . $bf . '",system-ui,sans-serif}';
}

function fonts_link(): string {
    $t = settings()['theme'] ?? [];
    $fams = array_unique([in_array($t['heading_font'] ?? '', FONTS, true) ? $t['heading_font'] : 'Manrope',
        in_array($t['body_font'] ?? '', FONTS, true) ? $t['body_font'] : 'Inter']);
    $q = implode('&', array_map(fn($f) => 'family=' . str_replace(' ', '+', $f) . ':wght@400;500;600;700;800', $fams));
    return '<link href="https://fonts.googleapis.com/css2?' . $q . '&display=swap" rel="stylesheet">';
}

// ---------------------------------------------------------------- icons
function icon_svg(string $name): string {
    static $icons = null;
    if ($icons === null) $icons = json_decode((string)file_get_contents(__DIR__ . '/icons.json'), true) ?: [];
    $p = $icons[$name] ?? $icons['sparkle'] ?? '';
    return '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">' . $p . '</svg>';
}
function icon_names(): array {
    return array_keys(json_decode((string)file_get_contents(__DIR__ . '/icons.json'), true) ?: []);
}

const SOCIAL_ICONS = [
    'linkedin' => '<path d="M6 9v9M6 6v.01M10 18v-5a3 3 0 0 1 6 0v5M10 9v9"/><rect x="2" y="2" width="20" height="20" rx="4"/>',
    'facebook' => '<path d="M15 3h-2a4 4 0 0 0-4 4v3H6v4h3v7h4v-7h3l1-4h-4V7a1 1 0 0 1 1-1h2z"/>',
    'instagram' => '<rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><path d="M17.5 6.5h.01"/>',
    'x' => '<path d="M4 4l16 16M20 4L4 20"/>',
    'youtube' => '<rect x="2" y="5" width="20" height="14" rx="4"/><path d="M10 9l5 3-5 3z"/>',
    'tiktok' => '<path d="M14 3v11a4 4 0 1 1-4-4"/><path d="M14 3a5 5 0 0 0 5 5"/>',
];

// ---------------------------------------------------------------- tokens
/** Replace {{email}}, {{phone}} etc. For the editor, text tokens are wrapped so they survive saving. */
function token_values(): array {
    $c = settings()['contact'] ?? [];
    return [
        'email' => $c['email'] ?? '', 'phone' => $c['phone'] ?? '', 'address' => $c['address'] ?? '',
        'whatsapp' => $c['whatsapp'] ?? '', 'hours' => $c['hours'] ?? '',
        'company_name' => $c['company_name'] ?? '', 'company_number' => $c['company_number'] ?? '',
        'site_name' => settings()['site_name'] ?? '', 'year' => date('Y'),
    ];
}
function apply_tokens(string $html, bool $forEdit = false): string {
    $vals = token_values();
    $parts = preg_split('~(<[^>]+>)~', $html, -1, PREG_SPLIT_DELIM_CAPTURE) ?: [];
    foreach ($parts as $i => $p) {
        $isTag = isset($p[0]) && $p[0] === '<';
        $parts[$i] = preg_replace_callback('~\{\{\s*([a-z_]+)\s*\}\}~', function ($m) use ($vals, $isTag, $forEdit) {
            if (!array_key_exists($m[1], $vals)) return $m[0];
            if ($forEdit && $isTag) return $m[0];
            $v = e($vals[$m[1]]);
            return ($forEdit && !$isTag) ? '<span data-token="' . $m[1] . '" contenteditable="false" class="cms-token">' . ($v !== '' ? $v : '{{' . $m[1] . '}}') . '</span>' : $v;
        }, $p);
    }
    return implode('', $parts);
}

// ---------------------------------------------------------------- layout
function logo_html(bool $dark = false): string {
    $s = settings();
    $img = $dark ? ($s['logo_dark'] ?: $s['logo']) : $s['logo'];
    $name = $s['site_name'] ?? 'DPayments';
    if ($img) return '<img src="' . e($img) . '" alt="' . e($name) . '" class="logo-img">';
    $w = 46 + (int)(mb_strlen($name) * 13.2);
    $fill = $dark ? '#ffffff' : 'var(--ink)';
    return '<svg viewBox="0 0 ' . $w . ' 36" height="30" role="img" aria-label="' . e($name) . '">'
        . '<rect x="0" y="2" width="32" height="32" rx="9" style="fill:var(--accent)"/>'
        . '<path d="M10 10h6.2c5 0 8.3 3.1 8.3 8s-3.3 8-8.3 8H10z" fill="none" stroke="#fff" stroke-width="3"/>'
        . '<path d="M14.5 15.2a4 4 0 0 1 0 5.6" fill="none" stroke="#fff" stroke-width="2" stroke-linecap="round"/>'
        . '<text x="42" y="26" font-family="var(--font-head), Inter, Arial, sans-serif" font-size="22" font-weight="800" letter-spacing="-0.6" style="fill:' . $fill . '">' . e($name) . '</text></svg>';
}

function url_matches(string $url, string $current): bool {
    return $current !== '' && strtok($url, '#') === $current;
}

function render_header(string $current): string {
    $m = menus();
    $s = settings();
    $chev = '<svg class="chev" viewBox="0 0 12 12" aria-hidden="true"><path d="M3 4.5l3 3 3-3" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></svg>';
    $items = '';
    foreach ($m['header'] ?? [] as $k => $it) {
        if (($it['type'] ?? 'link') === 'mega') {
            $cols = $it['columns'] ?? [];
            $active = false; $colhtml = '';
            foreach ($cols as $col) {
                $li = '';
                foreach ($col['items'] ?? [] as $x) {
                    $cur = url_matches($x['url'] ?? '', $current);
                    $active = $active || $cur;
                    $li .= '<li><a href="' . e($x['url'] ?? '#') . '"' . ($cur ? ' aria-current="page"' : '') . '><div class="mi">' . icon_svg($x['icon'] ?? 'sparkle')
                        . '</div><span><b>' . e($x['label'] ?? '') . '</b>' . (!empty($x['desc']) ? '<small>' . e($x['desc']) . '</small>' : '') . '</span></a></li>';
                }
                $colhtml .= '<div class="mega-col">' . (!empty($col['title']) ? '<h5>' . e($col['title']) . '</h5>' : '') . '<ul>' . $li . '</ul></div>';
            }
            $n = max(1, min(4, count($cols)));
            $items .= '<li class="has-menu' . ($active ? ' is-active' : '') . ($n >= 3 ? ' wide' : '') . '"><button class="menu-btn" type="button" aria-expanded="false" aria-controls="m-' . $k . '">'
                . e($it['label'] ?? '') . $chev . '</button><div class="mega mega-' . $n . '" id="m-' . $k . '">' . $colhtml . '</div></li>';
        } else {
            $cur = url_matches($it['url'] ?? '', $current);
            $items .= '<li><a class="top-link" href="' . e($it['url'] ?? '#') . '"' . ($cur ? ' aria-current="page"' : '') . '>' . e($it['label'] ?? '') . '</a></li>';
        }
    }
    if (!empty($m['cta']['label'])) {
        $items .= '<li class="nav-cta"><a class="btn btn-primary btn-sm" href="' . e($m['cta']['url'] ?? '/contact/') . '">' . e($m['cta']['label']) . '</a></li>';
    }
    $top = '';
    if (!empty($s['topbar']['enabled'])) {
        $c = $s['contact'] ?? [];
        $bits = [];
        if (!empty($s['topbar']['text'])) $bits[] = '<span>' . e($s['topbar']['text']) . '</span>';
        $right = '';
        if (!empty($c['phone'])) $right .= '<a href="tel:' . e(preg_replace('~[^0-9+]~', '', $c['phone'])) . '">' . icon_svg('phone') . e($c['phone']) . '</a>';
        if (!empty($c['email'])) $right .= '<a href="mailto:' . e($c['email']) . '">' . icon_svg('mail') . e($c['email']) . '</a>';
        $top = '<div class="topbar"><div class="container">' . implode('', $bits) . '<div class="tb-right">' . $right . '</div></div></div>';
    }
    return '<a class="skip" href="#main">Skip to content</a>' . $top . '
<header class="site-header">
  <div class="container nav">
    <a class="logo" href="/" aria-label="' . e($s['site_name'] ?? '') . ' home">' . logo_html() . '</a>
    <button class="menu-toggle" type="button" aria-label="Menu" aria-expanded="false" aria-controls="nav-links"><span></span></button>
    <ul class="nav-links" id="nav-links">' . $items . '</ul>
  </div>
</header>';
}

function render_footer(): string {
    $s = settings(); $m = menus(); $c = $s['contact'] ?? [];
    $cols = '';
    foreach ($m['footer'] ?? [] as $col) {
        $li = '';
        foreach ($col['items'] ?? [] as $x) $li .= '<li><a href="' . e($x['url'] ?? '#') . '">' . e($x['label'] ?? '') . '</a></li>';
        $cols .= '<div><h4>' . e($col['title'] ?? '') . '</h4><ul>' . $li . '</ul></div>';
    }
    $contact = '';
    if (!empty($c['email'])) $contact .= '<li><a href="mailto:' . e($c['email']) . '">' . icon_svg('mail') . e($c['email']) . '</a></li>';
    if (!empty($c['phone'])) $contact .= '<li><a href="tel:' . e(preg_replace('~[^0-9+]~', '', $c['phone'])) . '">' . icon_svg('phone') . e($c['phone']) . '</a></li>';
    if (!empty($c['whatsapp'])) $contact .= '<li><a href="https://wa.me/' . e(preg_replace('~[^0-9]~', '', $c['whatsapp'])) . '" rel="noopener">' . icon_svg('phone') . 'WhatsApp</a></li>';
    if (!empty($c['address'])) $contact .= '<li>' . icon_svg('store') . '<span>' . nl2br(e($c['address'])) . '</span></li>';
    if (!empty($c['hours'])) $contact .= '<li>' . icon_svg('clock') . '<span>' . e($c['hours']) . '</span></li>';
    $social = '';
    foreach ($s['social'] ?? [] as $k => $url) {
        if ($url && isset(SOCIAL_ICONS[$k]) && preg_match('~^https?://~', $url)) {
            $social .= '<a href="' . e($url) . '" target="_blank" rel="noopener" aria-label="' . e(ucfirst($k)) . '"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">' . SOCIAL_ICONS[$k] . '</svg></a>';
        }
    }
    $legal = '';
    foreach ($m['legal'] ?? [] as $x) $legal .= '<li><a href="' . e($x['url']) . '">' . e($x['label']) . '</a></li>';
    $company = '';
    if (!empty($c['company_name'])) {
        $company = '<p class="company-line">' . e($c['company_name']) . (!empty($c['company_number']) ? ', registered in England and Wales, company no. ' . e($c['company_number']) : '')
            . (!empty($c['registered_address']) ? '. Registered office: ' . e($c['registered_address']) : '') . '.</p>';
    }
    return '<footer class="site-footer">
  <div class="container">
    <div class="footer-grid footer-cols-' . (count($m['footer'] ?? []) + 1) . '">
      <div class="footer-brand">
        <a href="/" aria-label="' . e($s['site_name'] ?? '') . ' home">' . logo_html(true) . '</a>
        <p style="margin-top:18px">' . e($s['tagline'] ?? '') . '</p>
        <ul class="footer-contact">' . $contact . '</ul>
        ' . ($social ? '<div class="social">' . $social . '</div>' : '') . '
      </div>' . $cols . '
    </div>
    <div class="footer-bottom">
      <div><span>&copy; ' . date('Y') . ' ' . e($s['site_name'] ?? '') . '. ' . e($s['footer_note'] ?? '') . '</span>' . $company . '</div>
      <ul>' . $legal . '</ul>
    </div>
  </div>
</footer>';
}

function render_document(array $meta, string $main, string $path, array $opt = []): string {
    $s = settings();
    $title = $meta['title'] ?? ($s['site_name'] ?? '');
    $desc = $meta['description'] ?? '';
    $canonical = rtrim($s['site_url'] ?? '', '/') . $path;
    $robots = !empty($meta['noindex']) ? '<meta name="robots" content="noindex">' . "\n" : '';
    $ga = trim($s['analytics']['ga4'] ?? '');
    $gtag = preg_match('~^G-[A-Z0-9]{4,15}$~', $ga)
        ? '<script async src="https://www.googletagmanager.com/gtag/js?id=' . $ga . '"></script><script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments)}gtag("js",new Date());gtag("config","' . $ga . '");</script>' : '';
    $gv = trim($s['analytics']['google_verification'] ?? '');
    $verify = preg_match('~^[A-Za-z0-9_\-]{10,100}$~', $gv) ? '<meta name="google-site-verification" content="' . $gv . '">' : '';
    $image = !empty($meta['image']) ? '<meta property="og:image" content="' . e(rtrim($s['site_url'] ?? '', '/') . $meta['image']) . '">' : '';
    $schema = $meta['schema'] ?? '';
    $current = $meta['nav'] ?? $path;
    $main = apply_tokens($main, !empty($opt['edit']));
    return '<!doctype html>
<html lang="en-GB">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>' . e($title) . '</title>
<meta name="description" content="' . e($desc) . '">
' . $robots . '<link rel="canonical" href="' . e($canonical) . '">
<meta property="og:type" content="' . (!empty($opt['article']) ? 'article' : 'website') . '">
<meta property="og:site_name" content="' . e($s['site_name'] ?? '') . '">
<meta property="og:title" content="' . e($title) . '">
<meta property="og:description" content="' . e($desc) . '">
<meta property="og:url" content="' . e($canonical) . '">
' . $image . $verify . '
<meta name="theme-color" content="' . e(safe_color($s['theme']['ink'] ?? null, '#0d1b26')) . '">
<link rel="icon" href="' . e($s['favicon'] ?: '/assets/img/favicon.svg') . '">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
' . fonts_link() . '
<link rel="stylesheet" href="/assets/css/style.css?v=' . @filemtime(SITE_ROOT . '/assets/css/style.css') . '">
<style>' . theme_css() . '</style>
' . $schema . $gtag . '
</head>
<body>
' . render_header($current) . '
<main id="main">
' . $main . '
</main>
' . render_footer() . '
<script src="/assets/js/main.js?v=' . @filemtime(SITE_ROOT . '/assets/js/main.js') . '" defer></script>
</body>
</html>';
}

// ---------------------------------------------------------------- blog
function format_date(string $d): string {
    $t = strtotime($d);
    return $t ? date('j F Y', $t) : '';
}

function published_posts(): array {
    $list = array_filter(posts(), fn($p) => ($p['status'] ?? 'draft') === 'published');
    uasort($list, fn($a, $b) => strcmp($b['date'] ?? '', $a['date'] ?? ''));
    return $list;
}

function post_card(string $slug, array $p): string {
    $img = !empty($p['cover']) ? '<div class="pc-img" style="background-image:url(\'' . e($p['cover']) . '\')"></div>' : '<div class="pc-img pc-none">' . icon_svg('file') . '</div>';
    return '<a class="post-card reveal" href="/blog/' . e($slug) . '/">' . $img . '<div class="pc-body">'
        . (!empty($p['category']) ? '<span class="tag">' . e($p['category']) . '</span>' : '')
        . '<h3>' . e($p['title'] ?? '') . '</h3><p>' . e($p['excerpt'] ?? '') . '</p><small>' . e(format_date($p['date'] ?? '')) . '</small></div></a>';
}

function render_blog_index(): string {
    $s = settings();
    $list = published_posts();
    $cards = '';
    foreach ($list as $slug => $p) $cards .= post_card($slug, $p);
    if (!$cards) $cards = '<div class="card card-lg center" style="grid-column:1/-1"><h3>No posts yet</h3><p>Check back soon.</p></div>';
    $bt = $s['blog']['title'] ?? 'Blog';
    $main = '<section class="page-hero"><div class="container"><div class="crumbs"><a href="/">Home</a> / ' . e($bt) . '</div>'
        . '<span class="eyebrow">' . e($bt) . '</span><h1>' . e($bt) . '</h1><p class="lede">' . e($s['blog']['intro'] ?? '') . '</p></div></section>'
        . '<section style="padding-top:0"><div class="container"><div class="post-grid">' . $cards . '</div></div></section>';
    return render_document(['title' => $bt . ' | ' . ($s['site_name'] ?? ''), 'description' => $s['blog']['intro'] ?? '', 'nav' => '/blog/'], $main, '/blog/');
}

function render_post(string $slug, array $p, bool $preview = false): string {
    $s = settings();
    $cover = !empty($p['cover']) ? '<div class="container narrow"><img class="post-cover" src="' . e($p['cover']) . '" alt=""></div>' : '';
    $more = '';
    foreach (array_slice(array_diff_key(published_posts(), [$slug => 1]), 0, 3, true) as $k => $o) $more .= post_card($k, $o);
    $schema = '<script type="application/ld+json">' . json_encode([
        '@context' => 'https://schema.org', '@type' => 'BlogPosting', 'headline' => $p['title'] ?? '',
        'datePublished' => $p['date'] ?? '', 'description' => $p['excerpt'] ?? '',
        'publisher' => ['@type' => 'Organization', 'name' => $s['site_name'] ?? ''],
        'image' => !empty($p['cover']) ? rtrim($s['site_url'] ?? '', '/') . $p['cover'] : null,
    ], JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE) . '</script>';
    $bt = $s['blog']['title'] ?? 'Blog';
    $main = '<article><section class="page-hero post-hero"><div class="container narrow">'
        . '<div class="crumbs"><a href="/">Home</a> / <a href="/blog/">' . e($bt) . '</a></div>'
        . (!empty($p['category']) ? '<span class="eyebrow">' . e($p['category']) . '</span>' : '')
        . '<h1>' . e($p['title'] ?? '') . '</h1><p class="post-meta">' . e(format_date($p['date'] ?? '')) . (!empty($p['author']) ? ' &middot; ' . e($p['author']) : '') . '</p></div></section>'
        . $cover . '<section style="padding-top:40px"><div class="container narrow prose post-body">' . post_body($slug) . '</div></section></article>'
        . ($more ? '<section class="section-white section-tight"><div class="container"><div class="section-head"><h2>More from ' . e($bt) . '</h2></div><div class="post-grid">' . $more . '</div></div></section>' : '');
    return render_document(['title' => ($p['seo_title'] ?? '') ?: (($p['title'] ?? '') . ' | ' . ($s['site_name'] ?? '')),
        'description' => $p['excerpt'] ?? '', 'image' => $p['cover'] ?? '', 'schema' => $schema, 'nav' => '/blog/',
        'noindex' => $preview], $main, '/blog/' . $slug . '/', ['article' => true]);
}

// ---------------------------------------------------------------- sitemap
function render_sitemap(): string {
    $base = rtrim(settings()['site_url'] ?? '', '/');
    $out = '<?xml version="1.0" encoding="UTF-8"?>' . "\n" . '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' . "\n";
    foreach (pages() as $slug => $m) {
        $slug = (string)$slug;
        if (!empty($m['noindex']) || !empty($m['draft']) || $slug === '404') continue;
        $out .= '  <url><loc>' . e($base . page_url($slug)) . '</loc></url>' . "\n";
    }
    if (published_posts()) $out .= '  <url><loc>' . e($base . '/blog/') . '</loc></url>' . "\n";
    foreach (published_posts() as $slug => $p) $out .= '  <url><loc>' . e($base . '/blog/' . $slug . '/') . '</loc><lastmod>' . e(substr($p['date'] ?? '', 0, 10)) . '</lastmod></url>' . "\n";
    return $out . '</urlset>';
}

// ---------------------------------------------------------------- page render
function render_page(string $slug, ?string $bodyOverride = null, bool $edit = false): string {
    $meta = pages()[$slug] ?? [];
    $body = $bodyOverride ?? page_body($slug);
    $path = $slug === '404' ? '/404/' : page_url($slug);
    if (empty($meta['nav'])) $meta['nav'] = $path;
    return render_document($meta, $body, $path, ['edit' => $edit]);
}

function route(): void {
    ensure_content();
    $uri = parse_url($_SERVER['REQUEST_URI'] ?? '/', PHP_URL_PATH) ?: '/';
    $uri = rawurldecode($uri);
    if ($uri === '/sitemap.xml') { header('Content-Type: application/xml; charset=utf-8'); echo render_sitemap(); return; }
    if ($uri !== '/' && substr($uri, -1) !== '/' && !preg_match('~\.[a-z0-9]{2,5}$~i', $uri)) {
        $q = $_SERVER['QUERY_STRING'] ?? '';
        header('Location: ' . $uri . '/' . ($q !== '' ? '?' . $q : ''), true, 301);
        return;
    }
    if (preg_match('~^/([a-z0-9-]+)\.html$~', $uri, $m) && isset(pages()[$m[1]])) { header('Location: /' . $m[1] . '/', true, 301); return; }
    $slug = trim($uri, '/');
    if ($slug === '') $slug = 'home';
    header('X-Content-Type-Options: nosniff');
    if ($slug === 'blog') { echo render_blog_index(); return; }
    if (preg_match('~^blog/([a-z0-9-]+)$~', $slug, $m)) {
        $p = posts()[$m[1]] ?? null;
        if ($p && ($p['status'] ?? '') === 'published') { echo render_post($m[1], $p); return; }
    } elseif (isset(pages()[$slug]) && $slug !== '404' && empty(pages()[$slug]['draft'])) {
        echo render_page($slug); return;
    }
    http_response_code(404);
    echo render_page('404');
}
