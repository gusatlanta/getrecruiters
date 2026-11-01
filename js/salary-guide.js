/* GetRecruiters Group — salary guide page: saves the request, then shows the download */
(function () {
  var API = 'https://100xrecruiting.com/api/public/salary-guide';
  var LABEL = 'Download the Salary Guide →';
  var form = document.getElementById('guide-form');
  if (!form) return;
  var err = document.getElementById('g-err');
  var btn = document.getElementById('g-go');

  function fail(message) {
    btn.disabled = false;
    btn.textContent = LABEL;
    err.textContent = message;
    err.hidden = false;
  }

  form.addEventListener('submit', function (e) {
    e.preventDefault();
    var data = {};
    new FormData(form).forEach(function (v, k) { data[k] = String(v); });
    if (!data.name.trim() || !/^[^@\s]+@[^@\s]+\.[a-z]{2,}$/i.test(data.email.trim()) || !data.company.trim()) {
      err.textContent = 'Please add your name, work email and company.';
      err.hidden = false;
      return;
    }
    btn.disabled = true;
    btn.textContent = 'One moment…';
    err.hidden = true;
    fetch(API, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(data) })
      .then(function (r) { return r.json().catch(function () { return { ok: false }; }); })
      .then(function (d) {
        if (!d.ok) { fail(d.error || 'Something went wrong. Please try again.'); return; }
        form.hidden = true;
        document.getElementById('g-done').hidden = false;
      })
      .catch(function () { fail('Network error. Please email gus@stafffinancial.com and we will send it.'); });
  });
})();
