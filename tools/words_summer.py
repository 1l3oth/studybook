# -*- coding: utf-8 -*-
"""Word pictures for the summer speech unit (viewBox 0 0 100 100). Merged into draw_words.D."""
from word_icons import *  # noqa: F401,F403


def J(*parts):
    return ''.join(parts)


def flame(x, y, k=1.0, c=ORANGE):
    return f'<path transform="translate({x} {y}) scale({k})" d="M0 0 C-9 -3 -9 -13 -3 -21 C-1 -14 3 -13 4 -17 C9 -10 9 -3 0 0Z" fill="{c}"/>'


def sweat(x, y, k=1.0):
    return drop(x, y, k, SKY)


def aircon(x, y, w=70):
    return rect(x, y, w, 26, WHITE, 6, LINE, 2) + rect(x + 8, y + 18, w - 16, 3, LINE, 1.5) + ''.join(path(f'M{x + 16 + i * 18} {y + 32} q-4 8 0 16', stroke=SKY, sw=3) for i in range(3))


def hat(cx, cy, fill=BLUE):
    return path(f'M{cx - 24} {cy} Q{cx - 24} {cy - 26} {cx} {cy - 26} Q{cx + 24} {cy - 26} {cx + 24} {cy}Z', fill=fill) + rect(cx - 30, cy - 4, 60, 8, fill, 4)


def glasses(cx, cy):
    return (rect(cx - 30, cy - 9, 24, 18, INK, 7) + rect(cx + 6, cy - 9, 24, 18, INK, 7) + path(f'M{cx - 6} {cy - 3} H{cx + 6}', stroke=INK, sw=4)
            + path(f'M{cx - 30} {cy - 5} l-8 -4 M{cx + 30} {cy - 5} l8 -4', stroke=INK, sw=3))


def noodles(cx, top, broth='#F2E3B3', c='#F5EBC6'):
    return bowl(cx, top, 32, broth) + ''.join(path(f'M{cx - 20 + i * 8} {top - 1} q4 -8 0 -16 q-4 -8 0 -16', stroke=c, sw=3) for i in range(6))


SUMMER = {}
S = SUMMER

# weather
S['여름'] = J(sun(50, 42, 18), waves(18, 78, 2))
S['날씨'] = J(sun(36, 40, 14), cloud(62, 50, .9), rain(48, 66, 3, 10))
S['덥다'] = J(thermo(30, 14, .9, RED), sun(68, 36, 13), sweat(70, 74, 1.3))
S['습하다'] = J(drop(30, 34, 1.6), drop(60, 26, 1.3), drop(46, 64, 1.8), drop(76, 58, 1.4), cloud(50, 16, .6, '#D3D9E3'))
S['건조하다'] = J(sun(50, 30, 14), path('M14 74 L30 66 L44 76 L58 64 L72 74 L88 66', stroke=MEAT, sw=3), rect(10, 78, 80, 10, '#E9D8BC', 2))
S['바람'] = J(path('M12 34 H62 q12 0 12 -10 q0 -9 -9 -9', stroke=SKY, sw=5), path('M12 52 H80 q10 0 10 10 q0 9 -9 9', stroke=SKY, sw=5), path('M12 70 H50', stroke=SKY, sw=5))
S['장마'] = J(cloud(50, 26, 1.1, '#9AA3B2'), rain(24, 50, 5, 12), rain(30, 70, 4, 12))
S['온도'] = J(thermo(50, 12, .55, ORANGE), ''.join(rect(62, 18 + i * 12, 10, 3, LINE, 1.5) for i in range(5)))
S['에어컨'] = J(aircon(15, 24, 70))
S['선풍기'] = J(fan(50, 40, 26), rect(46, 66, 8, 20, STEEL, 2), rect(32, 84, 36, 6, STEEL, 3))
S['시원하다'] = J(face(46, 56, 28, 'smile', '#BDE6F5'), path('M74 26 q10 6 0 12 M82 20 q14 12 0 24', stroke=SKY, sw=3))
S['춥다'] = J(thermo(30, 14, .2, SKY), path('M66 30 V70 M48 40 L84 60 M84 40 L48 60', stroke=SKY, sw=4))

