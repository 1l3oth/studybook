# -*- coding: utf-8 -*-
"""Flat 2D object drawings for the Korean culture unit. Hand-authored SVG, no image generation.
Run: python korean-culture-talk/draw.py"""
import io
import os

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'img')
NAVY, INK, WHITE, LINE = '#1C2A4A', '#23262D', '#FFFFFF', '#C9CED8'
BLUE, GREEN, ORANGE, SKY, PURPLE, BROWN = '#0052A4', '#00A84D', '#EF7C1C', '#00A5DE', '#996CAC', '#CD7C2F'
RED, YELLOW, SKIN, STEEL, STEEL_D, WOOD = '#D7372B', '#F5B700', '#F2C9A0', '#C7CDD6', '#8E97A5', '#E9D8BC'
KF = 'Malgun Gothic, Apple SD Gothic Neo, Noto Sans KR, sans-serif'


def svg(name, body, vb='0 0 160 100'):
    s = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}">{body}</svg>\n'
    io.open(os.path.join(OUT, name), 'w', encoding='utf-8', newline='\n').write(s)


def T(x, y, s, size=14, fill=INK, weight=700):
    return f'<text x="{x}" y="{y}" font-family="{KF}" font-size="{size}" font-weight="{weight}" fill="{fill}" text-anchor="middle">{s}</text>'


def person(cx, base, h=64, body=BLUE, tilt=0, hair=INK):
    """Standing person; tilt rotates the upper body forward (a bow) around the hips."""
    hip = base - h * .42
    upper = (f'<rect x="{cx - h * .14:.1f}" y="{hip - h * .36:.1f}" width="{h * .28:.1f}" height="{h * .38:.1f}" rx="{h * .1:.1f}" fill="{body}"/>'
             f'<circle cx="{cx}" cy="{hip - h * .46:.1f}" r="{h * .12:.1f}" fill="{SKIN}"/>'
             f'<path d="M{cx - h * .12:.1f} {hip - h * .48:.1f} a{h * .12:.1f} {h * .12:.1f} 0 0 1 {h * .24:.1f} 0Z" fill="{hair}"/>')
    legs = (f'<rect x="{cx - h * .12:.1f}" y="{hip - 2:.1f}" width="{h * .1:.1f}" height="{h * .42 + 2:.1f}" rx="2" fill="{NAVY}"/>'
            f'<rect x="{cx + h * .02:.1f}" y="{hip - 2:.1f}" width="{h * .1:.1f}" height="{h * .42 + 2:.1f}" rx="2" fill="{NAVY}"/>')
    return legs + f'<g transform="rotate({tilt} {cx} {hip:.1f})">{upper}</g>'


def bowl(cx, top, w, fill=WHITE, food='#F7F3E8'):
    return (f'<path d="M{cx - w / 2} {top} H{cx + w / 2} Q{cx + w / 2} {top + w * .5} {cx} {top + w * .52} Q{cx - w / 2} {top + w * .5} {cx - w / 2} {top}Z" fill="{fill}" stroke="{LINE}" stroke-width="1.8"/>'
            f'<ellipse cx="{cx}" cy="{top}" rx="{w / 2}" ry="{w * .1}" fill="{food}" stroke="{LINE}" stroke-width="1.8"/>')


def steam(x, y, n=3, gap=10, h=10):
    return ''.join(f'<path d="M{x + i * gap} {y} q-4 -{h / 2} 0 -{h} q4 -{h / 2} 0 -{h}" stroke="{LINE}" stroke-width="2.4" fill="none" stroke-linecap="round"/>' for i in range(n))


def note(x, y, c=PURPLE):
    return (f'<g fill="{c}"><ellipse cx="{x}" cy="{y}" rx="5" ry="3.8" transform="rotate(-20 {x} {y})"/>'
            f'<rect x="{x + 3.6}" y="{y - 20}" width="2.2" height="20"/><path d="M{x + 5.8} {y - 20} q8 4 6 12 q-1 -6 -6 -7Z"/></g>')


def dish(x, y, c):
    return (f'<ellipse cx="{x}" cy="{y}" rx="15" ry="8" fill="{WHITE}" stroke="{LINE}" stroke-width="1.8"/>'
            f'<ellipse cx="{x}" cy="{y - 1}" rx="9" ry="4.4" fill="{c}"/>')


os.makedirs(OUT, exist_ok=True)

# 1. one person bows to another
svg('c01-bow.svg',
    f'<rect x="20" y="92" width="120" height="3" rx="1.5" fill="{LINE}"/>'
    + person(56, 92, 70, BLUE, 38) + person(108, 92, 70, GREEN, 0))

