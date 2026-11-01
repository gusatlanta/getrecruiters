/* GetRecruiters Group — home page search (loaded on the home page only)
   Rows come from the #bench-data block that tools/build_pages.py writes. */

(function () {
  var BENCH = JSON.parse(document.getElementById('bench-data').textContent);
  var TRACKS = [
    { id: 'all', name: 'All recruiters' },
    { id: 'full', name: 'Full-cycle', tag: 'Full-cycle' },
    { id: 'support', name: 'Sourcers & coordinators', tag: 'Sourcer / coordinator' },
    { id: 'ta', name: 'TA leaders', tag: 'TA leader' },
    { id: 'hr', name: 'HR talent', tag: 'HR' }
  ];
  var PAGE_SIZE = 10;
  var benchTrack = 'all';
  var benchShown = PAGE_SIZE;

  var byId = function (id) { return document.getElementById(id); };
  var benchForm = byId('bench-filters');
  var filters = {
    q: byId('bench-q'), exp: byId('bench-exp'), spec: byId('bench-spec'), tool: byId('bench-tool'),
    mode: byId('bench-mode'), bg: byId('bench-bg'), sort: byId('bench-sort')
  };

  function esc(text) {
    return String(text == null ? '' : text).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/"/g, '&quot;');
  }

  function unique(list) {
    return list.filter(function (v, i) { return list.indexOf(v) === i; }).sort();
  }

  function flat(key) {
    return [].concat.apply([], BENCH.map(function (r) { return r[key]; }));
  }

  function addOptions(select, values) {
    values.forEach(function (v) { select.add(new Option(v, v)); });
  }

  function trackTag(id) {
    return TRACKS.filter(function (t) { return t.id === id; })[0].tag;
  }

  function askUrl(r) {
    return 'request-talent.html?candidate=' + encodeURIComponent(r.code);
  }

  function matches(r, anyTrack) {
    var q = filters.q.value.trim().toLowerCase();
    var yrs = filters.exp.value.split('-');
    var text = [r.code, r.title, r.place, r.win, r.pills.join(' '), r.sectors.join(' '), r.tools.join(' ')].join(' ').toLowerCase();
    return (anyTrack || benchTrack === 'all' || r.track === benchTrack) &&
      (!q || text.indexOf(q) >= 0) &&
      (!filters.exp.value || (r.yrs >= Number(yrs[0]) && r.yrs <= Number(yrs[1]))) &&
      (!filters.spec.value || r.sectors.indexOf(filters.spec.value) >= 0) &&
      (!filters.tool.value || r.tools.indexOf(filters.tool.value) >= 0) &&
      (!filters.mode.value || r.modes.indexOf(filters.mode.value) >= 0) &&
      (!filters.bg.value || r.backgrounds.indexOf(filters.bg.value) >= 0);
  }

  function median(rows) {
    var yrs = rows.map(function (r) { return r.yrs; }).filter(Boolean).sort(function (a, b) { return a - b; });
    if (!yrs.length) return '–';
    var mid = Math.floor(yrs.length / 2);
    return yrs.length % 2 ? yrs[mid] : Math.round((yrs[mid - 1] + yrs[mid]) / 2);
  }

  function pills(list) {
    return '<span class="bench-pills">' + list.map(function (v) {
      return '<span class="bench-pill">' + esc(v) + '</span>';
    }).join('') + '</span>';
  }

  function benchRow(r) {
    return '<tr>' +
      '<td><span class="bench-title">' + esc(r.title) + '</span> <span class="bench-tag">' + esc(trackTag(r.track)) + '</span>' +
      '<span class="bench-meta">' + esc(r.code + ' · ' + r.place) + '</span>' +
      (r.win ? '<span class="bench-win">' + esc(r.win) + '</span>' : '') + '</td>' +
      '<td class="bench-yrs" data-label="Yrs">' + (r.yrs || '–') + '</td>' +
      '<td data-label="Specialties">' + pills(r.pills) + '</td>' +
      '<td data-label="Tools">' + (r.tools.length ? pills(r.tools) : '–') + '</td>' +
      '<td data-label="Work style">' + esc(r.modes.join(' · ') || '–') + '</td>' +
      '<td><a class="unlock" href="' + askUrl(r) + '">Unlock</a></td>' +
      '</tr>';
  }

  var trackButtons = TRACKS.map(function (t) {
    var button = document.createElement('button');
    button.type = 'button';
    button.className = 'bench-track';
    button.addEventListener('click', function () {
      benchTrack = t.id;
      benchShown = PAGE_SIZE;
      renderBench();
    });
    byId('bench-tracks').appendChild(button);
    return button;
  });

  function renderBench() {
    TRACKS.forEach(function (t, i) {
      var rows = BENCH.filter(function (r) { return matches(r, true) && (t.id === 'all' || r.track === t.id); });
      var remote = rows.filter(function (r) { return r.modes.indexOf('Remote') >= 0; }).length;
      trackButtons[i].setAttribute('aria-pressed', benchTrack === t.id ? 'true' : 'false');
      trackButtons[i].innerHTML = '<span class="bench-track-name">' + t.name + '</span>' +
        '<span class="bench-track-count">' + rows.length + '<small>median ' + median(rows) + ' yrs</small></span>' +
        '<span class="bench-track-detail">' + remote + ' open to remote</span>' +
        '<span class="bench-track-bar"><i style="width:' + (rows.length ? remote / rows.length * 100 : 0) + '%"></i></span>';
    });

    var rows = BENCH.filter(function (r) { return matches(r); });
    rows.sort(function (a, b) {
      return filters.sort.value === 'least' ? (a.yrs || 99) - (b.yrs || 99) : (b.yrs || 0) - (a.yrs || 0);
    });
    byId('bench-rows').innerHTML = rows.length ?
      rows.slice(0, benchShown).map(benchRow).join('') :
      '<tr><td class="bench-empty" colspan="6">No recruiters match those filters. Clear a filter to see more.</td></tr>';
    byId('bench-count').textContent = rows.length + ' of ' + BENCH.length + ' recruiters match';
    byId('bench-more-row').hidden = rows.length <= benchShown;
    byId('bench-more').textContent = 'Show ' + Math.min(PAGE_SIZE, rows.length - benchShown) + ' more';
  }

  function clearBench() {
    benchTrack = 'all';
    benchShown = PAGE_SIZE;
    benchForm.reset();
  }

  addOptions(filters.spec, unique(flat('sectors')));
  addOptions(filters.tool, unique(flat('tools')));

  benchForm.addEventListener('input', function () {
    benchShown = PAGE_SIZE;
    renderBench();
  });
  benchForm.addEventListener('submit', function (e) { e.preventDefault(); });
  byId('bench-clear').addEventListener('click', function () {
    clearBench();
    renderBench();
  });
  byId('bench-more').addEventListener('click', function () {
    benchShown += PAGE_SIZE;
    renderBench();
  });

  // Get my Fab Five: fill the hero card with the five closest recruiters and filter the bench to exact matches.
  function fabFive() {
    var type = byId('hire-type');
    var mode = byId('hire-mode').value;
    var engagement = byId('hire-engagement').value;

    function fit(r) {
      return (r.track === type.value ? 4 : 0) + (r.modes.indexOf(mode) >= 0 ? 2 : 0) + (r.win ? 1 : 0);
    }

    var five = BENCH.slice().sort(function (a, b) { return fit(b) - fit(a) || (b.yrs || 0) - (a.yrs || 0); }).slice(0, 5);
    byId('fab-sub').textContent = type.options[type.selectedIndex].text + ' · ' + engagement + ' · ' + mode;
    byId('fab-list').innerHTML = five.map(function (r, i) {
      var line = [r.yrs ? r.yrs + '+ yrs' : '', r.place, r.pills[0]].filter(Boolean).join(' · ');
      return '<li class="fab-row"><span class="fab-rank">' + (i + 1) + '</span>' +
        '<div class="fab-who"><strong>' + esc(r.title) + '</strong><span>' + esc(line) + '</span></div>' +
        '<a class="unlock" href="' + askUrl(r) + '">Unlock</a></li>';
    }).join('');
  }

  byId('panel-hire').addEventListener('submit', function (e) {
    e.preventDefault();
    clearBench();
    benchTrack = byId('hire-type').value;
    filters.mode.value = byId('hire-mode').value;
    var exact = BENCH.filter(function (r) { return matches(r); }).length;
    if (!exact) clearBench();
    renderBench();
    fabFive();
    byId('fab-more').textContent = !exact ? 'Search the full bench' :
      exact === 1 ? 'See the 1 exact match' : 'See all ' + exact + ' exact matches';
    if (window.matchMedia('(max-width: 920px)').matches) byId('fab').scrollIntoView();
  });

  // Search tabs
  var tabs = Array.prototype.slice.call(document.querySelectorAll('[role="tab"]'));
  function showTab(name) {
    tabs.forEach(function (tab) {
      var on = tab.dataset.tab === name;
      tab.setAttribute('aria-selected', on ? 'true' : 'false');
      tab.tabIndex = on ? 0 : -1;
      byId('panel-' + tab.dataset.tab).hidden = !on;
    });
  }
  tabs.forEach(function (tab, i) {
    tab.addEventListener('click', function () { showTab(tab.dataset.tab); });
    tab.addEventListener('keydown', function (e) {
      if (e.key !== 'ArrowLeft' && e.key !== 'ArrowRight') return;
      var next = tabs[(i + 1) % tabs.length];
      showTab(next.dataset.tab);
      next.focus();
    });
  });

  renderBench();
  fabFive();
})();
