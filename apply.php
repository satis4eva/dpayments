<?php
// DPayments merchant application handler: emails each application to the sales inbox.
$to = 'info@dpayments.co.uk';
$from = 'no-reply@dpayments.co.uk';

function clean($v, $max = 500) {
    $v = trim((string)($v ?? ''));
    $v = str_replace(["\r", "\n"], ' ', $v);
    return mb_substr(strip_tags($v), 0, $max);
}

function page($title, $msg) {
    $t = htmlspecialchars($title);
    $m = htmlspecialchars($msg);
    echo "<!doctype html><html lang=\"en\"><head><meta charset=\"utf-8\"><meta name=\"viewport\" content=\"width=device-width, initial-scale=1\"><title>$t | DPayments</title></head>"
       . "<body style=\"margin:0;font-family:Inter,system-ui,sans-serif;background:#0B1726;color:#fff;min-height:100vh;display:flex;align-items:center;justify-content:center;padding:24px;box-sizing:border-box\">"
       . "<div style=\"max-width:520px;text-align:center\"><h1 style=\"font-size:36px;margin:0 0 16px\">$t</h1><p style=\"font-size:18px;line-height:1.6;color:#CBD5E1\">$m</p>"
       . "<p><a href=\"/\" style=\"display:inline-block;margin-top:16px;background:#2DD4AA;color:#0B1726;text-decoration:none;padding:14px 24px;border-radius:8px;font-weight:600\">Back to DPayments</a></p></div></body></html>";
    exit;
}

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    header('Location: /#apply');
    exit;
}

// Honeypot: bots fill hidden fields.
if (!empty($_POST['company_url'])) {
    page('Thank you', 'Your application has been received.');
}

$name     = clean($_POST['name'] ?? '', 120);
$email    = clean($_POST['email'] ?? '', 200);
$company  = clean($_POST['company'] ?? '', 200);
$website  = clean($_POST['website'] ?? '', 300);
$industry = clean($_POST['industry'] ?? '', 100);
$volume   = clean($_POST['volume'] ?? '', 100);
$notes    = mb_substr(strip_tags(trim((string)($_POST['notes'] ?? ''))), 0, 3000);

if ($name === '' || $company === '' || !filter_var($email, FILTER_VALIDATE_EMAIL)) {
    page('Please check your details', 'Name, company and a valid email address are required. Please go back and try again.');
}

$subject = "New merchant application: $company";
$body = "New merchant application from crypto.dpayments.co.uk\n\n"
      . "Name: $name\nEmail: $email\nCompany: $company\nWebsite: $website\n"
      . "Industry: $industry\nExpected monthly volume: $volume\n\nNotes:\n$notes\n\n"
      . "Submitted: " . gmdate('Y-m-d H:i') . " UTC\nIP: " . ($_SERVER['REMOTE_ADDR'] ?? '') . "\n";

$headers = "From: DPayments Website <$from>\r\n"
         . "Reply-To: $email\r\n"
         . "Content-Type: text/plain; charset=UTF-8\r\n";

if (mail($to, $subject, $body, $headers, "-f$from")) {
    page('Thank you', 'Your application has been received. Our team will be in touch shortly.');
}
page('Something went wrong', 'We could not send your application. Please email us at info@dpayments.co.uk.');
