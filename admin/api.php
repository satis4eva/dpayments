<?php
declare(strict_types=1);
require __DIR__ . '/lib.php';

$action = (string)($_POST['action'] ?? '');

// Restore (local mode, regular form post)
if ($action === 'restore') {
    require_login();
    $rel = (string)($_POST['page'] ?? '');
    $b = basename((string)($_POST['backup'] ?? ''));
    if (!check_csrf($_POST['csrf'] ?? null) || !valid_page($rel) || storage_mode() !== 'local') {
        http_response_code(400); exit('Bad request');
    }
    $prefix = str_replace('/', '__', $rel) . '.';
    $file = DATA_DIR . '/backups/' . $b;
    if (!str_starts_with($b, $prefix) || !is_file($file)) { http_response_code(404); exit('Backup not found'); }
    [$cur, $ver] = read_page($rel);
    write_page($rel, (string)file_get_contents($file), $ver, 'Restore ' . $b);
    header('Location: /admin/edit.php?p=' . rawurlencode($rel));
    exit;
}

require_login(true);
if (!check_csrf($_POST['csrf'] ?? null)) json_out(['ok' => false, 'error' => 'Session expired. Reload the page.'], 403);

if ($action === 'save') {
    $rel = (string)($_POST['page'] ?? '');
    if (!valid_page($rel)) json_out(['ok' => false, 'error' => 'Unknown page'], 400);
    $main = (string)($_POST['main'] ?? '');
    $title = trim((string)($_POST['title'] ?? ''));
    $desc = trim((string)($_POST['description'] ?? ''));
    $version = (string)($_POST['version'] ?? '');
    if (trim($main) === '') json_out(['ok' => false, 'error' => 'Page content is empty'], 400);
    if (strlen($main) > 600000) json_out(['ok' => false, 'error' => 'Content too large'], 400);

    try {
        [$current, $curVersion] = read_page($rel);
        if ($version !== $curVersion) {
            json_out(['ok' => false, 'error' => 'This page was changed elsewhere since you opened it. Copy your changes, reload and try again.'], 409);
        }
        $new = apply_edits($current, $main, $title, $desc);
        if ($new === $current) json_out(['ok' => true, 'version' => $curVersion, 'unchanged' => true]);
        $user = $_SESSION['user'] ?? 'admin';
        $newVersion = write_page($rel, $new, $curVersion, 'Portal edit: ' . page_url($rel) . ' (by ' . $user . ')');
        json_out(['ok' => true, 'version' => $newVersion]);
    } catch (Throwable $e) {
        $msg = $e->getMessage() === 'conflict'
            ? 'This page was changed elsewhere since you opened it. Copy your changes, reload and try again.'
            : $e->getMessage();
        json_out(['ok' => false, 'error' => $msg], 500);
    }
}

json_out(['ok' => false, 'error' => 'Unknown action'], 400);
