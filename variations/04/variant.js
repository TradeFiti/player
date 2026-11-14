/*
  Half-Space: trait-to-evidence focus.
  Each trait card gets a "Focus" toggle. Focusing a trait dims the others and
  highlights its evidence links. Without JS every trait and its evidence is listed.
*/
(function () {
  'use strict';

  function init() {
    var list = document.querySelector('[data-traits]');
    if (!list) return;
    var traits = Array.prototype.slice.call(list.querySelectorAll('.trait'));
    var buttons = [];

    traits.forEach(function (trait) {
      var title = trait.querySelector('h4');
      var btn = document.createElement('button');
      btn.type = 'button';
      btn.className = 'trait-focus';
      btn.setAttribute('aria-pressed', 'false');
      btn.textContent = 'Focus';
      var label = document.createElement('span');
      label.className = 'sr-only';
      label.textContent = ' on ' + (title ? title.textContent : 'this trait');
      btn.appendChild(label);
      trait.insertBefore(btn, trait.firstChild);
      buttons.push(btn);

      btn.addEventListener('click', function () {
        var on = btn.getAttribute('aria-pressed') !== 'true';
        buttons.forEach(function (b) { b.setAttribute('aria-pressed', 'false'); });
        traits.forEach(function (t) { t.classList.remove('is-focus'); });
        list.classList.toggle('has-focus', on);
        if (on) {
          btn.setAttribute('aria-pressed', 'true');
          trait.classList.add('is-focus');
        }
      });
    });

    list.addEventListener('keydown', function (ev) {
      if (ev.key === 'Escape' && list.classList.contains('has-focus')) {
        var active = list.querySelector('.trait-focus[aria-pressed="true"]');
        if (active) active.click();
      }
    });
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();
