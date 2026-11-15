<?php
declare(strict_types=1);

define('ADMIN_DIR', __DIR__);
define('SITE_ROOT', dirname(__DIR__));
define('DATA_DIR', __DIR__ . '/data');
define('CONFIGURED', is_file(__DIR__ . '/config.php'));

if (CONFIGURED) {
    require __DIR__ . '/config.php';
}

// ---------- Session ----------
function start_session(): void {
    if (session_status() === PHP_SESSION_ACTIVE) return;
    $secure = (!empty($_SERVER['HTTPS']) && $_SERVER['HTTPS'] !== 'off');
    session_name('dp_admin');
    session_set_cookie_params([
        'lifetime' => 0, 'path' => '/admin/', 'secure' => $secure,
        'httponly' => true, 'samesite' => 'Strict',
    ]);
    session_start();
    if (!empty($_SESSION['last']) && time() - $_SESSION['last'] > 7200) {
        $_SESSION = [];
        session_regenerate_id(true);
    }
    $_SESSION['last'] = time();
}

function is_logged_in(): bool {
    start_session();
    return !empty($_SESSION['user']);
}

function require_login(bool $json = false): void {
    if (!CONFIGURED || !is_logged_in()) {
        if ($json) { json_out(['ok' => false, 'error' => 'Not logged in'], 401); }
        header('Location: /admin/');
        exit;
    }
}

function csrf_token(): string {
    start_session();
    if (empty($_SESSION['csrf'])) $_SESSION['csrf'] = bin2hex(random_bytes(32));
    return $_SESSION['csrf'];
}

function check_csrf(?string $t): bool {
    start_session();
    return is_string($t) && !empty($_SESSION['csrf']) && hash_equals($_SESSION['csrf'], $t);
}

function h(?string $s): string {
    return htmlspecialchars((string)$s, ENT_QUOTES | ENT_SUBSTITUTE, 'UTF-8');
}

function json_out(array $data, int $code = 200): void {
    http_response_code($code);
    header('Content-Type: application/json; charset=utf-8');
    header('Cache-Control: no-store');
    echo json_encode($data);
    exit;
}

// ---------- Login throttling ----------
function throttle_file(): string { return DATA_DIR . '/login-attempts.json'; }

function too_many_attempts(): bool {
    $ip = $_SERVER['REMOTE_ADDR'] ?? 'x';
    $d = is_file(throttle_file()) ? (json_decode((string)file_get_contents(throttle_file()), true) ?: []) : [];
    $r = $d[$ip] ?? null;
    return $r && $r['n'] >= 5 && time() - $r['t'] < 900;
}

function record_attempt(bool $ok): void {
    $ip = $_SERVER['REMOTE_ADDR'] ?? 'x';
    $f = throttle_file();
    $d = is_file($f) ? (json_decode((string)file_get_contents($f), true) ?: []) : [];
    if ($ok) { unset($d[$ip]); }
    else {
        $r = $d[$ip] ?? ['n' => 0, 't' => time()];
        if (time() - $r['t'] > 900) $r = ['n' => 0, 't' => time()];
        $r['n']++; $r['t'] = time();
        $d[$ip] = $r;
    }
    @file_put_contents($f, json_encode($d), LOCK_EX);
}

// ---------- Pages ----------
/** List editable pages: relative path => title */
function list_pages(): array {
    $files = array_merge(
        glob(SITE_ROOT . '/index.html') ?: [],
        glob(SITE_ROOT . '/*/index.html') ?: [],
        glob(SITE_ROOT . '/*/*/index.html') ?: []
    );
    $pages = [];
    foreach ($files as $f) {
        $rel = ltrim(substr($f, strlen(SITE_ROOT)), '/');
        if (str_starts_with($rel, 'admin/')) continue;
        $html = (string)file_get_contents($f, false, null, 0, 4000);
        $title = preg_match('~<title>(.*?)</title>~s', $html, $m) ? html_entity_decode($m[1], ENT_QUOTES, 'UTF-8') : $rel;
        $pages[$rel] = $title;
    }
    uksort($pages, function ($a, $b) {
        if ($a === 'index.html') return -1;
        if ($b === 'index.html') return 1;
        return strcmp($a, $b);
    });
    return $pages;
}

function valid_page(string $rel): bool {
    if (!preg_match('~^([a-z0-9-]+/){0,2}index\.html$~', $rel)) return false;
    if (str_starts_with($rel, 'admin/')) return false;
    return is_file(SITE_ROOT . '/' . $rel);
}

function page_url(string $rel): string {
    return '/' . substr($rel, 0, -strlen('index.html'));
}

// ---------- Storage ----------
function storage_mode(): string {
    return defined('STORAGE_MODE') && STORAGE_MODE === 'local' ? 'local' : 'github';
}

function gh_request(string $method, string $path, ?array $body = null): array {
    $url = 'https://api.github.com/repos/' . GITHUB_REPO . '/contents/' . GITHUB_PREFIX . $path;
    if ($method === 'GET') $url .= '?ref=' . rawurlencode(GITHUB_BRANCH);
    $ch = curl_init($url);
    $headers = [
        'Authorization: Bearer ' . GITHUB_TOKEN,
        'Accept: application/vnd.github+json',
        'X-GitHub-Api-Version: 2022-11-28',
        'User-Agent: dpayments-portal',
    ];
    curl_setopt_array($ch, [
        CURLOPT_RETURNTRANSFER => true,
        CURLOPT_CUSTOMREQUEST => $method,
        CURLOPT_TIMEOUT => 25,
    ]);
    if ($body !== null) {
        $headers[] = 'Content-Type: application/json';
        curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode($body));
    }
    curl_setopt($ch, CURLOPT_HTTPHEADER, $headers);
    $res = curl_exec($ch);
    $code = (int)curl_getinfo($ch, CURLINFO_HTTP_CODE);
    $err = curl_error($ch);
    curl_close($ch);
    if ($res === false) throw new RuntimeException('Could not reach GitHub: ' . $err);
    $data = json_decode((string)$res, true) ?: [];
    if ($code >= 400) {
        $msg = $data['message'] ?? ('HTTP ' . $code);
        if ($code === 409) throw new RuntimeException('conflict');
        throw new RuntimeException('GitHub error: ' . $msg);
    }
    return $data;
}

