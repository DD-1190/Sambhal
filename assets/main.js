// Sambhal — use-case phone carousel
(function () {
  var root = document.querySelector('[data-showcase]');
  if (!root) return;

  var slides = root.querySelectorAll('.slide');
  var tabs = root.querySelectorAll('.uc-tab');
  var caption = root.querySelector('.uc-caption');
  var screen = root.querySelector('.screen');
  var current = 0;
  var timer = null;
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  function show(i) {
    current = (i + slides.length) % slides.length;
    slides.forEach(function (s, n) {
      var on = n === current;
      s.classList.toggle('is-active', on);
      s.setAttribute('aria-hidden', on ? 'false' : 'true');
    });
    tabs.forEach(function (t, n) {
      var on = n === current;
      t.setAttribute('aria-selected', on ? 'true' : 'false');
      t.tabIndex = on ? 0 : -1;
      if (on && t.scrollIntoView && root.dataset.ready) {
        t.scrollIntoView({ block: 'nearest', inline: 'center', behavior: reduce ? 'auto' : 'smooth' });
      }
    });
    if (caption) caption.textContent = slides[current].getAttribute('data-caption') || '';
  }

  function start() {
    if (reduce) return;
    stop();
    timer = setInterval(function () { show(current + 1); }, 4500);
  }
  function stop() { if (timer) { clearInterval(timer); timer = null; } }

  tabs.forEach(function (t, n) {
    t.addEventListener('click', function () { show(n); stop(); });
    t.addEventListener('keydown', function (e) {
      if (e.key === 'ArrowRight' || e.key === 'ArrowLeft') {
        e.preventDefault();
        show(current + (e.key === 'ArrowRight' ? 1 : -1));
        tabs[current].focus();
        stop();
      }
    });
  });

  // Swipe on the phone screen
  var x0 = null;
  screen.addEventListener('touchstart', function (e) { x0 = e.touches[0].clientX; }, { passive: true });
  screen.addEventListener('touchend', function (e) {
    if (x0 === null) return;
    var dx = e.changedTouches[0].clientX - x0;
    if (Math.abs(dx) > 40) { show(current + (dx < 0 ? 1 : -1)); stop(); }
    x0 = null;
  });

  root.addEventListener('mouseenter', stop);
  root.addEventListener('mouseleave', start);

  show(0);
  root.dataset.ready = '1';
  start();
})();