# 2. desk name plate with a job title
svg('c02-title.svg',
    f'<path d="M30 74 L44 40 H116 L130 74Z" fill="{NAVY}"/>'
    f'<rect x="44" y="40" width="72" height="34" fill="#2B3B60"/>'
    f'<rect x="26" y="74" width="108" height="8" rx="2" fill="{WOOD}"/>'
    + T(80, 64, '팀장님', 17, WHITE)
    + f'<rect x="58" y="12" width="44" height="22" rx="4" fill="{WHITE}" stroke="{LINE}" stroke-width="2"/>'
    + T(80, 28, '님', 13, BLUE))

# 3. two hands hold out a gift
svg('c03-two-hands.svg',
    f'<rect x="56" y="26" width="48" height="38" rx="3" fill="{RED}"/>'
    f'<rect x="76" y="26" width="8" height="38" fill="{YELLOW}"/><rect x="56" y="40" width="48" height="8" fill="{YELLOW}"/>'
    f'<path d="M80 26 q-14 -16 -18 -4 q2 6 18 4Z M80 26 q14 -16 18 -4 q-2 6 -18 4Z" fill="{YELLOW}"/>'
    f'<path d="M14 78 Q34 60 56 58 Q66 58 66 66 Q58 72 46 74 L30 90Z" fill="{SKIN}"/>'
    f'<path d="M146 78 Q126 60 104 58 Q94 58 94 66 Q102 72 114 74 L130 90Z" fill="{SKIN}"/>'
    f'<rect x="4" y="80" width="26" height="16" rx="4" fill="{BLUE}" transform="rotate(-38 17 88)"/>'
    f'<rect x="130" y="80" width="26" height="16" rx="4" fill="{BLUE}" transform="rotate(38 143 88)"/>')

# 4. shared side dishes around one table
svg('c04-banchan.svg',
    f'<ellipse cx="80" cy="56" rx="74" ry="38" fill="{WOOD}"/>'
    + dish(42, 40, RED) + dish(80, 30, GREEN) + dish(118, 40, YELLOW) + dish(42, 72, BROWN) + dish(118, 72, '#E8A0A0')
    + bowl(80, 56, 26) + f'<ellipse cx="80" cy="56" rx="13" ry="2.6" fill="{WHITE}"/>')

# 5. one pot of stew, two spoons
svg('c05-jjigae.svg',
    f'<path d="M36 46 H124 Q122 88 80 90 Q38 88 36 46Z" fill="#5A3B2E"/>'
    f'<ellipse cx="80" cy="46" rx="44" ry="10" fill="{RED}"/>'
    f'<rect x="62" y="40" width="10" height="7" rx="1.5" fill="{WHITE}"/><rect x="86" y="42" width="9" height="6" rx="1.5" fill="{WHITE}"/>'
    f'<path d="M72 48 q6 -6 12 0" stroke="{GREEN}" stroke-width="3" fill="none"/>'
    + steam(66, 30, 3, 12, 10)
    + f'<g transform="rotate(-35 40 30)"><rect x="38" y="4" width="4" height="40" rx="2" fill="{STEEL_D}"/><ellipse cx="40" cy="46" rx="6" ry="8" fill="{STEEL}"/></g>'
    + f'<g transform="rotate(35 120 30)"><rect x="118" y="4" width="4" height="40" rx="2" fill="{STEEL_D}"/><ellipse cx="120" cy="46" rx="6" ry="8" fill="{STEEL}"/></g>')

# 6. empty bowl and a stopwatch
svg('c06-fast.svg',
    bowl(56, 54, 60, WHITE, '#EFEFEF')
    + f'<circle cx="118" cy="50" r="26" fill="{WHITE}" stroke="{NAVY}" stroke-width="5"/>'
    f'<rect x="112" y="16" width="12" height="7" rx="2" fill="{NAVY}"/>'
    f'<path d="M118 50 V32" stroke="{RED}" stroke-width="4" stroke-linecap="round"/><path d="M118 50 L130 56" stroke="{INK}" stroke-width="3" stroke-linecap="round"/>'
    f'<path d="M6 40 H26 M2 52 H22 M8 64 H26" stroke="{LINE}" stroke-width="3" stroke-linecap="round"/>')

