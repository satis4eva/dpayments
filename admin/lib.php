<?php
declare(strict_types=1);
require dirname(__DIR__) . '/core/site.php';
require dirname(__DIR__) . '/core/setup.php';
ensure_content();
header('X-Robots-Tag: noindex, nofollow');
header('X-Frame-Options: SAMEORIGIN');

// ---------------------------------------------------------------- auth
function admin_account(): array { return read_json('data/admin.json'); }
function has_admin(): bool { $a = admin_account(); return !empty($a['user']) && !empty($a['hash']); }

function start_session(): void {
    if (session_status() === PHP_SESSION_ACTIVE) return;
    $secure = (!empty($_SERVER['HTTPS']) && $_SERVER['HTTPS'] !== 'off') || (($_SERVER['HTTP_X_FORWARDED_PROTO'] ?? '') === 'https');
    session_name('dp_admin');
    session_set_cookie_params(['lifetime' => 0, 'path' => '/', 'secure' => $secure, 'httponly' => true, 'samesite' => 'Lax']);
    session_start();
    if (!empty($_SESSION['last']) && time() - $_SESSION['last'] > 4 * 3600) { $_SESSION = []; session_regenerate_id(true); }
    $_SESSION['last'] = time();
}
function is_logged_in(): bool { start_session(); return !empty($_SESSION['user']) && has_admin(); }

function require_login(bool $json = false): void {
    if (!is_logged_in()) {
        if ($json) json_out(['ok' => false, 'error' => 'Your session has expired. Please log in again.'], 401);
        header('Location: /admin/'); exit;
    }
}
function csrf_token(): string { start_session(); if (empty($_SESSION['csrf'])) $_SESSION['csrf'] = bin2hex(random_bytes(32)); return $_SESSION['csrf']; }
function check_csrf(): bool {
    start_session();
    $t = $_POST['csrf'] ?? ($_SERVER['HTTP_X_CSRF'] ?? null);
    return is_string($t) && !empty($_SESSION['csrf']) && hash_equals($_SESSION['csrf'], $t);
}
function require_post(): void {
    if ($_SERVER['REQUEST_METHOD'] !== 'POST' || !check_csrf()) { http_response_code(400); exit('Session expired — please go back, reload and try again.'); }
}
function csrf_field(): string { return '<input type="hidden" name="csrf" value="' . e(csrf_token()) . '">'; }

function json_out(array $d, int $code = 200): void {
    http_response_code($code);
    header('Content-Type: application/json; charset=utf-8');
    header('Cache-Control: no-store');
    echo json_encode($d); exit;
}

// login throttling
function too_many_attempts(): bool {
    $ip = $_SERVER['REMOTE_ADDR'] ?? 'x'; $d = read_json('data/login-attempts.json'); $r = $d[$ip] ?? null;
    return $r && $r['n'] >= 5 && time() - $r['t'] < 900;
}
function record_attempt(bool $ok): void {
    $ip = $_SERVER['REMOTE_ADDR'] ?? 'x'; $d = read_json('data/login-attempts.json');
    if ($ok) unset($d[$ip]);
    else { $r = $d[$ip] ?? ['n' => 0, 't' => time()]; if (time() - $r['t'] > 900) $r = ['n' => 0, 't' => time()]; $r['n']++; $r['t'] = time(); $d[$ip] = $r; }
    @file_put_contents(content_path('data/login-attempts.json'), json_encode($d), LOCK_EX);
}

function flash(?string $msg = null, string $type = 'ok'): ?array {
    start_session();
    if ($msg !== null) { $_SESSION['flash'] = [$msg, $type]; return null; }
    $f = $_SESSION['flash'] ?? null; unset($_SESSION['flash']); return $f;
}
function redirect(string $to): void { header('Location: ' . $to); exit; }

// ---------------------------------------------------------------- uploads
const UPLOAD_TYPES = ['image/jpeg' => 'jpg', 'image/png' => 'png', 'image/webp' => 'webp', 'image/gif' => 'gif', 'image/x-icon' => 'ico', 'image/vnd.microsoft.icon' => 'ico'];

function handle_upload(array $f): string {
    if (($f['error'] ?? UPLOAD_ERR_NO_FILE) !== UPLOAD_ERR_OK) throw new RuntimeException('Upload failed (code ' . ($f['error'] ?? '?') . ').');
    if ($f['size'] > 6 * 1024 * 1024) throw new RuntimeException('Images must be under 6 MB.');
    $mime = (new finfo(FILEINFO_MIME_TYPE))->file($f['tmp_name']) ?: '';
    if (!isset(UPLOAD_TYPES[$mime])) throw new RuntimeException('Please upload a JPG, PNG, WebP, GIF or ICO image.');
    if ($mime !== 'image/x-icon' && $mime !== 'image/vnd.microsoft.icon' && !@getimagesize($f['tmp_name'])) throw new RuntimeException('That file is not a valid image.');
    $base = slugify(pathinfo((string)$f['name'], PATHINFO_FILENAME));
    $name = $base . '-' . date('ymdHis') . '.' . UPLOAD_TYPES[$mime];
    if (!is_dir(UPLOAD_DIR)) mkdir(UPLOAD_DIR, 0755, true);
    if (!move_uploaded_file($f['tmp_name'], UPLOAD_DIR . '/' . $name)) throw new RuntimeException('Could not save the image.');
    @chmod(UPLOAD_DIR . '/' . $name, 0644);
    return '/uploads/' . $name;
}

