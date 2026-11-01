/* GetRecruiters Group — AI recruiting page: swaps the AI app named in the hero */
(function () {
  var word = document.getElementById('ai-word');
  var tabs = Array.prototype.slice.call(document.querySelectorAll('[data-app]'));
  if (!word || !tabs.length) return;
  var index = 0;
  var timer = null;

  function show(next) {
    index = next;
    word.textContent = tabs[next].getAttribute('data-app');
    tabs.forEach(function (tab, i) {
      tab.setAttribute('aria-pressed', i === next ? 'true' : 'false');
    });
  }

  tabs.forEach(function (tab, i) {
    tab.addEventListener('click', function () {
      clearInterval(timer);
      show(i);
    });
  });

  if (!window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
    timer = setInterval(function () {
      show((index + 1) % tabs.length);
    }, 2800);
  }
})();