# 7. noodles lifted from a pot, with sound lines
svg('c07-slurp.svg',
    f'<path d="M34 54 H112 V82 Q112 90 104 90 H42 Q34 90 34 82Z" fill="{YELLOW}"/>'
    f'<rect x="26" y="50" width="94" height="8" rx="3" fill="#D99E00"/><rect x="118" y="52" width="22" height="5" rx="2" fill="#D99E00"/>'
    f'<ellipse cx="73" cy="54" rx="38" ry="5" fill="#E7612C"/>'
    + ''.join(f'<path d="M{64 + i * 5} 54 q-3 -14 2 -24 q3 -8 0 -16" stroke="#F2D27A" stroke-width="2.6" fill="none"/>' for i in range(4))
    + f'<path d="M60 4 L74 16 M88 4 L80 18" stroke="{STEEL_D}" stroke-width="3.2" stroke-linecap="round"/>'
    f'<path d="M112 14 q8 8 0 16 M122 8 q14 14 0 28 M132 4 q18 20 0 38" stroke="{ORANGE}" stroke-width="3" fill="none" stroke-linecap="round"/>')

# 8. metal spoon and chopsticks (sujeo)
svg('c08-chopsticks.svg',
    f'<rect x="20" y="72" width="120" height="16" rx="4" fill="{WOOD}"/>'
    f'<g transform="rotate(-8 80 50)"><rect x="40" y="38" width="96" height="5" rx="2.5" fill="{STEEL_D}"/>'
    f'<rect x="40" y="50" width="96" height="5" rx="2.5" fill="{STEEL}"/>'
    f'<rect x="22" y="62" width="72" height="5" rx="2.5" fill="{STEEL_D}"/><ellipse cx="108" cy="64.5" rx="16" ry="9" fill="{STEEL}"/>'
    f'<ellipse cx="106" cy="62" rx="9" ry="3.5" fill="{WHITE}" opacity=".6"/></g>')

# 9. a bill passed back and forth: today me, next time you
svg('c09-next-time.svg',
    f'<path d="M58 12 H102 V86 l-5.5 -5 l-5.5 5 l-5.5 -5 l-5.5 5 l-5.5 -5 l-5.5 5 l-5.5 -5 l-5.5 5Z" fill="{WHITE}" stroke="{LINE}" stroke-width="2"/>'
    + ''.join(f'<rect x="66" y="{24 + i * 10}" width="{28 - (i % 2) * 10}" height="4" rx="2" fill="{LINE}"/>' for i in range(4))
    + f'<rect x="66" y="66" width="28" height="5" rx="2.5" fill="{INK}"/>'
    f'<path d="M14 40 Q30 16 50 26" stroke="{BLUE}" stroke-width="4" fill="none" stroke-linecap="round"/><path d="M50 26 l-10 -2 l4 9Z" fill="{BLUE}"/>'
    f'<path d="M146 60 Q130 84 110 74" stroke="{GREEN}" stroke-width="4" fill="none" stroke-linecap="round"/><path d="M110 74 l10 2 l-4 -9Z" fill="{GREEN}"/>'
    + T(26, 62, '오늘', 12, BLUE) + T(134, 38, '다음', 12, GREEN))

# 10. 우리: one roof over a family
svg('c10-uri.svg',
    f'<path d="M24 50 L80 12 L136 50Z" fill="{ORANGE}"/><rect x="36" y="48" width="88" height="44" fill="{WHITE}" stroke="{LINE}" stroke-width="2"/>'
    + person(62, 92, 38, BLUE) + person(80, 92, 30, GREEN) + person(98, 92, 38, PURPLE)
    + f'<rect x="56" y="22" width="48" height="22" rx="11" fill="{WHITE}"/>' + T(80, 38, '우리', 15, ORANGE))

# 11. New Year calendar: everyone one year older
svg('c11-age.svg',
    f'<rect x="20" y="16" width="64" height="72" rx="6" fill="{WHITE}" stroke="{LINE}" stroke-width="2"/>'
    f'<rect x="20" y="16" width="64" height="18" rx="6" fill="{RED}"/><rect x="20" y="28" width="64" height="6" fill="{RED}"/>'
    + T(52, 30, '1월', 12, WHITE) + T(52, 74, '1', 36, INK, 800)
    + f'<rect x="100" y="56" width="44" height="28" rx="4" fill="#F6E1C8"/><rect x="100" y="56" width="44" height="8" rx="4" fill="{WHITE}"/>'
    f'<rect x="119" y="40" width="6" height="16" rx="2" fill="{SKY}"/><path d="M122 30 q5 6 0 10 q-5 -4 0 -10Z" fill="{YELLOW}"/>'
    + T(122, 24, '+1', 14, GREEN, 800))

