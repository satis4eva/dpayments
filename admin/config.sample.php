<?php
/**
 * DPayments website portal — configuration.
 *
 * 1. Copy this file to config.php (same folder) on your Hostinger server
 *    using hPanel → File Manager. Never commit config.php to GitHub.
 * 2. Visit https://dpayments.co.uk/admin/ to generate your password hash
 *    and paste it below.
 */

// Login
const ADMIN_USER      = 'admin';
const ADMIN_PASS_HASH = ''; // paste the hash generated on /admin/ here

// How saves are stored:
//   'github' — each save is committed to your GitHub repo; Hostinger's
//              auto-deploy then publishes it (recommended if you deploy from GitHub).
//   'local'  — files on the server are edited directly, with automatic backups.
//              Use this only if you do NOT deploy from GitHub, otherwise the
//              next deploy will overwrite your edits.
const STORAGE_MODE = 'github';

// GitHub settings (only for STORAGE_MODE = 'github')
const GITHUB_TOKEN  = '';                  // fine-grained token with "Contents: Read and write" on the repo only
const GITHUB_REPO   = 'satis4eva/dpayments-site'; // owner/repo
const GITHUB_BRANCH = 'main';
const GITHUB_PREFIX = '';                  // folder inside the repo where the site lives, e.g. 'site/' (blank = repo root)
