<?php
declare(strict_types=1);
require __DIR__ . '/lib.php';
require __DIR__ . '/templates.php';
require_login();

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    require_post();
    $pages = pages();
    $action = $_POST['action'] ?? '';
    try {
        if ($action === 'create') {
            $title = trim((string)($_POST['title'] ?? ''));
            $parent = trim((string)($_POST['parent'] ?? ''));
            $slug = trim((string)($_POST['slug'] ?? '')) ?: slugify($title);
            if ($parent !== '' && valid_slug($parent) && strpos($parent, '/') === false) $slug = $parent . '/' . $slug;
            if ($title === '') throw new RuntimeException('Please give the page a title.');
            if (!valid_slug($slug)) throw new RuntimeException('The address can only use lowercase letters, numbers and dashes.');
            if (isset($pages[$slug]) || in_array(explode('/', $slug)[0], ['admin', 'assets', 'uploads', 'blog', 'core', 'content', 'content-default'], true))
                throw new RuntimeException('A page with that address already exists or the address is reserved.');
            $copy = (string)($_POST['copy'] ?? '');
            $body = ($copy !== '' && isset($pages[$copy])) ? page_body($copy) : page_template((string)($_POST['template'] ?? 'standard'), $title);
            $pages[$slug] = ['title' => $title . ' | ' . (settings()['site_name'] ?? ''), 'description' => '', 'noindex' => false, 'core' => false, 'schema' => '', 'nav' => '', 'draft' => false, 'created' => gmdate('c')];
            write_file('pages/' . slug_file($slug), $body);
            write_json('pages.json', $pages);
            if (!empty($_POST['add_menu'])) {
                $m = menus();
                $m['header'][] = ['type' => 'link', 'label' => $title, 'url' => page_url($slug)];
                write_json('menus.json', $m);
            }
            flash('Page created. Click any text to edit it, and use "Add section" to build it out.');
            redirect('/admin/edit.php?page=' . rawurlencode($slug));
        }
        if ($action === 'delete') {
            $slug = (string)($_POST['slug'] ?? '');
            if (!isset($pages[$slug])) throw new RuntimeException('Page not found.');
            if (!empty($pages[$slug]['core'])) throw new RuntimeException('This page is part of the site structure and can’t be deleted. You can edit its content instead.');
            backup_file('pages/' . slug_file($slug));
            @unlink(content_path('pages/' . slug_file($slug)));
            unset($pages[$slug]);
            write_json('pages.json', $pages);
            flash('Page deleted. Remember to remove any menu links pointing to it.');
            redirect('/admin/pages.php');
        }
    } catch (Throwable $ex) {
        flash($ex->getMessage(), 'err');
        redirect('/admin/pages.php' . ($action === 'create' ? '#new' : ''));
    }
}

$pages = pages();
ksort($pages);
$groups = [];
foreach ($pages as $slug => $m) {
    $slug = (string)$slug;
    $top = strpos($slug, '/') !== false ? explode('/', $slug)[0] : '';
    $g = ['solutions' => 'Solutions', 'industries' => 'Industries'][$top] ?? ($top !== '' ? ucfirst($top) : 'Main pages');
    $groups[$g][$slug] = $m;
}
if (isset($groups['Main pages']['home'])) { $h = ['home' => $groups['Main pages']['home']]; unset($groups['Main pages']['home']); $groups['Main pages'] = $h + $groups['Main pages']; }
uksort($groups, fn($a, $b) => ($a === 'Main pages' ? -1 : ($b === 'Main pages' ? 1 : strcmp($a, $b))));
admin_header('Pages', 'pages');
?>
<main>
  <div class="head"><div><h1>Pages</h1><p class="muted">Edit any page, or add new ones. The blog has its own section.</p></div><a class="btn" href="#new">+ New page</a></div>
  <?php foreach ($groups as $g => $items): ?>
    <h2><?= e($g) ?></h2>
    <div class="list">
      <?php foreach ($items as $slug => $m): $slug = (string)$slug; ?>
        <div class="row">
          <a class="grow" href="/admin/edit.php?page=<?= e(rawurlencode((string)$slug)) ?>"><b><?= e(preg_replace('~\s*\|.*$~', '', $m['title'] ?? $slug)) ?></b><small><?= e($slug === '404' ? 'Page not found (404)' : page_url((string)$slug)) ?><?= !empty($m['draft']) ? ' · <em>hidden</em>' : '' ?></small></a>
          <span class="actions">
            <?php if ($slug !== '404'): ?><a href="<?= e(page_url((string)$slug)) ?>" target="_blank" rel="noopener" class="muted small">View</a><?php endif; ?>
            <a href="/admin/edit.php?page=<?= e(rawurlencode((string)$slug)) ?>" class="go">Edit</a>
            <?php if (empty($m['core'])): ?>
            <form method="post" onsubmit="return confirm('Delete this page? A backup is kept.')"><?= csrf_field() ?><input type="hidden" name="action" value="delete"><input type="hidden" name="slug" value="<?= e((string)$slug) ?>"><button class="link-danger">Delete</button></form>
            <?php endif; ?>
          </span>
        </div>
      <?php endforeach; ?>
    </div>
  <?php endforeach; ?>

  <h2 id="new">Add a new page</h2>
  <form method="post" class="panel stack" style="max-width:720px">
    <?= csrf_field() ?><input type="hidden" name="action" value="create">
    <label>Page title <input name="title" required maxlength="100" placeholder="e.g. About us" oninput="if(!this.form.slug.dataset.touched){this.form.slug.value=this.value.toLowerCase().replace(/[^a-z0-9]+/g,'-').replace(/^-|-$/g,'')}"></label>
    <div class="two">
      <label>Web address <span class="muted small"><?= e(preg_replace("~^https?://~", "", settings()["site_url"] ?? "")) ?>/<b>address</b>/</span><input name="slug" maxlength="70" pattern="[a-z0-9]+(-[a-z0-9]+)*" oninput="this.dataset.touched=1" placeholder="about-us"></label>
      <label>Inside section <span class="muted small">(optional)</span>
        <select name="parent"><option value="">— Top level —</option><option value="solutions">solutions/</option><option value="industries">industries/</option></select></label>
    </div>
    <div class="two">
      <label>Start from
        <select name="template"><option value="standard">Standard page (intro, text, call to action)</option><option value="landing">Landing page (features, image, steps, FAQ)</option><option value="blank">Blank (intro only)</option></select></label>
      <label>…or copy an existing page
        <select name="copy"><option value="">— Don’t copy —</option><?php foreach ($pages as $s => $m): if ($s === '404') continue; ?><option value="<?= e((string)$s) ?>"><?= e(preg_replace('~\s*\|.*$~', '', $m['title'] ?? $s)) ?></option><?php endforeach; ?></select></label>
    </div>
    <label class="check"><input type="checkbox" name="add_menu" value="1"> Add a link to this page in the top menu</label>
    <button class="btn">Create page</button>
  </form>
</main>
<?php admin_footer();
