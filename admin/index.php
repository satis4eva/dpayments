<?php
declare(strict_types=1);
require __DIR__ . '/lib.php';
header('X-Robots-Tag: noindex, nofollow');

// ---------- Not configured: setup helper ----------
if (!CONFIGURED) {
    $hash = '';
    if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['pw']) && is_string($_POST['pw'])) {
        if (strlen($_POST['pw']) >= 10) $hash = password_hash($_POST['pw'], PASSWORD_DEFAULT);
    }
    admin_header('Set up');
    ?>
    <main class="narrow">
      <div class="panel">
        <h1>Set up your portal</h1>
        <p>The portal isn&rsquo;t configured yet. It takes about five minutes:</p>
        <ol>
          <li>Choose a strong password below (at least 10 characters) and generate its hash.</li>
          <li>In Hostinger hPanel &rarr; <strong>File Manager</strong>, open <code>public_html/admin/</code>, copy <code>config.sample.php</code> to <code>config.php</code>.</li>
          <li>Paste the hash into <code>ADMIN_PASS_HASH</code>, and add your GitHub token (see the README).</li>
          <li>Reload this page and log in.</li>
        </ol>
        <form method="post" class="stack">
          <label>Password <input type="password" name="pw" minlength="10" required autocomplete="new-password"></label>
          <button class="btn">Generate hash</button>
        </form>
        <?php if ($hash): ?>
          <p class="mt">Your hash (copy everything):</p>
          <textarea readonly class="code" rows="2" onclick="this.select()"><?= h($hash) ?></textarea>
        <?php elseif ($_SERVER['REQUEST_METHOD'] === 'POST'): ?>
          <p class="err">Please use at least 10 characters.</p>
        <?php endif; ?>
      </div>
    </main>
    <?php
    admin_footer();
    exit;
}

start_session();

// ---------- Login ----------
if (!is_logged_in()) {
    $error = '';
    if ($_SERVER['REQUEST_METHOD'] === 'POST') {
        if (!check_csrf($_POST['csrf'] ?? null)) {
            $error = 'Your session expired. Please try again.';
        } elseif (too_many_attempts()) {
            $error = 'Too many attempts. Please wait 15 minutes.';
        } else {
            $u = (string)($_POST['user'] ?? '');
            $p = (string)($_POST['pass'] ?? '');
            $ok = ADMIN_PASS_HASH !== '' && hash_equals(ADMIN_USER, $u) && password_verify($p, ADMIN_PASS_HASH);
            record_attempt($ok);
            if ($ok) {
                session_regenerate_id(true);
                $_SESSION['user'] = $u;
                header('Location: /admin/');
                exit;
            }
            usleep(400000);
            $error = 'Incorrect username or password.';
        }
    }
    admin_header('Log in');
    ?>
    <main class="login">
      <form method="post" class="panel stack">
        <img src="/assets/img/logo.svg" alt="DPayments" class="logo">
        <h1>Website portal</h1>
        <?php if ($error): ?><p class="err"><?= h($error) ?></p><?php endif; ?>
        <input type="hidden" name="csrf" value="<?= h(csrf_token()) ?>">
        <label>Username <input name="user" required autocomplete="username"></label>
        <label>Password <input type="password" name="pass" required autocomplete="current-password"></label>
        <button class="btn">Log in</button>
      </form>
    </main>
    <?php
    admin_footer();
    exit;
}

// ---------- Dashboard ----------
$pages = list_pages();
$enq = read_enquiries();
$groups = [];
foreach ($pages as $rel => $title) {
    $top = strpos($rel, '/') === false ? 'Main pages' : explode('/', $rel)[0];
    $label = ['Main pages' => 'Main pages', 'solutions' => 'Solutions', 'industries' => 'Industries'][$top] ?? 'Main pages';
    $groups[$label][$rel] = $title;
}
admin_header('Pages', 'pages');
?>
<main>
  <div class="head">
    <div>
      <h1>Pages</h1>
      <p class="muted">Click a page to edit its text. Changes go live about a minute after you save<?= storage_mode() === 'github' ? ' (published through GitHub)' : '' ?>.</p>
    </div>
    <a class="stat" href="/admin/enquiries.php"><b><?= count($enq) ?></b> enquir<?= count($enq) === 1 ? 'y' : 'ies' ?></a>
  </div>
  <?php if (storage_mode() === 'github' && (!defined('GITHUB_TOKEN') || GITHUB_TOKEN === '')): ?>
    <p class="err">GitHub token missing in <code>admin/config.php</code> &mdash; you won&rsquo;t be able to save until it&rsquo;s added.</p>
  <?php endif; ?>
  <?php foreach ($groups as $g => $items): ?>
    <h2><?= h($g) ?></h2>
    <div class="list">
      <?php foreach ($items as $rel => $title): ?>
        <a class="row" href="/admin/edit.php?p=<?= h(rawurlencode($rel)) ?>">
          <span><b><?= h(preg_replace('~\s*\|.*$~', '', $title)) ?></b><small><?= h(page_url($rel)) ?></small></span>
          <span class="go">Edit &rarr;</span>
        </a>
      <?php endforeach; ?>
    </div>
  <?php endforeach; ?>
</main>
<?php admin_footer();
