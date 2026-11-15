<?php
declare(strict_types=1);
require __DIR__ . '/lib.php';
require_login();

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    require_post();
    $n = 0; $errs = [];
    $files = $_FILES['files'] ?? null;
    if ($files && is_array($files['name'])) {
        foreach ($files['name'] as $i => $name) {
            if ($name === '') continue;
            try { handle_upload(['name' => $name, 'tmp_name' => $files['tmp_name'][$i], 'error' => $files['error'][$i], 'size' => $files['size'][$i]]); $n++; }
            catch (Throwable $ex) { $errs[] = $name . ': ' . $ex->getMessage(); }
        }
    }
    flash($errs ? implode(' ', $errs) : $n . ' image' . ($n === 1 ? '' : 's') . ' uploaded.', $errs ? 'err' : 'ok');
    redirect('/admin/media.php');
}
$media = media_list();
admin_header('Media', 'media');
?>
<main>
  <div class="head"><div><h1>Media</h1><p class="muted">Images you upload here can be used on pages, posts and the industry tiles. Copy an image’s address to use it in HTML.</p></div></div>
  <form method="post" enctype="multipart/form-data" class="panel upload-box">
    <?= csrf_field() ?>
    <?= icon_svg('sparkle') ?>
    <div><b>Upload images</b><small class="muted">JPG, PNG, WebP or GIF, up to 6 MB each</small></div>
    <input type="file" name="files[]" multiple accept="image/jpeg,image/png,image/webp,image/gif" required>
    <button class="btn">Upload</button>
  </form>
  <div class="panel muted small" style="margin-top:14px">Tip: to show photos on the home page industry tiles, upload images named <code>retail</code>, <code>hospitality</code>, <code>hotels</code>, <code>ecommerce</code>, <code>igaming</code>, <code>forex</code>, <code>trades</code>, <code>automotive</code> or <code>professional</code> — then open the home page in the editor, switch to HTML, and point each tile’s <code>--img</code> at the image address.</div>
  <?php if (!$media): ?><p class="muted mt">No images yet.</p><?php else: ?>
  <div class="media-grid mt">
    <?php foreach ($media as $m): ?>
      <figure class="media-item">
        <a href="<?= e($m['url']) ?>" target="_blank" rel="noopener" class="mi-img" style="background-image:url('<?= e($m['url']) ?>')"></a>
        <figcaption><span title="<?= e($m['name']) ?>"><?= e($m['name']) ?></span><small><?= round($m['size'] / 1024) ?> KB</small></figcaption>
        <div class="mi-actions"><button type="button" class="copy" data-url="<?= e($m['url']) ?>">Copy address</button><button type="button" class="link-danger del" data-name="<?= e($m['name']) ?>">Delete</button></div>
      </figure>
    <?php endforeach; ?>
  </div>
  <?php endif; ?>
</main>
<script>
document.addEventListener('click', function (e) {
  var c = e.target.closest('.copy');
  if (c) { navigator.clipboard.writeText(location.origin + c.dataset.url).then(function () { c.textContent = 'Copied ✓'; setTimeout(function () { c.textContent = 'Copy address'; }, 1500); }); }
  var d = e.target.closest('.del');
  if (d && confirm('Delete this image? Pages using it will show a broken image.')) {
    var fd = new FormData(); fd.append('action', 'delete_media'); fd.append('csrf', <?= json_encode(csrf_token()) ?>); fd.append('name', d.dataset.name);
    fetch('/admin/api.php', { method: 'POST', body: fd, credentials: 'same-origin' }).then(function (r) { return r.json(); }).then(function (res) { if (res.ok) d.closest('figure').remove(); else alert(res.error); });
  }
});
</script>
<?php admin_footer();
