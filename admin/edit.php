<?php
declare(strict_types=1);
require __DIR__ . '/lib.php';
require_login();
header('X-Robots-Tag: noindex, nofollow');

$rel = (string)($_GET['p'] ?? '');
if (!valid_page($rel)) { header('Location: /admin/'); exit; }

$error = '';
$html = '';
$version = '';
try {
    [$html, $version] = read_page($rel);
} catch (Throwable $e) {
    $error = $e->getMessage();
}
[$title, $desc] = $html ? meta_of($html) : ['', ''];
$backups = storage_mode() === 'local' ? list_backups($rel) : [];

admin_header('Edit ' . page_url($rel), 'pages');
?>
<div class="editor-bar">
  <div class="left">
    <a href="/admin/" class="back">&larr; Pages</a>
    <strong><?= h(page_url($rel)) ?></strong>
    <a href="<?= h(page_url($rel)) ?>" target="_blank" rel="noopener" class="muted small">open live &#8599;</a>
  </div>
  <div class="right">
    <div class="seg" role="tablist">
      <button type="button" data-mode="visual" class="on">Edit text</button>
      <button type="button" data-mode="html">HTML</button>
      <button type="button" data-mode="seo">SEO</button>
    </div>
    <span id="status" class="muted small" aria-live="polite"></span>
    <button type="button" id="save" class="btn" disabled>Save &amp; publish</button>
  </div>
</div>

<?php if ($error): ?>
  <main><p class="err">Could not load this page: <?= h($error) ?></p></main>
<?php else: ?>
<div class="editor-wrap">
  <div class="hint" id="hint">
    Click any text to edit it. <kbd>Ctrl</kbd>/<kbd>&#8984;</kbd>+<kbd>B</kbd> for bold. <kbd>Alt</kbd>+click a link or button to change where it goes.
    FAQ answers are opened so you can edit them.
  </div>
  <iframe id="frame" title="Page editor"></iframe>
  <div id="html-pane" class="pane" hidden>
    <p class="muted small">Advanced: edit the HTML of the main content area. The header and footer are shared and not edited here.</p>
    <textarea id="html-src" class="code" spellcheck="false"></textarea>
  </div>
  <div id="seo-pane" class="pane narrow" hidden>
    <div class="panel stack">
      <h2>Search &amp; sharing</h2>
      <label>Page title <small class="muted">(shown in Google and browser tabs, ideally under 60 characters)</small>
        <input id="seo-title" value="<?= h($title) ?>" maxlength="120"></label>
      <label>Meta description <small class="muted">(the snippet under the title in Google, ideally 140&ndash;160 characters)</small>
        <textarea id="seo-desc" rows="3" maxlength="300"><?= h($desc) ?></textarea></label>
      <p class="muted small"><span id="seo-count"></span></p>
    </div>
    <?php if ($backups): ?>
    <div class="panel stack mt">
      <h2>Restore an earlier version</h2>
      <form method="post" action="/admin/api.php" onsubmit="return confirm('Restore this version? The current version will be backed up first.')">
        <input type="hidden" name="action" value="restore">
        <input type="hidden" name="csrf" value="<?= h(csrf_token()) ?>">
        <input type="hidden" name="page" value="<?= h($rel) ?>">
        <select name="backup"><?php foreach ($backups as $b): ?><option><?= h($b) ?></option><?php endforeach; ?></select>
        <button class="btn btn-ghost">Restore</button>
      </form>
    </div>
    <?php elseif (storage_mode() === 'github' && defined('GITHUB_REPO')): ?>
    <p class="muted small mt">Every save is a commit, so you can see and undo changes in the <a href="https://github.com/<?= h(GITHUB_REPO) ?>/commits/<?= h(GITHUB_BRANCH) ?>" target="_blank" rel="noopener">GitHub history</a>.</p>
    <?php endif; ?>
  </div>
</div>
<script>
window.DP_EDITOR = <?= json_encode([
    'page' => $rel,
    'version' => $version,
    'csrf' => csrf_token(),
    'html' => base64_encode($html),
    'mode' => storage_mode(),
], JSON_HEX_TAG | JSON_HEX_AMP | JSON_HEX_APOS | JSON_HEX_QUOT) ?>;
</script>
<script src="/admin/assets/editor.js"></script>
<?php endif; ?>
<?php admin_footer();
