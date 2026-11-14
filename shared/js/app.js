/*
  Joseph Ojwang profile: shared progressive enhancement. No dependencies.
  The HTML is complete without this file; everything here is an upgrade.
*/
(function () {
  'use strict';

  var doc = document.documentElement;
  var $ = function (sel, root) { return (root || document).querySelector(sel); };
  var $$ = function (sel, root) { return Array.prototype.slice.call((root || document).querySelectorAll(sel)); };

  var reduceQuery = window.matchMedia ? window.matchMedia('(prefers-reduced-motion: reduce)') : { matches: false };
  var saveData = !!(navigator.connection && navigator.connection.saveData);
  var STORE_KEY = 'jo-profile-motion-paused';
  var paused = false;
  try { paused = window.localStorage.getItem(STORE_KEY) === '1'; } catch (err) { /* storage blocked */ }

  function motionAllowed() {
    return !reduceQuery.matches && !saveData && !paused;
  }

  /* ------------------------------------------------------------ motion: reveal */
  var revealObserver = null;
  var pendingReveal = [];

  // Fallback for fast jumps where an IntersectionObserver callback arrives late: never leave content hidden.
  function revealPassed() {
    if (!pendingReveal.length) return;
    var limit = window.innerHeight;
    pendingReveal = pendingReveal.filter(function (el) {
      if (el.classList.contains('is-in')) return false;
      if (el.getBoundingClientRect().top < limit) { el.classList.add('is-in'); return false; }
      return true;
    });
  }

  function revealAllInView() {
    var limit = window.innerHeight * 1.1;
    $$('[data-reveal]').forEach(function (el) {
      if (el.getBoundingClientRect().top < limit) el.classList.add('is-in');
    });
  }

  function initReveal() {
    if (!('IntersectionObserver' in window)) return false;
    var groups = new Map();
    $$('[data-reveal]').forEach(function (el) {
      // Stagger siblings slightly so grids cascade.
      var parent = el.parentElement;
      var i = groups.get(parent) || 0;
      groups.set(parent, i + 1);
      el.style.setProperty('--reveal-delay', Math.min(i, 6) * 60 + 'ms');
    });
    revealObserver = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add('is-in');
          revealObserver.unobserve(entry.target);
        }
      });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.08 });
    pendingReveal = $$('[data-reveal]');
    pendingReveal.forEach(function (el) { revealObserver.observe(el); });
    return true;
  }

  function applyMotionState() {
    var allowed = motionAllowed();
    doc.classList.toggle('motion-reduced', reduceQuery.matches);
    doc.classList.toggle('save-data', saveData);
    doc.classList.toggle('motion-paused', paused);
    if (allowed) {
      // Anything already on screen or scrolled past stays visible when motion resumes.
      revealAllInView();
      doc.classList.add('motion-ready');
    } else {
      doc.classList.remove('motion-ready');
    }
    $$('[data-motion-toggle]').forEach(function (btn) {
      var system = reduceQuery.matches || saveData;
      btn.setAttribute('aria-pressed', String(paused || system));
      var label = btn.querySelector('.mt-label') || btn;
      label.textContent = system ? 'Motion reduced' : (paused ? 'Resume motion' : 'Pause motion');
      btn.disabled = system;
      btn.title = system ? 'Your device asks for reduced motion or data saving' : '';
    });
  }

  function initMotionToggle() {
    $$('[data-motion-toggle]').forEach(function (btn) {
      btn.addEventListener('click', function () {
        paused = !paused;
        try { window.localStorage.setItem(STORE_KEY, paused ? '1' : '0'); } catch (err) { /* ignore */ }
        applyMotionState();
      });
    });
    if (reduceQuery.addEventListener) reduceQuery.addEventListener('change', applyMotionState);
  }

  /* ------------------------------------------------------------ motion: scroll progress + parallax */
  var ticking = false;
  var parallaxEls = [];
  var visibleParallax = new Set();

  function onScrollFrame() {
    ticking = false;
    var max = doc.scrollHeight - window.innerHeight;
    doc.style.setProperty('--scroll', max > 0 ? (window.scrollY / max).toFixed(4) : '0');
    revealPassed();
    if (!motionAllowed() || document.hidden) return;
    visibleParallax.forEach(function (el) {
      var rect = el.getBoundingClientRect();
      var factor = parseFloat(el.getAttribute('data-parallax')) || 0;
      var offset = (rect.top + rect.height / 2 - window.innerHeight / 2) * factor;
      el.style.setProperty('--py', offset.toFixed(1) + 'px');
    });
  }

  function requestScrollFrame() {
    if (!ticking) {
      ticking = true;
      window.requestAnimationFrame(onScrollFrame);
    }
  }

  function initScrollEffects() {
    parallaxEls = $$('[data-parallax]');
    if (parallaxEls.length && 'IntersectionObserver' in window) {
      var io = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) visibleParallax.add(entry.target);
          else visibleParallax.delete(entry.target);
        });
      });
      parallaxEls.forEach(function (el) { io.observe(el); });
    }
    window.addEventListener('scroll', requestScrollFrame, { passive: true });
    window.addEventListener('resize', requestScrollFrame, { passive: true });
    requestScrollFrame();
  }

  /* ------------------------------------------------------------ motion: pointer lighting */
  function initPointerLight() {
    if (!window.matchMedia || !window.matchMedia('(pointer: fine)').matches) return;
    $$('[data-pointer-light]').forEach(function (el) {
      var frame = 0;
      var x = 0;
      var y = 0;
      el.addEventListener('pointermove', function (ev) {
        if (!motionAllowed()) return;
        var rect = el.getBoundingClientRect();
        x = ev.clientX - rect.left;
        y = ev.clientY - rect.top;
        if (frame) return;
        frame = window.requestAnimationFrame(function () {
          frame = 0;
          el.style.setProperty('--mx', x + 'px');
          el.style.setProperty('--my', y + 'px');
        });
      });
    });
  }

  /* ------------------------------------------------------------ hidden tab */
  function initVisibility() {
    document.addEventListener('visibilitychange', function () {
      doc.classList.toggle('motion-hidden', document.hidden);
    });
  }

  /* ------------------------------------------------------------ section tracking + anchor-preserving design links */
  var currentSection = '';

  function routeLinks() {
    return $$('[data-variant-link], a[rel="prev"], a[rel="next"]');
  }

  function updateRouteLinks() {
    var hash = currentSection && currentSection !== 'overview' ? '#' + currentSection : '';
    routeLinks().forEach(function (a) {
      var base = a.getAttribute('href').split('#')[0];
      a.setAttribute('href', base + hash);
    });
  }

  function setCurrent(id) {
    if (!id || id === currentSection) return;
    currentSection = id;
    $$('.site-nav a, .dossier-index a, .ten-chapters a').forEach(function (a) {
      if (a.getAttribute('href') === '#' + id) a.setAttribute('aria-current', 'true');
      else a.removeAttribute('aria-current');
    });
    doc.setAttribute('data-section', id);
    updateRouteLinks();
  }

  function initSectionTracking() {
    var sections = $$('main section[id]');
    if (!sections.length) return;
    if (location.hash && document.getElementById(location.hash.slice(1))) {
      var target = document.getElementById(location.hash.slice(1)).closest('section[id]');
      if (target) setCurrent(target.id);
    }
    if (!('IntersectionObserver' in window)) return;
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) setCurrent(entry.target.id);
      });
    }, { rootMargin: '-35% 0px -60% 0px' });
    sections.forEach(function (s) { io.observe(s); });
    window.addEventListener('hashchange', function () {
      var el = document.getElementById(location.hash.slice(1));
      var sec = el && el.closest('section[id]');
      if (sec) setCurrent(sec.id);
    });
  }

  /* ------------------------------------------------------------ disclosure helper (switcher + mobile menu) */
  function disclosure(toggle, panel, opts) {
    opts = opts || {};
    var useHidden = opts.useHidden !== false;

    function isOpen() { return toggle.getAttribute('aria-expanded') === 'true'; }

    function open() {
      toggle.setAttribute('aria-expanded', 'true');
      if (useHidden) panel.hidden = false;
      panel.classList.add('is-open');
      var first = opts.focusSelector ? $(opts.focusSelector, panel) : null;
      if (first) first.focus();
      document.addEventListener('pointerdown', onOutside, true);
    }

    function close(restoreFocus) {
      if (!isOpen()) return;
      toggle.setAttribute('aria-expanded', 'false');
      if (useHidden) panel.hidden = true;
      panel.classList.remove('is-open');
      document.removeEventListener('pointerdown', onOutside, true);
      if (restoreFocus) toggle.focus();
    }

    function onOutside(ev) {
      if (!panel.contains(ev.target) && !toggle.contains(ev.target)) close(false);
    }

    toggle.addEventListener('click', function () { if (isOpen()) close(true); else open(); });
    [toggle, panel].forEach(function (el) {
      el.addEventListener('keydown', function (ev) {
        if (ev.key === 'Escape' && isOpen()) {
          ev.preventDefault();
          close(true);
        }
      });
    });
    panel.addEventListener('focusout', function (ev) {
      if (ev.relatedTarget && !panel.contains(ev.relatedTarget) && ev.relatedTarget !== toggle) close(false);
    });
    return { close: close, isOpen: isOpen };
  }

  function initSwitcher() {
    var toggle = $('[data-switcher-toggle]');
    if (!toggle) return;
    var panel = document.getElementById(toggle.getAttribute('aria-controls'));
    if (!panel) return;
    var d = disclosure(toggle, panel, { focusSelector: 'a[aria-current="page"]' });
    // Arrow keys move through the list for quicker switching.
    panel.addEventListener('keydown', function (ev) {
      if (ev.key !== 'ArrowDown' && ev.key !== 'ArrowUp') return;
      var links = $$('a', panel);
      var i = links.indexOf(document.activeElement);
      if (i < 0) return;
      ev.preventDefault();
      links[(i + (ev.key === 'ArrowDown' ? 1 : -1) + links.length) % links.length].focus();
    });
    panel.addEventListener('click', function (ev) { if (ev.target.closest('a')) d.close(false); });
  }

  function initMenu() {
    var toggle = $('[data-menu-toggle]');
    if (!toggle) return;
    var panel = document.getElementById(toggle.getAttribute('aria-controls'));
    if (!panel) return;
    var d = disclosure(toggle, panel, { useHidden: false, focusSelector: 'a' });
    panel.addEventListener('click', function (ev) { if (ev.target.closest('a')) d.close(false); });
    window.addEventListener('resize', function () { if (window.innerWidth > 920) d.close(false); }, { passive: true });
  }

  /* ------------------------------------------------------------ footage */
  function initFootage() {
    // Only one clip plays at a time.
    document.addEventListener('play', function (ev) {
      if (!(ev.target instanceof HTMLVideoElement)) return;
      $$('video').forEach(function (v) { if (v !== ev.target && !v.paused) v.pause(); });
    }, true);

    var bar = $('[data-clip-filters]');
    if (!bar) return;
    bar.hidden = false;
    var clips = $$('.clip[data-orientation]');
    $$('[data-clip-filter]', bar).forEach(function (btn) {
      btn.addEventListener('click', function () {
        var f = btn.getAttribute('data-clip-filter');
        $$('[data-clip-filter]', bar).forEach(function (b) { b.setAttribute('aria-pressed', String(b === btn)); });
        clips.forEach(function (c) {
          var show = f === 'all' || c.getAttribute('data-orientation') === f;
          if (!show) { var v = $('video', c); if (v && !v.paused) v.pause(); }
          c.hidden = !show;
        });
      });
    });
  }

  /* ------------------------------------------------------------ gallery filters */
  function initGalleryFilters() {
    var bar = $('[data-gallery-filters]');
    if (!bar) return;
    bar.hidden = false;
    var items = $$('.g-item[data-cat]');
    var count = $('[data-gallery-count]');
    function apply(f) {
      var n = 0;
      items.forEach(function (it) {
        var show = f === 'all' || it.getAttribute('data-cat') === f;
        it.hidden = !show;
        if (show) n += 1;
      });
      if (count) count.textContent = 'Showing ' + n + ' of ' + items.length + ' images';
    }
    $$('[data-gallery-filter]', bar).forEach(function (btn) {
      btn.addEventListener('click', function () {
        $$('[data-gallery-filter]', bar).forEach(function (b) { b.setAttribute('aria-pressed', String(b === btn)); });
        apply(btn.getAttribute('data-gallery-filter'));
      });
    });
    // A link to a specific photo (e.g. #photo-joseph-match-carry) should never land on a hidden item.
    window.addEventListener('hashchange', function () {
      var el = document.getElementById(location.hash.slice(1));
      if (el && el.hidden) {
        var all = $('[data-gallery-filter="all"]', bar);
        if (all) all.click();
      }
    });
  }

  /* ------------------------------------------------------------ lightbox dialog */
  function initLightbox() {
    var dialog = $('dialog.lightbox');
    if (!dialog || typeof dialog.showModal !== 'function') return; // links keep opening the image directly
    var imgEl = $('.lb-img', dialog);
    var cap = $('[data-lb-caption]', dialog);
    var count = $('[data-lb-count]', dialog);
    var group = [];
    var index = 0;
    var opener = null;

    function show(i) {
      index = (i + group.length) % group.length;
      var link = group[index];
      var thumb = $('img', link);
      imgEl.src = link.getAttribute('href');
      imgEl.alt = link.getAttribute('data-caption') || (thumb ? thumb.alt : '');
      imgEl.removeAttribute('width');
      imgEl.removeAttribute('height');
      cap.textContent = link.getAttribute('data-caption') || '';
      count.textContent = 'Image ' + (index + 1) + ' of ' + group.length;
      var single = group.length < 2;
      $('[data-lb-prev]', dialog).hidden = single;
      $('[data-lb-next]', dialog).hidden = single;
    }

    function focusables() {
      return $$('button:not([hidden]), a[href]', dialog).filter(function (el) { return !el.disabled && el.offsetParent !== null; });
    }

    document.addEventListener('click', function (ev) {
      var link = ev.target.closest && ev.target.closest('a[data-lightbox]');
      if (!link || ev.metaKey || ev.ctrlKey || ev.shiftKey || ev.button > 0) return;
      ev.preventDefault();
      var name = link.getAttribute('data-lightbox');
      group = $$('a[data-lightbox="' + name + '"]').filter(function (a) { return !a.closest('[hidden]'); });
      opener = link;
      show(group.indexOf(link));
      dialog.showModal();
      $('[data-lb-close]', dialog).focus();
    });

    $('[data-lb-prev]', dialog).addEventListener('click', function () { show(index - 1); });
    $('[data-lb-next]', dialog).addEventListener('click', function () { show(index + 1); });
    $('[data-lb-close]', dialog).addEventListener('click', function () { dialog.close(); });
    dialog.addEventListener('click', function (ev) { if (ev.target === dialog) dialog.close(); });
    dialog.addEventListener('keydown', function (ev) {
      if (ev.key === 'ArrowRight' && group.length > 1) { ev.preventDefault(); show(index + 1); }
      else if (ev.key === 'ArrowLeft' && group.length > 1) { ev.preventDefault(); show(index - 1); }
      else if (ev.key === 'Tab') {
        // Keep focus inside the dialog.
        var f = focusables();
        if (!f.length) return;
        var first = f[0];
        var last = f[f.length - 1];
        if (ev.shiftKey && document.activeElement === first) { ev.preventDefault(); last.focus(); }
        else if (!ev.shiftKey && document.activeElement === last) { ev.preventDefault(); first.focus(); }
      }
    });
    dialog.addEventListener('close', function () {
      if (opener) opener.focus();
      opener = null;
    });
  }

  /* ------------------------------------------------------------ contact form */
  function initContactForm() {
    var form = $('[data-contact-form]');
    if (!form || !window.fetch || !window.FormData) return; // native POST still works
    var status = $('[data-form-status]', form);
    var button = $('button[type="submit"]', form);
    form.addEventListener('submit', function (ev) {
      var honey = form.querySelector('[name="_honey"]');
      if (honey && honey.value) { ev.preventDefault(); return; }
      if (!form.checkValidity()) return; // let the browser show its messages
      ev.preventDefault();
      status.removeAttribute('data-state');
      status.textContent = 'Sending your enquiry…';
      button.disabled = true;
      var endpoint = form.action.replace('formsubmit.co/', 'formsubmit.co/ajax/');
      fetch(endpoint, { method: 'POST', body: new FormData(form), headers: { Accept: 'application/json' } })
        .then(function (res) { if (!res.ok) throw new Error(String(res.status)); return res.json(); })
        .then(function (data) {
          if (!data || (data.success !== true && data.success !== 'true')) {
            throw new Error(data && data.message ? data.message : 'Form processor rejected the enquiry');
          }
          form.reset();
          status.setAttribute('data-state', 'ok');
          status.textContent = 'Thank you. Your enquiry has been sent to Joseph’s representative.';
        })
        .catch(function () {
          status.setAttribute('data-state', 'error');
          status.textContent = 'Sorry, the enquiry could not be sent. Please email oluwamartin@gmail.com directly.';
        })
        .then(function () { button.disabled = false; });
    });
  }

  /* ------------------------------------------------------------ boot */
  function init() {
    initSwitcher();
    initMenu();
    initFootage();
    initGalleryFilters();
    initLightbox();
    initContactForm();
    initSectionTracking();
    initScrollEffects();
    initPointerLight();
    initVisibility();
    initMotionToggle();
    // Motion is opted into last, and only once the observers exist.
    if (initReveal()) applyMotionState();
    else {
      doc.classList.remove('motion-ready');
      $$('[data-motion-toggle]').forEach(function (b) { b.hidden = true; });
    }
    doc.classList.toggle('motion-hidden', document.hidden);
    doc.classList.add('app-ready');
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();

  window.JOProfile = { motionAllowed: motionAllowed };
})();