# 12. older friend and younger friend: 언니
svg('c12-unnie.svg',
    f'<rect x="20" y="92" width="120" height="3" rx="1.5" fill="{LINE}"/>'
    + person(56, 92, 74, PURPLE) + person(104, 92, 60, SKY)
    + f'<path d="M98 20 H140 A8 8 0 0 1 148 28 V40 A8 8 0 0 1 140 48 H116 L108 56 L109 48 H98 A8 8 0 0 1 90 40 V28 A8 8 0 0 1 98 20Z" fill="{WHITE}" stroke="{LINE}" stroke-width="2"/>'
    + T(119, 40, '언니!', 13, PURPLE))

# 13. karaoke screen, microphone and notes
svg('c13-noraebang.svg',
    f'<rect x="16" y="14" width="74" height="50" rx="5" fill="{NAVY}"/><rect x="22" y="20" width="62" height="38" rx="2" fill="#2B3B60"/>'
    f'<rect x="30" y="44" width="46" height="5" rx="2.5" fill="{YELLOW}"/><rect x="30" y="30" width="34" height="5" rx="2.5" fill="{WHITE}"/>'
    f'<rect x="46" y="64" width="14" height="12" fill="{NAVY}"/><rect x="34" y="76" width="38" height="5" rx="2" fill="{NAVY}"/>'
    f'<g transform="rotate(24 120 60)"><rect x="114" y="52" width="12" height="40" rx="5" fill="{INK}"/>'
    f'<circle cx="120" cy="44" r="13" fill="{STEEL}"/><path d="M110 40 H130 M109 46 H131" stroke="{STEEL_D}" stroke-width="1.6"/></g>'
    + note(102, 28) + note(140, 18, ORANGE))

# vocab-only pictures
svg('w-age-man.svg',
    f'<rect x="40" y="16" width="80" height="70" rx="8" fill="{WHITE}" stroke="{LINE}" stroke-width="2"/>'
    + T(80, 48, '만', 26, BLUE, 800) + T(80, 74, '0 → 1', 15, INK))
svg('w-coin.svg',
    f'<rect x="40" y="10" width="56" height="80" rx="6" fill="{PURPLE}"/><rect x="48" y="20" width="40" height="28" rx="3" fill="#2B3B60"/>'
    f'<rect x="60" y="60" width="16" height="4" rx="2" fill="{INK}"/>'
    f'<circle cx="118" cy="62" r="16" fill="{YELLOW}" stroke="#D99E00" stroke-width="3"/>' + T(118, 67, '원', 12, '#8A6400', 800))
svg('w-dinner.svg',
    f'<rect x="20" y="58" width="120" height="10" rx="3" fill="{WOOD}"/>'
    + ''.join(f'<path d="M{40 + i * 26} 58 V30 q0 -6 6 -6 h4 q6 0 6 6 V58" fill="#BFE3F2" stroke="{LINE}" stroke-width="1.5"/>' for i in range(4))
    + f'<path d="M30 20 L44 10 M116 20 L130 10" stroke="{YELLOW}" stroke-width="3" stroke-linecap="round"/>')
svg('w-wow.svg',
    f'<circle cx="80" cy="50" r="36" fill="{YELLOW}"/><circle cx="66" cy="42" r="6" fill="{INK}"/><circle cx="94" cy="42" r="6" fill="{INK}"/>'
    f'<ellipse cx="80" cy="66" rx="8" ry="10" fill="{INK}"/><path d="M124 18 v20 M124 46 v4" stroke="{RED}" stroke-width="5" stroke-linecap="round"/>')
svg('w-used-to.svg',
    f'<circle cx="80" cy="50" r="36" fill="{YELLOW}"/><path d="M62 44 q6 -6 12 0 M86 44 q6 -6 12 0" stroke="{INK}" stroke-width="4" fill="none" stroke-linecap="round"/>'
    f'<path d="M64 62 q16 14 32 0" stroke="{INK}" stroke-width="4" fill="none" stroke-linecap="round"/>')
svg('w-polite.svg',
    f'<path d="M30 20 H130 A10 10 0 0 1 140 30 V60 A10 10 0 0 1 130 70 H70 L54 86 L56 70 H30 A10 10 0 0 1 20 60 V30 A10 10 0 0 1 30 20Z" fill="{WHITE}" stroke="{LINE}" stroke-width="2"/>'
    + T(80, 52, '-요 · -습니다', 15, BLUE))
print('drawn')
