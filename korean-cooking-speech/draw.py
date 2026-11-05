# -*- coding: utf-8 -*-
"""Flat 2D object drawings for the cooking speech unit (K-Specialist 2026-11-28).
Replaces the older scene drawings (Rex, 2026-11-05: "redraw everything, from now we adopt the new UI").
Hand-authored SVG, no image generation. Run: python korean-cooking-speech/draw.py"""
import io
import os

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'img')
NAVY, INK, WHITE, LINE = '#1C2A4A', '#23262D', '#FFFFFF', '#C9CED8'
GREEN, YELLOW, RED, BLUE, SKY, ORANGE = '#00A84D', '#F5B700', '#D7372B', '#0052A4', '#00A5DE', '#EF7C1C'
CABBAGE, CABBAGE_D, MEAT, STEEL = '#B8DC8A', '#8FC25E', '#9C5A3C', '#9AA3B2'
KFONT = 'Malgun Gothic, Apple SD Gothic Neo, Noto Sans KR, sans-serif'


def svg(name, body, vb='0 0 160 100'):
    s = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}">{body}</svg>\n'
    io.open(os.path.join(OUT, name), 'w', encoding='utf-8', newline='\n').write(s)


def text(x, y, t, size=11, fill=INK, weight=700):
    return (f'<text x="{x}" y="{y}" font-family="{KFONT}" font-size="{size}" font-weight="{weight}" '
            f'fill="{fill}" text-anchor="middle">{t}</text>')


def steam(x, y, n=3, gap=14, h=10):
    return ''.join(f'<path d="M{x + i * gap} {y} q-4 -{h / 2} 0 -{h} t0 -{h}" fill="none" stroke="{LINE}" '
                   f'stroke-width="2.6" stroke-linecap="round"/>' for i in range(n))


def heart(cx, cy, k=1.0, fill=RED):
    return (f'<path transform="translate({cx} {cy}) scale({k})" d="M0 6 C-10 -1 -9 -10 -4 -10 C-1.5 -10 0 -8 0 -6 '
            f'C0 -8 1.5 -10 4 -10 C9 -10 10 -1 0 6Z" fill="{fill}"/>')


def bowl(cx, top, w, broth):
    return (f'<path d="M{cx - w} {top} Q{cx - w + 2} {top + w * .76:.1f} {cx} {top + w * .8:.1f} Q{cx + w - 2} {top + w * .76:.1f} {cx + w} {top}Z" '
            f'fill="{WHITE}" stroke="{LINE}" stroke-width="2"/>'
            f'<ellipse cx="{cx}" cy="{top}" rx="{w}" ry="{w * .24:.1f}" fill="{broth}" stroke="{LINE}" stroke-width="2"/>')


def wok(cx, cy, w, food=True):
    out = (f'<rect x="{cx + w - 4}" y="{cy - 4}" width="{w * .9:.1f}" height="7" rx="3.5" fill="{INK}"/>'
           f'<path d="M{cx - w} {cy} Q{cx} {cy + w * .7:.1f} {cx + w} {cy}Z" fill="#3A3E47"/>'
           f'<rect x="{cx - w - 2}" y="{cy - 3}" width="{2 * w + 4}" height="5" rx="2.5" fill="#55595F"/>')
    if food:
        out += (f'<path d="M{cx - w * .7:.1f} {cy - 2} q{w * .3:.1f} -12 {w * .6:.1f} -4 q{w * .3:.1f} -12 {w * .5:.1f} -2 '
                f'q{w * .3:.1f} -10 {w * .3:.1f} 4Z" fill="{CABBAGE}"/>'
                f'<rect x="{cx - w * .45:.1f}" y="{cy - 9}" width="12" height="5" rx="2.5" fill="{MEAT}"/>'
                f'<rect x="{cx + w * .15:.1f}" y="{cy - 11}" width="12" height="5" rx="2.5" fill="{MEAT}"/>'
                f'<path d="M{cx - w * .1:.1f} {cy - 6} l6 -3" stroke="{RED}" stroke-width="3" stroke-linecap="round"/>')
    return out


def chili(x, y, rot=0, k=1.0):
    return (f'<g transform="translate({x} {y}) rotate({rot}) scale({k})">'
            f'<path d="M0 0 Q14 2 28 -6 Q30 -2 26 2 Q12 10 0 6Z" fill="{RED}"/>'
            f'<path d="M0 0 Q-5 1 -7 -4 M0 3 L-4 3" stroke="#4E8A4F" stroke-width="3" fill="none" stroke-linecap="round"/></g>')


