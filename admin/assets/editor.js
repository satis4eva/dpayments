(function () {
  var cfg = window.DP_EDITOR;
  var frame = document.getElementById('frame');
  var saveBtn = document.getElementById('save');
  var statusEl = document.getElementById('status');
  var htmlPane = document.getElementById('html-pane');
  var htmlSrc = document.getElementById('html-src');
  var seoPane = document.getElementById('seo-pane');
  var seoTitle = document.getElementById('seo-title');
  var seoDesc = document.getElementById('seo-desc');
  var seoCount = document.getElementById('seo-count');
  var hint = document.getElementById('hint');
  var mode = 'visual';
  var dirty = false;
  var doc, main;

  var EDITABLE = 'h1,h2,h3,h4,h5,p,summary,td,th,.eyebrow,.tag,.btn,.text-link,.email-link,.more,.crumbs,' +
    '.feature-list li > span,.hero-points li,.pill,.float-card b,.float-card small,.rail-step .time,.timing-bar b,.timing-bar span,' +
    '.terminal-screen .merchant,.terminal-screen .amount,dd,dt,label,b,small,.mchip,.big-ticks li > span:last-child,.big-ticks li';
  var SINGLE_LINE = 'h1,h2,h3,h4,h5,summary,.eyebrow,.tag,.btn,.text-link,.more,.pill,td,th,.time';

  function b64ToUtf8(b64) {
    var bin = atob(b64);
    var bytes = new Uint8Array(bin.length);
    for (var i = 0; i < bin.length; i++) bytes[i] = bin.charCodeAt(i);
    return new TextDecoder('utf-8').decode(bytes);
  }

  function setStatus(t, cls) {
    statusEl.textContent = t;
    statusEl.className = 'small ' + (cls || 'muted');
  }

  function setDirty(v) {
    dirty = v;
    saveBtn.disabled = !v;
    if (v) setStatus('Unsaved changes', 'warn');
  }

  // ---- Load page into iframe ----
  var source = b64ToUtf8(cfg.html).replace(/<script[^>]*src="\/assets\/js\/main\.js"[^>]*><\/script>/, '');
  frame.addEventListener('load', prepare, { once: true });
  frame.srcdoc = source;

  function prepare() {
    doc = frame.contentDocument;
    main = doc.querySelector('main');
    var style = doc.createElement('style');
    style.setAttribute('data-editor', '');
    style.textContent =
      '.reveal{opacity:1!important;transform:none!important;transition:none!important}' +
      '.site-header,.site-footer{opacity:.45;pointer-events:none;user-select:none}' +
      '.site-header{position:relative!important}' +
      '[data-ed]{outline:1px dashed transparent;outline-offset:3px;cursor:text;transition:outline-color .15s}' +
      '[data-ed]:hover{outline-color:rgba(14,156,116,.55)}' +
      '[data-ed]:focus{outline:2px solid #0e9c74}' +
      'a[data-ed],a [data-ed]{cursor:text}';
    doc.head.appendChild(style);
    prepMain();

    doc.addEventListener('click', function (e) {
      var a = e.target.closest('a');
      var sum = e.target.closest('summary');
      if (sum) e.preventDefault();
      if (!a) return;
      e.preventDefault();
      if (e.altKey && main.contains(a)) {
        var href = window.prompt('Link address for this link/button:', a.getAttribute('href') || '');
        if (href !== null && href.trim() !== '') {
          href = href.trim();
          if (/^\s*javascript:/i.test(href)) { alert('That link type is not allowed.'); return; }
          a.setAttribute('href', href);
          setDirty(true);
        }
      }
    }, true);

    doc.addEventListener('input', function () { setDirty(true); });

    doc.addEventListener('keydown', function (e) {
      var el = e.target.closest && e.target.closest('[data-ed]');
      if (!el) return;
      if (e.key === 'Enter') {
        e.preventDefault();
        if (!el.matches(SINGLE_LINE)) doc.execCommand('insertLineBreak');
      } else if (e.key === ' ' && el.matches('summary')) {
        e.preventDefault();
        doc.execCommand('insertText', false, ' ');
      } else if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 's') {
        e.preventDefault();
        save();
      }
    });

    doc.addEventListener('paste', function (e) {
      if (!e.target.closest || !e.target.closest('[data-ed]')) return;
      e.preventDefault();
      var text = (e.clipboardData || window.clipboardData).getData('text/plain');
      doc.execCommand('insertText', false, text.replace(/\s*\n\s*/g, ' '));
    });

    setStatus(cfg.mode === 'github' ? 'Saves publish via GitHub' : 'Ready', 'muted');
  }

  function prepMain() {
    main.querySelectorAll('details').forEach(function (d) {
      if (d.open) d.setAttribute('data-was-open', '');
      d.open = true;
    });
    main.querySelectorAll(EDITABLE).forEach(function (el) {
      if (el.closest('form') && !el.matches('label,p,h1,h2,h3,h4')) return;
      if (el.querySelector('input,select,textarea')) return; // labels wrapping fields
      el.setAttribute('contenteditable', 'true');
      el.setAttribute('spellcheck', 'true');
      el.setAttribute('data-ed', '');
    });
  }

  function cleanHTML() {
    var clone = main.cloneNode(true);
    clone.querySelectorAll('[data-ed]').forEach(function (el) {
      el.removeAttribute('contenteditable');
      el.removeAttribute('spellcheck');
      el.removeAttribute('data-ed');
    });
    clone.querySelectorAll('details').forEach(function (d) {
      if (d.hasAttribute('data-was-open')) { d.removeAttribute('data-was-open'); d.setAttribute('open', ''); }
      else d.removeAttribute('open');
    });
    // Browsers insert non-breaking spaces while typing; turn them back into normal spaces
    var walker = doc.createTreeWalker(clone, NodeFilter.SHOW_TEXT);
    while (walker.nextNode()) {
      if (walker.currentNode.nodeValue.indexOf(' ') !== -1) {
        walker.currentNode.nodeValue = walker.currentNode.nodeValue.replace(/ /g, ' ');
      }
    }
    clone.querySelectorAll('.reveal.in').forEach(function (el) { el.classList.remove('in'); });
    clone.querySelectorAll('[class=""]').forEach(function (el) { el.removeAttribute('class'); });
    clone.querySelectorAll('[style=""]').forEach(function (el) { el.removeAttribute('style'); });
    return clone.innerHTML.trim();
  }

  // ---- Modes ----
  document.querySelectorAll('.seg button').forEach(function (b) {
    b.addEventListener('click', function () { switchMode(b.getAttribute('data-mode')); });
  });

  function switchMode(next) {
    if (!main || next === mode) return;
    if (mode === 'html') {
      main.innerHTML = htmlSrc.value;
      prepMain();
    }
    if (next === 'html') htmlSrc.value = cleanHTML();
    mode = next;
    document.querySelectorAll('.seg button').forEach(function (b) {
      b.classList.toggle('on', b.getAttribute('data-mode') === next);
    });
    frame.hidden = next !== 'visual';
    hint.hidden = next !== 'visual';
    htmlPane.hidden = next !== 'html';
    seoPane.hidden = next !== 'seo';
  }

  htmlSrc.addEventListener('input', function () { setDirty(true); });
  [seoTitle, seoDesc].forEach(function (el) {
    el.addEventListener('input', function () { setDirty(true); updateCount(); });
  });
  function updateCount() {
    seoCount.textContent = 'Title: ' + seoTitle.value.length + ' characters · Description: ' + seoDesc.value.length + ' characters';
  }
  updateCount();

  // ---- Save ----
  saveBtn.addEventListener('click', save);
  document.addEventListener('keydown', function (e) {
    if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 's') { e.preventDefault(); save(); }
  });

  function save() {
    if (!dirty || !main) return;
    var html = mode === 'html' ? htmlSrc.value : cleanHTML();
    var fd = new FormData();
    fd.append('action', 'save');
    fd.append('csrf', cfg.csrf);
    fd.append('page', cfg.page);
    fd.append('version', cfg.version);
    fd.append('main', html);
    fd.append('title', seoTitle.value);
    fd.append('description', seoDesc.value);
    saveBtn.disabled = true;
    setStatus('Saving…', 'muted');
    fetch('/admin/api.php', { method: 'POST', body: fd, credentials: 'same-origin' })
      .then(function (r) { return r.json().catch(function () { return { ok: false, error: 'Unexpected server response' }; }); })
      .then(function (res) {
        if (res.ok) {
          cfg.version = res.version || cfg.version;
          dirty = false;
          saveBtn.disabled = true;
          setStatus(res.unchanged ? 'No changes to save' :
            (cfg.mode === 'github' ? 'Saved ✓ Live in about a minute' : 'Saved ✓ Live now'), 'ok');
        } else {
          saveBtn.disabled = false;
          setStatus(res.error || 'Save failed', 'err');
        }
      })
      .catch(function () {
        saveBtn.disabled = false;
        setStatus('Network error — not saved', 'err');
      });
  }

  window.addEventListener('beforeunload', function (e) {
    if (dirty) { e.preventDefault(); e.returnValue = ''; }
  });
})();
