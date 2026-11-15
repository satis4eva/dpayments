<?php
/**
 * DPayments enquiry form handler (Hostinger / any PHP host).
 * Emails the enquiry to TO_EMAIL and redirects to /thank-you/.
 */

const TO_EMAIL   = 'info@dpayments.co.uk';
const FROM_EMAIL = 'noreply@dpayments.co.uk'; // must be a mailbox/domain on your hosting for best deliverability

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    header('Location: /contact/');
    exit;
}

function field(string $key, int $max = 500): string {
    $v = isset($_POST[$key]) && is_string($_POST[$key]) ? trim($_POST[$key]) : '';
    $v = str_replace(["\r", "\0"], '', $v);
    return mb_substr($v, 0, $max);
}

function back(string $source, string $error): void {
    $pages = ['switch' => '/switch/', 'crypto' => '/crypto/', 'contact' => '/contact/'];
    $anchors = ['switch' => '#review', 'crypto' => '#apply', 'contact' => ''];
    header('Location: ' . $pages[$source] . '?error=' . urlencode($error) . $anchors[$source]);
    exit;
}

$source = field('source', 20);
if (!in_array($source, ['switch', 'crypto'], true)) $source = 'contact';

// Honeypot: bots fill this in. Pretend success.
if (field('website') !== '') {
    header('Location: /thank-you/');
    exit;
}

$name     = str_replace("\n", ' ', field('name', 120));
$email    = str_replace("\n", '', field('email', 160));
$business = str_replace("\n", ' ', field('business', 160));
$phone    = str_replace("\n", ' ', field('phone', 40));
$industry = str_replace("\n", ' ', field('industry', 80));
$turnover = str_replace("\n", ' ', field('turnover', 80));
$message  = field('message', 4000);
$site     = str_replace("\n", '', field('site', 200));

$allowed  = ['in-person' => 'In person', 'online' => 'Online', 'phone' => 'Over the phone', 'not-yet' => 'Not yet'];
$channels = [];
if (!empty($_POST['channels']) && is_array($_POST['channels'])) {
    foreach ($_POST['channels'] as $c) {
        if (is_string($c) && isset($allowed[$c])) $channels[] = $allowed[$c];
    }
}

if ($name === '' || !filter_var($email, FILTER_VALIDATE_EMAIL)) {
    back($source, 'missing');
}

$subjectPrefix = ['switch' => 'Statement review request', 'crypto' => 'Crypto merchant application', 'contact' => 'Quote request'][$source];
$subject = $subjectPrefix . ' — ' . ($business !== '' ? $business : $name);

$lines = [
    'New enquiry from dpayments.co.uk (' . ['switch' => 'Switch & save', 'crypto' => 'Crypto payments', 'contact' => 'Get a quote'][$source] . ')',
    '',
    'Name:       ' . $name,
    'Email:      ' . $email,
    'Business:   ' . ($business ?: '—'),
    'Phone:      ' . ($phone ?: '—'),
    'Website:    ' . ($site ?: '—'),
    'Industry:   ' . ($industry ?: '—'),
    'Turnover:   ' . ($turnover ?: '—'),
    'Takes cards: ' . ($channels ? implode(', ', $channels) : '—'),
    '',
    'Message:',
    $message !== '' ? $message : '—',
    '',
    '---',
    'Sent: ' . gmdate('Y-m-d H:i') . ' UTC',
    'IP: ' . ($_SERVER['REMOTE_ADDR'] ?? 'unknown'),
];
$body = implode("\n", $lines);

$headers = [
    'From: DPayments Website <' . FROM_EMAIL . '>',
    'Reply-To: ' . $name . ' <' . $email . '>',
    'MIME-Version: 1.0',
    'Content-Type: text/plain; charset=UTF-8',
    'Content-Transfer-Encoding: 8bit',
];

// Store a copy for the website portal (admin/data is blocked from public access)
$dataDir = __DIR__ . '/admin/data';
if (is_dir($dataDir) && is_writable($dataDir)) {
    $record = [
        'date' => gmdate('Y-m-d H:i'), 'source' => $source, 'name' => $name, 'email' => $email,
        'business' => $business, 'phone' => $phone, 'site' => $site, 'industry' => $industry, 'turnover' => $turnover,
        'channels' => $channels, 'message' => $message,
    ];
    @file_put_contents($dataDir . '/enquiries.jsonl', json_encode($record, JSON_UNESCAPED_UNICODE) . "\n", FILE_APPEND | LOCK_EX);
}

$encodedSubject ='=?UTF-8?B?' . base64_encode($subject) . '?=';
$ok = @mail(TO_EMAIL, $encodedSubject, $body, implode("\r\n", $headers), '-f' . FROM_EMAIL);

if (!$ok) {
    back($source, 'send');
}

header('Location: /thank-you/');
exit;
