/*
  60-Second Scout: user-controlled six-step briefing.
  Without JS all six steps are listed. With JS one step shows at a time with
  Previous / Next buttons, numbered step buttons and arrow-key support. No timer.
*/
(function () {
  'use strict';

  function init() {
    var root = document.querySelector('[data-stepper]');
    if (!root) return;
    var steps = Array.prototype.slice.call(root.querySelectorAll('[data-step]'));
    var nav = root.querySelector('[data-step-nav]');
    var prev = root.querySelector('[data-step-prev]');
    var next = root.querySelector('[data-step-next]');
    var count = root.querySelector('[data-step-count]');
    if (!steps.length || !nav) return;

    var dots = document.createElement('ol');
    dots.className = 'step-dots';
    dots.setAttribute('aria-label', 'Briefing steps');
    steps.forEach(function (step, i) {
      var li = document.createElement('li');
      var b = document.createElement('button');
      b.type = 'button';
      b.className = 'step-dot';
      var h = step.querySelector('h2');
      b.textContent = String(i + 1).padStart(2, '0');
      b.setAttribute('aria-label', 'Step ' + (i + 1) + ': ' + (h ? h.textContent : ''));
      b.addEventListener('click', function () { go(i, true); });
      li.appendChild(b);
      dots.appendChild(li);
    });
    nav.parentNode.insertBefore(dots, nav);

    var current = 0;
    function go(i, moveFocus) {
      current = Math.max(0, Math.min(steps.length - 1, i));
      steps.forEach(function (s, j) {
        s.hidden = j !== current;
        s.classList.toggle('is-current', j === current);
      });
      Array.prototype.forEach.call(dots.querySelectorAll('.step-dot'), function (b, j) {
        if (j === current) b.setAttribute('aria-current', 'step');
        else b.removeAttribute('aria-current');
      });
      prev.disabled = current === 0;
      next.disabled = current === steps.length - 1;
      next.textContent = current === steps.length - 1 ? 'End of briefing' : 'Next step';
      count.textContent = 'Step ' + (current + 1) + ' of ' + steps.length;
      root.style.setProperty('--step-progress', ((current + 1) / steps.length).toFixed(3));
      if (moveFocus) {
        var h = steps[current].querySelector('h2');
        if (h) { h.setAttribute('tabindex', '-1'); h.focus(); }
      }
    }

    prev.addEventListener('click', function () { go(current - 1, false); });
    next.addEventListener('click', function () { go(current + 1, false); });
    root.addEventListener('keydown', function (ev) {
      if (ev.target.closest('input, textarea')) return;
      if (ev.key === 'ArrowRight') { ev.preventDefault(); go(current + 1, false); }
      if (ev.key === 'ArrowLeft') { ev.preventDefault(); go(current - 1, false); }
    });

    nav.hidden = false;
    root.classList.add('is-stepper');
    go(0, false);
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();
