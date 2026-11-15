<?php
declare(strict_types=1);
require __DIR__ . '/lib.php';
require_login();

$s = settings();
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    require_post();
    $txt = fn($k, $n = 200) => mb_substr(trim((string)($_POST[$k] ?? '')), 0, $n);
    $col = fn($k, $d) => safe_color($_POST[$k] ?? null, $d);
    $tab = (string)($_POST['tab'] ?? 'brand');
    try {
        if ($tab === 'brand') {
            $s['site_name'] = $txt('site_name', 60) ?: ($s['site_name'] ?? 'Site');
            $s['tagline'] = $txt('tagline', 300);
            foreach (['logo', 'logo_dark', 'favicon'] as $k) {
                if (!empty($_FILES[$k]['name'])) $s[$k] = handle_upload($_FILES[$k]);
                elseif (!empty($_POST[$k . '_remove'])) $s[$k] = $k === 'favicon' ? '/assets/img/favicon.svg' : '';
            }
            $s['theme']['accent'] = $col('accent', '#0e9c74');
            $s['theme']['accent_dark'] = $col('accent_dark', mix($s['theme']['accent'], '#000000', .35));
            $s['theme']['ink'] = $col('ink', '#0d1b26');
            $s['theme']['bg'] = $col('bg', '#f6f7f4');
            $s['theme']['heading_font'] = in_array($_POST['heading_font'] ?? '', FONTS, true) ? $_POST['heading_font'] : 'Manrope';
            $s['theme']['body_font'] = in_array($_POST['body_font'] ?? '', FONTS, true) ? $_POST['body_font'] : 'Inter';
            $s['theme']['radius'] = max(0, min(30, (int)($_POST['radius'] ?? 14)));
        } elseif ($tab === 'contact') {
            foreach (['email' => 120, 'phone' => 40, 'whatsapp' => 40, 'hours' => 120, 'company_name' => 120, 'company_number' => 30, 'registered_address' => 200] as $k => $n) $s['contact'][$k] = $txt($k, $n);
            $s['contact']['address'] = $txt('address', 300);
            if ($s['contact']['email'] !== '' && !filter_var($s['contact']['email'], FILTER_VALIDATE_EMAIL)) throw new RuntimeException('Please enter a valid email address.');
            $s['topbar']['enabled'] = !empty($_POST['topbar_enabled']);
            $s['topbar']['text'] = $txt('topbar_text', 140);
        } elseif ($tab === 'social') {
            foreach (array_keys(SOCIAL_ICONS) as $k) {
                $u = $txt($k, 300);
                if ($u !== '' && !preg_match('~^https?://~', $u)) $u = 'https://' . $u;
                $s['social'][$k] = $u;
            }
        } elseif ($tab === 'advanced') {
            $url = rtrim($txt('site_url', 120), '/');
            if (preg_match('~^https?://[a-z0-9.-]+$~i', $url)) $s['site_url'] = $url;
            $s['footer_note'] = $txt('footer_note', 160);
            $from = $txt('form_from', 120);
            if ($from === '' || filter_var($from, FILTER_VALIDATE_EMAIL)) $s['form_from'] = $from;
            $s['analytics']['ga4'] = strtoupper($txt('ga4', 20));
            $s['analytics']['google_verification'] = $txt('google_verification', 100);
        }
        write_json('settings.json', $s);
        flash('Settings saved — live now.');
    } catch (Throwable $ex) { flash($ex->getMessage(), 'err'); }
    redirect('/admin/settings.php#' . $tab);
}