function media_list(): array {
    $files = glob(UPLOAD_DIR . '/*.{jpg,jpeg,png,webp,gif,ico}', GLOB_BRACE) ?: [];
    usort($files, fn($a, $b) => filemtime($b) <=> filemtime($a));
    return array_map(fn($f) => ['url' => '/uploads/' . basename($f), 'name' => basename($f), 'size' => filesize($f)], $files);
}

// ---------------------------------------------------------------- enquiries
function read_enquiries(): array {
    $f = content_path('data/enquiries.jsonl');
    if (!is_file($f)) return [];
    $rows = [];
    foreach (file($f, FILE_IGNORE_NEW_LINES | FILE_SKIP_EMPTY_LINES) ?: [] as $l) { $r = json_decode($l, true); if (is_array($r)) $rows[] = $r; }
    return array_reverse($rows);
}

// ---------------------------------------------------------------- html cleaning (pages & posts)
/** Remove scripts, event handlers and javascript: URLs from editor HTML. Admin-only input, but defence in depth. */
function clean_html(string $html): string {
    // Allow embeds only from YouTube and Google Maps
    $html = preg_replace_callback('~<iframe\b[^>]*>.*?</iframe>~is', function ($m) {
        return preg_match('~\ssrc="https://(www\.youtube(-nocookie)?\.com/embed/|www\.google\.com/maps/embed)~i', $m[0]) ? $m[0] : '';
    }, $html);
    $html = preg_replace('~<\s*(script|object|embed|style)\b[^>]*>.*?<\s*/\s*\1\s*>~is', '', $html);
    $html = preg_replace('~<\s*(script|object|embed|link|meta|base)\b[^>]*/?>~is', '', $html);
    $html = preg_replace('~\son[a-z]+\s*=\s*("[^"]*"|\'[^\']*\'|[^\s>]+)~i', '', $html);
    $html = preg_replace('~(href|src|action)\s*=\s*(["\'])\s*(javascript|vbscript|data):[^"\']*\2~i', '$1="#"', $html);
    return trim($html);
}

// ---------------------------------------------------------------- layout
function admin_header(string $title, string $active = '', bool $wide = false): void {
    $nav = [
        'dashboard' => ['/admin/', 'Dashboard', 'chart'],
        'pages' => ['/admin/pages.php', 'Pages', 'file'],
        'blog' => ['/admin/blog.php', 'Blog', 'receipt'],
        'menus' => ['/admin/menus.php', 'Menus', 'clipboard'],
        'media' => ['/admin/media.php', 'Media', 'sparkle'],
        'settings' => ['/admin/settings.php', 'Brand &amp; settings', 'store'],
        'enquiries' => ['/admin/enquiries.php', 'Enquiries', 'mail'],
        'account' => ['/admin/account.php', 'Account &amp; backups', 'lock'],
    ];
    $s = settings();
    echo '<!doctype html><html lang="en-GB"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">';
    echo '<meta name="robots" content="noindex, nofollow"><title>' . e($title) . ' · ' . e($s['site_name'] ?? '') . ' admin</title>';
    echo '<link rel="icon" href="' . e($s['favicon'] ?: '/assets/img/favicon.svg') . '"><link rel="stylesheet" href="/admin/assets/admin.css?v=' . @filemtime(__DIR__ . '/assets/admin.css') . '"></head><body class="' . ($wide ? 'wide' : '') . '">';
    if (is_logged_in()) {
        echo '<aside class="side"><a class="brand" href="/admin/"><span class="bmark">' . icon_svg('sparkle') . '</span>' . e($s['site_name'] ?? 'Site') . '<small>admin</small></a><nav>';
        foreach ($nav as $k => [$href, $label, $ic]) echo '<a href="' . $href . '"' . ($k === $active ? ' class="on"' : '') . '>' . icon_svg($ic) . '<span>' . $label . '</span></a>';
        echo '</nav><div class="side-foot"><a href="/" target="_blank" rel="noopener">' . icon_svg('globe') . '<span>View site</span></a>'
            . '<form method="post" action="/admin/logout.php">' . csrf_field() . '<button>' . icon_svg('lock') . '<span>Log out</span></button></form></div></aside>';
        echo '<div class="shell">';
        $f = flash();
        if ($f) echo '<div class="flash ' . e($f[1]) . '">' . e($f[0]) . '</div>';
    } else {
        echo '<div class="shell solo">';
    }
}
function admin_footer(): void { echo '</div></body></html>'; }

function icon_options(string $selected): string {
    $o = '';
    foreach (icon_names() as $n) $o .= '<option' . ($n === $selected ? ' selected' : '') . '>' . e($n) . '</option>';
    return $o;
}
