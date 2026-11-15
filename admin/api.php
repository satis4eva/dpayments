<?php
declare(strict_types=1);
require __DIR__ . '/lib.php';

$action = (string)($_POST['action'] ?? '');

// Form-post actions (redirect back)
if ($action === 'restore_page') {
    require_login(); require_post();
    $slug = (string)($_POST['page'] ?? ''); $b = basename((string)($_POST['backup'] ?? ''));
    $prefix = 'pages__' . str_replace('/', '__', $slug) . '.html.';
    $file = CONTENT_DIR . '/_backups/' . $b;
    if (!isset(pages()[$slug]) || !str_starts_with($b, $prefix) || !is_file($file)) { flash('Backup not found.', 'err'); redirect('/admin/pages.php'); }
    write_file('pages/' . slug_file($slug), (string)file_get_contents($file));
    flash('Earlier version restored.');
    redirect('/admin/edit.php?page=' . rawurlencode($slug));
}

require_login(true);
if ($_SERVER['REQUEST_METHOD'] !== 'POST' || !check_csrf()) json_out(['ok' => false, 'error' => 'Session expired. Reload the page.'], 403);

try {
    switch ($action) {
        case 'save_page': {
            $slug = (string)($_POST['page'] ?? '');
            $pages = pages();
            if (!isset($pages[$slug])) throw new RuntimeException('Unknown page');
            $main = clean_html((string)($_POST['main'] ?? ''));
            if ($main === '') throw new RuntimeException('The page is empty — add at least one section.');
            if (strlen($main) > 800000) throw new RuntimeException('Page is too large.');
            write_file('pages/' . slug_file($slug), $main);
            $title = trim((string)($_POST['title'] ?? ''));
            if ($title !== '') $pages[$slug]['title'] = mb_substr($title, 0, 140);
            $pages[$slug]['description'] = mb_substr(trim((string)($_POST['description'] ?? '')), 0, 320);
            $pages[$slug]['noindex'] = !empty($_POST['noindex']);
            if (empty($pages[$slug]['core'])) $pages[$slug]['draft'] = !empty($_POST['draft']);
            $pages[$slug]['updated'] = gmdate('c');
            write_json('pages.json', $pages);
            json_out(['ok' => true]);
        }
        case 'upload': {
            if (empty($_FILES['file'])) throw new RuntimeException('No file received.');
            json_out(['ok' => true, 'url' => handle_upload($_FILES['file'])]);
        }
        case 'save_menus': {
            $data = json_decode((string)($_POST['menus'] ?? ''), true);
            if (!is_array($data) || !isset($data['header'], $data['footer'])) throw new RuntimeException('Menu data is invalid.');
            $clean = fn($s, $n = 120) => mb_substr(trim(strip_tags((string)$s)), 0, $n);
            $url = function ($u) { $u = trim((string)$u); return preg_match('~^\s*(javascript|data|vbscript):~i', $u) ? '#' : mb_substr($u, 0, 300); };
            $icons = icon_names();
            $out = ['header' => [], 'footer' => [], 'legal' => [], 'cta' => ['label' => $clean($data['cta']['label'] ?? '', 40), 'url' => $url($data['cta']['url'] ?? '')]];
            foreach ($data['header'] as $it) {
                if (($it['type'] ?? '') === 'mega') {
                    $cols = [];
                    foreach (array_slice($it['columns'] ?? [], 0, 4) as $c) {
                        $items = [];
                        foreach ($c['items'] ?? [] as $x) if ($clean($x['label'] ?? '') !== '')
                            $items[] = ['label' => $clean($x['label']), 'url' => $url($x['url'] ?? ''), 'icon' => in_array($x['icon'] ?? '', $icons, true) ? $x['icon'] : 'sparkle', 'desc' => $clean($x['desc'] ?? '', 160)];
                        $cols[] = ['title' => $clean($c['title'] ?? '', 60), 'items' => $items];
                    }
                    if ($clean($it['label'] ?? '') !== '') $out['header'][] = ['type' => 'mega', 'label' => $clean($it['label'], 40), 'columns' => $cols];
                } elseif ($clean($it['label'] ?? '') !== '') {
                    $out['header'][] = ['type' => 'link', 'label' => $clean($it['label'], 40), 'url' => $url($it['url'] ?? '')];
                }
            }
            foreach ($data['footer'] as $c) {
                $items = [];
                foreach ($c['items'] ?? [] as $x) if ($clean($x['label'] ?? '') !== '') $items[] = ['label' => $clean($x['label']), 'url' => $url($x['url'] ?? '')];
                if ($clean($c['title'] ?? '') !== '' || $items) $out['footer'][] = ['title' => $clean($c['title'] ?? '', 60), 'items' => $items];
            }
            foreach ($data['legal'] ?? [] as $x) if ($clean($x['label'] ?? '') !== '') $out['legal'][] = ['label' => $clean($x['label'], 40), 'url' => $url($x['url'] ?? '')];
            write_json('menus.json', $out);
            json_out(['ok' => true]);
        }
        case 'delete_media': {
            $name = basename((string)($_POST['name'] ?? ''));
            $p = UPLOAD_DIR . '/' . $name;
            if (!preg_match('~^[a-z0-9-]+\.(jpg|jpeg|png|webp|gif|ico)$~', $name) || !is_file($p)) throw new RuntimeException('File not found.');
            unlink($p);
            json_out(['ok' => true]);
        }
    }
    throw new RuntimeException('Unknown action');
} catch (Throwable $ex) {
    json_out(['ok' => false, 'error' => $ex->getMessage()], 400);
}
