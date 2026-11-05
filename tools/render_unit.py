# -*- coding: utf-8 -*-
"""Render one Studybook unit page from <unit>/unit.json (standard library only).

    python tools/render_unit.py korean-funeral-visit

The page links the shared ../assets/line.css, unit.css and unit.js, so every unit has the same
look and behaviour. Audio and images stay as files beside the page (audio/, img/).
"""
import html
import io
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def e(s):
    return html.escape(s or '', quote=True)


PLAY = ('<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M8 5v14l11-7z" fill="currentColor"/></svg>')


def listen(au, label='듣기 · Listen', mini=False, extra=''):
    if not au:
        return ''
    if mini:
        return f'<button class="listen mini" type="button" data-au="{e(au)}" aria-label="Listen"{extra}>{PLAY}</button>'
    return f'<button class="listen" type="button" data-au="{e(au)}">{PLAY}<span>{e(label)}</span></button>'


def cplay(au, n, cls):
    if not au:
        return ''
    return (f'<button class="{cls}" type="button" data-au="{e(au)}" aria-label="Listen to card {n}">'
            '<svg viewBox="0 0 24 24" aria-hidden="true"><path class="i-play" d="M8 5v14l11-7z" fill="currentColor"/>'
            '<path class="i-stop" d="M7 6h3.5v12H7zM13.5 6H17v12h-3.5z" fill="currentColor"/></svg></button>')


