<?php
declare(strict_types=1);
require __DIR__ . '/lib.php';
require_login();

$posts = posts();
$slug = (string)($_GET['slug'] ?? '');
$isNew = $slug === '' || !isset($posts[$slug]);
$p = $isNew ? ['title' => '', 'date' => date('Y-m-d'), 'status' => 'draft', 'category' => '', 'excerpt' => '', 'cover' => '', 'author' => '', 'seo_title' => ''] : $posts[$slug];
$body = $isNew ? '<p>Start writing here…</p>' : post_body($slug);
$err = '';

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    require_post();
    $title = trim((string)($_POST['title'] ?? ''));
    $newSlug = trim((string)($_POST['slug'] ?? '')) ?: slugify($title);
    $newSlug = strtolower($newSlug);
    $data = [
        'title' => mb_substr($title, 0, 160),
        'date' => preg_match('~^\d{4}-\d{2}-\d{2}$~', (string)($_POST['date'] ?? '')) ? $_POST['date'] : date('Y-m-d'),
        'status' => ($_POST['status'] ?? '') === 'published' ? 'published' : 'draft',
        'category' => mb_substr(trim((string)($_POST['category'] ?? '')), 0, 40),
        'excerpt' => mb_substr(trim((string)($_POST['excerpt'] ?? '')), 0, 300),
        'cover' => preg_match('~^/uploads/[a-z0-9-]+\.(jpg|jpeg|png|webp|gif)$~', (string)($_POST['cover'] ?? '')) ? $_POST['cover'] : '',
        'author' => mb_substr(trim((string)($_POST['author'] ?? '')), 0, 60),
        'seo_title' => mb_substr(trim((string)($_POST['seo_title'] ?? '')), 0, 140),
        'updated' => gmdate('c'),
    ];
    $html = clean_html((string)($_POST['body'] ?? ''));
    if ($title === '') $err = 'Please add a title.';
    elseif (!preg_match('~^[a-z0-9]+(-[a-z0-9]+)*$~', $newSlug)) $err = 'The web address can only use lowercase letters, numbers and dashes.';
    elseif ($newSlug !== $slug && isset($posts[$newSlug])) $err = 'Another post already uses that web address.';
    else {
        if (!$isNew && $newSlug !== $slug) { @rename(content_path('posts/' . $slug . '.html'), content_path('posts/' . $newSlug . '.html')); unset($posts[$slug]); }
        if ($data['excerpt'] === '') $data['excerpt'] = mb_substr(trim(preg_replace('~\s+~', ' ', html_entity_decode(strip_tags($html)))), 0, 180);
        $posts[$newSlug] = ($isNew ? ['created' => gmdate('c')] : []) + $data + ($posts[$newSlug] ?? []);
        $posts[$newSlug] = array_merge($posts[$newSlug], $data);
        write_file('posts/' . $newSlug . '.html', $html);
        write_json('posts.json', $posts);
        flash($data['status'] === 'published' ? 'Post published.' : 'Draft saved.');
        redirect('/admin/post.php?slug=' . rawurlencode($newSlug));
    }
    $p = $data; $body = $html; $slug = $newSlug;
}

