# -*- coding: utf-8 -*-
"""One-off: turn the old emotion dictionary page (korean-emotion-words) into unit.json.
Each word becomes a card (the book's example sentence), a vocab entry, and a pattern item.
Words, readings and sentences are the book's (2000 Essential Korean Words, Darakwon).

    python tools/extract_emotion_dictionary.py [old-page.html]

Reads the old page from the given path (default: korean-emotion-words/index.html; once the new page
is rendered, get the old one back with `git show <commit>:korean-emotion-words/index.html`).
"""
import html
import io
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SLUG = 'korean-emotion-words'
TONES = [('pos', '긍정', 'Positive', '#00A84D'), ('react', '반응', 'Reaction', '#00A5DE'), ('neg', '부정', 'Negative', '#EF7C1C')]
POS_EN = {'명사': 'noun', '동사': 'verb', '형용사': 'adjective'}


def txt(s):
    return html.unescape(re.sub(r'<[^>]+>', '', s or '')).strip()


def first(pat, s, default=''):
    m = re.search(pat, s, re.S)
    return m.group(1) if m else default


def main():
    d = os.path.join(ROOT, SLUG)
    src = sys.argv[1] if len(sys.argv) > 1 else os.path.join(d, 'index.html')
    s = io.open(src, encoding='utf-8').read()
    ents = []
    for tone, eid, a in re.findall(r'<article class="ent" data-tone="(\w+)" id="(e\d+)">(.*?)</article>', s, re.S):
        meta = dict((txt(k).split(' ')[0], txt(v)) for k, v in re.findall(r'<dt>(.*?)</dt>\s*<dd[^>]*>(.*?)</dd>', a, re.S))
        pos_ko = txt(first(r'<span class="pos">(.*?)</span>', a)).split(' ')[0]
        ents.append({
            'id': eid, 'tone': tone,
            'hw': txt(first(r'<h3 class="hw"[^>]*>(.*?)</h3>', a)),
            'pron': txt(first(r'<span class="pron"[^>]*>(.*?)</span>', a)),
            'pos': pos_ko, 'pos_en': POS_EN.get(pos_ko, ''),
            'irr': txt(first(r'<span class="irr"[^>]*>(.*?)</span>', a)),
            'gloss': txt(first(r'<p class="gloss">(.*?)</p>', a)),
            'exko': txt(first(r'<p class="exko"[^>]*>(.*?)</p>', a)),
            'exen': txt(first(r'<p class="exen">(.*?)</p>', a)),
            'wau': first(r'class="play mini wplay" data-au="([^"]+)"', a),
            'sau': first(r'class="play mini splay" data-au="([^"]+)"', a),
            'forms': meta.get('파생', ''), 'patterns': meta.get('문형', ''), 'opp': meta.get('반대', ''),
            'note': txt(first(r'<p class="note">(.*?)</p>', a)),
        })

    sections = [{'id': t, 'ko': ko, 'en': en, 'color': c} for t, ko, en, c in TONES]
    cards, vocab, gram, full = [], [], [], []
    for t, ko, en, c in TONES:
        group = [x for x in ents if x['tone'] == t]
        for x in group:
            cards.append({'sec': t, 'img': f'img/{x["id"]}.svg', 'flat': True,
                          'alt': f'A face for {x["hw"]}: {x["gloss"].split(",")[0]}',
                          'hook': x['hw'], 'ko': x['exko'], 'en': x['exen'], 'audio': x['sau']})
        vocab.append({'title': f'{ko} · {en}', 'color': c, 'items': [
            {'ko': x['hw'], 'en': f'{x["gloss"]} · {x["pos_en"]} {x["pron"]}' + (f' · {x["irr"]}' if x['irr'] else ''),
             'audio': x['wau']} for x in group]})
        for x in group:
            extra = ' · '.join(p for p in [x['forms'], ('반대 ' + x['opp']) if x['opp'] else ''] if p)
            gram.append({k: v for k, v in {
                'group': f'{ko} · {en}', 'q': x['hw'], 'qen': x['gloss'], 'qaudio': x['wau'],
                'a': x['patterns'] or x['hw'], 'aen': extra, 'why': x['note']}.items() if v})
        full.append({'title': f'{ko} · {en}', 'ko': ' '.join(x['exko'] for x in group), 'en': ' '.join(x['exen'] for x in group)})

    counts = {t: sum(1 for x in ents if x['tone'] == t) for t, *_ in TONES}
    unit = {
        'slug': SLUG,
        'title_ko': '감정 사전',
        'title_en': 'Emotion Words',
        'subtitle': '2000 Essential Korean Words (Darakwon)',
        'description': f'{len(ents)} feeling words from 2000 Essential Korean Words, each with the book\'s own example sentence and audio.',
        'sections': sections,
        'spine': {'title': '노선도 · 감정의 세 갈래',
                  'note': 'The words run in three groups: ' + ', '.join(f'{ko} ({en}, {counts[t]})' for t, ko, en, _ in TONES) + '.',
                  'audio': None,
                  'caption': 'Good feelings, reactions, hard feelings. Every card is a sentence from the book.'},
        'explain': {'title': '한눈에 · The big picture',
                    'why': 'Learn each feeling from a face and one real sentence from the book. Most of these words end in -하다 or are -ㅂ irregular.',
                    'tiles': [
                        {'img': 'img/e26.svg', 'ko': '긍정', 'en': f'{counts["pos"]} good feelings', 'color': '#00A84D'},
                        {'img': 'img/e06.svg', 'ko': '반응', 'en': f'{counts["react"]} reactions', 'color': '#00A5DE'},
                        {'img': 'img/e15.svg', 'ko': '부정', 'en': f'{counts["neg"]} hard feelings', 'color': '#EF7C1C'},
                        {'img': 'img/e09.svg', 'ko': '무섭다 → 무서워요', 'en': 'ㅂ becomes 워', 'color': '#996CAC'}]},
        'cards': cards,
        'qa_tab': {'ko': '문형', 'en': 'patterns'},
        'qa': [{'title': '문형 · Patterns', 'small': '', 'kind': 'gram', 'items': gram,
                'note': 'How each word is used in a sentence. Think of the pattern first, then tap to check.'}],
        'vocab': vocab,
        'full_title': '예문 · The sentences',
        'full': full,
        'published': '2026-09-15',
    }
    io.open(os.path.join(d, 'unit.json'), 'w', encoding='utf-8', newline='\n').write(json.dumps(unit, ensure_ascii=False, indent=1) + '\n')
    print(f'{SLUG}: {len(ents)} words, {len(cards)} cards, counts {counts}')


if __name__ == '__main__':
    main()
