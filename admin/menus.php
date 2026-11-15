<?php
declare(strict_types=1);
require __DIR__ . '/lib.php';
require_login();
$urls = ['/blog/'];
foreach (pages() as $s => $m) if ($s !== '404') $urls[page_url((string)$s)] = preg_replace('~\s*\|.*$~', '', $m['title'] ?? '');
admin_header('Menus', 'menus');
?>
<main class="menus">
  <div class="head"><div><h1>Menus</h1><p class="muted">The top menu, the “Get a quote” button and the footer links. Drag order with the arrows. Changes go live when you save.</p></div>
    <div><span id="status" class="small muted"></span> <button class="btn" id="save" disabled>Save menus</button></div></div>

  <h2>Top menu</h2>
  <div id="header-items" class="stack"></div>
  <div class="btn-row"><button type="button" class="btn btn-ghost btn-sm" data-add="link">+ Add link</button><button type="button" class="btn btn-ghost btn-sm" data-add="mega">+ Add dropdown</button></div>

  <h2>Button (right of the menu)</h2>
  <div class="panel two" id="cta"></div>

  <h2>Footer columns</h2>
  <div id="footer-cols" class="grid-cols"></div>
  <div class="btn-row"><button type="button" class="btn btn-ghost btn-sm" id="add-footer">+ Add footer column</button></div>

  <h2>Small links (bottom of footer)</h2>
  <div class="panel" id="legal"></div>

  <datalist id="page-urls"><?php foreach ($urls as $u => $t): ?><option value="<?= e(is_int($u) ? $t : $u) ?>"><?= e(is_int($u) ? 'Blog' : $t) ?></option><?php endforeach; ?></datalist>
</main>
<script>
window.DP = <?= json_encode(['csrf' => csrf_token(), 'menus' => menus(), 'icons' => icon_names()], JSON_HEX_TAG | JSON_HEX_AMP) ?>;
</script>
<script src="/admin/assets/menus.js?v=<?= @filemtime(__DIR__ . '/assets/menus.js') ?>"></script>
<?php admin_footer();