admin_header($isNew ? 'New post' : 'Edit post', 'blog');
?>
<main class="post-editor">
  <div class="head"><div><a href="/admin/blog.php" class="back">&larr; Blog</a><h1><?= $isNew ? 'New post' : 'Edit post' ?></h1></div>
    <?php if (!$isNew && ($p['status'] ?? '') === 'published'): ?><a class="btn btn-ghost" href="/blog/<?= e($slug) ?>/" target="_blank" rel="noopener">View post &#8599;</a><?php endif; ?></div>
  <?php if ($err): ?><p class="err"><?= e($err) ?></p><?php endif; ?>
  <form method="post" id="post-form" class="post-grid-admin">
    <?= csrf_field() ?>
    <div class="stack">
      <input class="title-input" name="title" value="<?= e($p['title'] ?? '') ?>" placeholder="Post title" required maxlength="160">
      <div class="rte">
        <div class="rte-bar" role="toolbar">
          <button type="button" data-cmd="formatBlock" data-val="H2" title="Heading">H2</button>
          <button type="button" data-cmd="formatBlock" data-val="H3" title="Subheading">H3</button>
          <button type="button" data-cmd="formatBlock" data-val="P" title="Paragraph">¶</button>
          <span class="sep"></span>
          <button type="button" data-cmd="bold" title="Bold"><b>B</b></button>
          <button type="button" data-cmd="italic" title="Italic"><i>I</i></button>
          <button type="button" data-cmd="insertUnorderedList" title="Bullet list">• List</button>
          <button type="button" data-cmd="insertOrderedList" title="Numbered list">1. List</button>
          <button type="button" data-cmd="formatBlock" data-val="BLOCKQUOTE" title="Quote">“ Quote</button>
          <span class="sep"></span>
          <button type="button" data-act="link" title="Link">Link</button>
          <button type="button" data-act="image" title="Image">Image</button>
          <button type="button" data-act="video" title="YouTube">Video</button>
          <button type="button" data-act="html" title="Edit HTML">&lt;/&gt;</button>
        </div>
        <div class="rte-body prose" contenteditable="true" id="rte"><?= $body ?></div>
        <textarea class="code rte-html" id="rte-html" hidden spellcheck="false"></textarea>
      </div>
      <input type="hidden" name="body" id="body-field">
    </div>
    <aside class="stack">
      <div class="panel stack">
        <label>Status <select name="status"><option value="draft">Draft (not visible)</option><option value="published" <?= ($p['status'] ?? '') === 'published' ? 'selected' : '' ?>>Published</option></select></label>
        <label>Date <input type="date" name="date" value="<?= e($p['date'] ?? date('Y-m-d')) ?>"></label>
        <button class="btn">Save</button>
      </div>
      <div class="panel stack">
        <label>Cover image</label>
        <div class="cover-pick" id="cover-pick" style="<?= !empty($p['cover']) ? "background-image:url('" . e($p['cover']) . "')" : '' ?>"><span><?= empty($p['cover']) ? 'Click to upload' : '' ?></span></div>
        <input type="hidden" name="cover" id="cover" value="<?= e($p['cover'] ?? '') ?>">
        <button type="button" class="link-danger small" id="cover-remove" <?= empty($p['cover']) ? 'hidden' : '' ?>>Remove cover</button>
        <label>Category <input name="category" value="<?= e($p['category'] ?? '') ?>" maxlength="40" placeholder="e.g. News or Articles" list="cats">
          <datalist id="cats"><?php foreach (array_unique(array_merge(['News', 'Articles', 'Guides'], array_filter(array_column(posts(), 'category')))) as $c): ?><option value="<?= e($c) ?>"><?php endforeach; ?></datalist></label>
        <label>Author <input name="author" value="<?= e($p['author'] ?? '') ?>" maxlength="60"></label>
        <label>Summary <small class="muted">(shown on the blog page and in Google)</small><textarea name="excerpt" rows="3" maxlength="300"><?= e($p['excerpt'] ?? '') ?></textarea></label>
      </div>
      <div class="panel stack">
        <label>Web address <small class="muted">/blog/<b>address</b>/</small><input name="slug" value="<?= e($isNew ? '' : $slug) ?>" pattern="[a-z0-9]+(-[a-z0-9]+)*" placeholder="made from the title"></label>
        <label>Google title <small class="muted">(optional)</small><input name="seo_title" value="<?= e($p['seo_title'] ?? '') ?>" maxlength="140"></label>
      </div>
    </aside>
  </form>
</main>
<input type="file" id="file" accept="image/jpeg,image/png,image/webp,image/gif" hidden>
<script>window.DP = {csrf: <?= json_encode(csrf_token()) ?>};</script>
<script src="/admin/assets/post.js?v=<?= @filemtime(__DIR__ . '/assets/post.js') ?>"></script>
<?php admin_footer();
