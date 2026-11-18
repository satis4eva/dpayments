(function () {
  var cfg = window.DP;
  var frame = document.getElementById('frame');
  var saveBtn = document.getElementById('save');
  var statusEl = document.getElementById('status');
  var htmlPane = document.getElementById('html-pane');
  var htmlSrc = document.getElementById('html-src');
  var seoPane = document.getElementById('seo-pane');
  var seoTitle = document.getElementById('seo-title');
  var seoDesc = document.getElementById('seo-desc');
  var seoCount = document.getElementById('seo-count');
  var seoNoindex = document.getElementById('seo-noindex');
  var seoDraft = document.getElementById('seo-draft');
  var hint = document.getElementById('hint');
  var blockMenu = document.getElementById('block-menu');
  var fileInput = document.getElementById('img-file');
  var mode = 'visual', dirty = false, doc, main, lastSection = null, imgTarget = null;

  var EDITABLE = 'h1,h2,h3,h4,h5,p,summary,td,th,li,blockquote,figcaption,.eyebrow,.tag,.btn,.text-link,.email-link,.more,.crumbs,' +
    '.pill,.mchip,b,small,dd,dt,label,.lede';
  var SINGLE_LINE = 'h1,h2,h3,h4,h5,summary,.eyebrow,.tag,.btn,.text-link,.more,.pill,.mchip,td,th,b,small,label';

  function b64(s) { var b = atob(s), u = new Uint8Array(b.length); for (var i = 0; i < b.length; i++) u[i] = b.charCodeAt(i); return new TextDecoder().decode(u); }
  function setStatus(t, c) { statusEl.textContent = t; statusEl.className = 'small ' + (c || 'muted'); }
  function setDirty(v) { dirty = v; saveBtn.disabled = !v; if (v) setStatus('Unsaved changes', 'warn'); }

  var src = b64(cfg.html).replace(/<script[^>]*src="\/assets\/js\/main\.js[^"]*"[^>]*><\/script>/, '');
  frame.addEventListener('load', prepare, { once: true });
  frame.srcdoc = src;

  function prepare() {
    doc = frame.contentDocument;
    main = doc.querySelector('main');
    var st = doc.createElement('style');
    st.textContent =
      '.reveal{opacity:1!important;transform:none!important;transition:none!important}' +
      '.site-header,.site-footer,.topbar{opacity:.4;pointer-events:none;user-select:none}.site-header{position:relative!important}' +
      '[data-ed]{outline:1px dashed transparent;outline-offset:3px;cursor:text}[data-ed]:hover{outline-color:rgba(14,156,116,.55)}[data-ed]:focus{outline:2px solid #0e9c74}' +
      '.cms-token{background:rgba(245,184,74,.25);border-radius:4px;padding:0 3px;cursor:default}' +
      '.cms-block-token{display:block;max-width:1132px;margin:24px auto;padding:30px;text-align:center;border:2px dashed #e0a43a;border-radius:16px;font:600 15px system-ui;color:#8a5a0b;background:#fff8ea}' +
      'main img{cursor:pointer}main img:hover{outline:3px solid #0e9c74;outline-offset:2px}' +
      'main > section, main > article > section{position:relative}' +
      '.cms-sec-tools{position:absolute;top:10px;right:10px;z-index:30;display:none;gap:4px;background:#0d1b26;border-radius:10px;padding:4px;box-shadow:0 6px 18px rgba(0,0,0,.25)}' +
      'main > section:hover > .cms-sec-tools{display:flex}' +
      '.cms-sec-tools button{border:0;background:transparent;color:#fff;font:600 12px system-ui;padding:6px 9px;border-radius:7px;cursor:pointer}.cms-sec-tools button:hover{background:rgba(255,255,255,.15)}' +
      '.cms-sec-tools button.del:hover{background:#c44a3f}' +
      'main > section.cms-last{box-shadow:inset 0 0 0 2px rgba(14,156,116,.35)}';
    doc.head.appendChild(st);
    prepMain();

    doc.addEventListener('click', function (e) {
      var tool = e.target.closest('.cms-sec-tools button');
      if (tool) { e.preventDefault(); sectionAction(tool.getAttribute('data-act'), tool.closest('section')); return; }
      var sec = e.target.closest('main > section');
      if (sec) markLast(sec);
      var img = e.target.closest('main img');
      if (img) { e.preventDefault(); imgTarget = img; fileInput.click(); return; }
      if (e.target.closest('summary')) e.preventDefault();
      var a = e.target.closest('a');
      if (!a) return;
      e.preventDefault();
      if (e.altKey && main.contains(a)) {
        var href = window.prompt('Where should this link go? (e.g. /contact/ or https://…)', a.getAttribute('href') || '');
        if (href !== null && href.trim() !== '') {
          if (/^\s*(javascript|data|vbscript):/i.test(href)) { alert('That kind of link is not allowed.'); return; }
          a.setAttribute('href', href.trim()); setDirty(true);
        }
      }
    }, true);
    doc.addEventListener('input', function () { setDirty(true); });
    doc.addEventListener('keydown', function (e) {
      if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 's') { e.preventDefault(); save(); return; }
      var el = e.target.closest && e.target.closest('[data-ed]');
      if (!el) return;
      if (e.key === 'Enter') {
        if (el.matches('p,li') && !e.shiftKey && el.parentNode) {
          // new paragraph / list item after this one
          e.preventDefault();
          var n = doc.createElement(el.tagName);
          if (el.className) n.className = el.className;
          n.innerHTML = '<br>';
          el.parentNode.insertBefore(n, el.nextSibling);
          makeEditable(n); n.focus(); setDirty(true);
        } else {
          e.preventDefault();
          if (!el.matches(SINGLE_LINE)) doc.execCommand('insertLineBreak');
        }
      } else if (e.key === 'Backspace' && el.matches('p,li') && el.textContent === '' && el.parentNode.querySelectorAll(':scope > ' + el.tagName).length > 1) {
        e.preventDefault();
        var prev = el.previousElementSibling; el.remove(); if (prev && prev.focus) prev.focus(); setDirty(true);
      } else if (e.key === ' ' && el.matches('summary')) { e.preventDefault(); doc.execCommand('insertText', false, ' '); }
    });
    doc.addEventListener('paste', function (e) {
      if (!e.target.closest || !e.target.closest('[data-ed]')) return;
      e.preventDefault();
      doc.execCommand('insertText', false, (e.clipboardData || window.clipboardData).getData('text/plain').replace(/\s*\n\s*/g, ' '));
    });
    setStatus('Ready', 'muted');
  }

  function makeEditable(el) {
    if (el.closest('.cms-sec-tools') || el.closest('[data-token]')) return;
    if (el.querySelector('input,select,textarea,.step,.card,section,div.grid')) return;
    if (el.matches('li') && el.querySelector('span:not(.tick)')) return; // feature lists: edit the span instead
    el.setAttribute('contenteditable', 'true'); el.setAttribute('spellcheck', 'true'); el.setAttribute('data-ed', '');
  }
  function addTools(sec) {
    if (sec.querySelector(':scope > .cms-sec-tools')) return;
    var t = doc.createElement('div');
    t.className = 'cms-sec-tools'; t.setAttribute('contenteditable', 'false');
    t.innerHTML = '<button data-act="up" title="Move up">&uarr;</button><button data-act="down" title="Move down">&darr;</button>' +
      '<button data-act="dup" title="Duplicate">Copy</button><button data-act="bg" title="Change background">Style</button><button data-act="del" class="del" title="Delete">Delete</button>';
    sec.insertBefore(t, sec.firstChild);
  }
  function prepMain() {
    main.querySelectorAll('details').forEach(function (d) { if (d.open) d.setAttribute('data-was-open', ''); d.open = true; });
    main.querySelectorAll(EDITABLE).forEach(function (el) { if (!el.closest('form') || el.matches('h1,h2,h3,h4,p')) makeEditable(el); });
    main.querySelectorAll('.feature-list li > span:not(.tick)').forEach(makeEditable);
    main.querySelectorAll(':scope > section').forEach(addTools);
  }
  function markLast(sec) {
    if (lastSection) lastSection.classList.remove('cms-last');
    lastSection = sec; sec.classList.add('cms-last');
  }
  var BGS = ['', 'section-white', 'section-dark'];
  function sectionAction(act, sec) {
    if (!sec) return;
    if (act === 'up' && sec.previousElementSibling) sec.parentNode.insertBefore(sec, sec.previousElementSibling);
    else if (act === 'down' && sec.nextElementSibling) sec.parentNode.insertBefore(sec.nextElementSibling, sec);
    else if (act === 'dup') { var c = sec.cloneNode(true); c.classList.remove('cms-last'); sec.parentNode.insertBefore(c, sec.nextSibling); }
    else if (act === 'del') { if (!confirm('Delete this section?')) return; if (lastSection === sec) lastSection = null; sec.remove(); }
    else if (act === 'bg') {
      var cur = BGS.findIndex(function (b) { return b && sec.classList.contains(b); });
      BGS.forEach(function (b) { if (b) sec.classList.remove(b); });
      var next = BGS[(cur + 1 + BGS.length) % BGS.length]; if (next) sec.classList.add(next);
    }
    setDirty(true);
  }

  // ---- add block ----
  document.getElementById('add-block').addEventListener('click', function () { blockMenu.hidden = !blockMenu.hidden; });
  blockMenu.addEventListener('click', function (e) {
    var b = e.target.closest('[data-block]'); if (!b || !main) return;
    var tmp = doc.createElement('div'); tmp.innerHTML = cfg.blocks[b.getAttribute('data-block')].html;
    var sec = tmp.firstElementChild; if (!sec) return;
    if (lastSection && lastSection.parentNode === main) main.insertBefore(sec, lastSection.nextSibling); else main.appendChild(sec);
    sec.querySelectorAll(EDITABLE).forEach(makeEditable);
    sec.querySelectorAll('.feature-list li > span:not(.tick)').forEach(makeEditable);
    addTools(sec); markLast(sec);
    sec.scrollIntoView({ behavior: 'smooth', block: 'center' });
    blockMenu.hidden = true; setDirty(true);
  });

  // ---- images ----
  fileInput.addEventListener('change', function () {
    var f = fileInput.files[0]; if (!f || !imgTarget) return;
    setStatus('Uploading image…', 'muted');
    upload(f).then(function (url) {
      imgTarget.setAttribute('src', url);
      var alt = window.prompt('Describe the image for accessibility and Google (optional):', imgTarget.getAttribute('alt') || '');
      if (alt !== null) imgTarget.setAttribute('alt', alt);
      setDirty(true); setStatus('Image added — remember to save', 'warn');
    }).catch(function (err) { setStatus(err.message || 'Upload failed', 'err'); })
      .finally(function () { fileInput.value = ''; });
  });
  function upload(file) {
    var fd = new FormData(); fd.append('action', 'upload'); fd.append('csrf', cfg.csrf); fd.append('file', file);
    return fetch('/admin/api.php', { method: 'POST', body: fd, credentials: 'same-origin' }).then(function (r) { return r.json(); })
      .then(function (res) { if (!res.ok) throw new Error(res.error); return res.url; });
  }

  // ---- clean & save ----
  function cleanHTML() {
    var clone = main.cloneNode(true);
    clone.querySelectorAll('.cms-sec-tools').forEach(function (t) { t.remove(); });
    clone.querySelectorAll('[data-token]').forEach(function (t) { t.replaceWith(doc.createTextNode('{{' + t.getAttribute('data-token') + '}}')); });
    clone.querySelectorAll('[data-ed]').forEach(function (el) { el.removeAttribute('contenteditable'); el.removeAttribute('spellcheck'); el.removeAttribute('data-ed'); });
    clone.querySelectorAll('details').forEach(function (d) { if (d.hasAttribute('data-was-open')) { d.removeAttribute('data-was-open'); d.setAttribute('open', ''); } else d.removeAttribute('open'); });
    clone.querySelectorAll('.cms-last').forEach(function (el) { el.classList.remove('cms-last'); });
    clone.querySelectorAll('.reveal.in').forEach(function (el) { el.classList.remove('in'); });
    clone.querySelectorAll('[class=""]').forEach(function (el) { el.removeAttribute('class'); });
    var w = doc.createTreeWalker(clone, NodeFilter.SHOW_TEXT);
    while (w.nextNode()) if (w.currentNode.nodeValue.indexOf(' ') !== -1) w.currentNode.nodeValue = w.currentNode.nodeValue.replace(/ /g, ' ');
    return clone.innerHTML.trim();
  }

  document.querySelectorAll('.seg button').forEach(function (b) { b.addEventListener('click', function () { switchMode(b.getAttribute('data-mode')); }); });
  function switchMode(next) {
    if (!main || next === mode) return;
    if (mode === 'html') { main.innerHTML = htmlSrc.value; prepMain(); }
    if (next === 'html') htmlSrc.value = cleanHTML();
    mode = next;
    document.querySelectorAll('.seg button').forEach(function (b) { b.classList.toggle('on', b.getAttribute('data-mode') === next); });
    frame.hidden = next !== 'visual'; hint.hidden = next !== 'visual'; blockMenu.hidden = true;
    htmlPane.hidden = next !== 'html'; seoPane.hidden = next !== 'seo';
  }
  htmlSrc.addEventListener('input', function () { setDirty(true); });
  [seoTitle, seoDesc, seoNoindex, seoDraft].forEach(function (el) { if (el) el.addEventListener('input', function () { setDirty(true); count(); }); });
  [seoNoindex, seoDraft].forEach(function (el) { if (el) el.addEventListener('change', function () { setDirty(true); }); });
  function count() { seoCount.textContent = 'Title: ' + seoTitle.value.length + ' characters · Description: ' + seoDesc.value.length + ' characters'; }
  count();

  saveBtn.addEventListener('click', save);
  document.addEventListener('keydown', function (e) { if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 's') { e.preventDefault(); save(); } });
  function save() {
    if (!dirty || !main) return;
    var html = mode === 'html' ? htmlSrc.value : cleanHTML();
    var fd = new FormData();
    fd.append('action', 'save_page'); fd.append('csrf', cfg.csrf); fd.append('page', cfg.page); fd.append('main', html);
    fd.append('title', seoTitle.value); fd.append('description', seoDesc.value);
    fd.append('noindex', seoNoindex && seoNoindex.checked ? '1' : ''); fd.append('draft', seoDraft && seoDraft.checked ? '1' : '');
    saveBtn.disabled = true; setStatus('Saving…', 'muted');
    fetch('/admin/api.php', { method: 'POST', body: fd, credentials: 'same-origin' })
      .then(function (r) { return r.json().catch(function () { return { ok: false, error: 'Unexpected server response' }; }); })
      .then(function (res) {
        if (res.ok) { dirty = false; saveBtn.disabled = true; setStatus('Saved ✓ Live now', 'ok'); }
        else { saveBtn.disabled = false; setStatus(res.error || 'Save failed', 'err'); }
      }).catch(function () { saveBtn.disabled = false; setStatus('Network error — not saved', 'err'); });
  }
  window.addEventListener('beforeunload', function (e) { if (dirty) { e.preventDefault(); e.returnValue = ''; } });
})();