/** @return array{0:string,1:string} [html, version] */
function read_page(string $rel): array {
    if (storage_mode() === 'github') {
        if (!GITHUB_TOKEN) throw new RuntimeException('GitHub token is not set in admin/config.php');
        $d = gh_request('GET', $rel);
        return [base64_decode(str_replace("\n", '', $d['content'] ?? '')), (string)($d['sha'] ?? '')];
    }
    $html = (string)file_get_contents(SITE_ROOT . '/' . $rel);
    return [$html, sha1($html)];
}

function write_page(string $rel, string $html, string $version, string $message): string {
    if (storage_mode() === 'github') {
        $d = gh_request('PUT', $rel, [
            'message' => $message,
            'content' => base64_encode($html),
            'sha' => $version,
            'branch' => GITHUB_BRANCH,
        ]);
        return (string)($d['content']['sha'] ?? '');
    }
    $path = SITE_ROOT . '/' . $rel;
    $current = (string)file_get_contents($path);
    if (sha1($current) !== $version) throw new RuntimeException('conflict');
    $bdir = DATA_DIR . '/backups';
    if (!is_dir($bdir)) mkdir($bdir, 0750, true);
    file_put_contents($bdir . '/' . str_replace('/', '__', $rel) . '.' . date('Ymd-His') . '.html', $current);
    if (file_put_contents($path, $html, LOCK_EX) === false) throw new RuntimeException('Could not write file');
    return sha1($html);
}

function list_backups(string $rel): array {
    $files = glob(DATA_DIR . '/backups/' . str_replace('/', '__', $rel) . '.*.html') ?: [];
    rsort($files);
    return array_map('basename', array_slice($files, 0, 20));
}

// ---------- Editing helpers ----------
function apply_edits(string $html, string $main, string $title, string $desc): string {
    if (!preg_match('~<main id="main">.*</main>~s', $html)) throw new RuntimeException('Page structure not recognised');
    if (stripos($main, '</main') !== false || stripos($main, '<script') !== false) {
        throw new RuntimeException('Content contains tags that are not allowed (main/script)');
    }
    $html = preg_replace_callback('~(<main id="main">).*(</main>)~s', fn($m) => $m[1] . "\n" . $main . "\n" . $m[2], $html, 1);
    if ($title !== '') {
        $t = h($title);
        $html = preg_replace('~<title>.*?</title>~s', '<title>' . $t . '</title>', $html, 1);
        $html = preg_replace('~<meta property="og:title" content="[^"]*">~', '<meta property="og:title" content="' . $t . '">', $html, 1);
    }
    if ($desc !== '') {
        $d = h($desc);
        $html = preg_replace('~<meta name="description" content="[^"]*">~', '<meta name="description" content="' . $d . '">', $html, 1);
        $html = preg_replace('~<meta property="og:description" content="[^"]*">~', '<meta property="og:description" content="' . $d . '">', $html, 1);
    }
    return $html;
}

function meta_of(string $html): array {
    $title = preg_match('~<title>(.*?)</title>~s', $html, $m) ? html_entity_decode($m[1], ENT_QUOTES, 'UTF-8') : '';
    $desc = preg_match('~<meta name="description" content="([^"]*)">~', $html, $m) ? html_entity_decode($m[1], ENT_QUOTES, 'UTF-8') : '';
    return [$title, $desc];
}

// ---------- Enquiries ----------
function read_enquiries(): array {
    $f = DATA_DIR . '/enquiries.jsonl';
    if (!is_file($f)) return [];
    $rows = [];
    foreach (file($f, FILE_IGNORE_NEW_LINES | FILE_SKIP_EMPTY_LINES) ?: [] as $line) {
        $r = json_decode($line, true);
        if (is_array($r)) $rows[] = $r;
    }
    return array_reverse($rows);
}

// ---------- Layout ----------
function admin_header(string $title, string $active = ''): void {
    $nav = [
        'pages' => ['/admin/', 'Pages'],
        'enquiries' => ['/admin/enquiries.php', 'Enquiries'],
    ];
    echo '<!doctype html><html lang="en-GB"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">';
    echo '<meta name="robots" content="noindex, nofollow"><title>' . h($title) . ' · DPayments portal</title>';
    echo '<link rel="icon" href="/assets/img/favicon.svg"><link rel="stylesheet" href="/admin/assets/admin.css"></head><body>';
    if (is_logged_in()) {
        echo '<header class="top"><a class="brand" href="/admin/"><img src="/assets/img/favicon.svg" alt=""> DPayments <span>portal</span></a><nav>';
        foreach ($nav as $k => [$href, $label]) {
            echo '<a href="' . $href . '"' . ($k === $active ? ' class="on"' : '') . '>' . $label . '</a>';
        }
        echo '<a href="/" target="_blank" rel="noopener">View site &#8599;</a>';
        echo '<form method="post" action="/admin/logout.php"><input type="hidden" name="csrf" value="' . h(csrf_token()) . '"><button>Log out</button></form>';
        echo '</nav></header>';
    }
}

function admin_footer(): void {
    echo '</body></html>';
}
