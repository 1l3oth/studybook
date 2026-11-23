# -*- coding: utf-8 -*-
"""Give each bridge question its asker voice and each answer the Korean voice (edge-tts, free).
Run: python interview-prep/make_audio.py   Safe to re-run: existing clips are kept."""
import asyncio
import hashlib
import io
import json
import os

import edge_tts

D = os.path.dirname(os.path.abspath(__file__))
ASKER, VOICE, EN = 'ko-KR-SunHiNeural', 'ko-KR-InJoonNeural', 'en-US-AvaMultilingualNeural'


def name(text, pre):
    return f'audio/{pre}-' + hashlib.sha1(text.encode('utf-8')).hexdigest()[:10] + '.mp3'


def main():
    path = os.path.join(D, 'bridges.json')
    items = json.load(io.open(path, encoding='utf-8'))
    jobs = []
    for it in items:
        it['iaudio'], it['audio'], it['aen_audio'] = name(it['q'], 'i'), name(it['a'], 'a'), name(it['aen'], 'e')
        jobs += [(it['q'], it['iaudio'], ASKER), (it['a'], it['audio'], VOICE), (it['aen'], it['aen_audio'], EN)]
    io.open(path, 'w', encoding='utf-8', newline='\n').write(json.dumps(items, ensure_ascii=False, indent=1) + '\n')
    os.makedirs(os.path.join(D, 'audio'), exist_ok=True)
    todo = [(t, os.path.join(D, o), v) for t, o, v in jobs if not os.path.exists(os.path.join(D, o))]

    async def run():
        for t, o, v in todo:
            await edge_tts.Communicate(t, v, rate='-5%').save(o)
    asyncio.run(run())
    print(f'{len(items)} bridges, {len(todo)} clips made')


if __name__ == '__main__':
    main()
