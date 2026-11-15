(function () {
  var M = JSON.parse(JSON.stringify(DP.menus || {}));
  M.header = M.header || []; M.footer = M.footer || []; M.legal = M.legal || []; M.cta = M.cta || { label: '', url: '' };
  var saveBtn = document.getElementById('save'), statusEl = document.getElementById('status');
  var dirty = false;
  function changed() { dirty = true; saveBtn.disabled = false; statusEl.textContent = 'Unsaved changes'; statusEl.className = 'small warn'; }
  function esc(s) { return String(s == null ? '' : s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }
  function iconOpts(sel) { return DP.icons.map(function (n) { return '<option' + (n === sel ? ' selected' : '') + '>' + n + '</option>'; }).join(''); }
  function move(arr, i, d) { var j = i + d; if (j < 0 || j >= arr.length) return; var t = arr[i]; arr[i] = arr[j]; arr[j] = t; }
  function ctrls(path) { return '<span class="ctrls"><button type="button" data-mv="' + path + '|-1" title="Up">&uarr;</button><button type="button" data-mv="' + path + '|1" title="Down">&darr;</button><button type="button" data-rm="' + path + '" class="rm" title="Remove">&times;</button></span>'; }
  function get(path) { var o = M; path.split('.').forEach(function (k) { o = o[k]; }); return o; }
  function parentOf(path) { var p = path.split('.'); var idx = +p.pop(); return { arr: get(p.join('.')), idx: idx }; }

  function render() {
    var h = '';
    M.header.forEach(function (it, i) {
      var p = 'header.' + i;
      h += '<div class="mitem">';
      h += '<div class="mrow"><select data-f="' + p + '.type"><option value="link"' + (it.type !== 'mega' ? ' selected' : '') + '>Link</option><option value="mega"' + (it.type === 'mega' ? ' selected' : '') + '>Dropdown</option></select>' +
        '<input data-f="' + p + '.label" value="' + esc(it.label) + '" placeholder="Label">' +
        (it.type !== 'mega' ? '<input data-f="' + p + '.url" value="' + esc(it.url) + '" placeholder="/page/ or https://…" list="page-urls">' : '<span class="muted small grow">Dropdown with ' + (it.columns || []).length + ' column(s)</span>') +
        ctrls(p) + '</div>';
      if (it.type === 'mega') {
        it.columns = it.columns || [];
        h += '<div class="mcols">';
        it.columns.forEach(function (c, ci) {
          var cp = p + '.columns.' + ci;
          h += '<div class="mcol"><div class="mrow"><input data-f="' + cp + '.title" value="' + esc(c.title) + '" placeholder="Column heading">' + ctrls(cp) + '</div>';
          (c.items || []).forEach(function (x, xi) {
            var xp = cp + '.items.' + xi;
            h += '<div class="msub"><div class="mrow"><input data-f="' + xp + '.label" value="' + esc(x.label) + '" placeholder="Link label">' + ctrls(xp) + '</div>' +
              '<div class="mrow"><input data-f="' + xp + '.url" value="' + esc(x.url) + '" placeholder="/page/" list="page-urls"><select data-f="' + xp + '.icon" class="ic" title="Icon">' + iconOpts(x.icon) + '</select></div>' +
              '<div class="mrow"><input data-f="' + xp + '.desc" value="' + esc(x.desc) + '" placeholder="Short description (optional)"></div></div>';
          });
          h += '<button type="button" class="addlink" data-addsub="' + cp + '">+ Add link</button></div>';
        });
        if (it.columns.length < 4) h += '<button type="button" class="addcol" data-addcol="' + p + '">+ Add column</button>';
        h += '</div>';
      }
      h += '</div>';
    });
    document.getElementById('header-items').innerHTML = h || '<p class="muted">No menu items.</p>';

    document.getElementById('cta').innerHTML = '<label>Button text <input data-f="cta.label" value="' + esc(M.cta.label) + '" placeholder="Leave empty to hide"></label>' +
      '<label>Links to <input data-f="cta.url" value="' + esc(M.cta.url) + '" list="page-urls"></label>';

    var f = '';
    M.footer.forEach(function (c, ci) {
      var cp = 'footer.' + ci;
      f += '<div class="panel mcol"><div class="mrow"><input data-f="' + cp + '.title" value="' + esc(c.title) + '" placeholder="Column heading">' + ctrls(cp) + '</div>';
      (c.items || []).forEach(function (x, xi) {
        var xp = cp + '.items.' + xi;
        f += '<div class="mrow"><input data-f="' + xp + '.label" value="' + esc(x.label) + '" placeholder="Label"><input data-f="' + xp + '.url" value="' + esc(x.url) + '" placeholder="/page/" list="page-urls">' + ctrls(xp) + '</div>';
      });
      f += '<button type="button" class="addlink" data-addfooter="' + cp + '">+ Add link</button></div>';
    });
    document.getElementById('footer-cols').innerHTML = f;

    var l = '';
    M.legal.forEach(function (x, i) {
      l += '<div class="mrow"><input data-f="legal.' + i + '.label" value="' + esc(x.label) + '" placeholder="Label"><input data-f="legal.' + i + '.url" value="' + esc(x.url) + '" list="page-urls">' + ctrls('legal.' + i) + '</div>';
    });
    document.getElementById('legal').innerHTML = l + '<button type="button" class="addlink" id="add-legal">+ Add link</button>';
  }

  document.addEventListener('input', function (e) {
    var p = e.target.getAttribute('data-f'); if (!p) return;
    var parts = p.split('.'), key = parts.pop(), obj = get(parts.join('.'));
    obj[key] = e.target.value; changed();
    if (key === 'type') { if (obj.type === 'mega' && !obj.columns) obj.columns = [{ title: '', items: [] }]; render(); }
  });
  document.addEventListener('click', function (e) {
    var t = e.target.closest('button'); if (!t) return;
    var mv = t.getAttribute('data-mv'), rm = t.getAttribute('data-rm');
    if (mv) { var a = mv.split('|'), q = parentOf(a[0]); move(q.arr, q.idx, +a[1]); }
    else if (rm) { if (!confirm('Remove this item?')) return; var r = parentOf(rm); r.arr.splice(r.idx, 1); }
    else if (t.hasAttribute('data-add')) { M.header.push(t.getAttribute('data-add') === 'mega' ? { type: 'mega', label: 'New dropdown', columns: [{ title: '', items: [{ label: 'New link', url: '/', icon: 'sparkle', desc: '' }] }] } : { type: 'link', label: 'New link', url: '/' }); }
    else if (t.hasAttribute('data-addcol')) { get(t.getAttribute('data-addcol')).columns.push({ title: '', items: [] }); }
    else if (t.hasAttribute('data-addsub')) { var c = get(t.getAttribute('data-addsub')); (c.items = c.items || []).push({ label: '', url: '', icon: 'sparkle', desc: '' }); }
    else if (t.hasAttribute('data-addfooter')) { var fc = get(t.getAttribute('data-addfooter')); (fc.items = fc.items || []).push({ label: '', url: '' }); }
    else if (t.id === 'add-footer') { M.footer.push({ title: 'New column', items: [] }); }
    else if (t.id === 'add-legal') { M.legal.push({ label: '', url: '' }); }
    else if (t.id === 'save') { save(); return; }
    else return;
    changed(); render();
  });
  function save() {
    var fd = new FormData(); fd.append('action', 'save_menus'); fd.append('csrf', DP.csrf); fd.append('menus', JSON.stringify(M));
    saveBtn.disabled = true; statusEl.textContent = 'Saving…'; statusEl.className = 'small muted';
    fetch('/admin/api.php', { method: 'POST', body: fd, credentials: 'same-origin' }).then(function (r) { return r.json(); }).then(function (res) {
      if (res.ok) { dirty = false; statusEl.textContent = 'Saved ✓ Live now'; statusEl.className = 'small ok'; }
      else { saveBtn.disabled = false; statusEl.textContent = res.error || 'Save failed'; statusEl.className = 'small err'; }
    }).catch(function () { saveBtn.disabled = false; statusEl.textContent = 'Network error'; statusEl.className = 'small err'; });
  }
  window.addEventListener('beforeunload', function (e) { if (dirty) { e.preventDefault(); e.returnValue = ''; } });
  render();
})();
