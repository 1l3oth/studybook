/* Interview prep: one daily session over the cooking talk, the Korean culture unit and the bridge
   questions. Spaced recall (Leitner boxes squeezed to the interview day), interleaved sources,
   active recall in your head, and a short before-sleep review of what you missed today. */
(function () {
  'use strict';
  var KEY = 'sb-prep-v1';
  var SOURCES = [
    { id: 'hobby', slug: 'korean-cooking-speech', name: '요리 이야기 · Cooking talk', color: '#00A84D' },
    { id: 'culture', slug: 'korean-culture-talk', name: '한국 문화 · Korean culture', color: '#996CAC' },
    { id: 'bridge', slug: 'interview-prep', name: '연결 질문 · Both together', color: '#EF7C1C' }
  ];
  var INTERVAL = [0, 1, 2, 3, 5, 8];
  var $ = function (id) { return document.getElementById(id); };
  var audio = new Audio();
  var items = [];
  var st = load();
  var queue = [], pos = 0, total = 0, cur = null;

  function load() {
    try { return JSON.parse(localStorage.getItem(KEY)) || {}; } catch (e) { return {}; }
  }
  function save() { localStorage.setItem(KEY, JSON.stringify(st)); }
  function day(d) { d = d || new Date(); return d.getFullYear() + '-' + ('0' + (d.getMonth() + 1)).slice(-2) + '-' + ('0' + d.getDate()).slice(-2); }
  function addDays(s, n) { var d = new Date(s + 'T12:00:00'); d.setDate(d.getDate() + n); return day(d); }
  function daysLeft() { return Math.round((new Date(interview() + 'T12:00:00') - new Date(day() + 'T12:00:00')) / 864e5); }
  function interview() { return st.interview || '2026-11-28'; }
  function rec(id) { return (st.items = st.items || {})[id] || null; }

  function url(src, p) { return src.slug === 'interview-prep' ? p : '../' + src.slug + '/' + p; }

  function build(unitBySrc, bridges) {
    SOURCES.forEach(function (src) {
      if (src.id === 'bridge') {
        bridges.forEach(function (b, i) { items.push(qItem(src, 'b' + i, b)); });
        return;
      }
      var u = unitBySrc[src.id];
      var secs = {};
      u.sections.forEach(function (s) { secs[s.id] = s; });
      u.cards.forEach(function (c, i) {
        items.push({ id: src.id + ':c' + i, src: src, type: 'card', img: url(src, c.img), alt: c.alt || '',
          hook: c.hook || '', prompt: c.en, ko: c.ko, en: c.en, audio: url(src, c.audio),
          chip: (secs[c.sec] || {}).ko || '' });
      });
      u.qa.forEach(function (b, bi) {
        if (b.kind === 'surv' || b.kind === 'gram') return;
        b.items.forEach(function (q, i) { items.push(qItem(src, 'q' + bi + '.' + i, q)); });
      });
    });
  }
  function qItem(src, key, q) {
    return { id: src.id + ':' + key, src: src, type: 'q', prompt: q.q, promptEn: q.qen, ko: q.a, en: q.aen,
      ask: q.iaudio ? url(src, q.iaudio) : (q.qaudio ? url(src, q.qaudio) : ''), audio: url(src, q.audio),
      check: !!q.check, chip: '질문' };
  }

  /* today's queue: due reviews first, then a share of new items so everything is seen before the interview */
  function todayQueue() {
    var today = day(), left = Math.max(1, daysLeft());
    var unseen = items.filter(function (it) { return !rec(it.id); });
    var newCap = Math.min(30, Math.max(10, Math.ceil(unseen.length / left)));
    if (st.newDay !== today) { st.newDay = today; st.newDone = 0; }
    newCap = Math.max(0, newCap - (st.newDone || 0));
    var pools = SOURCES.map(function (src) {
      var mine = items.filter(function (it) { return it.src === src; });
      var due = mine.filter(function (it) { var r = rec(it.id); return r && r.due <= today; });
      return { due: due, fresh: mine.filter(function (it) { return !rec(it.id); }) };
    });
    var out = [], added = true, n = 0;
    while (added) {  // interleave: one from each source in turn, each source keeps its own order
      added = false;
      pools.forEach(function (p) {
        if (p.due.length) { out.push(p.due.shift()); added = true; }
        else if (p.fresh.length && n < newCap) { out.push(p.fresh.shift()); n++; added = true; }
      });
    }
    return out;
  }
  function nightQueue() {
    var today = day();
    return items.filter(function (it) { var r = rec(it.id); return r && r.last === today && r.lastRate < 2; });
  }

  /* home */
  function renderHome() {
    var dl = daysLeft();
    $('dday').textContent = dl > 0 ? 'D-' + dl : dl === 0 ? 'D-Day' : 'Done';
    $('date').value = interview();
    var q = todayQueue();
    $('todayCount').textContent = q.length ? q.length + ' cards' : 'All done for today';
    $('todaySub').textContent = q.length ? 'About ' + Math.max(3, Math.round(q.length * 0.3)) + ' min · hobby, culture and both mixed' : 'Come back tomorrow. Spacing is what makes it stick.';
    $('start').disabled = !q.length;
    var nq = nightQueue();
    $('nightPanel').hidden = !nq.length;
    $('nightSub').textContent = nq.length + ' you missed or nearly knew today. One quick look before sleep helps them stay.';
    $('map').innerHTML = SOURCES.map(function (src) {
      var mine = items.filter(function (it) { return it.src === src; });
      var strong = mine.filter(function (it) { var r = rec(it.id); return r && r.box >= 3; }).length;
      return '<div class="maprow"><div class="name"><span style="color:' + src.color + '">' + src.name + '</span><em>' + strong + ' / ' + mine.length + ' solid</em></div><div class="dots">' +
        mine.map(function (it) { var r = rec(it.id); return '<i class="' + (r ? 'b' + Math.min(4, r.box) : 'b-n') + '"></i>'; }).join('') + '</div></div>';
    }).join('');
    show('home');
  }
  function show(id) { ['home', 'study', 'done'].forEach(function (x) { $(x).hidden = x !== id; }); window.scrollTo(0, 0); }

  /* study */
  function startSession(q) { queue = q.slice(); pos = 0; total = queue.length; show('study'); next(); }
  function next() {
    if (pos >= queue.length) return finish();
    cur = queue[pos];
    $('bar').style.width = Math.round(pos / Math.max(1, queue.length) * 100) + '%';
    $('left').textContent = (queue.length - pos) + ' left';
    $('chip').textContent = cur.src.name.split(' · ')[0] + (cur.chip ? ' · ' + cur.chip : '');
    $('chip').style.background = cur.src.color;
    var pic = $('pic');
    if (cur.type === 'card') {
      pic.className = 'pic';
      pic.innerHTML = '<img src="' + cur.img + '" alt="' + cur.alt.replace(/"/g, '&quot;') + '">';
      $('prompt').textContent = cur.prompt;
      $('promptEn').textContent = cur.hook ? 'Hint: ' + cur.hook : '';
    } else {
      pic.className = 'pic q';
      pic.innerHTML = '<span class="who">?</span><span>면접관 · The interviewer asks</span>';
      $('prompt').textContent = cur.prompt;
      $('promptEn').textContent = cur.promptEn || '';
      if (cur.ask) play(cur.ask);
    }
    $('answer').hidden = true; $('rate').hidden = true; $('reveal').hidden = false;
  }
  function reveal() {
    $('ko').textContent = cur.ko;
    $('en').textContent = cur.type === 'card' ? '' : cur.en;
    $('check').hidden = !cur.check;
    $('answer').hidden = false; $('rate').hidden = false; $('reveal').hidden = true;
    play(cur.audio);
  }
  function rate(r) {
    var today = day(), old = rec(cur.id), box = old ? old.box : 0;
    if (!old) st.newDone = (st.newDone || 0) + 1;
    box = r === 2 ? box + 1 : r === 1 ? Math.max(1, box) : 0;
    var gap = r === 2 ? INTERVAL[Math.min(box, INTERVAL.length - 1)] : 1;
    var dl = daysLeft();
    if (dl > 1) gap = Math.min(gap, dl - 1);  // always one last look the day before the interview
    st.items[cur.id] = { box: box, due: addDays(today, Math.max(1, gap)), last: today, lastRate: r };
    save();
    if (r === 0) queue.splice(Math.min(queue.length, pos + 4), 0, cur);  // see it again in a few cards
    pos++;
    next();
  }
  function finish() {
    $('bar').style.width = '100%';
    $('doneSub').textContent = total + ' cards done. Your memory map is updated.';
    show('done');
  }
  function play(src) { if (!src) return; audio.pause(); audio.src = src; audio.play().catch(function () {}); }

  $('start').onclick = function () { startSession(todayQueue()); };
  $('night').onclick = function () { startSession(nightQueue()); };
  $('reveal').onclick = reveal;
  $('listen').onclick = function () { play(cur.audio); };
  $('quit').onclick = function () { audio.pause(); renderHome(); };
  $('home2').onclick = renderHome;
  Array.prototype.forEach.call(document.querySelectorAll('#rate button'), function (b) { b.onclick = function () { rate(+b.dataset.r); }; });
  $('date').onchange = function () { if (this.value) { st.interview = this.value; save(); renderHome(); } };
  $('reset').onclick = function () { if (confirm('Clear your progress and start over?')) { st = { interview: st.interview }; save(); renderHome(); } };
  document.addEventListener('keydown', function (e) {
    if ($('study').hidden) return;
    if (e.key === ' ' || e.key === 'Enter') { e.preventDefault(); if (!$('reveal').hidden) reveal(); else play(cur.audio); }
    else if (!$('rate').hidden && '123'.indexOf(e.key) >= 0) rate(+e.key - 1);
  });

  function get(u) { return fetch(u).then(function (r) { return r.json(); }); }
  Promise.all([get('../korean-cooking-speech/unit.json'), get('../korean-culture-talk/unit.json'), get('bridges.json')])
    .then(function (r) { build({ hobby: r[0], culture: r[1] }, r[2]); st.items = st.items || {}; renderHome(); })
    .catch(function () { $('todayCount').textContent = 'Could not load the units. Check your connection.'; });
})();
