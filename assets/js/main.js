(function () {
  var body = document.body;
  var header = document.querySelector('.site-header');
  var toggle = document.querySelector('.menu-toggle');

  if (toggle) {
    toggle.addEventListener('click', function () {
      var open = body.classList.toggle('menu-open');
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
    document.querySelectorAll('.nav-links a').forEach(function (a) {
      a.addEventListener('click', function () {
        body.classList.remove('menu-open');
        toggle.setAttribute('aria-expanded', 'false');
      });
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && body.classList.contains('menu-open')) {
        body.classList.remove('menu-open');
        toggle.setAttribute('aria-expanded', 'false');
        toggle.focus();
      }
    });
  }

  // Mega menus
  var menus = document.querySelectorAll('.has-menu');
  var desktop = window.matchMedia('(min-width: 981px) and (hover: hover)');
  function closeAll(except) {
    menus.forEach(function (m) {
      if (m !== except) { m.classList.remove('open'); m.querySelector('.menu-btn').setAttribute('aria-expanded', 'false'); }
    });
  }
  menus.forEach(function (m) {
    var btn = m.querySelector('.menu-btn');
    var timer;
    btn.addEventListener('click', function (e) {
      e.stopPropagation();
      var open = !m.classList.contains('open');
      closeAll(m);
      m.classList.toggle('open', open);
      btn.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
    m.addEventListener('mouseenter', function () {
      if (!desktop.matches) return;
      clearTimeout(timer); closeAll(m);
      m.classList.add('open'); btn.setAttribute('aria-expanded', 'true');
    });
    m.addEventListener('mouseleave', function () {
      if (!desktop.matches) return;
      timer = setTimeout(function () { m.classList.remove('open'); btn.setAttribute('aria-expanded', 'false'); }, 160);
    });
    m.addEventListener('focusout', function (e) {
      if (desktop.matches && !m.contains(e.relatedTarget)) { m.classList.remove('open'); btn.setAttribute('aria-expanded', 'false'); }
    });
  });
  document.addEventListener('click', function (e) {
    if (desktop.matches && !e.target.closest('.has-menu')) closeAll();
  });
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') {
      var open = document.querySelector('.has-menu.open');
      if (open) { closeAll(); open.querySelector('.menu-btn').focus(); }
    }
  });

  function onScroll() {
    if (header) header.classList.toggle('scrolled', window.scrollY > 8);
  }
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  // Reveal on scroll
  var items = document.querySelectorAll('.reveal');
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) { en.target.classList.add('in'); io.unobserve(en.target); }
      });
    }, { rootMargin: '0px 0px -8% 0px' });
    items.forEach(function (el) { io.observe(el); });
  } else {
    items.forEach(function (el) { el.classList.add('in'); });
  }

  // Show form error from query string (?error=...)
  var params = new URLSearchParams(window.location.search);
  var err = params.get('error');
  var box = document.querySelector('[data-form-alert]');
  if (err && box) {
    var msgs = {
      missing: 'Please add your name and a valid email address.',
      send: 'Sorry, something went wrong sending your enquiry. Please email info@dpayments.co.uk instead.'
    };
    box.textContent = msgs[err] || msgs.send;
    box.hidden = false;
  }

  // Pre-select a channel from ?channel=
  var ch = params.get('channel');
  if (ch) {
    var input = document.querySelector('input[name="channels[]"][value="' + ch + '"]');
    if (input) input.checked = true;
  }

  // Year
  document.querySelectorAll('[data-year]').forEach(function (el) { el.textContent = new Date().getFullYear(); });
})();