def salt(x, y, k=1.0):
    holes = ''.join(f'<circle cx="{x + dx * k:.1f}" cy="{y + 4 * k:.1f}" r="{1.4 * k:.1f}" fill="{STEEL}"/>' for dx in (-6, 0, 6))
    return (f'<rect x="{x - 12 * k:.1f}" y="{y + 10 * k:.1f}" width="{24 * k:.1f}" height="{36 * k:.1f}" rx="{5 * k:.1f}" fill="{WHITE}" stroke="{LINE}" stroke-width="2"/>'
            f'<path d="M{x - 12 * k:.1f} {y + 12 * k:.1f} Q{x} {y - 4 * k:.1f} {x + 12 * k:.1f} {y + 12 * k:.1f}Z" fill="{STEEL}"/>'
            + holes + text(x, y + 33 * k, '소금', 7.5 * k))


def coin(x, y, r=7):
    return (f'<circle cx="{x}" cy="{y}" r="{r}" fill="{YELLOW}"/><circle cx="{x}" cy="{y}" r="{r - 2.5}" fill="none" '
            f'stroke="#D99E00" stroke-width="1.5"/>')


def check(x, y, k=1.0):
    return (f'<circle cx="{x}" cy="{y}" r="{10 * k}" fill="{GREEN}"/>'
            f'<path d="M{x - 4.5 * k} {y} l{3.5 * k} {3.5 * k} l{6.5 * k} {-7 * k}" fill="none" stroke="{WHITE}" stroke-width="{2.8 * k}" stroke-linecap="round" stroke-linejoin="round"/>')


def piggy(cx, cy):
    return (f'<ellipse cx="{cx}" cy="{cy}" rx="30" ry="22" fill="#F4A6B5"/>'
            f'<circle cx="{cx + 30}" cy="{cy - 2}" r="8" fill="#EE8FA2"/><circle cx="{cx + 28}" cy="{cy - 3}" r="1.5" fill="{INK}"/>'
            f'<circle cx="{cx + 32}" cy="{cy - 3}" r="1.5" fill="{INK}"/><path d="M{cx + 12} {cy - 18} l6 -10 l4 10Z" fill="#EE8FA2"/>'
            f'<circle cx="{cx + 14}" cy="{cy - 6}" r="2.2" fill="{INK}"/>'
            f'<rect x="{cx - 20}" y="{cy + 16}" width="8" height="12" rx="3" fill="#EE8FA2"/><rect x="{cx + 10}" y="{cy + 16}" width="8" height="12" rx="3" fill="#EE8FA2"/>'
            f'<rect x="{cx - 8}" y="{cy - 22}" width="16" height="3.5" rx="1.75" fill="#B5687A"/>')


os.makedirs(OUT, exist_ok=True)

# 01. who I am: a laptop with code and a team badge
svg('k01-intro.svg',
    f'<rect x="28" y="16" width="80" height="54" rx="5" fill="{NAVY}"/>'
    f'<rect x="33" y="21" width="70" height="44" rx="2" fill="#2B3B60"/>'
    + ''.join(f'<rect x="{38 + d}" y="{28 + i * 8}" width="{w}" height="3.5" rx="1.75" fill="{c}"/>'
              for i, (d, w, c) in enumerate([(0, 30, GREEN), (6, 40, SKY), (6, 24, YELLOW), (0, 18, GREEN)]))
    + f'<path d="M18 74 H118 L110 82 H26Z" fill="{STEEL}"/>'
    f'<path d="M128 6 Q134 20 135 28 M142 6 Q136 20 135 28" stroke="{BLUE}" stroke-width="3" fill="none"/>'
    f'<rect x="118" y="28" width="34" height="46" rx="5" fill="{WHITE}" stroke="{LINE}" stroke-width="2"/>'
    f'<rect x="118" y="28" width="34" height="9" rx="4" fill="{NAVY}"/>'
    f'<circle cx="135" cy="49" r="6" fill="{NAVY}"/><path d="M125 64 Q135 52 145 64Z" fill="{NAVY}"/>'
    f'<rect x="124" y="67" width="22" height="3.5" rx="1.75" fill="{INK}"/>')

# 02. my new habit: cooking (a pan with a "new" tag)
svg('k02-habit.svg',
    wok(66, 56, 40)
    + f'<rect x="114" y="14" width="34" height="20" rx="10" fill="{RED}"/>' + text(131, 28, '새', 12, WHITE)
    + f'<path d="M114 30 L102 40" stroke="{RED}" stroke-width="2.5" stroke-linecap="round"/>' + steam(52, 34, 3, 13, 8))

