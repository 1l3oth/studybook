# -*- coding: utf-8 -*-
"""Draw one flat picture per vocab word and link it from each unit's vocab list.
    python tools/draw_words.py            (all units)
Words are keyed by their Korean, so a word that appears in two units is drawn once. Pictures are written
to <unit>/img/w-<hash>.svg and each vocab item gets "img". The emotion unit reuses its card faces.
Words without a drawing are listed at the end; nothing is invented for them."""
import glob
import hashlib
import io
import json
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from word_icons import *  # noqa: E402,F401,F403
from words_summer import SUMMER  # noqa: E402
from word_examples import EX  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def J(*parts):
    return ''.join(parts)


D = {}

# ---------- cooking: habit and cooking ----------
D['습관'] = J(calendar(14, 16, 72, '', GREEN), ''.join(check(30 + (i % 3) * 20, 50 + (i // 3) * 20, .55) for i in range(6)))
D['취미'] = J(wok(44, 62, 28), heart(76, 30, 1.2), steam(32, 44, 3, 10, 7))
D['요리하다'] = J(person(30, 96, 60, BLUE), rect(14, 52, 32, 8, WHITE, 3), wok(68, 66, 22))
D['직접'] = J(person(42, 96, 64, BLUE), path('M60 40 l14 -14', stroke=INK, sw=4), circ(80, 22, 9, YELLOW), T(80, 27, '!', 13, INK))
D['재료'] = J(circ(30, 62, 18, CABBAGE), path('M20 60 q10 -10 20 2', stroke=CABBAGE_D, sw=2.5), path('M58 46 q8 12 10 20 q-8 8 -20 0 q2 -8 10 -20Z', fill='#F3EBDD', stroke=LINE, sw=1.6),
              rect(56, 70, 34, 16, '#D9776A', 5), chili(10, 30, -10, .9))
D['레시피'] = J(rect(24, 10, 52, 80, WHITE, 4, LINE, 2), ''.join(rect(32, 26 + i * 12, 36 - (i % 2) * 12, 4, LINE, 2) for i in range(5)), rect(24, 10, 52, 10, ORANGE, 4))
D['장을 보다'] = J(path('M14 34 H82 L74 84 H24Z', fill='#E9D8BC'), path('M34 34 Q34 16 48 16 Q62 16 62 34', stroke='#C9B38E', sw=4), circ(40, 34, 13, CABBAGE), chili(52, 30, -20, .8))
D['간단하다'] = J(circ(50, 50, 34, '#E6F4EA'), check(50, 50, 1.8))
D['양배추'] = J(circ(50, 54, 34, CABBAGE), path('M26 50 q14 -18 30 2 M30 66 q14 -10 26 0 M50 22 q10 18 0 40', stroke=CABBAGE_D, sw=3))
D['마늘'] = J(path('M50 14 q20 26 24 46 q-6 26 -24 26 q-18 0 -24 -26 q4 -20 24 -46Z', fill='#F3EBDD', stroke=LINE, sw=2), path('M50 30 V82 M38 44 q-4 20 4 36 M62 44 q4 20 -4 36', stroke=LINE, sw=2))
D['고기'] = J(path('M18 58 q0 -30 34 -30 q34 0 34 26 q0 26 -34 26 q-34 0 -34 -22Z', fill='#D9776A'), path('M30 52 q16 -12 34 0 q-10 14 -34 0Z', fill='#F2D3C8'), circ(66, 60, 6, '#F2D3C8'))
D['고추'] = J(chili(14, 52, -20, 2.4))
D['소금'] = J(rect(32, 30, 36, 56, WHITE, 7, LINE, 2), path('M32 34 Q50 10 68 34Z', fill=STEEL), circ(44, 26, 2, WHITE), circ(56, 26, 2, WHITE), T(50, 68, '소금', 13))
D['썰다'] = J(rect(10, 66, 80, 18, WOOD, 4), ''.join(rect(20 + i * 12, 54, 9, 12, CABBAGE, 2) for i in range(4)), knife(52, 30, -25))
D['볶다'] = J(wok(44, 64, 32), steam(30, 46, 3, 12, 8), path('M70 30 l10 -16', stroke=WOOD, sw=6))
D['넣다'] = J(bowl(50, 60, 32), arrow(50, 10, 50, 48, GREEN), chili(28, 30, 20, .8))
D['냉동'] = J(rect(24, 14, 52, 74, '#E6F4FB', 6, SKY, 3), path('M50 30 V72 M32 40 L68 62 M68 40 L32 62', stroke=SKY, sw=4))
D['봉지'] = J(path('M24 26 H76 L80 88 H20Z', fill='#E6F4FB', stroke=SKY, sw=2.5), rect(24, 18, 52, 10, SKY, 2), chili(30, 56, -8, 1.2))

# ---------- cooking: taste ----------
D['맛'] = J(face(50, 54, 32, 'smile'), path('M42 72 q8 10 16 0', fill=RED))
D['짜다'] = J(face(38, 58, 28, 'wavy', '#FFD9B0'), rect(66, 20, 22, 34, WHITE, 5, LINE, 2), path('M66 24 Q77 10 88 24Z', fill=STEEL), ''.join(rect(70 + (i % 3) * 6, 60 + (i // 3) * 7, 3, 3, STEEL, 1) for i in range(6)))
D['짠맛'] = D['짜다']
D['맵다'] = J(face(40, 58, 28, 'open', '#FFB199'), chili(60, 30, -30, 1.3), path('M18 26 q4 -10 0 -18 M30 22 q4 -10 0 -18', stroke=RED, sw=3))
D['싱겁다'] = J(bowl(50, 50, 34, '#F4F1E8'), T(50, 40, '?', 20, STEEL))
D['간'] = J(rect(18, 36, 22, 40, WHITE, 5, LINE, 2), path('M18 40 Q29 24 40 40Z', fill=STEEL), rect(58, 36, 22, 40, '#3A3E47', 5), path('M58 40 Q69 24 80 40Z', fill=INK))
D['간을 보다'] = J(person(34, 96, 62, BLUE), path('M48 52 L76 38', stroke=WOOD, sw=4), bowl(80, 62, 14, '#E9C88A'))
D['입맛'] = J(face(50, 54, 32, 'smile', '#FFD9B0'), heart(76, 22, .9))
D['더 맵다'] = J(chili(6, 56, -10, 1.3), path('M30 38 c-3 -5 -3 -10 2 -14 c0 6 4 6 4 2 c4 4 4 10 -6 12Z', fill=ORANGE), T(50, 64, '&lt;', 22, INK),
                 chili(56, 56, -10, 1.3), path('M80 38 c-3 -5 -3 -10 2 -14 c0 6 4 6 4 2 c4 4 4 10 -6 12Z', fill=ORANGE), path('M92 38 c-3 -5 -3 -10 2 -14 c0 6 4 6 4 2 c4 4 4 10 -6 12Z', fill=ORANGE))

# ---------- cooking: money ----------
D['식비'] = J(bowl(34, 52, 24), coin(70, 40, 13), coin(80, 66, 11), T(70, 45, '₩', 13, '#8A5A00'))
D['아끼다'] = J(path('M24 50 q0 -24 30 -24 q30 0 30 24 q0 24 -30 24 q-30 0 -30 -24Z', fill=PINK), circ(84, 48, 8, '#EE8FA2'), coin(54, 16, 9), rect(28, 70, 8, 14, PINK, 3), rect(66, 70, 8, 14, PINK, 3))
D['외식'] = J(rect(14, 40, 72, 48, WHITE, 3, LINE, 2), path('M10 40 L20 22 H80 L90 40Z', fill=RED), ''.join(rect(14 + i * 14, 22, 7, 18, WHITE) for i in range(5)), rect(42, 62, 16, 26, NAVY, 2))
D['사 먹다'] = J(coin(26, 40, 13), arrow(42, 40, 58, 40, INK), bowl(74, 48, 20), steam(66, 36, 2, 10, 7))
D['돈이 들다'] = J(rect(20, 30, 60, 42, MEAT, 8), coin(34, 22, 9), coin(54, 16, 9), coin(74, 24, 9), path('M20 42 H80', stroke='#7A4530', sw=2))
D['덜'] = J(rect(14, 56, 26, 30, STEEL, 3), rect(60, 26, 26, 60, STEEL, 3), arrow(44, 40, 30, 52, RED))
D['네다섯 달'] = J(calendar(18, 18, 64, '4~5', RED))

# ---------- cooking: feelings and life ----------
D['그립다'] = J(person(30, 96, 58, BLUE), bubble(48, 10, 46, 38), heart(71, 30, .9), house(71, 80, 30))
D['고향'] = J(house(50, 88, 64), tree(16, 92, .6), tree(86, 92, .6))
D['마음이 편하다'] = J(face(50, 52, 32, 'smile', '#BFE6C9'), path('M32 42 q4 -4 8 0 M60 42 q4 -4 8 0', stroke=INK, sw=3))
D['달라지다'] = J(rect(10, 40, 26, 26, STEEL, 4), arrow(40, 53, 60, 53, INK), circ(78, 53, 14, GREEN))
D['자취하다'] = J(house(50, 90, 66), person(50, 90, 30, BLUE))
D['다른 사람'] = J(person(26, 92, 50, GREEN), person(50, 92, 56, ORANGE), person(74, 92, 50, PURPLE))
D['부모님'] = J(person(34, 94, 62, GREEN), person(66, 94, 66, PURPLE), heart(50, 20, .8))
D['떨어져 살다'] = J(house(22, 80, 30), path('M40 64 H62', stroke=LINE, sw=3), plane(36, 40, .55), person(80, 92, 44, BLUE))
D['부엌'] = J(rect(12, 40, 76, 48, '#E7EAF0', 3, LINE, 2), rect(16, 34, 68, 8, INK, 2), circ(32, 38, 5, RED), circ(56, 38, 5, '#55595F'), rect(24, 52, 20, 30, WHITE, 2, LINE, 1.5), rect(56, 52, 20, 30, WHITE, 2, LINE, 1.5))
D['룸메이트'] = J(house(50, 92, 76), person(38, 92, 34, GREEN), person(62, 92, 34, BLUE))
D['형'] = J(person(40, 94, 70, ORANGE), person(70, 94, 46, BLUE), path('M52 62 L62 64', stroke=SKIN, sw=4))
D['돌아가다'] = J(plane(14, 50, 1.0, SKY), house(80, 88, 30), path('M10 72 q30 20 56 6', stroke=LINE, sw=3))
D['처음으로'] = J(circ(50, 50, 34, YELLOW), T(50, 64, '1', 40, '#8A5A00'))

# ---------- cooking: presentation phrases ----------
D['말씀드리겠습니다'] = J(person(30, 94, 60, NAVY), bubble(50, 14, 44, 32), ''.join(rect(56, 22 + i * 8, 30 - i * 8, 3, LINE, 1.5) for i in range(3)))
D['이유는 두 가지입니다'] = J(circ(30, 50, 20, GREEN), T(30, 58, '1', 22, WHITE), circ(70, 50, 20, BLUE), T(70, 58, '2', 22, WHITE))
D['첫 번째로'] = J(circ(50, 50, 32, GREEN), T(50, 64, '1', 40, WHITE))
D['두 번째로'] = J(circ(50, 50, 32, BLUE), T(50, 64, '2', 40, WHITE))
D['그다음에'] = J(circ(22, 50, 12, LINE), arrow(38, 50, 62, 50, INK), circ(78, 50, 12, GREEN))
D['왜냐하면'] = J(circ(50, 50, 32, '#FFE9A8'), T(50, 64, '?', 40, '#8A5A00'))
D['제 생각에는'] = J(person(34, 96, 60, BLUE), circ(60, 34, 4, WHITE, LINE, 1.5), circ(68, 24, 6, WHITE, LINE, 1.5), cloud(78, 14, .7, WHITE))
D['이상으로 발표를 마치겠습니다'] = J(rect(14, 16, 72, 50, WHITE, 4, LINE, 2), check(50, 41, 1.3), rect(46, 66, 8, 20, STEEL), rect(30, 84, 40, 5, STEEL, 2))

# ---------- dating ----------
D['연애'] = J(person(34, 94, 58, BLUE), person(66, 94, 56, PINK), heart(50, 24, 1.2))
D['소개팅'] = J(person(20, 94, 48, BLUE), person(80, 94, 48, PINK), person(50, 94, 56, GREEN), path('M36 66 L28 60 M64 66 L72 60', stroke=SKIN, sw=4))
D['선배'] = J(person(36, 94, 72, NAVY), person(70, 94, 50, SKY), path('M50 50 l12 -6', stroke=SKIN, sw=4))
D['데이트'] = J(person(30, 94, 56, BLUE), person(54, 94, 54, PINK), rect(70, 50, 20, 28, WHITE, 3, LINE, 2), circ(80, 44, 6, RED), heart(42, 24, .8))
D['썸'] = J(person(30, 94, 56, BLUE), person(70, 94, 56, PINK), path('M44 44 q6 -10 12 0 t12 0', stroke=PINK, sw=3), T(50, 30, '?', 16, PINK))
D['썸타다'] = J(person(30, 94, 56, BLUE), person(70, 94, 56, PINK), heart(42, 30, .6, PINK), heart(58, 22, .6, '#F5C7D1'), T(50, 52, '?', 14, PINK))
D['애교'] = J(face(50, 52, 32, 'smile', PINK), circ(30, 60, 6, '#EE8FA2'), circ(70, 60, 6, '#EE8FA2'), heart(82, 20, .7))
D['밀당'] = J(person(22, 94, 54, BLUE), person(78, 94, 54, PINK), arrow(38, 46, 60, 46, INK, 3), arrow(62, 60, 40, 60, INK, 3))
D['고백'] = J(person(30, 94, 58, BLUE), person(74, 94, 56, PINK), heart(52, 44, 1.1))
D['사귀다'] = J(person(36, 94, 58, BLUE), person(64, 94, 56, PINK), path('M44 70 Q50 64 56 70', stroke=SKIN, sw=5), heart(50, 22, 1))
D['짝사랑'] = J(person(28, 94, 56, BLUE), heart(28, 22, .9), person(76, 94, 56, PINK), path('M46 40 H62', stroke=LINE, sw=3))
D['커플'] = J(person(36, 94, 60, BLUE), person(64, 94, 58, PINK), heart(50, 18, 1.1), heart(50, 18, .5, WHITE))
D['백 일'] = J(calendar(14, 18, 72, '100', PINK), heart(80, 18, .8))
D['헤어지다'] = J(person(22, 94, 56, BLUE), person(78, 94, 56, PINK), path('M50 12 l-6 14 l8 6 l-6 16', stroke=RED, sw=3), heart(50, 66, 1, '#F5C7D1'))

# ---------- funeral ----------
D['고인'] = J(rect(26, 12, 48, 62, WHITE, 3, INK, 4), person(50, 68, 40, '#55595F'), path('M26 12 L36 22 M74 12 L64 22', stroke=INK, sw=4))
D['상주'] = J(person(50, 96, 72, INK), rect(40, 50, 20, 6, WHITE, 2))
D['유족'] = J(person(24, 94, 50, INK), person(50, 94, 60, INK), person(76, 94, 46, INK))
D['조문객'] = J(person(36, 96, 64, INK), envelope(56, 52, 36, 24))
D['동료'] = J(person(30, 94, 56, NAVY), person(70, 94, 56, BLUE), rect(14, 70, 72, 6, STEEL, 2))
D['장례식장'] = J(rect(12, 36, 76, 52, WHITE, 3, LINE, 2), path('M8 38 L50 14 L92 38', stroke=INK, sw=5), rect(42, 62, 16, 26, INK, 2), flower(26, 56, 9, WHITE, YELLOW), flower(74, 56, 9, WHITE, YELLOW))
D['빈소'] = J(rect(34, 14, 32, 40, WHITE, 2, INK, 3), ''.join(flower(14 + i * 18, 70, 8, WHITE, YELLOW) for i in range(5)), rect(10, 80, 80, 8, WOOD, 2))
D['영정 사진'] = J(rect(24, 12, 52, 66, WHITE, 2, INK, 4), person(50, 72, 46, '#55595F'), path('M24 12 L34 22 M76 12 L66 22', stroke=INK, sw=3))
D['부의금'] = J(envelope(14, 30, 72, 46), T(50, 62, '부의', 15, INK))
D['흰 봉투'] = J(envelope(14, 28, 72, 48))
D['방명록'] = J(book(18, 30, 64, 46), path('M66 20 L80 56', stroke=INK, sw=4), path('M80 56 l-2 6 l5 -3Z', fill=INK))
D['국화'] = J(path('M50 54 V94', stroke='#4E8A4F', sw=4), path('M50 76 q-14 -4 -18 -14 q12 0 18 8', fill='#4E8A4F'), flower(50, 40, 30, WHITE, YELLOW))
D['조화'] = J(rect(46, 60, 8, 32, WOOD, 2), circ(50, 40, 28, WHITE, LINE, 2), ''.join(flower(50 + 18 * math.cos(i * .785), 40 + 18 * math.sin(i * .785), 7, '#F2F2F2', YELLOW) for i in range(8)), rect(36, 60, 28, 8, INK, 2))
D['검은 옷'] = J(shirt(50, 16, 46, INK, 'long'))
D['돌아가시다'] = J(flower(50, 46, 26, WHITE, YELLOW), path('M50 70 V94', stroke='#4E8A4F', sw=4))
D['조문하다'] = J(person(30, 96, 60, INK), rect(56, 30, 30, 38, WHITE, 2, INK, 3), flower(71, 78, 8, WHITE, YELLOW))
D['절하다'] = J(rect(8, 86, 84, 6, WOOD, 2), path('M20 84 Q22 64 40 62 L70 66 Q80 70 76 84Z', fill=INK), circ(80, 74, 8, SKIN))
D['묵념하다'] = J(person(50, 96, 74, INK), path('M42 44 q8 6 16 0', stroke=INK, sw=3))
D['명복을 빌다'] = J(path('M30 70 Q30 30 50 20 Q70 30 70 70Z', fill=SKIN), path('M50 20 V70', stroke='#C99670', sw=2), rect(26, 70, 48, 16, INK, 6))
D['위로하다'] = J(person(34, 96, 64, BLUE), person(66, 96, 60, INK), path('M44 62 L60 54', stroke=SKIN, sw=5), heart(50, 20, .9))
D['발인'] = J(rect(10, 52, 66, 26, INK, 6), rect(70, 58, 22, 20, INK, 4), circ(24, 80, 8, '#55595F'), circ(70, 80, 8, '#55595F'), flower(40, 46, 9, WHITE, YELLOW))

D.update(SUMMER)

SVG = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">{}</svg>\n'


def emotion_faces(u):
    """The emotion unit already draws one face per word on its cards: point the vocab at those."""
    out = {c['hook']: c['img'] for c in u['cards'] if c.get('hook')}
    for c in u['cards']:  # fall back to a card whose sentence uses the word
        for g in u['vocab']:
            for it in g['items']:
                if it['ko'] in c.get('ko', ''):
                    out.setdefault(it['ko'], c['img'])
    return out


def main():
    missing = []
    for p in sorted(glob.glob(os.path.join(ROOT, '*', 'unit.json'))):
        d = os.path.dirname(p)
        slug = os.path.basename(d)
        u = json.load(io.open(p, encoding='utf-8'))
        faces = emotion_faces(u) if slug == 'korean-emotion-words' else {}
        sents = {c['hook']: c for c in u['cards'] if c.get('hook')} if faces else {}
        n = 0
        for g in u['vocab']:
            for it in g['items']:
                w = it['ko']
                if w in EX:  # a real-life example sentence
                    it['ex'] = dict(it.get('ex') or {}, ko=EX[w][0], en=EX[w][1])
                elif w in sents:  # the emotion unit's own card sentence
                    it['ex'] = dict(it.get('ex') or {}, ko=sents[w]['ko'], en=sents[w]['en'])
                if w in faces:
                    it['img'] = faces[w]
                elif w in D:
                    name = 'img/w-' + hashlib.sha1(w.encode('utf-8')).hexdigest()[:10] + '.svg'
                    os.makedirs(os.path.join(d, 'img'), exist_ok=True)
                    io.open(os.path.join(d, name), 'w', encoding='utf-8', newline='\n').write(SVG.format(D[w]))
                    it['img'] = name
                else:
                    missing.append(f'{slug}: {w}')
                    continue
                n += 1
        io.open(p, 'w', encoding='utf-8', newline='\n').write(json.dumps(u, ensure_ascii=False, indent=1))
        print(f'{slug}: {n} word pictures')
    if missing:
        print('no drawing yet:', ', '.join(missing))


if __name__ == '__main__':
    main()