# clothes
S['옷'] = J(shirt(50, 18, 46, SKY))
S['반바지'] = J(path('M28 22 H72 L76 66 H54 L50 40 L46 66 H24Z', fill=BLUE))
S['긴팔'] = J(shirt(50, 18, 44, GREEN, 'long'))
S['긴바지'] = J(pants(50, 14, 76, NAVY))
S['유니폼'] = J(shirt(50, 18, 46, NAVY), rect(56, 34, 12, 8, YELLOW, 2))
S['출근하다'] = J(person(30, 94, 58, NAVY), rect(42, 66, 18, 14, WOOD, 3), rect(62, 30, 30, 60, '#E3E7EE', 2), ''.join(rect(66 + (i % 2) * 12, 36 + (i // 2) * 12, 8, 7, SKY, 1) for i in range(8)))
S['햇빛'] = J(sun(36, 30, 14), ''.join(path(f'M{44 + i * 8} {42 + i * 4} L{60 + i * 8} {86}', stroke=YELLOW, sw=4) for i in range(3)))
S['편하다'] = J(path('M14 62 q0 -16 16 -16 h40 q16 0 16 16 v14 h-72Z', fill=PURPLE), rect(10, 74, 80, 10, '#7D5591', 4), face(70, 32, 14, 'smile'))

# food
S['음식'] = J(bowl(32, 54, 22, '#F7F3E8'), bowl(70, 58, 20, '#D9776A'), steam(26, 40, 2, 10, 7))
S['국물'] = J(bowl(50, 50, 34, '#E9C88A'), steam(38, 36, 3, 12, 8))
S['국수'] = J(noodles(50, 54))
S['냉면'] = J(noodles(50, 54, '#D7EEF5', '#B9A68A'), rect(56, 40, 10, 10, '#E3F2F8', 2, SKY, 1.5), rect(34, 42, 10, 10, '#E3F2F8', 2, SKY, 1.5))
S['삼계탕'] = J(bowl(50, 54, 34, '#F2E3B3'), path('M32 50 q18 -22 36 0Z', fill='#F3E3C3', stroke='#E0C79A', sw=2), steam(38, 30, 3, 12, 8))
S['뜨겁다'] = J(bowl(46, 56, 28, '#D9776A'), path('M30 40 q-5 -8 0 -16 t0 -16 M46 40 q-5 -8 0 -16 t0 -16 M62 40 q-5 -8 0 -16 t0 -16', stroke=RED, sw=3.5), flame(84, 86, 1.2, RED))
S['채소'] = J(circ(34, 58, 22, CABBAGE), path('M22 56 q12 -14 24 2', stroke=CABBAGE_D, sw=3), path('M64 84 L78 40 L86 44 L70 86Z', fill=ORANGE), path('M80 40 l-2 -12 M82 41 l6 -10', stroke='#4E8A4F', sw=3))
S['고기'] = J(path('M18 58 q0 -30 34 -30 q34 0 34 26 q0 26 -34 26 q-34 0 -34 -22Z', fill='#D9776A'), path('M30 52 q16 -12 34 0 q-10 14 -34 0Z', fill='#F2D3C8'), circ(66, 60, 6, '#F2D3C8'))
S['끓이다'] = J(rect(22, 40, 56, 40, STEEL, 6), rect(14, 46, 10, 6, INK, 3), rect(76, 46, 10, 6, INK, 3), ''.join(circ(34 + i * 10, 36 - (i % 2) * 5, 4, WHITE, LINE, 1.5) for i in range(4)), flame(40, 96, .8, RED), flame(60, 96, .8, RED))
S['계절'] = J(circ(30, 30, 16, '#F5C7D1'), sun(70, 30, 11, False), circ(30, 70, 16, ORANGE), path('M58 62 L82 78 M82 62 L58 78 M70 58 V82', stroke=SKY, sw=4))
S['맛'] = J(face(50, 54, 32, 'smile'), path('M42 72 q8 10 16 0', fill=RED))

# escaping the heat
S['더위'] = J(sun(50, 36, 18), path('M14 82 q8 -8 16 0 t16 0 t16 0 t16 0 t16 0', stroke=ORANGE, sw=4))
S['피하다'] = J(sun(22, 24, 11), arrow(34, 34, 52, 50, LINE, 3), umbrella(66, 48, 24, BLUE), person(66, 96, 38, GREEN))
S['수영장'] = J(rect(10, 40, 80, 48, '#9ED9F0', 6), waves(16, 56, 3, WHITE), path('M74 40 V20 M84 40 V20 M74 28 H84', stroke=STEEL, sw=3))
S['강'] = J(path('M10 20 Q50 30 40 50 Q30 70 90 84 V96 Q20 80 26 50 Q32 30 10 30Z', fill=SKY), tree(80, 50, .7), tree(16, 86, .6))
S['공원'] = J(tree(30, 80, .9), tree(70, 80, .7), rect(40, 72, 34, 6, WOOD, 2), rect(10, 82, 80, 8, '#6FAF7A', 3))
S['캠핑'] = J(path('M14 84 L46 24 L82 84Z', fill=ORANGE), path('M46 24 L40 84 H52Z', fill='#C85E12'), flame(82, 90, .8))
S['산'] = J(mountain(40, 86, 70, 60), mountain(72, 86, 50, 40))
S['나무'] = J(tree(50, 92, 1.5))
S['친구'] = J(person(34, 94, 58, BLUE), person(66, 94, 58, GREEN), path('M44 66 L56 66', stroke=SKIN, sw=5))

# talking about it
S['발표'] = J(rect(56, 14, 36, 28, WHITE, 3, LINE, 2), rect(62, 22, 20, 3, LINE), rect(62, 30, 14, 3, LINE), person(30, 94, 60, NAVY), rect(18, 80, 28, 16, WOOD, 2))
S['소개하다'] = J(person(30, 94, 58, NAVY), person(72, 94, 54, GREEN), path('M44 62 L58 52', stroke=SKIN, sw=5))
S['차이'] = J(rect(14, 30, 30, 40, BLUE, 4), circ(72, 50, 20, ORANGE), T(50, 56, '≠', 18, INK))
S['다르다'] = J(rect(12, 32, 30, 36, BLUE, 4), path('M72 30 L92 68 H52Z', fill=ORANGE), T(47, 56, '≠', 16, INK))
S['비슷하다'] = J(circ(30, 50, 18, BLUE), circ(72, 52, 16, SKY), T(51, 57, '≈', 18, INK))
S['익숙하다'] = J(person(30, 94, 58, BLUE), house(72, 88, 40), check(78, 30, .8))
S['영향'] = J(circ(24, 50, 14, ORANGE), path('M42 50 q8 -10 16 0 t16 0', stroke=LINE, sw=3), ''.join(circ(80, 50, r, 'none', SKY, 2.5) for r in (6, 12, 18)))
S['건강'] = J(heart(50, 50, 2.6, '#2BB866'), path('M28 50 H40 L46 38 L54 62 L60 50 H72', stroke=WHITE, sw=4))
S['생활'] = J(house(30, 88, 40), rect(56, 34, 32, 30, WHITE, 3, LINE, 2), path('M72 38 V50 L80 54', stroke=INK, sw=3), circ(72, 49, 14, 'none', INK, 2.5))
S['기억하다'] = J(person(30, 94, 58, BLUE), circ(60, 30, 4, WHITE, LINE, 1.5), rect(66, 8, 28, 26, WHITE, 3, LINE, 2), heart(80, 22, .5))

# sky
S['하늘'] = J(rect(6, 6, 88, 88, '#CDEBF7', 10), cloud(36, 40, .6, WHITE), sun(72, 28, 9, False))
S['구름'] = J(cloud(50, 50, 1.4, '#DDE2EA'))
S['해'] = J(sun(50, 50, 22))
S['맑다'] = J(rect(6, 6, 88, 88, '#CDEBF7', 10), sun(50, 50, 18))
S['흐리다'] = J(cloud(40, 42, 1.0, '#AAB2BF'), cloud(60, 60, 1.1, '#C3C9D3'))
S['그늘'] = J(sun(20, 18, 9, False), tree(54, 82, 1.2), f'<ellipse cx="54" cy="88" rx="34" ry="6" fill="#9AA3B2"/>', person(70, 90, 30, BLUE))
S['소나기'] = J(sun(70, 24, 10, False), cloud(42, 34, .9, '#9AA3B2'), path('M20 54 l-6 14 M32 54 l-6 14 M44 54 l-6 14 M56 54 l-6 14 M26 72 l-6 14 M38 72 l-6 14', stroke=SKY, sw=4))

# summer things
S['손선풍기'] = J(fan(50, 36, 22, SKY), rect(45, 58, 10, 32, INK, 4))
S['양산'] = J(umbrella(50, 46, 38, PINK), sun(80, 14, 8, False))
S['우산'] = J(umbrella(50, 48, 38, BLUE), rain(18, 10, 4, 18))
S['선크림'] = J(path('M34 18 H66 L62 82 H38Z', fill=WHITE, stroke=LINE, sw=2), rect(40, 82, 20, 10, ORANGE, 2), sun(50, 44, 9, False))
S['모자'] = J(hat(50, 62, BLUE))
S['선글라스'] = J(glasses(50, 50))
S['헬멧'] = J(path('M18 64 Q18 22 50 22 Q82 22 82 64Z', fill=RED), rect(14, 60, 72, 8, '#A82A21', 4), rect(48, 26, 4, 34, WHITE, 2))
S['물병'] = J(bottle(50, 14, 76, SKY))

# comparing
S['비교하다'] = J(path('M50 16 V84 M24 30 H76', stroke=INK, sw=4), path('M14 52 L24 30 L34 52Z', fill=BLUE), path('M66 52 L76 30 L86 52Z', fill=ORANGE), rect(36, 82, 28, 6, INK, 3))
S['차이점'] = S['차이']
S['공통점'] = J(circ(38, 50, 24, BLUE), circ(62, 50, 24, ORANGE), path('M50 30 A24 24 0 0 1 50 70 A24 24 0 0 1 50 30Z', fill=PURPLE))
S['같다'] = J(circ(28, 50, 16, BLUE), T(50, 58, '=', 24, INK), circ(72, 50, 16, BLUE))
S['처럼'] = J(person(30, 94, 56, BLUE), path('M24 56 l-12 -14', stroke=SKIN, sw=5), person(70, 94, 56, GREEN), path('M64 56 l-12 -14', stroke=SKIN, sw=5))
S['더'] = J(rect(14, 56, 26, 30, STEEL, 3), rect(60, 26, 26, 60, GREEN, 3), arrow(44, 52, 56, 36, GREEN))
S['덜'] = J(rect(14, 56, 26, 30, STEEL, 3), rect(60, 26, 26, 60, STEEL, 3), arrow(44, 40, 30, 52, RED))
S['둘 다'] = J(check(30, 50, 1.3), check(70, 50, 1.3))
S['반면에'] = J(sun(26, 40, 12, False), path('M50 14 V86', stroke=LINE, sw=3), cloud(74, 40, .7, '#AAB2BF'), rain(64, 56, 3, 9))

# feelings and body
S['졸리다'] = J(face(46, 56, 30, 'flat', '#E3E7EE'), T(78, 30, 'z', 14, BLUE), T(88, 18, 'z', 10, BLUE))
S['피곤하다'] = J(face(50, 56, 30, 'sad', '#E3E7EE'), path('M30 48 q6 4 12 0 M58 48 q6 4 12 0', stroke=INK, sw=3), rect(76, 16, 14, 26, WHITE, 3, INK, 2), rect(79, 34, 8, 5, RED, 1))
S['답답하다'] = J(face(50, 54, 30, 'wavy', '#E3E7EE'), path('M14 14 h72 v72 h-72Z', stroke=STEEL, sw=3))
S['상쾌하다'] = J(face(46, 56, 28, 'smile', '#BFE6C9'), path('M74 24 q12 6 0 12 M80 44 q12 6 0 12', stroke=GREEN, sw=3))
S['불편하다'] = J(face(50, 54, 30, 'wavy', '#FFD9B0'), cross(82, 18, .7))
S['땀'] = J(drop(36, 50, 2.6), drop(66, 36, 1.8), drop(70, 72, 1.5))
S['목마르다'] = J(face(40, 56, 26, 'open', '#FFD9B0'), bottle(80, 24, 60, SKY))
S['지치다'] = J(path('M14 82 Q30 60 52 64 Q74 68 86 82Z', fill=BLUE), circ(76, 58, 9, SKIN), sweat(60, 42, 1.2), rect(16, 84, 70, 5, WOOD, 2))

# useful verbs
S['입다'] = J(shirt(50, 20, 42, SKY), arrow(50, 4, 50, 18, GREEN, 3))
S['쓰다'] = J(person(50, 96, 62, BLUE), hat(50, 40, ORANGE))
S['벗다'] = J(shirt(50, 30, 40, SKY), arrow(50, 26, 50, 6, RED, 3))
S['켜다'] = J(rect(30, 20, 40, 60, WHITE, 6, LINE, 2), rect(40, 30, 20, 20, GREEN, 4), T(50, 72, 'ON', 12, GREEN))
S['끄다'] = J(rect(30, 20, 40, 60, WHITE, 6, LINE, 2), rect(40, 50, 20, 20, STEEL, 4), T(50, 42, 'OFF', 12, STEEL))
S['쉬다'] = J(path('M14 62 q0 -16 16 -16 h40 q16 0 16 16 v14 h-72Z', fill=GREEN), rect(10, 74, 80, 10, '#08803A', 4), T(70, 30, 'z', 14, BLUE), T(80, 20, 'z', 10, BLUE))
S['사용하다'] = J(phone(32, 16, 36, 64), circ(78, 70, 9, SKIN))

# mentor: sun and clothes
S['햇빛이 따갑다'] = J(sun(26, 26, 12), path('M44 44 L56 56 M50 40 L62 52', stroke=YELLOW, sw=4), path('M50 90 Q50 60 74 60 Q90 60 90 90Z', fill='#F5A88E'), path('M66 70 l4 4 l4 -4 M76 78 l4 4 l4 -4', stroke=RED, sw=2.5))
S['피부가 따갑다'] = J(path('M20 92 Q20 50 50 50 Q80 50 80 92Z', fill='#F5A88E'), path('M36 66 l5 5 l5 -5 M54 74 l5 5 l5 -5 M44 82 l5 5 l5 -5', stroke=RED, sw=3), sun(80, 20, 10, False))
S['햇빛이 세다'] = J(sun(50, 44, 22), path('M18 88 H82', stroke=YELLOW, sw=6), T(50, 52, '!', 20, '#8A5A00'))
S['반팔'] = J(shirt(50, 18, 46, ORANGE, 'short'))

# mentor: summer food
S['콩국수'] = J(noodles(50, 54, '#F6F1E1', '#F5EBC6'), circ(30, 40, 4, CABBAGE_D), circ(66, 42, 4, CABBAGE_D))
S['복날'] = J(calendar(14, 14, 54, '', RED), T(41, 52, '삼복', 13), bowl(74, 70, 20, '#F2E3B3'), sun(80, 20, 9, False))
S['보양식'] = J(bowl(50, 54, 34, '#F2E3B3'), heart(50, 30, 1.0, '#2BB866'), steam(32, 30, 2, 36, 8))

# mentor: beating the heat
S['햇빛을 막아 주다'] = J(sun(20, 20, 10), path('M30 30 L44 44', stroke=YELLOW, sw=4), umbrella(62, 50, 30, BLUE), person(62, 96, 40, GREEN))
S['해수욕장'] = J(sun(80, 18, 9, False), rect(6, 54, 88, 18, SKY, 2), waves(10, 56, 2, WHITE), rect(6, 72, 88, 22, '#F2DDA4', 2), umbrella(36, 70, 18, RED))
S['피서'] = J(mountain(36, 70, 52, 40), sun(80, 20, 9, False), waves(10, 80, 2, SKY), plane(52, 34, .6))