# 03. before Korea I almost never cooked: a take-away box, a cold empty pan
svg('k03-before.svg',
    f'<path d="M24 44 H80 L74 90 H30Z" fill="{WHITE}" stroke="{LINE}" stroke-width="2"/>'
    f'<path d="M24 44 L34 30 H70 L80 44" fill="#EEF0F4" stroke="{LINE}" stroke-width="2"/>'
    f'<path d="M44 30 Q52 18 60 30" fill="none" stroke="{STEEL}" stroke-width="3"/>'
    f'<rect x="40" y="58" width="24" height="14" rx="3" fill="{RED}"/>'
    f'<rect x="138" y="62" width="18" height="6" rx="3" fill="{INK}"/>'
    f'<path d="M92 64 Q115 92 138 64Z" fill="#C3C7CE"/><rect x="90" y="61" width="50" height="5" rx="2.5" fill="#B0B5BD"/>'
    f'<path d="M100 40 l16 16 M116 40 l-16 16" stroke="{RED}" stroke-width="4" stroke-linecap="round"/>')

# 04. I missed Cambodian food: a bowl of rice with a heart above
svg('k04-miss.svg',
    bowl(72, 52, 44, '#F7F3E8')
    + ''.join(f'<ellipse cx="{50 + i * 9}" cy="{50 + (i % 2) * 3}" rx="3.5" ry="2" fill="{WHITE}" stroke="{LINE}" stroke-width=".8"/>' for i in range(6))
    + f'<path d="M104 18 h36 a8 8 0 0 1 8 8 v14 a8 8 0 0 1 -8 8 h-20 l-8 7 l1 -7 h-9 a8 8 0 0 1 -8 -8 v-14 a8 8 0 0 1 8 -8Z" fill="{WHITE}" stroke="{LINE}" stroke-width="2"/>'
    + heart(122, 34, 1.15))

# 05. eating out costs a lot, I wanted to save: a wallet with coins flying out
svg('k05-money.svg',
    f'<rect x="30" y="36" width="76" height="52" rx="8" fill="{MEAT}"/>'
    f'<path d="M30 46 H106" stroke="#7A4530" stroke-width="2"/>'
    f'<rect x="84" y="54" width="28" height="18" rx="6" fill="#B87652"/><circle cx="96" cy="63" r="3" fill="{YELLOW}"/>'
    f'<rect x="38" y="26" width="46" height="18" rx="2" fill="{GREEN}" transform="rotate(-8 61 35)"/>'
    + coin(122, 30) + coin(138, 48, 6) + coin(130, 70, 5)
    + f'<path d="M110 40 l6 -4 M114 52 l8 -2" stroke="{LINE}" stroke-width="2.5" stroke-linecap="round"/>')

# 06. cha spey: stir-fried cabbage and meat
svg('k06-chaspey.svg',
    f'<ellipse cx="80" cy="66" rx="64" ry="22" fill="{WHITE}" stroke="{LINE}" stroke-width="2"/>'
    f'<ellipse cx="80" cy="62" rx="46" ry="14" fill="#F1F3F6"/>'
    + ''.join(f'<path d="M{44 + i * 12} {64 - (i % 3) * 3} q6 -12 14 -2" fill="{CABBAGE if i % 2 else CABBAGE_D}"/>' for i in range(6))
    + ''.join(f'<rect x="{52 + i * 16}" y="{52 + (i % 2) * 8}" width="13" height="6" rx="3" fill="{MEAT}"/>' for i in range(4))
    + f'<path d="M66 54 l6 -3 M96 60 l6 -3" stroke="{RED}" stroke-width="3" stroke-linecap="round"/>'
    f'<circle cx="84" cy="50" r="2.4" fill="#F2E3B3"/><circle cx="60" cy="62" r="2.4" fill="#F2E3B3"/>'
    + steam(64, 34, 3, 16, 8))

# 07. first I buy garlic, cabbage and meat, then cut and stir-fry
svg('k07-buy.svg',
    f'<path d="M22 40 H82 L76 92 H28Z" fill="#E9D8BC"/>'
    f'<path d="M38 40 Q38 26 52 26 Q66 26 66 40" fill="none" stroke="#C9B38E" stroke-width="3.5"/>'
    f'<circle cx="44" cy="40" r="15" fill="{CABBAGE}"/><path d="M36 38 q8 -8 16 2 M40 46 q6 -4 10 0" stroke="{CABBAGE_D}" stroke-width="2" fill="none"/>'
    f'<path d="M64 26 q6 8 8 14 q-6 6 -16 0 q2 -6 8 -14Z" fill="#F3EBDD" stroke="{LINE}" stroke-width="1.5"/>'
    f'<rect x="94" y="56" width="52" height="30" rx="4" fill="#F4F6F9" stroke="{LINE}" stroke-width="2"/>'
    f'<path d="M100 76 q10 -14 22 -6 q10 -12 20 0 v8 h-42Z" fill="#D9776A"/>'
    f'<g transform="rotate(-30 120 30)"><rect x="96" y="26" width="34" height="9" rx="2" fill="{STEEL}"/><rect x="128" y="27" width="20" height="7" rx="3" fill="{INK}"/></g>')

