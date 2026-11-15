<?php
declare(strict_types=1);
require __DIR__ . '/lib.php';
require __DIR__ . '/templates.php';
require_login();

$slug = (string)($_GET['page'] ?? '');
$pages = pages();
if (!isset($pages[$slug])) { flash('Page not found.', 'err'); redirect('/admin/pages.php'); }
$meta = $pages[$slug];
$html = render_page($slug, null, true);
$blocks = [];
foreach (BLOCKS as $k => $label) $blocks[$k] = ['label' => $label, 'html' => apply_tokens(block_html($k), true)];
$title = preg_replace('~\s*\|.*$~', '', $meta['title'] ?? $slug);

admin_header('Edit ' . $title, 'pages', true);
?>
<div class="editor-bar">
  <div class="left">
    <a href="/admin/pages.php" class="back">&larr; Pages</a>
    <strong><?= e($title) ?></strong>
    <?php if ($slug !== '404'): ?><a href="<?= e(page_url($slug)) ?>" target="_blank" rel="noopener" class="muted small">view live &#8599;</a><?php endif; ?>
  </div>
  <div class="right">
    <div class="seg" role="tablist">
      <button type="button" data-mode="visual" class="on">Edit page</button>
      <button type="button" data-mode="html">HTML</button>
      <button type="button" data-mode="seo">Page settings</button>
    </div>
    <span id="status" class="muted small" aria-live="polite"></span>
    <button type="button" id="save" class="btn" disabled>Save</button>
  </div>
</div>
<div class="editor-wrap">
  <div class="hint" id="hint">
    <span>Click text to edit &middot; <kbd>Ctrl</kbd>+<kbd>B</kbd> bold &middot; <kbd>Alt</kbd>+click a link or button to change it &middot; click an image to replace it &middot; hover a section to move, copy or delete it</span>
    <span class="hint-actions">
      <button type="button" class="btn btn-sm" id="add-block">+ Add section</button>
    </span>
  </div>
  <div id="block-menu" class="block-menu" hidden>
    <p class="muted small">Adds below the section you last clicked (or at the end).</p>
    <div class="block-grid">
      <?php foreach (BLOCKS as $k => $label): ?><button type="button" data-block="<?= e($k) ?>"><?= e($label) ?></button><?php endforeach; ?>
    </div>
  </div>
  <iframe id="frame" title="Page editor"></iframe>
  <div id="html-pane" class="pane" hidden>
    <p class="muted small">Advanced: the HTML of this page&rsquo;s content (header and footer are managed under Menus and Settings). Tokens like <code>{{email}}</code>, <code>{{phone}}</code> and <code>{{address}}</code> are replaced with your contact details.</p>
    <textarea id="html-src" class="code" spellcheck="false"></textarea>
  </div>
  <div id="seo-pane" class="pane" hidden>
    <div class="panel stack" style="max-width:760px">
      <h2>Search &amp; sharing</h2>
      <label>Page title <small class="muted">(shown in Google and the browser tab — about 60 characters)</small>
        <input id="seo-title" value="<?= e($meta['title'] ?? '') ?>" maxlength="140"></label>
      <label>Description <small class="muted">(the snippet under the title in Google — about 150 characters)</small>
        <textarea id="seo-desc" rows="3" maxlength="320"><?= e($meta['description'] ?? '') ?></textarea></label>
      <p class="muted small" id="seo-count"></p>
      <label class="check"><input type="checkbox" id="seo-noindex" <?= !empty($meta['noindex']) ? 'checked' : '' ?>> Hide from Google (noindex)</label>
      <?php if (empty($meta['core'])): ?>
      <label class="check"><input type="checkbox" id="seo-draft" <?= !empty($meta['draft']) ? 'checked' : '' ?>> Hidden — only visible here in the editor, not on the live site</label>
      <?php endif; ?>
      <p class="muted small">Web address: <code><?= e($slug === '404' ? '(shown for missing pages)' : page_url($slug)) ?></code></p>
    </div>
    <div class="panel stack mt" style="max-width:760px">
      <h2>Earlier versions</h2>
      <p class="muted small">A copy is kept every time you save (the last 15 versions).</p>
      <?php $bks = glob(CONTENT_DIR . '/_backups/pages__' . str_replace('/', '__', $slug) . '.html.*.bak') ?: []; rsort($bks); ?>
      <?php if ($bks): ?>
        <form method="post" action="/admin/api.php" class="inline" onsubmit="return confirm('Restore this version? Your current version will be kept as a backup.')">
          <?= csrf_field() ?><input type="hidden" name="action" value="restore_page"><input type="hidden" name="page" value="<?= e($slug) ?>">
          <select name="backup"><?php foreach ($bks as $b): $bn = basename($b); preg_match('~\.(\d{8})-(\d{6})\.bak$~', $bn, $mm); ?><option value="<?= e($bn) ?>"><?= e(isset($mm[1]) ? date('j M Y, H:i', strtotime($mm[1] . ' ' . $mm[2])) : $bn) ?></option><?php endforeach; ?></select>
          <button class="btn btn-ghost">Restore</button>
        </form>
      <?php else: ?><p class="muted small">No earlier versions yet.</p><?php endif; ?>
    </div>
  </div>
</div>
<input type="file" id="img-file" accept="image/jpeg,image/png,image/webp,image/gif" hidden>
<script>
window.DP = <?= json_encode([
    'kind' => 'page', 'page' => $slug, 'csrf' => csrf_token(),
    'html' => base64_encode($html), 'blocks' => $blocks,
], JSON_HEX_TAG | JSON_HEX_AMP | JSON_HEX_APOS | JSON_HEX_QUOT) ?>;
</script>
<script src="/admin/assets/editor.js?v=<?= @filemtime(__DIR__ . '/assets/editor.js') ?>"></script>
<?php admin_footer();
