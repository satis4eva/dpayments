<?php
declare(strict_types=1);
require __DIR__ . '/lib.php';
require_login();

if (isset($_GET['download'])) {
    if (!class_exists('ZipArchive')) { flash('Backups need the PHP Zip extension, which isn’t available on this server.', 'err'); redirect('/admin/account.php'); }
    $tmp = tempnam(sys_get_temp_dir(), 'bk');
    $zip = new ZipArchive();
    $zip->open($tmp, ZipArchive::OVERWRITE);
    $add = function (string $dir, string $prefix) use ($zip) {
        if (!is_dir($dir)) return;
        $it = new RecursiveIteratorIterator(new RecursiveDirectoryIterator($dir, FilesystemIterator::SKIP_DOTS));
        foreach ($it as $f) {
            $rel = substr($f->getPathname(), strlen($dir) + 1);
            if (str_starts_with($rel, '_backups') || $rel === 'data/admin.json' || $rel === 'data/login-attempts.json') continue;
            $zip->addFile($f->getPathname(), $prefix . '/' . $rel);
        }
    };
    $add(CONTENT_DIR, 'content'); $add(UPLOAD_DIR, 'uploads');
    $zip->close();
    header('Content-Type: application/zip');
    header('Content-Disposition: attachment; filename="site-backup-' . date('Y-m-d') . '.zip"');
    header('Content-Length: ' . filesize($tmp));
    readfile($tmp); @unlink($tmp); exit;
}

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    require_post();
    $a = admin_account();
    if (!password_verify((string)($_POST['current'] ?? ''), (string)$a['hash'])) { flash('Your current password is not correct.', 'err'); redirect('/admin/account.php'); }
    $user = trim((string)($_POST['user'] ?? $a['user']));
    $new = (string)($_POST['new'] ?? '');
    if (!preg_match('~^[A-Za-z0-9._@-]{3,60}$~', $user)) { flash('Usernames can use letters, numbers, dots and dashes (3–60).', 'err'); redirect('/admin/account.php'); }
    if ($new !== '') {
        if (strlen($new) < 10) { flash('Use a password of at least 10 characters.', 'err'); redirect('/admin/account.php'); }
        if ($new !== ($_POST['new2'] ?? '')) { flash('The new passwords do not match.', 'err'); redirect('/admin/account.php'); }
        $a['hash'] = password_hash($new, PASSWORD_DEFAULT);
    }
    $a['user'] = $user; $_SESSION['user'] = $user;
    write_json('data/admin.json', $a);
    flash('Account updated.');
    redirect('/admin/account.php');
}
admin_header('Account & backups', 'account');
?>
<main>
  <div class="head"><div><h1>Account &amp; backups</h1></div></div>
  <form method="post" class="panel stack" style="max-width:620px">
    <?= csrf_field() ?>
    <h2>Your login</h2>
    <label>Username <input name="user" value="<?= e(admin_account()['user'] ?? '') ?>" autocomplete="username"></label>
    <label>New password <small class="muted">(leave blank to keep your current one)</small><input type="password" name="new" minlength="10" autocomplete="new-password"></label>
    <label>Confirm new password <input type="password" name="new2" minlength="10" autocomplete="new-password"></label>
    <label>Current password <small class="muted">(required to save changes)</small><input type="password" name="current" required autocomplete="current-password"></label>
    <button class="btn">Update account</button>
  </form>
  <div class="panel stack mt" style="max-width:620px">
    <h2>Backups</h2>
    <p class="muted">Every page, post, menu and setting is copied automatically before each save. You can also download everything — all content and uploaded images — as one file to keep safe.</p>
    <a class="btn btn-ghost" href="?download=1">Download full backup (.zip)</a>
  </div>
</main>
<?php admin_footer();
