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
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from romanize import romanize  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def e(s):
    return html.escape(s or '', quote=True)


HANGUL = re.compile('[가-힣ㄱ-ㅎ]')
V = 'v=voc2'  # bump when assets change, so a new page never meets an old cached stylesheet
SITE = 'https://1l3oth.github.io/studybook/'


def t(s):
    """Text that can hold Korean: the Hangul, plus its Lyric. The page's switch shows one of them."""
    if not s or not HANGUL.search(s):
        return e(s)
    return f'<span class="t-ko">{e(s)}</span><span class="t-ro" lang="ko-Latn">{e(romanize(s))}</span>'


def m(s):
    """A label such as 시작 · Opening. In English mode only the English part stays."""
    parts = (s or '').split(' · ')
    has_en = any(not HANGUL.search(p) for p in parts)
    if len(parts) < 2 or not has_en:
        return t(s)
    out = []
    for i, p in enumerate(parts):
        sep = ' · ' if i < len(parts) - 1 else ''
        if HANGUL.search(p):
            out.append(f'<span class="mk">{t(p)}{sep}</span>')
        else:
            out.append(e(p) + (f'<span class="not-ko-end">{sep}</span>' if sep else ''))
    return ''.join(out)


def ui(ko, en):
    """A control's label: Korean in Korean mode, English otherwise, so anyone can work the page."""
    return f'<span class="ui-ko">{e(ko)}</span><span class="ui-en">{e(en)}</span>'


def he(cls, has):
    return f'{cls} has-en' if has else cls


SWITCH = ('<div class="script" role="group" aria-label="Show text in">'
          '<button type="button" data-set="en" aria-pressed="false">English</button>'
          '<button type="button" data-set="ko" aria-pressed="true" lang="ko">한국어</button>'
          '<button type="button" data-set="ro" aria-pressed="false">Lyric</button></div>')
GUIDE = ('<p class="note only-ro">Lyric: Korean in English letters, so you can read it out loud. '
         'eo sounds like the u in up, eu like the oo in good, ae like the e in bed.</p>')

PLAY = ('<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M8 5v14l11-7z" fill="currentColor"/></svg>')


def listen(au, label=None, mini=False, extra=''):
    if not au:
        return ''
    if mini:
        return f'<button class="listen mini" type="button" data-au="{e(au)}" aria-label="Listen"{extra}>{PLAY}</button>'
    return f'<button class="listen" type="button" data-au="{e(au)}">{PLAY}<span>{ui('듣기 · Listen', 'Listen')}</span></button>'


XP = ('<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 9h4l5-4v14l-5-4H4z" fill="currentColor"/>'
      '<path d="M16 8.5a5 5 0 0 1 0 7M18.5 6a8.5 8.5 0 0 1 0 12" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>')


def xp(au):
    """The English explainer button: a small speaker that reads the meaning or the note in English."""
    if not au:
        return ''
    return f'<button class="xp" type="button" data-au="{e(au)}" aria-label="Explain in English">{XP}<b>EN</b></button>'


# Chat-style Q&A: the asker on the left, you on the right. Inline SVG so CSS can animate the mouth
# while a clip plays (.msg.speaking) and blink the eyes.
ASKER_SVG = ('<svg class="av" viewBox="0 0 64 64" aria-hidden="true"><circle cx="32" cy="32" r="32" fill="#E7E2F3"/>'
             '<path d="M10 64 Q10 44 32 44 Q54 44 54 64Z" fill="#1C2A4A"/><path d="M26 44 L32 54 L38 44Z" fill="#fff"/>'
             '<path d="M17 34 Q15 12 32 12 Q49 12 47 34 Q47 40 44 42 L44 28 Q32 26 20 28 L20 42 Q17 40 17 34Z" fill="#3B2A23"/>'
             '<ellipse cx="32" cy="30" rx="12" ry="14" fill="#F2C9A5"/>'
             '<path d="M20 26 Q26 14 44 24 Q40 18 32 17 Q22 17 20 26Z" fill="#3B2A23"/>'
             '<g class="eye"><circle cx="27" cy="29" r="1.8" fill="#23262D"/><circle cx="37" cy="29" r="1.8" fill="#23262D"/></g>'
             '<circle cx="27" cy="29" r="4.2" fill="none" stroke="#23262D" stroke-width="1.3"/>'
             '<circle cx="37" cy="29" r="4.2" fill="none" stroke="#23262D" stroke-width="1.3"/><path d="M31.2 29 H32.8" stroke="#23262D" stroke-width="1.3"/>'
             '<ellipse class="mouth" cx="32" cy="37.5" rx="3.2" ry="1.6" fill="#B5544A"/></svg>')