def render(u):
    secs = {s['id']: s for s in u['sections']}
    color = lambda sid: secs.get(sid, {}).get('color', '#00A84D')
    cards = u['cards']
    vcount = sum(len(g['items']) for g in u['vocab'])
    qcount = sum(len(b['items']) for b in u['qa'] if b.get('kind') != 'surv')

    # ---- line map (spine) ----
    spine_secs = [s for s in u['sections'] if s.get('spine', True)]
    sp = u.get('spine', {})
    map_items = ''.join(
        f'<li data-sec="{e(s["id"])}" style="--lc:{e(s["color"])}"><button type="button">'
        f'<span class="m-ko" lang="ko">{e(s["ko"])}</span><span class="m-en">{e(s["en"])}</span></button></li>'
        for s in spine_secs)
    map_foot = ''
    if sp.get('audio') or sp.get('caption'):
        map_foot = f'<div class="foot">{listen(sp.get("audio"), mini=True)}<span>{e(sp.get("caption", ""))}</span></div>'
    map_html = (f'<section class="map" aria-label="Sections"><h2>{e(sp.get("title", "노선도 · The route"))}</h2>'
                f'<p class="note">{e(sp.get("note", ""))}</p><ol>{map_items}</ol>{map_foot}</section>')

    # ---- the big picture (eli5 style: big pictures, few words) ----
    ex = u.get('explain')
    ex_html = ''
    if ex:
        tiles = ''.join(
            f'<li style="--lc:{e(t.get("color", "#00A84D"))}"><img src="{e(t["img"])}" alt="" loading="lazy">'
            f'<b lang="ko">{e(t["ko"])}</b><span>{e(t["en"])}</span></li>' for t in ex['tiles'])
        why = f'<p class="eli-why">{e(ex["why"])}</p>' if ex.get('why') else ''
        ex_html = (f'<section class="eli" aria-label="The big picture"><h2>{e(ex.get("title", "한눈에 · The big picture"))}</h2>'
                   f'{why}<ol>{tiles}</ol></section>')

    # ---- cards ----
    ch = []
    for i, c in enumerate(cards):
        s = secs.get(c['sec'], {})
        flat = ' flat' if c.get('flat') else ''
        hook = f'<span class="hook" lang="ko">{e(c["hook"])}</span>' if c.get('hook') else ''
        ch.append(
            f'<article class="card" id="c{i + 1}" data-sec="{e(c["sec"])}" style="--lc:{e(color(c["sec"]))}">'
            f'<figure class="pic{flat}"><img loading="lazy" src="{e(c["img"])}" alt="{e(c.get("alt") or c["en"])}">'
            f'{cplay(c.get("audio"), i + 1, "cplay")}</figure>'
            f'<div class="cbody"><div class="ctop"><span class="num">{i + 1:02d}</span>'
            f'<span class="sec-chip"><span lang="ko">{e(s.get("ko", ""))}</span>&nbsp;· {e(s.get("en", ""))}</span>{hook}</div>'
            f'<p class="ko" lang="ko">{e(c["ko"])}</p><span class="prog" aria-hidden="true"><i></i></span>'
            f'<p class="en">{e(c["en"])}</p></div>{cplay(c.get("audio"), i + 1, "rplay")}</article>')

    # ---- Q&A ----
    qh = []
    n = 0
    for b in u['qa']:
        small = f' <small>{e(b["small"])}</small>' if b.get('small') else ''
        qh.append(f'<h2 class="qsec">{e(b["title"])}{small}</h2>')
        if b.get('note'):
            qh.append(f'<p class="note">{e(b["note"])}</p>')
        if b.get('kind') == 'surv':
            for it in b['items']:
                qh.append(f'<div class="surv"><span class="sko" lang="ko">{e(it["ko"])}'
                          f'<span class="sen">{e(it.get("en"))}</span></span>{listen(it.get("audio"), mini=True)}</div>')
            continue
        last_group = None
        for it in b['items']:
            if it.get('group') and it['group'] != last_group:
                qh.append(f'<h3 class="qgrp">{e(it["group"])}</h3>')
                last_group = it['group']
            n += 1
            trap = b.get('kind') == 'trap'
            mark = '문' if b.get('kind') == 'gram' else 'Q'
            check = '<span class="check">확인 필요 · check</span>' if it.get('check') else ''
            why = f'<p class="why">{e(it["why"])}</p>' if it.get('why') else ''
            aen = f'<p class="aen">{e(it["aen"])}</p>' if it.get('aen') else ''
            qen = f'<span class="qen">{e(it["qen"])}</span>' if it.get('qen') else ''
            aid = f'qa{n}'
            qh.append(
                f'<article class="qa{" trap" if trap else ""}"><div class="qhead">'
                f'<button class="q" type="button" aria-expanded="false" aria-controls="{aid}">'
                f'<span class="qm">{mark}</span><span class="qt"><span class="qko" lang="ko">{e(it["q"])}</span>{qen}</span>'
                f'<svg class="chev" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" aria-hidden="true"><path d="M6 9l6 6 6-6"/></svg>'
                f'</button>{listen(it.get("qaudio"), mini=True)}</div>'
                f'<div class="a" id="{aid}"><p class="ako" lang="ko">{e(it["a"])}{check}</p>{aen}{why}{listen(it.get("audio"))}</div></article>')

    # ---- vocab ----
    vh = []
    for g in u['vocab']:
        lc = f' style="--lc:{e(g["color"])}"' if g.get('color') else ''
        vh.append(f'<h2 class="vgrp"{lc}>{e(g["title"])}</h2><ul class="vlist">')
        for it in g['items']:
            vh.append(f'<li class="voc">{listen(it.get("audio"), mini=True)}<span class="vko" lang="ko">{e(it["ko"])}</span>'
                      f'<span class="ven">{e(it["en"])}</span></li>')
        vh.append('</ul>')

    # ---- full text ----
    fh = [f'<h2>{e(u.get("full_title", "대본 · The text"))}</h2>']
    for s in u['full']:
        fh.append(f'<h3>{e(s["title"])}</h3><p class="fko" lang="ko">{e(s["ko"])}</p><p class="fen">{e(s["en"])}</p>')
    qtab = u.get('qa_tab', {'ko': '예상 질문', 'en': 'Q&A'})
    fh.append(f'<h2>{e(qtab["ko"])} · {e(qtab["en"])}</h2>')
    for b in u['qa']:
        fh.append(f'<h3>{e(b["title"])}</h3>')
        for it in b['items']:
            if b.get('kind') == 'surv':
                fh.append(f'<div class="fqa"><p class="fa" lang="ko">{e(it["ko"])}</p><p class="fsub">{e(it.get("en"))}</p></div>')
            else:
                fh.append(f'<div class="fqa"><p class="fq" lang="ko">{"문" if b.get("kind") == "gram" else "Q"}. {e(it["q"])}</p>'
                          + (f'<p class="fsub">{e(it["qen"])}</p>' if it.get('qen') else '')
                          + f'<p class="fa" lang="ko">A. {e(it["a"])}</p>'
                          + (f'<p class="fsub">{e(it["aen"])}</p>' if it.get('aen') else '') + '</div>')
    fh.append(f'<h2>단어 · Vocabulary ({vcount})</h2>')
    for g in u['vocab']:
        fh.append(f'<h3>{e(g["title"])}</h3><div class="fvoc">'
                  + ''.join(f'<div class="fv"><b lang="ko">{e(it["ko"])}</b><span>{e(it["en"])}</span></div>' for it in g['items'])
                  + '</div>')

    ICON = {
        'play': '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M8 5v14l11-7z" fill="currentColor"/></svg>',
        'eye': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M3 3l18 18M10.6 6.1A9.8 9.8 0 0 1 12 6c5 0 9 6 9 6a17 17 0 0 1-2.6 3.2M6.3 7.6C4.2 9.2 3 12 3 12s4 6 9 6c1.4 0 2.7-.4 3.8-1"/></svg>',
        'focus': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M4 9V5h4M20 9V5h-4M4 15v4h4M20 15v4h-4"/></svg>',
        'print': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M7 9V3h10v6M7 17H4v-7h16v7h-3M7 14h10v7H7z"/></svg>',
        'back': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M15 5l-7 7 7 7"/></svg>',
        'close': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" aria-hidden="true"><path d="M6 6l12 12M18 6L6 18"/></svg>',
    }

    return f'''<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{e(u["title_ko"])} · {e(u["title_en"])} · 스터디북</title>
<meta name="description" content="{e(u.get("description", u["title_en"]))}">
<meta name="theme-color" content="#1C2A4A">
<link rel="manifest" href="../manifest.webmanifest">
<link rel="icon" href="../icons/icon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="../icons/apple-touch-icon.png">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Gothic+A1:wght@400;500;700;800&display=swap">
<link rel="stylesheet" href="../assets/line.css">
<link rel="stylesheet" href="../assets/unit.css">
</head>
<body data-unit="{e(u["slug"])}">
<header class="usign">
  <div class="wrap">
    <div class="row"><a class="back" href="../">{ICON["back"]}노선도 · All units</a></div>
    <div class="utitle"><h1>{e(u["title_ko"])}</h1><p>{e(u["title_en"])}{(" · " + e(u["subtitle"])) if u.get("subtitle") else ""}</p></div>
  </div>
  <div class="stripe" aria-hidden="true"></div>
  <nav class="tabs wrap" role="tablist" aria-label="Unit parts">
    <button role="tab" data-tab="cards" aria-controls="p-cards">그림 카드<small>{len(cards)} cards</small></button>
    <button role="tab" data-tab="qa" aria-controls="p-qa">{e(qtab["ko"])}<small>{qcount} {e(qtab["en"])}</small></button>
    <button role="tab" data-tab="voc" aria-controls="p-voc">단어<small>{vcount} words</small></button>
    <button role="tab" data-tab="full" aria-controls="p-full">전체<small>read all</small></button>
  </nav>
</header>

<main class="wrap">
  <section class="panel" id="p-cards" role="tabpanel">
    {ex_html}
    {map_html}
    <ol class="how"><li><b>1</b>Look at the picture</li><li><b>2</b>Recall the Korean in your head</li><li><b>3</b>Tap to check, then listen</li></ol>
    <div class="platform">
      <section class="stage" id="stage" aria-label="Now studying" aria-live="polite">
        <figure class="pic"><img src="{e(cards[0]["img"])}" alt=""></figure>
        <div class="st-body">
          <div class="ctop"></div>
          <p class="ko st-ko" lang="ko" tabindex="0"></p>
          <span class="prog" aria-hidden="true"><i></i></span>
          <p class="en st-en"></p>
          <div class="st-ctl">
            <button class="st-nav" id="stPrev" type="button" aria-label="Previous card"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M15 5l-7 7 7 7"/></svg></button>
            <button class="bigplay" id="stPlay" type="button" aria-label="Listen"><svg viewBox="0 0 24 24" aria-hidden="true"><path class="i-play" d="M8 5v14l11-7z" fill="currentColor"/><path class="i-stop" d="M7 6h3.5v12H7zM13.5 6H17v12h-3.5z" fill="currentColor"/></svg></button>
            <button class="st-nav" id="stNext" type="button" aria-label="Next card"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M9 5l7 7-7 7"/></svg></button>
            <span class="st-count"></span>
          </div>
          <p class="keys"><kbd>Space</kbd> listen · <kbd>←</kbd> <kbd>→</kbd> move · <kbd>K</kbd> show Korean</p>
        </div>
      </section>
      <div class="cards" role="list" aria-label="All lines">{"".join(ch)}</div>
    </div>
  </section>
  <section class="panel" id="p-qa" role="tabpanel">{"".join(qh)}</section>
  <section class="panel" id="p-voc" role="tabpanel">
    <p class="note">Tap a word's play button to hear it. Hide one side, then recall it before you tap to check.</p>
    {"".join(vh)}
  </section>
  <section class="panel full" id="p-full" role="tabpanel">{"".join(fh)}</section>
</main>

<div class="dock">
  <div class="acts" id="a-cards">
    <button class="btn primary" id="openFocus" type="button">{ICON["focus"]}집중</button>
    <button class="btn" id="playAll" type="button" aria-pressed="false">{ICON["play"]}<span>전체 듣기</span></button>
    <button class="btn" type="button" data-toggle="hide-ko" aria-pressed="false" aria-label="Hide Korean">{ICON["eye"]}한국어</button>
    <button class="btn" type="button" data-toggle="hide-en" aria-pressed="false" aria-label="Hide English">{ICON["eye"]}영어</button>
  </div>
  <div class="acts" id="a-qa" hidden>
    <button class="btn" type="button" data-toggle="reveal-all" aria-pressed="false">답 모두 보기 · Show all answers</button>
  </div>
  <div class="acts" id="a-voc" hidden>
    <button class="btn" type="button" data-toggle="hide-vko" aria-pressed="false">{ICON["eye"]}한국어 가리기</button>
    <button class="btn" type="button" data-toggle="hide-ven" aria-pressed="false">{ICON["eye"]}Hide English</button>
  </div>
  <div class="acts" id="a-full" hidden>
    <button class="btn" type="button" data-toggle="hide-fen" aria-pressed="false">{ICON["eye"]}Hide English</button>
    <button class="btn" id="printFull" type="button">{ICON["print"]}Print / PDF</button>
  </div>
</div>

<section class="focus" id="focus" role="dialog" aria-modal="true" aria-label="Focus mode, one card at a time" hidden>
  <div class="f-top">
    <button class="f-close" type="button" aria-label="Close focus mode">{ICON["close"]}</button>
    <span class="f-count">1 / {len(cards)}</span>
    <div class="f-track" aria-hidden="true"><span class="f-dot"></span></div>
  </div>
  <div class="f-stage">
    <div class="f-card">
      <figure class="pic"><img src="{e(cards[0]["img"])}" alt=""></figure>
      <div class="cbody">
        <div class="ctop"></div>
        <p class="ko hidden" lang="ko"></p>
        <p class="f-hint">Say it in your head first, then tap the box to check.</p>
        <p class="en"></p>
      </div>
    </div>
  </div>
  <div class="f-nav">
    <button class="btn" id="fPrev" type="button">이전 · Back</button>
    <button class="btn primary" id="fListen" type="button">{ICON["play"]}듣기 · Listen</button>
    <button class="btn" id="fNext" type="button"><span>다음 · Next</span></button>
  </div>
</section>

<script src="../assets/unit.js" defer></script>
</body>
</html>
'''


def main():
    slug = sys.argv[1]
    d = os.path.join(ROOT, slug)
    u = json.load(io.open(os.path.join(d, 'unit.json'), encoding='utf-8'))
    out = render(u)
    io.open(os.path.join(d, 'index.html'), 'w', encoding='utf-8', newline='\n').write(out)
    print(f'{slug}: {len(u["cards"])} cards, '
          f'{sum(len(b["items"]) for b in u["qa"])} Q&A items, {sum(len(g["items"]) for g in u["vocab"])} words, '
          f'{len(out) // 1024} KB')


if __name__ == '__main__':
    main()
