/* GetRecruiters Group — Main JS (loaded on every page) */

// Mega menu tabs (called from onclick in the nav markup)
window.switchMegaTab = function (tab, btn) {
  var menu = btn.closest('.mega-menu') || document;
  menu.querySelectorAll('.mega-tab-btn').forEach(function (b) { b.classList.remove('active'); });
  menu.querySelectorAll('.mega-panel').forEach(function (p) { p.classList.remove('active'); });
  btn.classList.add('active');
  var panel = document.getElementById('mega-' + tab);
  if (panel) panel.classList.add('active');
};

(function () {
  // Scroll-aware navbar
  var navbar = document.querySelector('.navbar');
  if (navbar) {
    window.addEventListener('scroll', function () {
      navbar.classList.toggle('scrolled', window.scrollY > 10);
    }, { passive: true });
  }

  // Mobile nav toggle
  var toggle = document.querySelector('.nav-toggle');
  var menu = document.querySelector('.nav-menu');
  if (toggle && menu && navbar) {
    toggle.addEventListener('click', function () {
      var open = menu.classList.toggle('open');
      toggle.classList.toggle('open', open);
      toggle.setAttribute('aria-expanded', open);
    });
    document.addEventListener('click', function (e) {
      if (!navbar.contains(e.target)) {
        menu.classList.remove('open');
        toggle.classList.remove('open');
        toggle.setAttribute('aria-expanded', false);
      }
    });
  }

  // Highlight the current page in the nav
  var currentPath = window.location.pathname.split('/').pop() || 'index.html';
  document.querySelectorAll('.nav-links > li > a').forEach(function (link) {
    var raw = link.getAttribute('href') || '';
    if (raw.indexOf('#') > -1) return;  // in-page anchors aren't pages
    if (raw === currentPath || raw === currentPath + '.html') link.classList.add('active');
  });

  // Form submit — posts to the hundredx public inquiry API
  var HUNDREDX_API = 'https://100xrecruiting.com';
  document.querySelectorAll('form[data-form]').forEach(function (form) {
    form.addEventListener('submit', async function (e) {
      e.preventDefault();
      if (!form.checkValidity()) { form.reportValidity(); return; }
      var btn = form.querySelector('button[type="submit"]');
      var successEl = form.querySelector('.alert-success');
      var orig = btn ? btn.textContent : '';
      if (btn) { btn.disabled = true; btn.textContent = 'Sending…'; }

      var d = Object.fromEntries(new FormData(form));
      var name = ((d.first_name || '') + ' ' + (d.last_name || '')).trim();
      var notes = [
        'Source: GetRecruiters (getrecruiters.com)',
        d.role_title   ? 'Role: '             + d.role_title   : '',
        d.hire_type    ? 'Type: '             + d.hire_type    : '',
        d.industry     ? 'Industry: '         + d.industry     : '',
        d.openings     ? 'Openings: '         + d.openings     : '',
        d.location     ? 'Location: '         + d.location     : '',
        d.timeline     ? 'Timeline: '         + d.timeline     : '',
        d.compensation ? 'Compensation: '     + d.compensation : '',
        d.your_title   ? 'Submitter title: '  + d.your_title   : '',
        d.phone        ? 'Phone: '            + d.phone        : '',
        d.topic        ? 'Topic: '            + d.topic        : '',
        d.message      ? 'Message: '          + d.message      : '',
        d.notes        ? 'Notes: '            + d.notes        : '',
      ].filter(Boolean).join('\n');

      try {
        var res = await fetch(HUNDREDX_API + '/api/public/inquiry', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            employer_name:    name || d.name || '',
            employer_email:   d.email || '',
            employer_company: d.company || '',
            inquiry_type:     form.dataset.form,
            notes:            notes,
          }),
        });
        var json = await res.json().catch(function () { return {}; });
        if (json.ok) {
          form.reset();
          if (successEl) successEl.style.display = 'block';
          if (btn) { btn.textContent = 'Sent ✓'; }
        } else {
          throw new Error(json.error || 'server error');
        }
      } catch (err) {
        if (btn) { btn.disabled = false; btn.textContent = orig; }
        alert('Something went wrong — please email gus@stafffinancial.com or call 404-250-0790.');
      }
    });
  });
})();