$t = $s['theme'] ?? []; $c = $s['contact'] ?? [];
function font_opts(string $sel): string { $o = ''; foreach (FONTS as $f) $o .= '<option' . ($f === $sel ? ' selected' : '') . '>' . e($f) . '</option>'; return $o; }
function img_field(string $name, string $label, ?string $val, string $help): string {
    return '<div class="imgfield"><label>' . $label . ' <small class="muted">' . $help . '</small></label><div class="imgrow"><div class="imgprev' . ($name === 'logo_dark' ? ' dark' : '') . '">'
        . ($val ? '<img src="' . e($val) . '" alt="">' : '<span class="muted small">Using default</span>') . '</div><input type="file" name="' . $name . '" accept="image/png,image/jpeg,image/webp,image/gif' . ($name === 'favicon' ? ',image/x-icon' : '') . '">'
        . ($val ? '<label class="check small"><input type="checkbox" name="' . $name . '_remove" value="1"> Use default</label>' : '') . '</div></div>';
}
admin_header('Brand & settings', 'settings');
?>
<main>
  <div class="head"><div><h1>Brand &amp; settings</h1><p class="muted">Changes apply to every page as soon as you save.</p></div></div>
  <nav class="tabs"><a href="#brand">Logo &amp; theme</a><a href="#contact">Contact details</a><a href="#social">Social media</a><a href="#advanced">Advanced</a></nav>

  <form method="post" enctype="multipart/form-data" class="panel stack tabpane" id="brand">
    <?= csrf_field() ?><input type="hidden" name="tab" value="brand">
    <h2>Logo &amp; theme</h2>
    <div class="two">
      <label>Business name <input name="site_name" value="<?= e($s['site_name'] ?? '') ?>" maxlength="60"></label>
      <label>Footer description <textarea name="tagline" rows="2" maxlength="300"><?= e($s['tagline'] ?? '') ?></textarea></label>
    </div>
    <?= img_field('logo', 'Logo', $s['logo'] ?? '', '(PNG with transparent background works best, about 400×100)') ?>
    <?= img_field('logo_dark', 'Logo for dark footer', $s['logo_dark'] ?? '', '(optional — a white version of your logo)') ?>
    <?= img_field('favicon', 'Browser icon', ($s['favicon'] ?? '') !== '/assets/img/favicon.svg' ? ($s['favicon'] ?? '') : '', '(square PNG, at least 64×64)') ?>
    <h3>Colours</h3>
    <div class="colors">
      <label>Brand colour <input type="color" name="accent" value="<?= e(safe_color($t['accent'] ?? null, '#0e9c74')) ?>"></label>
      <label>Brand colour (darker) <input type="color" name="accent_dark" value="<?= e(safe_color($t['accent_dark'] ?? null, '#076149')) ?>"></label>
      <label>Text &amp; dark sections <input type="color" name="ink" value="<?= e(safe_color($t['ink'] ?? null, '#0d1b26')) ?>"></label>
      <label>Page background <input type="color" name="bg" value="<?= e(safe_color($t['bg'] ?? null, '#f6f7f4')) ?>"></label>
    </div>
    <h3>Fonts &amp; shape</h3>
    <div class="three">
      <label>Headings font <select name="heading_font"><?= font_opts($t['heading_font'] ?? 'Manrope') ?></select></label>
      <label>Body font <select name="body_font"><?= font_opts($t['body_font'] ?? 'Inter') ?></select></label>
      <label>Corner roundness <input type="range" name="radius" min="0" max="30" value="<?= (int)($t['radius'] ?? 14) ?>" oninput="this.nextElementSibling.textContent=this.value+'px'"><small class="muted"><?= (int)($t['radius'] ?? 14) ?>px</small></label>
    </div>
    <div class="btn-row"><button class="btn">Save logo &amp; theme</button><a class="btn btn-ghost" href="/" target="_blank" rel="noopener">Preview site &#8599;</a></div>
  </form>

  <form method="post" class="panel stack tabpane" id="contact">
    <?= csrf_field() ?><input type="hidden" name="tab" value="contact">
    <h2>Contact details</h2>
    <p class="muted small">Shown in the footer on every page. In page content, use <code>{{email}}</code>, <code>{{phone}}</code> or <code>{{address}}</code> and they update automatically. Form enquiries are sent to the email below.</p>
    <div class="two">
      <label>Email <input type="email" name="email" value="<?= e($c['email'] ?? '') ?>"></label>
      <label>Phone <input name="phone" value="<?= e($c['phone'] ?? '') ?>" placeholder="+44 20 0000 0000"></label>
      <label>WhatsApp number <input name="whatsapp" value="<?= e($c['whatsapp'] ?? '') ?>" placeholder="+44 7000 000000"></label>
      <label>Opening hours <input name="hours" value="<?= e($c['hours'] ?? '') ?>" placeholder="Mon–Fri, 9am–6pm"></label>
    </div>
    <label>Address <textarea name="address" rows="3"><?= e($c['address'] ?? '') ?></textarea></label>
    <h3>Company information <small class="muted">(shown at the bottom of every page)</small></h3>
    <div class="three">
      <label>Registered company name <input name="company_name" value="<?= e($c['company_name'] ?? '') ?>" placeholder="e.g. DBS Group Ltd"></label>
      <label>Company number <input name="company_number" value="<?= e($c['company_number'] ?? '') ?>"></label>
      <label>Registered office <input name="registered_address" value="<?= e($c['registered_address'] ?? '') ?>"></label>
    </div>
    <h3>Top bar</h3>
    <label class="check"><input type="checkbox" name="topbar_enabled" value="1" <?= !empty($s['topbar']['enabled']) ? 'checked' : '' ?>> Show a thin bar above the menu with your phone and email</label>
    <label>Top bar message <small class="muted">(optional)</small><input name="topbar_text" value="<?= e($s['topbar']['text'] ?? '') ?>" placeholder="e.g. Free statement reviews for UK merchants"></label>
    <button class="btn">Save contact details</button>
  </form>

  <form method="post" class="panel stack tabpane" id="social">
    <?= csrf_field() ?><input type="hidden" name="tab" value="social">
    <h2>Social media</h2>
    <p class="muted small">Icons appear in the footer for each link you add. Leave blank to hide.</p>
    <div class="two">
      <?php foreach (['linkedin' => 'LinkedIn', 'facebook' => 'Facebook', 'instagram' => 'Instagram', 'x' => 'X (Twitter)', 'youtube' => 'YouTube', 'tiktok' => 'TikTok'] as $k => $l): ?>
        <label><?= $l ?> <input name="<?= $k ?>" value="<?= e($s['social'][$k] ?? '') ?>" placeholder="https://"></label>
      <?php endforeach; ?>
    </div>
    <button class="btn">Save social links</button>
  </form>

  <form method="post" class="panel stack tabpane" id="advanced">
    <?= csrf_field() ?><input type="hidden" name="tab" value="advanced">
    <h2>Advanced</h2>
    <div class="two">
      <label>Website address <input name="site_url" value="<?= e($s['site_url'] ?? '') ?>"></label>
      <label>Footer line <input name="footer_note" value="<?= e($s['footer_note'] ?? '') ?>"></label>
      <label>Send form emails from <input name="form_from" value="<?= e($s['form_from'] ?? '') ?>"><small class="muted">Must be a mailbox on your domain</small></label>
    </div>
    <h3>Google</h3>
    <div class="two">
      <label>Google Analytics ID <input name="ga4" value="<?= e($s['analytics']['ga4'] ?? '') ?>" placeholder="G-XXXXXXXXXX"><small class="muted">If you add analytics, update your cookie policy page and consider a consent banner.</small></label>
      <label>Search Console verification code <input name="google_verification" value="<?= e($s['analytics']['google_verification'] ?? '') ?>" placeholder="the content=&quot;…&quot; value only"></label>
    </div>
    <button class="btn">Save</button>
  </form>
</main>
<script>
(function(){var tabs=document.querySelectorAll('.tabs a'),panes=document.querySelectorAll('.tabpane');
function show(){var h=location.hash.slice(1)||'brand';panes.forEach(function(p){p.hidden=p.id!==h});tabs.forEach(function(a){a.classList.toggle('on',a.getAttribute('href')==='#'+h)});}
window.addEventListener('hashchange',show);show();})();
</script>
<?php admin_footer();