ME_SVG = ('<svg class="av" viewBox="0 0 64 64" aria-hidden="true"><circle cx="32" cy="32" r="32" fill="#DCEBFA"/>'
          '<path d="M10 64 Q10 44 32 44 Q54 44 54 64Z" fill="#0052A4"/><path d="M27 44 Q32 50 37 44" fill="none" stroke="#fff" stroke-width="2"/>'
          '<ellipse cx="32" cy="30" rx="12" ry="14" fill="#D9A27A"/>'
          '<path d="M19 28 Q18 13 32 13 Q46 13 45 28 Q42 20 32 20 Q23 20 19 28Z" fill="#1B1B1F"/>'
          '<g class="eye"><circle cx="27" cy="30" r="1.8" fill="#23262D"/><circle cx="37" cy="30" r="1.8" fill="#23262D"/></g>'
          '<ellipse class="mouth" cx="32" cy="37.5" rx="3.2" ry="1.6" fill="#9C4A3E"/></svg>')


def chat_pair(it, n, trap, them, me):
    """One question and answer as two chat messages. The answer stays covered until you tap it."""
    aid = f'qa{n}'
    qen = f'<p class="qen">{t(it["qen"])}</p>' if it.get('qen') else ''
    check = f'<span class="check">{ui("확인 필요 · check", "check")}</span>' if it.get('check') else ''
    why = f'<p class="why">{t(it["why"])}</p>' if it.get('why') else ''
    aen = f'<p class="aen">{xp(it.get("aen_audio"))}{t(it["aen"])}</p>' if it.get('aen') else ''
    tag = f'<span class="trap-tag">{ui("함정", "Trap")}</span>' if trap else ''
    qa_au = it.get('iaudio') or it.get('qaudio')
    return (f'<div class="msg them{" trap" if trap else ""}">{ASKER_SVG}<div class="bub">'
            f'<span class="who">{m(them)}{tag}</span>'
            f'<p class="{he("qko", it.get("qen"))}" lang="ko">{t(it["q"])}</p>{qen}'
            f'{listen(qa_au, mini=True)}</div></div>'
            f'<div class="msg me"><div class="bub ans" id="{aid}"><span class="who">{m(me)}</span>'
            f'<button class="cover" type="button" aria-controls="{aid}">{ui("먼저 생각하고, 탭하세요", "Think of your answer, then tap")}</button>'
            f'<div class="inner"><p class="{he("ako", it.get("aen"))}" lang="ko">{t(it["a"])}{check}</p>{aen}'
            f'{listen(it.get("audio"), mini=True)}{why}</div>'
            f'<span class="dots" aria-hidden="true"><i></i><i></i><i></i></span></div>{ME_SVG}</div>')


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
        f'<span class="m-ko has-en" lang="ko">{t(s["ko"])}</span><span class="m-en">{t(s["en"])}</span></button></li>'
        for s in spine_secs)
    map_foot = ''
    if sp.get('audio') or sp.get('caption'):
        map_foot = f'<div class="foot">{listen(sp.get("audio"), mini=True)}<span>{t(sp.get("caption", ""))}</span></div>'
    map_html = (f'<section class="map" aria-label="Sections"><h2>{m(sp.get("title", "노선도 · The route"))}</h2>'
                f'<p class="note">{t(sp.get("note", ""))}</p><ol>{map_items}</ol>{map_foot}</section>')

    # ---- the big picture (eli5 style: big pictures, few words) ----
    ex = u.get('explain')
    ex_html = ''
    if ex:
        tiles = ''.join(
            f'<li style="--lc:{e(x.get("color", "#00A84D"))}"><img src="{e(x["img"])}" alt="" loading="lazy">'
            f'<b class="has-en" lang="ko">{t(x["ko"])}</b><span>{t(x["en"])}</span></li>' for x in ex['tiles'])
        why = f'<p class="eli-why">{t(ex["why"])}</p>' if ex.get('why') else ''
        ex_html = (f'<section class="eli" aria-label="The big picture"><h2>{m(ex.get("title", "한눈에 · The big picture"))}</h2>'
                   f'{why}<ol>{tiles}</ol></section>')

    # ---- cards ----
    ch = []
    for i, c in enumerate(cards):
        s = secs.get(c['sec'], {})
        flat = ' flat' if c.get('flat') else ''
        hook = f'<span class="hook" lang="ko">{t(c["hook"])}</span>' if c.get('hook') else ''
        ch.append(
            f'<article class="card" id="c{i + 1}" data-sec="{e(c["sec"])}" style="--lc:{e(color(c["sec"]))}">'
            f'<figure class="pic{flat}"><img loading="lazy" src="{e(c["img"])}" alt="{e(c.get("alt") or c["en"])}">'
            f'{cplay(c.get("audio"), i + 1, "cplay")}</figure>'
            f'<div class="cbody"><div class="ctop"><span class="num">{i + 1:02d}</span>'
            f'<span class="sec-chip"><span class="mk" lang="ko">{t(s.get("ko", ""))}&nbsp;· </span>{t(s.get("en", ""))}</span>{hook}</div>'
            f'<p class="ko has-en" lang="ko">{t(c["ko"])}</p><span class="prog" aria-hidden="true"><i></i></span>'
            f'<p class="en">{xp(c.get("en_audio"))}{t(c["en"])}</p></div>{cplay(c.get("audio"), i + 1, "rplay")}</article>')

    # ---- Q&A ----
    qh = [f'<p class="note">{t(u["qa_note"])}</p>'] if u.get('qa_note') else []
    n = 0
    for b in u['qa']:
        small = f' <small>{t(b["small"])}</small>' if b.get('small') else ''
        qh.append(f'<h2 class="qsec">{m(b["title"])}{small}</h2>')
        if b.get('note'):
            qh.append(f'<p class="note">{t(b["note"])}</p>')
        if b.get('kind') == 'surv':
            for it in b['items']:
                qh.append(f'<div class="surv"><span class="sko" lang="ko"><span class="{"mk" if it.get("en") else ""}">{t(it["ko"])}</span>'
                          f'<span class="sen">{xp(it.get("en_audio"))}{t(it.get("en"))}</span></span>{listen(it.get("audio"), mini=True)}</div>')
            continue
        last_group = None
        if b.get('kind') != 'gram':  # questions someone asks you: a chat
            chat = u.get('chat', {})
            them, me = chat.get('them', '상대 · The other person'), chat.get('me', '나 · Me')
            qh.append('<div class="chat">')
            for it in b['items']:
                if it.get('group') and it['group'] != last_group:
                    qh.append(f'<h3 class="qgrp chip">{m(it["group"])}</h3>')
                    last_group = it['group']
                n += 1
                qh.append(chat_pair(it, n, b.get('kind') == 'trap', them, me))
            qh.append('</div>')
            continue
        for it in b['items']:
            if it.get('group') and it['group'] != last_group:
                qh.append(f'<h3 class="qgrp">{m(it["group"])}</h3>')
                last_group = it['group']
            n += 1
            trap = b.get('kind') == 'trap'
            mark = ui('문', 'G') if b.get('kind') == 'gram' else 'Q'
            check = f'<span class="check">{ui("확인 필요 · check", "check")}</span>' if it.get('check') else ''
            why = f'<p class="why">{xp(it.get("why_audio"))}{t(it["why"])}</p>' if it.get('why') else ''
            aen = f'<p class="aen">{xp(it.get("aen_audio"))}{t(it["aen"])}</p>' if it.get('aen') else ''
            qen = f'<span class="qen">{t(it["qen"])}</span>' if it.get('qen') else ''
            aid = f'qa{n}'
            qh.append(
                f'<article class="qa{" trap" if trap else ""}"><div class="qhead">'
                f'<button class="q" type="button" aria-expanded="false" aria-controls="{aid}">'
                f'<span class="qm">{mark}</span><span class="qt"><span class="{he("qko", it.get("qen"))}" lang="ko">{t(it["q"])}</span>{qen}</span>'
                f'<svg class="chev" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" aria-hidden="true"><path d="M6 9l6 6 6-6"/></svg>'
                f'</button>{listen(it.get("qaudio"), mini=True)}</div>'
                f'<div class="a" id="{aid}"><p class="{he("ako", it.get("aen"))}" lang="ko">{t(it["a"])}{check}</p>{aen}{why}{listen(it.get("audio"))}</div></article>')

    # ---- vocab ----
    vh = []
    for g in u['vocab']:
        lc = f' style="--lc:{e(g["color"])}"' if g.get('color') else ''
        vh.append(f'<h2 class="vgrp"{lc}>{m(g["title"])}</h2><ul class="vlist">')
        for it in g['items']:
            pic = (f'<figure class="vfig"><img class="vpic" src="{e(it["img"])}" alt="" loading="lazy"></figure>' if it.get('img') else '')
            ex = it.get('ex') or {}
            exh = (f'<div class="vex"><p class="exko has-en" lang="ko">{t(ex["ko"])}</p>{listen(ex.get("audio"), mini=True)}'
                   f'<p class="exen">{xp(ex.get("en_audio"))}{t(ex.get("en", ""))}</p></div>') if ex.get('ko') else ''
            vh.append(f'<li class="voc{" haspic" if pic else ""}">{pic}<div class="vtext"><div class="vrow">{listen(it.get("audio"), mini=True)}'
                      f'<span class="vko has-en" lang="ko">{t(it["ko"])}</span></div>'
                      f'<span class="ven">{xp(it.get("en_audio"))}{t(it["en"])}</span>{exh}</div></li>')
        vh.append('</ul>')

    # ---- full text ----
    fh = [GUIDE, f'<h2>{m(u.get("full_title", "대본 · The text"))}</h2>']
    for s in u['full']:
        fh.append(f'<h3>{m(s["title"])}</h3><p class="fko has-en" lang="ko">{t(s["ko"])}</p><p class="fen">{t(s["en"])}</p>')
    qtab = u.get('qa_tab', {'ko': '예상 질문', 'en': 'Q&A'})
    fh.append(f'<h2>{m(qtab["ko"] + " · " + qtab["en"])}</h2>')
    for b in u['qa']:
        fh.append(f'<h3>{m(b["title"])}</h3>')
        for it in b['items']:
            if b.get('kind') == 'surv':
                fh.append(f'<div class="fqa"><p class="{he("fa", it.get("en"))}" lang="ko">{t(it["ko"])}</p><p class="fsub">{t(it.get("en"))}</p></div>')
            else:
                qm = ui("문", "G") if b.get("kind") == "gram" else "Q"
                fh.append(f'<div class="fqa"><p class="{he("fq", it.get("qen"))}" lang="ko">{qm}. {t(it["q"])}</p>'
                          + (f'<p class="fsub">{qm}. {t(it["qen"])}</p>' if it.get('qen') else '')
                          + f'<p class="{he("fa", it.get("aen"))}" lang="ko">A. {t(it["a"])}</p>'
                          + (f'<p class="fsub">A. {t(it["aen"])}</p>' if it.get('aen') else '') + '</div>')
    fh.append(f'<h2>{m(f"단어 · Vocabulary ({vcount})")}</h2>')
    for g in u['vocab']:
        fh.append(f'<h3>{m(g["title"])}</h3><div class="fvoc">'
                  + ''.join(f'<div class="fv"><b class="has-en" lang="ko">{t(it["ko"])}</b><span>{t(it["en"])}</span></div>' for it in g['items'])
                  + '</div>')

    credit = f'<p class="credit">{t(u["credit"])}</p>' if u.get('credit') else ''
    fh.append(credit)

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
<meta property="og:type" content="website">
<meta property="og:site_name" content="다라봇 스터디북 · Studybook">
<meta property="og:title" content="{e(u["title_ko"])} · {e(u["title_en"])}">
<meta property="og:description" content="{e(u.get("description", u["title_en"]))}">
<meta property="og:url" content="{SITE}{e(u["slug"])}/">
<meta property="og:image" content="{SITE}og/{e(u["slug"])}.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{e(u["title_ko"])} · {e(u["title_en"])}">
<meta name="twitter:card" content="summary_large_image">
<link rel="manifest" href="../manifest.webmanifest">
<link rel="icon" href="../icons/icon.svg" type="image/svg+xml">
<link rel="icon" href="../icons/favicon-32.png" sizes="32x32" type="image/png">
<link rel="apple-touch-icon" href="../icons/apple-touch-icon.png">
<link rel="apple-touch-icon" sizes="120x120" href="../icons/apple-touch-icon-120.png">
<link rel="apple-touch-icon" sizes="152x152" href="../icons/apple-touch-icon-152.png">
<link rel="apple-touch-icon" sizes="167x167" href="../icons/apple-touch-icon-167.png">
<link rel="apple-touch-icon" sizes="180x180" href="../icons/apple-touch-icon.png">
<meta name="apple-mobile-web-app-title" content="스터디북">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Gothic+A1:wght@400;500;700;800&display=swap">
<link rel="stylesheet" href="../assets/line.css?{V}">
<link rel="stylesheet" href="../assets/unit.css?{V}">
<script src="../assets/script.js?{V}"></script>
</head>
<body data-unit="{e(u["slug"])}">
<header class="usign">
  <div class="wrap">
    <div class="row"><a class="back" href="../">{ICON["back"]}{ui("노선도 · All units", "All units")}</a>{SWITCH}</div>
    <div class="utitle"><h1><span class="mk">{t(u["title_ko"])}</span><span class="only-en">{e(u["title_en"])}</span></h1><p><span class="not-en">{e(u["title_en"])}{" · " if u.get("subtitle") else ""}</span>{t(u.get("subtitle"))}</p></div>
  </div>
  <div class="stripe" aria-hidden="true"></div>
  <nav class="tabs wrap" role="tablist" aria-label="Unit parts">
    <button role="tab" data-tab="cards" aria-controls="p-cards"><span>{ui("그림 카드", "Cards")}</span><small>{len(cards)} cards</small></button>
    <button role="tab" data-tab="qa" aria-controls="p-qa"><span>{ui(qtab["ko"], qtab["en"])}</span><small>{qcount} {e(qtab["en"])}</small></button>
    <button role="tab" data-tab="voc" aria-controls="p-voc"><span>{ui("단어", "Words")}</span><small>{vcount} words</small></button>
    <button role="tab" data-tab="full" aria-controls="p-full"><span>{ui("전체", "Full")}</span><small>read all</small></button>
  </nav>
