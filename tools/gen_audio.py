# -*- coding: utf-8 -*-
"""Fill a unit's missing audio with a native Korean neural voice (edge-tts, free, no key), plus the
English explainer clips (en-US-AvaMultilingualNeural): card meaning, Q&A answer meaning, grammar notes and word meaning.
Explainer clips are named from a hash of their text, so a changed text gets a new clip.

    python tools/gen_audio.py korean-funeral-visit [--voice ko-KR-InJoonNeural]

Gives every vocab word an audio path, fills the Full text from the cards when it is empty, then
synthesises every referenced clip that does not exist yet. Safe to re-run: existing files are kept.
"""
import asyncio
import io
import json
import os
import sys

import hashlib

import edge_tts

ASKER_VOICE = 'ko-KR-SunHiNeural'  # the person asking in the chat-style Q&A, so it never sounds like you
EXPLAIN_VOICE = 'en-US-AvaMultilingualNeural'  # multilingual: reads the Korean words inside English notes


def ename(text, pre='e'):
    return f'audio/{pre}-' + hashlib.sha1(text.encode('utf-8')).hexdigest()[:10] + '.mp3'

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def main():
    slug = sys.argv[1]
    voice = sys.argv[sys.argv.index('--voice') + 1] if '--voice' in sys.argv else 'ko-KR-InJoonNeural'
    d = os.path.join(ROOT, slug)
    path = os.path.join(d, 'unit.json')
    u = json.load(io.open(path, encoding='utf-8'))

    jobs = []
    ejobs = []
    ijobs = []

    def explain(it, field, key):
        if it.get(field):
            it[key] = ename(it[field])
            ejobs.append((it[field], it[key]))

    for c in u['cards']:
        jobs.append((c['ko'], c['audio']))
        explain(c, 'en', 'en_audio')
    for b in u['qa']:
        for it in b['items']:
            if b.get('kind') == 'surv':
                jobs.append((it['ko'], it['audio']))
                explain(it, 'en', 'en_audio')
            else:
                explain(it, 'aen', 'aen_audio')
                if b.get('kind') in (None, 'qa', 'trap') and it.get('q'):
                    it['iaudio'] = ename(it['q'], 'i')
                    ijobs.append((it['q'], it['iaudio']))
                if b.get('kind') == 'gram':
                    explain(it, 'why', 'why_audio')
                if it.get('qaudio'):
                    jobs.append((it['q'], it['qaudio']))
                if it.get('audio'):
                    jobs.append((it['a'], it['audio']))
    n = 0
    for g in u['vocab']:
        for it in g['items']:
            n += 1
            it.setdefault('audio', 'audio/v%02d.mp3' % n)
            jobs.append((it['ko'], it['audio']))
            explain(it, 'en', 'en_audio')
            if it.get('ex'):  # the example sentence in the Korean voice, its meaning in the English one
                it['ex']['audio'] = ename(it['ex']['ko'], 'x')
                jobs.append((it['ex']['ko'], it['ex']['audio']))
                explain(it['ex'], 'en', 'en_audio')
    if not u.get('full'):
        secs = {s['id']: s for s in u['sections']}
        for s in u['sections']:
            cs = [c for c in u['cards'] if c['sec'] == s['id']]
            if cs:
                u['full'].append({'title': f'{s["ko"]} · {s["en"]}', 'ko': ' '.join(c['ko'] for c in cs),
                                  'en': ' '.join(c['en'] for c in cs)})
    io.open(path, 'w', encoding='utf-8', newline='\n').write(json.dumps(u, ensure_ascii=False, indent=1))

    todo = [(t, os.path.join(d, a), v) for v, js in ((voice, jobs), (ASKER_VOICE, ijobs), (EXPLAIN_VOICE, ejobs)) for t, a in js if a and t
            if not (os.path.exists(os.path.join(d, a)) and os.path.getsize(os.path.join(d, a)) > 1000)]
    todo = list({o: (t, o, v) for t, o, v in todo}.values())

    async def run():
        sem = asyncio.Semaphore(4)

        async def one(text, out, v):
            async with sem:
                os.makedirs(os.path.dirname(out), exist_ok=True)
                await edge_tts.Communicate(text.replace("'", '') if v != EXPLAIN_VOICE else text, v, rate='-5%').save(out)
        await asyncio.gather(*(one(t, o, v) for t, o, v in todo))

    asyncio.run(run())
    print(f'{slug}: {len(jobs)} Korean + {len(ijobs)} asker + {len(ejobs)} English clips referenced, {len(todo)} generated')


if __name__ == '__main__':
    main()