# 08. not in the recipe, but I always add chili
svg('k08-chili.svg',
    f'<rect x="20" y="14" width="56" height="74" rx="4" fill="{WHITE}" stroke="{LINE}" stroke-width="2"/>'
    + ''.join(f'<rect x="28" y="{26 + i * 11}" width="{40 - (i % 2) * 12}" height="4" rx="2" fill="{LINE}"/>' for i in range(5))
    + chili(88, 46, -12, 1.6) + chili(96, 70, 8, 1.3) + check(140, 22))

# 09. my food is always a little salty
svg('k09-salty.svg',
    salt(56, 10, 1.5)
    + ''.join(f'<rect x="{96 + (i * 13) % 44}" y="{30 + (i * 7) % 50}" width="4" height="4" rx="1" fill="{WHITE}" stroke="{STEEL}" stroke-width="1"/>' for i in range(16))
    + f'<path d="M78 26 l10 4 M80 36 l10 0" stroke="{LINE}" stroke-width="2.5" stroke-linecap="round"/>')

# 10. so I usually eat it alone: one bowl, one spoon, the other place empty
svg('k10-alone.svg',
    f'<rect x="10" y="74" width="140" height="7" rx="3.5" fill="#B07A4A"/>'
    f'<rect x="20" y="81" width="6" height="16" fill="#8E6038"/><rect x="134" y="81" width="6" height="16" fill="#8E6038"/>'
    + bowl(48, 50, 26, '#E9C88A') + steam(40, 36, 2, 14, 7)
    + f'<rect x="78" y="60" width="4" height="14" rx="2" fill="{STEEL}"/><ellipse cx="80" cy="58" rx="4" ry="6" fill="{STEEL}"/>'
    f'<ellipse cx="118" cy="62" rx="24" ry="9" fill="none" stroke="{LINE}" stroke-width="2.5" stroke-dasharray="5 5"/>')

# 11. making my own food, I can save on food costs
svg('k11-save.svg',
    piggy(66, 60) + coin(66, 22, 8)
    + f'<path d="M66 32 v4" stroke="{LINE}" stroke-width="2.5" stroke-linecap="round"/>'
    + f'<rect x="114" y="18" width="34" height="62" rx="3" fill="{WHITE}" stroke="{LINE}" stroke-width="2"/>'
    + ''.join(f'<rect x="120" y="{28 + i * 9}" width="22" height="3.5" rx="1.75" fill="{LINE}"/>' for i in range(4))
    + f'<path d="M131 64 v10 m-6 -6 l6 6 l6 -6" fill="none" stroke="{GREEN}" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>')

# 12. eating cha spey eases my heart, I miss home less
svg('k12-home.svg',
    f'<path d="M30 52 L66 24 L102 52 V90 H30Z" fill="{WHITE}" stroke="{LINE}" stroke-width="2.5" stroke-linejoin="round"/>'
    f'<path d="M24 54 L66 20 L108 54" fill="none" stroke="{ORANGE}" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/>'
    f'<rect x="58" y="66" width="16" height="24" rx="2" fill="{NAVY}"/>'
    + heart(66, 48, 1.1)
    + f'<ellipse cx="128" cy="74" rx="22" ry="8" fill="{WHITE}" stroke="{LINE}" stroke-width="2"/>'
    f'<path d="M114 72 q4 -8 10 -2 q4 -8 10 0 q4 -6 8 2Z" fill="{CABBAGE}"/>' + steam(122, 58, 2, 10, 6))

# 13. in my opinion, cooking is the best habit I picked up in Korea
svg('k13-best.svg',
    f'<path d="M58 4 H72 L88 32 H74Z" fill="{BLUE}"/><path d="M102 4 H88 L72 32 H86Z" fill="{SKY}"/>'
    f'<circle cx="80" cy="56" r="30" fill="{YELLOW}"/><circle cx="80" cy="56" r="23" fill="none" stroke="#D99E00" stroke-width="2.5"/>'
    + text(80, 63, '1', 22, '#8A5A00', 800) + wok(132, 70, 16, True).replace(f'fill="{INK}"', f'fill="{INK}"', 1))

# 14. next time: a little less salt, so others can eat with me
svg('k14-next.svg',
    salt(30, 14, 1.2)
    + f'<rect x="46" y="24" width="3" height="3" rx="1" fill="{WHITE}" stroke="{STEEL}"/>'
    + bowl(84, 60, 18, '#E9C88A') + bowl(124, 60, 18, '#E9C88A') + bowl(104, 34, 14, '#E9C88A')
    + f'<rect x="58" y="86" width="96" height="5" rx="2.5" fill="#B07A4A"/>')

print('drawn:', sorted(f for f in os.listdir(OUT) if f.startswith('k')))