</header>

<main class="wrap">
  <section class="panel" id="p-cards" role="tabpanel">
    {ex_html}
    {map_html}
    {GUIDE}
    <ol class="how"><li><b>1</b>Look at the picture</li><li><b>2</b>Recall the Korean in your head</li><li><b>3</b>Tap to check, then listen</li></ol>
    <div class="platform">
      <section class="stage" id="stage" aria-label="Now studying" aria-live="polite">
        <figure class="pic"><img src="{e(cards[0]["img"])}" alt=""></figure>
        <div class="st-body">
          <div class="ctop"></div>
          <p class="ko st-ko has-en" lang="ko" tabindex="0"></p>
          <span class="prog" aria-hidden="true"><i></i></span>
          <p class="en st-en"></p>
          <div class="st-ctl">
            <button class="st-nav" id="stPrev" type="button" aria-label="Previous card"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M15 5l-7 7 7 7"/></svg></button>
            <button class="bigplay" id="stPlay" type="button" aria-label="Listen"><svg viewBox="0 0 24 24" aria-hidden="true"><path class="i-play" d="M8 5v14l11-7z" fill="currentColor"/><path class="i-stop" d="M7 6h3.5v12H7zM13.5 6H17v12h-3.5z" fill="currentColor"/></svg></button>
            <button class="st-nav" id="stNext" type="button" aria-label="Next card"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M9 5l7 7-7 7"/></svg></button>
            <span class="st-count"></span>
          </div>
          <p class="keys"><kbd>Space</kbd> listen · <kbd>←</kbd> <kbd>→</kbd> move · <kbd>K</kbd> show text</p>
        </div>
      </section>
      <div class="cards" role="list" aria-label="All lines">{"".join(ch)}</div>
    </div>
    {credit}
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
    <button class="btn primary" id="openFocus" type="button">{ICON["focus"]}{ui("집중", "Focus")}</button>
    <button class="btn" id="playAll" type="button" aria-pressed="false">{ICON["play"]}<span>{ui("전체 듣기", "Play all")}</span></button>
    <button class="btn" type="button" data-toggle="hide-ko" aria-pressed="false" aria-label="Hide Korean or Lyric">{ICON["eye"]}{ui("한국어", "Lyric")}</button>
    <button class="btn" type="button" data-toggle="hide-en" aria-pressed="false" aria-label="Hide English">{ICON["eye"]}{ui("영어", "English")}</button>
  </div>
  <div class="acts" id="a-qa" hidden>
    <button class="btn primary" id="playTalk" type="button" aria-pressed="false">{ICON["play"]}<span>{ui("대화 재생", "Play the talk")}</span></button>
    <button class="btn" type="button" data-toggle="reveal-all" aria-pressed="false">{ui("답 모두 보기", "Show all answers")}</button>
  </div>
  <div class="acts" id="a-voc" hidden>
    <button class="btn" type="button" data-toggle="hide-vko" aria-pressed="false">{ICON["eye"]}{ui("한국어 가리기", "Hide Lyric")}</button>
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
    <span class="f-count">1 / {len(cards)}</span>{SWITCH}
    <div class="f-track" aria-hidden="true"><span class="f-dot"></span></div>
  </div>
  <div class="f-stage">
    <div class="f-card">
      <figure class="pic"><img src="{e(cards[0]["img"])}" alt=""></figure>
      <div class="cbody">
        <div class="ctop"></div>
        <p class="ko hidden has-en" lang="ko"></p>
        <p class="f-hint">Say it in your head first, then tap the box to check.</p>
        <p class="en"></p>
      </div>
    </div>
  </div>
  <div class="f-nav">
    <button class="btn" id="fPrev" type="button">{ui("이전 · Back", "Back")}</button>
    <button class="btn primary" id="fListen" type="button">{ICON["play"]}{ui("듣기 · Listen", "Listen")}</button>
    <button class="btn" id="fNext" type="button"><span>{ui("다음 · Next", "Next")}</span></button>
  </div>
</section>

<script src="../assets/unit.js?{V}" defer></script>
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
