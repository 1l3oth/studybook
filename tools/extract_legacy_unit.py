# -*- coding: utf-8 -*-
"""One-off: turn a unit page built by the old build_study.py into unit.json for render_unit.py.
Keeps every line, answer, word and audio/image path; audio files stay where they are.

    python tools/extract_legacy_unit.py korean-summer-speech
"""
import html
import io
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GREY = '#6B7488'
LINES = ['#00A84D', '#00A5DE', '#EF7C1C', '#996CAC', '#0052A4', '#CD7C2F', '#E6186C', '#747F00']


def txt(s):
    return html.unescape(re.sub(r'<[^>]+>', '', s or '')).strip()


def first(pat, s, default=''):
    m = re.search(pat, s, re.S)
    return m.group(1) if m else default


def main():
    slug = sys.argv[1]
    d = os.path.join(ROOT, slug)
    s = io.open(os.path.join(d, 'index.html'), encoding='utf-8').read()
    panel = lambda pid: first(r'<section class="panel[^"]*" id="panel-%s">(.*?)</section>\s*(?=<section class="panel|</div>)' % pid, s)

    # sections, in card order
    sections, sid = [], {}
    cards = []
    for a in re.findall(r'<article class="card">(.*?)</article>', s, re.S):
        part = txt(first(r'<span class="chip part"[^>]*>(.*?)</span>', a))
        ko, _, en = part.partition(' · ')
        if ko not in sid:
            closing = ko in ('시작', '마무리')
            color = GREY if closing else LINES[len([x for x in sections if x['color'] != GREY]) % len(LINES)]
            sid[ko] = 's%d' % (len(sections) + 1)
            sections.append({'id': sid[ko], 'ko': ko, 'en': en, 'color': color})
        cards.append({
            'sec': sid[ko],
            'img': first(r'<img[^>]*src="([^"]+)"', a),
            'alt': html.unescape(first(r'alt="([^"]*)"', a)),
            'hook': txt(first(r'<span class="chip hook">(.*?)</span>', a)),
            'ko': txt(first(r'<p class="ko"[^>]*>(.*?)</p>', a)),
            'en': txt(first(r'<p class="en">(.*?)</p>', a)),
            'audio': first(r'data-au="([^"]+)"', a),
        })

    spine = first(r'<section class="spine-wrap">(.*?)</section>', s)
    days = [(txt(k), txt(dd)) for k, dd in re.findall(r'<span class="s-ko"[^>]*>(.*?)</span>.*?<span class="s-day">(.*?)</span>', spine, re.S)]
    foot = first(r'<div class="spine-foot">(.*?)</div>', spine)
    spine_out = {
        'title': '노선도 · ' + txt(first(r'<h2>(.*?)</h2>', spine)).replace('The spine · ', ''),
        'note': txt(first(r'<span class="note">(.*?)</span>', spine)) + ': ' + ', '.join('%s (%s)' % (k, dd) for k, dd in days) + '.',
        'audio': first(r'data-au="([^"]+)"', foot) or None,
        'caption': txt(re.sub(r'<button.*?</button>', '', foot, flags=re.S)),
    }

    # Q&A blocks, read in document order
    qa_html = panel('qa')
    blocks, group = [], None
    for m in re.finditer(r'<h2 class="sec">(.*?)</h2>(?:\s*<p class="secnote">(.*?)</p>)?|<h3 class="grp">(.*?)</h3>|'
                         r'<article class="(qa(?: trap)?)">(.*?)</article>|<div class="surv">(.*?)</div>', qa_html, re.S):
        if m.group(1) is not None:
            title = txt(re.sub(r'<span class="cnt">.*?</span>', '', m.group(1), flags=re.S))
            small = txt(first(r'<span class="cnt">(.*?)</span>', m.group(1)))
            note = txt(m.group(2)).replace('Answer aloud,', 'Answer in your head,')
            if note.startswith('확인 필요 means'):
                note = '“확인 필요 · check” ' + note[len('확인 필요 '):]
            kind = 'surv' if '막힐' in title else ('trap' if '함정' in title else 'qa')
            blocks.append({'title': title, 'small': small, 'note': note, 'kind': kind, 'items': []})
            group = None
        elif m.group(3) is not None:
            group = txt(m.group(3))
        elif m.group(4) is not None:
            a = m.group(5)
            ako = first(r'<p class="ako"[^>]*>(.*?)</p>', a)
            blocks[-1]['items'].append({k: v for k, v in {
                'group': group,
                'q': txt(first(r'<span class="qko"[^>]*>(.*?)</span>', a)),
                'qen': txt(first(r'<span class="qen">(.*?)</span>', a)),
                'qaudio': first(r'class="play mini qplay" data-au="([^"]+)"', a) or None,
                'a': txt(re.sub(r'<span class="confirm">.*?</span>', '', ako, flags=re.S)),
                'check': 'class="confirm"' in ako,
                'aen': txt(first(r'<p class="aen">(.*?)</p>', a)),
                'why': txt(first(r'<p class="why">(.*?)</p>', a)),
                'audio': first(r'<button class="play" data-au="([^"]+)"', a) or None,
            }.items() if v not in (None, '', False)})
        else:
            a = m.group(6)
            blocks[-1]['items'].append({
                'ko': txt(first(r'<span class="sko"[^>]*>(.*?)</span>', a)),
                'en': txt(first(r'<span class="sen">(.*?)</span>', a)),
                'audio': first(r'data-au="([^"]+)"', a) or None,
            })

    vocab = []
    for m in re.finditer(r'<h3 class="grp">(.*?)</h3>|<div class="voc">(.*?)</div>', panel('voc'), re.S):
        if m.group(1) is not None:
            vocab.append({'title': txt(m.group(1)), 'items': []})
        else:
            a = m.group(2)
            vocab[-1]['items'].append({'ko': txt(first(r'<span class="vko"[^>]*>(.*?)</span>', a)),
                                       'en': txt(first(r'<span class="ven">(.*?)</span>', a)),
                                       'audio': first(r'data-au="([^"]+)"', a) or None})

    speech = panel('full').split('<h2 class="fsec">')[1]
    full = [{'title': txt(t), 'ko': txt(k), 'en': txt(e)} for t, k, e in
            re.findall(r'<h3 class="fh">(.*?)</h3>\s*<p class="fko"[^>]*>(.*?)</p>\s*<p class="fen">(.*?)</p>', speech, re.S)]

    unit = {
        'slug': slug,
        'title_ko': txt(first(r'<h1>(.*?)</h1>', s)),
        'title_en': txt(first(r'<title>(.*?)</title>', s)),
        'subtitle': txt(first(r'class="eyebrow">(.*?)<', s)),
        'description': txt(first(r'class="sub">(.*?)<', s)),
        'sections': sections,
        'spine': spine_out,
        'cards': cards,
        'qa': blocks,
        'vocab': vocab,
        'full_title': '발표 대본 · The speech',
        'full': full,
    }
    out = os.path.join(d, 'unit.json')
    io.open(out, 'w', encoding='utf-8', newline='\n').write(json.dumps(unit, ensure_ascii=False, indent=1))
    print(f'{slug}: {len(sections)} sections, {len(cards)} cards, '
          f'{sum(len(b["items"]) for b in blocks)} Q&A items in {len(blocks)} blocks, '
          f'{sum(len(g["items"]) for g in vocab)} words, {len(full)} full sections')


if __name__ == '__main__':
    main()
