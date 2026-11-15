<?php
declare(strict_types=1);
require __DIR__ . '/lib.php';
require_login();
$rows = read_enquiries();
$labels = ['switch' => 'Statement review', 'crypto' => 'Crypto', 'contact' => 'Quote'];

if (isset($_GET['csv'])) {
    header('Content-Type: text/csv; charset=utf-8');
    header('Content-Disposition: attachment; filename="enquiries-' . date('Y-m-d') . '.csv"');
    $out = fopen('php://output', 'w');
    fputcsv($out, ['Date (UTC)', 'Form', 'Name', 'Email', 'Business', 'Phone', 'Website', 'Industry', 'Volume', 'Takes payments', 'Message']);
    foreach ($rows as $r) {
        $cells = [$r['date'] ?? '', $labels[$r['source'] ?? ''] ?? '', $r['name'] ?? '', $r['email'] ?? '', $r['business'] ?? '', $r['phone'] ?? '', $r['site'] ?? '',
            $r['industry'] ?? '', $r['turnover'] ?? '', implode(', ', $r['channels'] ?? []), $r['message'] ?? ''];
        fputcsv($out, array_map(fn($c) => preg_match('/^[=+\-@]/', (string)$c) ? "'" . $c : $c, $cells));
    }
    exit;
}
admin_header('Enquiries', 'enquiries');
?>
<main>
  <div class="head"><div><h1>Enquiries</h1><p class="muted">Every form submission from the website. Each one is also emailed to <?= e(settings()['contact']['email'] ?? '') ?>.</p></div>
    <?php if ($rows): ?><a class="btn btn-ghost" href="?csv=1">Download CSV</a><?php endif; ?></div>
  <?php if (!$rows): ?><div class="panel empty"><?= icon_svg('mail') ?><h2>No enquiries yet</h2><p class="muted">They’ll appear here as soon as someone uses a form on the site.</p></div>
  <?php else: ?><div class="list">
    <?php foreach ($rows as $r): ?>
      <details class="enq"><summary><span><b><?= e($r['name'] ?? '') ?></b><?= !empty($r['business']) ? ' · ' . e($r['business']) : '' ?><small><?= e($r['email'] ?? '') ?></small></span>
        <span class="meta"><span class="tag"><?= e($labels[$r['source'] ?? ''] ?? 'Quote') ?></span><small><?= e($r['date'] ?? '') ?> UTC</small></span></summary>
        <dl>
          <dt>Email</dt><dd><a href="mailto:<?= e($r['email'] ?? '') ?>"><?= e($r['email'] ?? '') ?></a></dd>
          <?php foreach (['phone' => 'Phone', 'site' => 'Website', 'industry' => 'Industry', 'turnover' => 'Volume'] as $k => $l): if (!empty($r[$k])): ?><dt><?= $l ?></dt><dd><?= e($r[$k]) ?></dd><?php endif; endforeach; ?>
          <?php if (!empty($r['channels'])): ?><dt>Takes payments</dt><dd><?= e(implode(', ', $r['channels'])) ?></dd><?php endif; ?>
          <?php if (!empty($r['message'])): ?><dt>Message</dt><dd><?= nl2br(e($r['message'])) ?></dd><?php endif; ?>
        </dl></details>
    <?php endforeach; ?>
  </div><?php endif; ?>
</main>
<?php admin_footer();
