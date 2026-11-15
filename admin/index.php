<?php
declare(strict_types=1);
require __DIR__ . '/lib.php';
start_session();

// ---------- First run: create the admin account with the one-time setup code ----------
if (!has_admin()) {
    $err = '';
    if ($_SERVER['REQUEST_METHOD'] === 'POST') {
        if (!check_csrf()) $err = 'Session expired. Please try again.';
        elseif (too_many_attempts()) $err = 'Too many attempts. Please wait 15 minutes.';
        else {
            $code = strtoupper(trim((string)($_POST['code'] ?? '')));
            $user = trim((string)($_POST['user'] ?? ''));
            $pass = (string)($_POST['pass'] ?? '');
            $ok = hash_equals(SETUP_CODE_SHA256, hash('sha256', $code));
            record_attempt($ok);
            if (!$ok) $err = 'That setup code is not correct.';
            elseif (!preg_match('~^[A-Za-z0-9._@-]{3,60}$~', $user)) $err = 'Choose a username of 3–60 letters, numbers, dots or dashes.';
            elseif (strlen($pass) < 10) $err = 'Use a password of at least 10 characters.';
            elseif ($pass !== ($_POST['pass2'] ?? '')) $err = 'The passwords do not match.';
            else {
                write_json('data/admin.json', ['user' => $user, 'hash' => password_hash($pass, PASSWORD_DEFAULT), 'created' => gmdate('c')]);
                session_regenerate_id(true);
                $_SESSION['user'] = $user;
                flash('Welcome! Your admin account is ready.');
                redirect('/admin/');
            }
        }
    }
    admin_header('Set up');
    ?>
    <main class="auth">
      <form method="post" class="panel stack">
        <h1>Create your admin account</h1>
        <p class="muted">Enter the one-time setup code you were given, then choose your login. The code stops working once your account exists.</p>
        <?php if ($err): ?><p class="err"><?= e($err) ?></p><?php endif; ?>
        <?= csrf_field() ?>
        <label>Setup code <input name="code" required autocomplete="off" placeholder="XXXXX-XXXXX-XXXXX-XXXXX"></label>
        <label>Username <input name="user" required autocomplete="username" value="<?= e($_POST['user'] ?? '') ?>"></label>
        <label>Password <input type="password" name="pass" required minlength="10" autocomplete="new-password"></label>
        <label>Confirm password <input type="password" name="pass2" required minlength="10" autocomplete="new-password"></label>
        <button class="btn">Create account</button>
      </form>
    </main>
    <?php admin_footer(); exit;
}

// ---------- Login ----------
if (!is_logged_in()) {
    $err = '';
    if ($_SERVER['REQUEST_METHOD'] === 'POST') {
        if (!check_csrf()) $err = 'Session expired. Please try again.';
        elseif (too_many_attempts()) $err = 'Too many attempts. Please wait 15 minutes.';
        else {
            $a = admin_account();
            $ok = hash_equals((string)$a['user'], (string)($_POST['user'] ?? '')) && password_verify((string)($_POST['pass'] ?? ''), (string)$a['hash']);
            record_attempt($ok);
            if ($ok) {
                if (password_needs_rehash($a['hash'], PASSWORD_DEFAULT)) { $a['hash'] = password_hash((string)$_POST['pass'], PASSWORD_DEFAULT); write_json('data/admin.json', $a); }
                session_regenerate_id(true); $_SESSION['user'] = $a['user']; redirect('/admin/');
            }
            usleep(400000); $err = 'Incorrect username or password.';
        }
    }
    admin_header('Log in');
    ?>
    <main class="auth">
      <form method="post" class="panel stack">
        <div class="auth-logo"><?= logo_html() ?></div>
        <h1>Log in</h1>
        <?php if ($err): ?><p class="err"><?= e($err) ?></p><?php endif; ?>
        <?= csrf_field() ?>
        <label>Username <input name="user" required autocomplete="username"></label>
        <label>Password <input type="password" name="pass" required autocomplete="current-password"></label>
        <button class="btn">Log in</button>
      </form>
    </main>
    <?php admin_footer(); exit;
}

// ---------- Dashboard ----------
$pages = pages(); $posts = posts(); $enq = read_enquiries();
$published = count(array_filter($posts, fn($p) => ($p['status'] ?? '') === 'published'));
admin_header('Dashboard', 'dashboard');
?>
<main>
  <div class="head"><div><h1>Dashboard</h1><p class="muted">Manage everything on <?= e(preg_replace('~^https?://~', '', settings()['site_url'] ?? '')) ?> from here.</p></div></div>
  <div class="stats">
    <a class="stat" href="/admin/pages.php"><b><?= count($pages) ?></b><span>Pages</span></a>
    <a class="stat" href="/admin/blog.php"><b><?= $published ?></b><span>Published posts</span></a>
    <a class="stat" href="/admin/enquiries.php"><b><?= count($enq) ?></b><span>Enquiries</span></a>
    <a class="stat" href="/admin/media.php"><b><?= count(media_list()) ?></b><span>Images</span></a>
  </div>
  <h2>Quick actions</h2>
  <div class="tiles">
    <a class="tile" href="/admin/pages.php#new"><?= icon_svg('file') ?><b>Add a page</b><small>Start from a template</small></a>
    <a class="tile" href="/admin/post.php"><?= icon_svg('receipt') ?><b>Write a blog post</b><small>News, guides, updates</small></a>
    <a class="tile" href="/admin/menus.php"><?= icon_svg('clipboard') ?><b>Edit menus</b><small>Header and footer links</small></a>
    <a class="tile" href="/admin/settings.php#brand"><?= icon_svg('store') ?><b>Logo &amp; theme</b><small>Colours, fonts, logo</small></a>
    <a class="tile" href="/admin/settings.php#contact"><?= icon_svg('phone') ?><b>Contact details</b><small>Phone, address, email</small></a>
    <a class="tile" href="/admin/settings.php#social"><?= icon_svg('users') ?><b>Social media</b><small>Links in the footer</small></a>
  </div>
  <?php if ($enq): ?>
  <h2>Latest enquiries</h2>
  <div class="list">
    <?php foreach (array_slice($enq, 0, 5) as $r): ?>
      <a class="row" href="/admin/enquiries.php"><span><b><?= e($r['name'] ?? '') ?></b><?= !empty($r['business']) ? ' · ' . e($r['business']) : '' ?><small><?= e($r['email'] ?? '') ?></small></span><small><?= e($r['date'] ?? '') ?></small></a>
    <?php endforeach; ?>
  </div>
  <?php endif; ?>
</main>
<?php admin_footer();
