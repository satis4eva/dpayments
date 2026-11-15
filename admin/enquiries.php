<?php
declare(strict_types=1);
require __DIR__ . '/lib.php';
require_login();
header('X-Robots-Tag: noindex, nofollow');

$rows = read_enquiries();

if (isset($_GET['csv'])) {
    header('Content-Type: text/csv; charset=utf-8');
    header('Content-Disposition: attachment; filename="dpayments-enquiries-' . date('Y-m-d') . '.csv"');
    $out = fopen('php://output', 'w');
    fputcsv($out, ['Date (UTC)', 'Form', 'Name', 'Email', 'Business', 'Phone', 'Website', 'Industry', 'Turnover', 'Takes payments', 'Message']);
    foreach ($rows as $r) {
        $cells = [$r['date'] ?? '', $r['source'] ?? '', $r['name'] ?? '', $r['email'] ?? '', $r['business'] ?? '',
            $r['phone'] ?? '', $r['site'] ?? '', $r['industry'] ?? '', $r['turnover'] ?? '', implode(', ', $r['channels'] ?? []), $r['message'] ?? ''];
        // Prevent spreadsheet formula injection
        $cells = array_map(fn($c) => preg_match('/^[=+\-@]/', (string)$c) ? "'" . $c : $c, $cells);
        fputcsv($out, $cells);
    }
    exit;
}

admin_header('Enquiries', 'enquiries');
?>
<main>
  <div class="head">
    <div>
      <h1>Enquiries</h1>
      <p class="muted">Every quote and statement-review request from the website. Each one is also emailed to you.</p>
    </div>
    <?php if ($rows): ?><a class="btn btn-ghost" href="?csv=1">Download CSV</a><?php endif; ?>
  </div>
  <?php if (!$rows): ?>
    <div class="panel"><p class="muted">No enquiries yet. They&rsquo;ll appear here as soon as someone uses a form on the site.</p></div>
  <?php else: ?>
    <div class="list">
    <?php foreach ($rows as $r): ?>
      <details class="enq">
        <summary>
          <span><b><?= h($r['name'] ?? '') ?></b><?= !empty($r['business']) ? ' &middot; ' . h($r['business']) : '' ?>
            <small><?= h($r['email'] ?? '') ?></small></span>
          <span class="meta"><span class="tag"><?= ['switch' => 'Statement review', 'crypto' => 'Crypto'][$r['source'] ?? ''] ?? 'Quote' ?></span><small><?= h($r['date'] ?? '') ?></small></span>
        </summary>
        <dl>
          <dt>Email</dt><dd><a href="mailto:<?= h($r['email'] ?? '') ?>"><?= h($r['email'] ?? '') ?></a></dd>
          <?php foreach (['phone' => 'Phone', 'site' => 'Website', 'industry' => 'Industry', 'turnover' => 'Monthly volume'] as $k => $l): if (!empty($r[$k])): ?>
            <dt><?= $l ?></dt><dd><?= h($r[$k]) ?></dd>
          <?php endif; endforeach; ?>
          <?php if (!empty($r['channels'])): ?><dt>Takes payments</dt><dd><?= h(implode(', ', $r['channels'])) ?></dd><?php endif; ?>
          <?php if (!empty($r['message'])): ?><dt>Message</dt><dd class="msg"><?= nl2br(h($r['message'])) ?></dd><?php endif; ?>
        </dl>
      </details>
    <?php endforeach; ?>
    </div>
  <?php endif; ?>
</main>
<?php admin_footer();
