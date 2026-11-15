<?php
declare(strict_types=1);
require __DIR__ . '/lib.php';
require_login();

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    require_post();
    $posts = posts();
    if (($_POST['action'] ?? '') === 'delete') {
        $slug = (string)($_POST['slug'] ?? '');
        if (isset($posts[$slug])) {
            backup_file('posts/' . $slug . '.html');
            @unlink(content_path('posts/' . $slug . '.html'));
            unset($posts[$slug]);
            write_json('posts.json', $posts);
            flash('Post deleted.');
        }
    }
    if (($_POST['action'] ?? '') === 'blog_settings') {
        $s = settings();
        $s['blog']['title'] = mb_substr(trim((string)($_POST['blog_title'] ?? 'Blog')), 0, 60) ?: 'Blog';
        $s['blog']['intro'] = mb_substr(trim((string)($_POST['blog_intro'] ?? '')), 0, 300);
        write_json('settings.json', $s);
        flash('Blog settings saved.');
    }
    if (($_POST['action'] ?? '') === 'add_menu') {
        $m = menus();
        $m['header'][] = ['type' => 'link', 'label' => settings()['blog']['title'] ?? 'Blog', 'url' => '/blog/'];
        write_json('menus.json', $m);
        flash('Blog added to the top menu. You can move it under Menus.');
    }
    redirect('/admin/blog.php');
}

$posts = posts();
uasort($posts, fn($a, $b) => strcmp($b['date'] ?? '', $a['date'] ?? ''));
$inMenu = strpos(json_encode(menus()), '"\/blog\/"') !== false || strpos(json_encode(menus()), '"/blog/"') !== false;
admin_header('Blog', 'blog');
?>
<main>
  <div class="head"><div><h1>Blog</h1><p class="muted">Posts appear at <a href="/blog/" target="_blank" rel="noopener">/blog/</a> once published.</p></div><a class="btn" href="/admin/post.php">+ New post</a></div>
  <?php if (!$inMenu): ?>
    <form method="post" class="notice"><?= csrf_field() ?><input type="hidden" name="action" value="add_menu"><span>The blog isn’t in your menu yet.</span><button class="btn btn-ghost btn-sm">Add “<?= e(settings()['blog']['title'] ?? 'Blog') ?>” to the top menu</button></form>
  <?php endif; ?>
  <?php if (!$posts): ?>
    <div class="panel empty"><?= icon_svg('receipt') ?><h2>No posts yet</h2><p class="muted">Share news, guides or updates. Posts help people find you on Google.</p><a class="btn" href="/admin/post.php">Write your first post</a></div>
  <?php else: ?>
    <div class="list">
      <?php foreach ($posts as $slug => $p): ?>
        <div class="row">
          <a class="grow post-row" href="/admin/post.php?slug=<?= e(rawurlencode((string)$slug)) ?>">
            <span class="thumb" style="<?= !empty($p['cover']) ? "background-image:url('" . e($p['cover']) . "')" : '' ?>"></span>
            <span><b><?= e($p['title'] ?? $slug) ?></b><small><?= e(format_date($p['date'] ?? '')) ?><?= !empty($p['category']) ? ' · ' . e($p['category']) : '' ?></small></span>
          </a>
          <span class="actions">
            <span class="pill-status <?= ($p['status'] ?? '') === 'published' ? 'pub' : '' ?>"><?= ($p['status'] ?? '') === 'published' ? 'Published' : 'Draft' ?></span>
            <?php if (($p['status'] ?? '') === 'published'): ?><a class="muted small" href="/blog/<?= e((string)$slug) ?>/" target="_blank" rel="noopener">View</a><?php endif; ?>
            <a class="go" href="/admin/post.php?slug=<?= e(rawurlencode((string)$slug)) ?>">Edit</a>
            <form method="post" onsubmit="return confirm('Delete this post?')"><?= csrf_field() ?><input type="hidden" name="action" value="delete"><input type="hidden" name="slug" value="<?= e((string)$slug) ?>"><button class="link-danger">Delete</button></form>
          </span>
        </div>
      <?php endforeach; ?>
    </div>
  <?php endif; ?>
  <h2>Blog settings</h2>
  <form method="post" class="panel stack" style="max-width:720px">
    <?= csrf_field() ?><input type="hidden" name="action" value="blog_settings">
    <label>Blog name <input name="blog_title" value="<?= e(settings()['blog']['title'] ?? 'Blog') ?>" maxlength="60"></label>
    <label>Introduction <textarea name="blog_intro" rows="2" maxlength="300"><?= e(settings()['blog']['intro'] ?? '') ?></textarea></label>
    <button class="btn">Save</button>
  </form>
</main>
<?php admin_footer();
