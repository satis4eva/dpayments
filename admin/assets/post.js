(function () {
  var rte = document.getElementById('rte');
  var raw = document.getElementById('rte-html');
  var form = document.getElementById('post-form');
  var bodyField = document.getElementById('body-field');
  var file = document.getElementById('file');
  var coverPick = document.getElementById('cover-pick');
  var cover = document.getElementById('cover');
  var coverRemove = document.getElementById('cover-remove');
  var dirty = false, uploadFor = null, savedRange = null, htmlMode = false;

  document.execCommand('defaultParagraphSeparator', false, 'p');
  rte.addEventListener('input', function () { dirty = true; });
  form.addEventListener('input', function () { dirty = true; });
  rte.addEventListener('paste', function (e) {
    e.preventDefault();
    var text = (e.clipboardData || window.clipboardData).getData('text/plain');
    var html = text.split(/\n{2,}/).map(function (para) { return '<p>' + para.replace(/[&<>]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;' }[c]; }).replace(/\n/g, '<br>') + '</p>'; }).join('');
    document.execCommand('insertHTML', false, html);
  });

  function keepRange() { var s = window.getSelection(); if (s.rangeCount && rte.contains(s.anchorNode)) savedRange = s.getRangeAt(0).cloneRange(); }
  function restoreRange() { rte.focus(); if (savedRange) { var s = window.getSelection(); s.removeAllRanges(); s.addRange(savedRange); } }
  rte.addEventListener('keyup', keepRange); rte.addEventListener('mouseup', keepRange);

  document.querySelector('.rte-bar').addEventListener('mousedown', function (e) { if (e.target.closest('button')) e.preventDefault(); });
  document.querySelector('.rte-bar').addEventListener('click', function (e) {
    var b = e.target.closest('button'); if (!b) return;
    var cmd = b.getAttribute('data-cmd'), act = b.getAttribute('data-act');
    if (htmlMode && act !== 'html') return;
    if (cmd) { restoreRange(); document.execCommand(cmd, false, b.getAttribute('data-val') || null); dirty = true; return; }
    if (act === 'link') {
      keepRange();
      var url = prompt('Link address (e.g. /contact/ or https://…):', 'https://');
      if (!url) return;
      if (/^\s*(javascript|data|vbscript):/i.test(url)) { alert('That kind of link is not allowed.'); return; }
      restoreRange(); document.execCommand('createLink', false, url.trim()); dirty = true;
    } else if (act === 'image') { keepRange(); uploadFor = 'body'; file.click(); }
    else if (act === 'video') {
      var v = prompt('Paste a YouTube link:'); if (!v) return;
      var m = v.match(/(?:youtu\.be\/|v=|embed\/|shorts\/)([A-Za-z0-9_-]{6,15})/);
      if (!m) { alert('That doesn’t look like a YouTube link.'); return; }
      restoreRange();
      document.execCommand('insertHTML', false, '<div style="position:relative;padding-top:56.25%;margin:1.2em 0"><iframe src="https://www.youtube-nocookie.com/embed/' + m[1] + '" title="Video" style="position:absolute;inset:0;width:100%;height:100%;border:0;border-radius:14px" allowfullscreen loading="lazy"></iframe></div><p><br></p>');
      dirty = true;
    } else if (act === 'html') {
      htmlMode = !htmlMode;
      if (htmlMode) { raw.value = rte.innerHTML; raw.hidden = false; rte.hidden = true; b.classList.add('on'); }
      else { rte.innerHTML = raw.value; raw.hidden = true; rte.hidden = false; b.classList.remove('on'); }
    }
  });

  coverPick.addEventListener('click', function () { uploadFor = 'cover'; file.click(); });
  coverRemove.addEventListener('click', function () { cover.value = ''; coverPick.style.backgroundImage = ''; coverPick.querySelector('span').textContent = 'Click to upload'; coverRemove.hidden = true; dirty = true; });

  file.addEventListener('change', function () {
    var f = file.files[0]; if (!f) return;
    var fd = new FormData(); fd.append('action', 'upload'); fd.append('csrf', DP.csrf); fd.append('file', f);
    fetch('/admin/api.php', { method: 'POST', body: fd, credentials: 'same-origin' }).then(function (r) { return r.json(); }).then(function (res) {
      if (!res.ok) throw new Error(res.error);
      if (uploadFor === 'cover') {
        cover.value = res.url; coverPick.style.backgroundImage = "url('" + res.url + "')"; coverPick.querySelector('span').textContent = ''; coverRemove.hidden = false;
      } else {
        var alt = prompt('Describe the image (optional):', '') || '';
        restoreRange(); document.execCommand('insertHTML', false, '<img src="' + res.url + '" alt="' + alt.replace(/"/g, '&quot;') + '">');
      }
      dirty = true;
    }).catch(function (err) { alert(err.message || 'Upload failed'); }).finally(function () { file.value = ''; });
  });

  form.addEventListener('submit', function () {
    bodyField.value = htmlMode ? raw.value : rte.innerHTML;
    dirty = false;
  });
  window.addEventListener('beforeunload', function (e) { if (dirty) { e.preventDefault(); e.returnValue = ''; } });
})();
