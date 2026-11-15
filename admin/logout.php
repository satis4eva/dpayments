<?php
declare(strict_types=1);
require __DIR__ . '/lib.php';
start_session();
if ($_SERVER['REQUEST_METHOD'] === 'POST' && check_csrf()) { $_SESSION = []; session_destroy(); }
redirect('/admin/');
