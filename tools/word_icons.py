# -*- coding: utf-8 -*-
"""Flat drawing pieces for the vocab word pictures (viewBox 0 0 100 100).
Same palette as the unit card drawings. Used by tools/draw_words.py."""

NAVY, INK, WHITE, LINE = '#1C2A4A', '#23262D', '#FFFFFF', '#C9CED8'
GREEN, YELLOW, RED, BLUE, SKY, ORANGE, PURPLE = '#00A84D', '#F5B700', '#D7372B', '#0052A4', '#00A5DE', '#EF7C1C', '#996CAC'
CABBAGE, CABBAGE_D, MEAT, STEEL, SKIN, WOOD, PINK = '#B8DC8A', '#8FC25E', '#9C5A3C', '#9AA3B2', '#E8B48C', '#B07A4A', '#F4A6B5'
KFONT = 'Malgun Gothic, Apple SD Gothic Neo, Noto Sans KR, sans-serif'


def T(x, y, s, size=14, fill=INK, weight=800):
    return (f'<text x="{x}" y="{y}" font-family="{KFONT}" font-size="{size}" font-weight="{weight}" '
            f'fill="{fill}" text-anchor="middle">{s}</text>')


def rect(x, y, w, h, fill, r=3, stroke=None, sw=2):
    st = f' stroke="{stroke}" stroke-width="{sw}"' if stroke else ''
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}"{st}/>'


def circ(cx, cy, r, fill, stroke=None, sw=2):
    st = f' stroke="{stroke}" stroke-width="{sw}"' if stroke else ''
    return f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{fill}"{st}/>'


def path(d, fill='none', stroke=None, sw=3, cap='round'):
    st = f' stroke="{stroke}" stroke-width="{sw}" stroke-linecap="{cap}" stroke-linejoin="round"' if stroke else ''
    return f'<path d="{d}" fill="{fill}"{st}/>'


def arrow(x1, y1, x2, y2, c=INK, sw=4):
    import math
    a = math.atan2(y2 - y1, x2 - x1)
    h = 9
    p1 = (x2 - h * math.cos(a - .5), y2 - h * math.sin(a - .5))
    p2 = (x2 - h * math.cos(a + .5), y2 - h * math.sin(a + .5))
    return (path(f'M{x1} {y1} L{x2} {y2}', stroke=c, sw=sw)
            + path(f'M{p1[0]:.1f} {p1[1]:.1f} L{x2} {y2} L{p2[0]:.1f} {p2[1]:.1f}', stroke=c, sw=sw))


def check(x, y, k=1.0):
    return circ(x, y, 12 * k, GREEN) + path(f'M{x - 5 * k} {y} l{4 * k} {4 * k} l{7 * k} {-8 * k}', stroke=WHITE, sw=3.4 * k)


def cross(x, y, k=1.0, c=RED):
    return path(f'M{x - 8 * k} {y - 8 * k} l{16 * k} {16 * k} M{x + 8 * k} {y - 8 * k} l{-16 * k} {16 * k}', stroke=c, sw=5 * k)


def heart(cx, cy, k=1.0, fill=RED):
    return (f'<path transform="translate({cx} {cy}) scale({k})" d="M0 9 C-15 -1 -13 -15 -6 -15 C-2 -15 0 -12 0 -9 '
            f'C0 -12 2 -15 6 -15 C13 -15 15 -1 0 9Z" fill="{fill}"/>')


def person(cx, base, h=60, body=BLUE, hair=INK, skin=SKIN):
    r = h * .17
    top = base - h
    return (path(f'M{cx - h * .3:.1f} {base} Q{cx - h * .3:.1f} {top + h * .45:.1f} {cx} {top + h * .45:.1f} '
                 f'Q{cx + h * .3:.1f} {top + h * .45:.1f} {cx + h * .3:.1f} {base}Z', fill=body)
            + circ(cx, round(top + r + 1, 1), round(r, 1), skin)
            + path(f'M{cx - r:.1f} {top + r:.1f} Q{cx} {top - r * .45:.1f} {cx + r:.1f} {top + r:.1f}Z', fill=hair))


def face(cx, cy, r=30, mood='smile', fill=YELLOW):
    eyes = circ(cx - r * .35, cy - r * .15, r * .09, INK) + circ(cx + r * .35, cy - r * .15, r * .09, INK)
    w = r * .4
    mouths = {
        'smile': f'M{cx - w} {cy + r * .25} Q{cx} {cy + r * .65} {cx + w} {cy + r * .25}',
        'sad': f'M{cx - w} {cy + r * .5} Q{cx} {cy + r * .15} {cx + w} {cy + r * .5}',
        'flat': f'M{cx - w} {cy + r * .4} L{cx + w} {cy + r * .4}',
        'open': None,
        'wavy': f'M{cx - w} {cy + r * .4} q{w / 2} -6 {w} 0 q{w / 2} 6 {w} 0',
    }
    m = mouths[mood]
    mouth = (circ(cx, cy + r * .4, r * .18, INK) if m is None else path(m, stroke=INK, sw=r * .1))
    return circ(cx, cy, r, fill) + eyes + mouth


def bowl(cx, top, w, broth='#F7F3E8'):
    return (path(f'M{cx - w} {top} Q{cx - w + 2} {top + w * .76:.1f} {cx} {top + w * .8:.1f} Q{cx + w - 2} {top + w * .76:.1f} {cx + w} {top}Z',
                 fill=WHITE, stroke=LINE, sw=2)
            + f'<ellipse cx="{cx}" cy="{top}" rx="{w}" ry="{w * .24:.1f}" fill="{broth}" stroke="{LINE}" stroke-width="2"/>')


def steam(x, y, n=3, gap=12, h=9):
    return ''.join(path(f'M{x + i * gap} {y} q-4 -{h / 2} 0 -{h} t0 -{h}', stroke=LINE, sw=3) for i in range(n))


def chili(x, y, rot=0, k=1.0):
    return (f'<g transform="translate({x} {y}) rotate({rot}) scale({k})">'
            f'<path d="M0 0 Q14 2 28 -6 Q30 -2 26 2 Q12 10 0 6Z" fill="{RED}"/>'
            f'<path d="M0 0 Q-5 1 -7 -4 M0 3 L-4 3" stroke="#4E8A4F" stroke-width="3" fill="none" stroke-linecap="round"/></g>')


def coin(x, y, r=9):
    return circ(x, y, r, YELLOW) + circ(x, y, r - 3, 'none', '#D99E00', 1.6)


def house(cx, base, w=60, roof=ORANGE):
    h = w * .65
    return (path(f'M{cx - w / 2} {base - h * .55:.1f} L{cx} {base - h:.1f} L{cx + w / 2} {base - h * .55:.1f} V{base} H{cx - w / 2}Z',
                 fill=WHITE, stroke=LINE, sw=2)
            + path(f'M{cx - w / 2 - 5} {base - h * .5:.1f} L{cx} {base - h - 4:.1f} L{cx + w / 2 + 5} {base - h * .5:.1f}', stroke=roof, sw=6)
            + rect(cx - w * .1, base - h * .4, w * .2, h * .4, NAVY, 2))


def sun(cx, cy, r=14, rays=True):
    out = ''
    if rays:
        import math
        for i in range(8):
            a = i * math.pi / 4
            out += path(f'M{cx + (r + 4) * math.cos(a):.1f} {cy + (r + 4) * math.sin(a):.1f} '
                        f'L{cx + (r + 11) * math.cos(a):.1f} {cy + (r + 11) * math.sin(a):.1f}', stroke=YELLOW, sw=4)
    return out + circ(cx, cy, r, YELLOW)


def cloud(cx, cy, k=1.0, fill='#E3E7EE'):
    return (circ(cx - 14 * k, cy + 2 * k, 11 * k, fill) + circ(cx, cy - 6 * k, 15 * k, fill)
            + circ(cx + 15 * k, cy + 2 * k, 11 * k, fill) + rect(cx - 25 * k, cy + 2 * k, 50 * k, 11 * k, fill, 5 * k))


def drop(x, y, k=1.0, c=SKY):
    return f'<path transform="translate({x} {y}) scale({k})" d="M0 -9 C4 -3 6 0 6 3 A6 6 0 0 1 -6 3 C-6 0 -4 -3 0 -9Z" fill="{c}"/>'


def rain(x, y, n=4, gap=12):
    return ''.join(path(f'M{x + i * gap} {y + (i % 2) * 6} l-4 9', stroke=SKY, sw=3.5) for i in range(n))


def thermo(x, y, level=.7, c=RED):
    h = 56
    return (rect(x - 6, y, 12, h, WHITE, 6, LINE, 2) + circ(x, y + h + 4, 10, c)
            + rect(x - 3, y + h * (1 - level), 6, h * level + 4, c, 3))


def bubble(x, y, w, h, fill=WHITE):
    return (rect(x, y, w, h, fill, 10, LINE, 2)
            + path(f'M{x + 14} {y + h - 1} l-4 12 l14 -12Z', fill=fill) + path(f'M{x + 14} {y + h} l-4 12 l14 -12', stroke=LINE, sw=2))


def calendar(x, y, w=56, label='', top=RED):
    return (rect(x, y, w, w * .9, WHITE, 5, LINE, 2) + rect(x, y, w, w * .24, top, 5)
            + (T(x + w / 2, y + w * .72, label, w * .3) if label else ''))


def envelope(x, y, w=64, h=42, fill=WHITE):
    return rect(x, y, w, h, fill, 3, LINE, 2) + path(f'M{x} {y} L{x + w / 2} {y + h * .55:.1f} L{x + w} {y}', stroke=LINE, sw=2)


def tree(cx, base, k=1.0):
    return rect(cx - 4 * k, base - 22 * k, 8 * k, 22 * k, WOOD, 2) + circ(cx, base - 34 * k, 20 * k, GREEN) + circ(cx - 10 * k, base - 26 * k, 12 * k, '#2BB866')


def mountain(cx, base, w=70, h=50):
    return (path(f'M{cx - w / 2} {base} L{cx} {base - h} L{cx + w / 2} {base}Z', fill='#6FAF7A')
            + path(f'M{cx - 9} {base - h + 13} L{cx} {base - h} L{cx + 9} {base - h + 13} l-4 3 l-5 -4 l-5 4Z', fill=WHITE))


def waves(x, y, n=3, c=SKY):
    return ''.join(path(f'M{x} {y + i * 10} q8 -6 16 0 t16 0 t16 0 t16 0', stroke=c, sw=3.5) for i in range(n))


def shirt(cx, top, w=50, fill=SKY, sleeves='short'):
    s = 16 if sleeves == 'short' else 34
    return path(f'M{cx - w / 2} {top + 8} L{cx - w / 2 - 14} {top + s} L{cx - w / 2 - 4} {top + s + 6} L{cx - w / 2 + 2} {top + 20} '
                f'V{top + 58} H{cx + w / 2 - 2} V{top + 20} L{cx + w / 2 + 4} {top + s + 6} L{cx + w / 2 + 14} {top + s} '
                f'L{cx + w / 2} {top + 8} L{cx + 8} {top} Q{cx} {top + 8} {cx - 8} {top}Z', fill=fill)


def pants(cx, top, h=56, fill=NAVY):
    return path(f'M{cx - 20} {top} H{cx + 20} L{cx + 22} {top + h} H{cx + 4} L{cx} {top + 16} L{cx - 4} {top + h} H{cx - 22}Z', fill=fill)


def umbrella(cx, cy, w=36, fill=BLUE):
    return (path(f'M{cx - w} {cy} Q{cx} {cy - w * 1.1:.1f} {cx + w} {cy} Q{cx + w / 2} {cy - 7} {cx} {cy} Q{cx - w / 2} {cy - 7} {cx - w} {cy}Z', fill=fill)
            + path(f'M{cx} {cy} V{cy + w * .9:.1f} q0 7 -7 7 q-6 0 -6 -6', stroke=INK, sw=3.5))


def fan(cx, cy, r=26, c=SKY):
    blades = ''.join(f'<ellipse cx="{cx}" cy="{cy - r * .5:.1f}" rx="{r * .28:.1f}" ry="{r * .5:.1f}" fill="{c}" transform="rotate({a} {cx} {cy})"/>'
                     for a in (0, 120, 240))
    return circ(cx, cy, r, 'none', LINE, 3) + blades + circ(cx, cy, 5, INK)


def phone(x, y, w=36, h=60):
    return rect(x, y, w, h, INK, 7) + rect(x + 3, y + 7, w - 6, h - 14, WHITE, 2)


def plane(x, y, k=1.0, c=SKY):
    return (f'<path transform="translate({x} {y}) scale({k})" d="M0 0 L22 -2 L30 -10 L34 -10 L30 -1 L40 0 L44 -5 L47 -5 '
            f'L45 2 L47 9 L44 9 L40 4 L30 5 L34 14 L30 14 L22 6 L0 4Z" fill="{c}"/>')


def flower(cx, cy, r=14, c=YELLOW, center='#D99E00'):
    import math
    petals = ''.join(f'<ellipse cx="{cx + r * .55 * math.cos(i * math.pi / 6):.1f}" cy="{cy + r * .55 * math.sin(i * math.pi / 6):.1f}" '
                     f'rx="{r * .5:.1f}" ry="{r * .2:.1f}" fill="{c}" transform="rotate({i * 30} {cx + r * .55 * math.cos(i * math.pi / 6):.1f} '
                     f'{cy + r * .55 * math.sin(i * math.pi / 6):.1f})"/>' for i in range(12))
    return petals + circ(cx, cy, r * .3, center)


def wok(cx, cy, w=30, food=True):
    out = (rect(cx + w - 4, cy - 4, w * .8, 7, INK, 3.5) + path(f'M{cx - w} {cy} Q{cx} {cy + w * .7:.1f} {cx + w} {cy}Z', fill='#3A3E47')
           + rect(cx - w - 2, cy - 3, 2 * w + 4, 5, '#55595F', 2.5))
    if food:
        out += (path(f'M{cx - w * .7:.1f} {cy - 2} q{w * .3:.1f} -12 {w * .6:.1f} -4 q{w * .3:.1f} -12 {w * .5:.1f} -2 q{w * .3:.1f} -10 {w * .3:.1f} 4Z', fill=CABBAGE)
                + rect(cx - w * .45, cy - 9, 10, 5, MEAT, 2.5))
    return out


def knife(x, y, rot=-30):
    return (f'<g transform="rotate({rot} {x} {y})">' + rect(x, y, 38, 11, STEEL, 2) + rect(x + 36, y + 2, 22, 8, INK, 3) + '</g>')


def bottle(cx, top, h=64, fill=SKY):
    return (rect(cx - 7, top, 14, 8, INK, 2) + path(f'M{cx - 8} {top + 8} H{cx + 8} L{cx + 14} {top + 20} V{top + h} H{cx - 14} V{top + 20}Z', fill=fill)
            + rect(cx - 14, top + 30, 28, 14, WHITE))


def book(x, y, w=60, h=44, c=BLUE):
    return (path(f'M{x} {y} Q{x + w / 4} {y - 6} {x + w / 2} {y} V{y + h} Q{x + w / 4} {y + h - 6} {x} {y + h}Z', fill=WHITE, stroke=LINE, sw=2)
            + path(f'M{x + w / 2} {y} Q{x + w * .75} {y - 6} {x + w} {y} V{y + h} Q{x + w * .75} {y + h - 6} {x + w / 2} {y + h}Z', fill=WHITE, stroke=LINE, sw=2)
            + ''.join(rect(x + 6, y + 9 + i * 8, w / 2 - 12, 3, c if i == 0 else LINE, 1.5) for i in range(4))
            + ''.join(rect(x + w / 2 + 6, y + 9 + i * 8, w / 2 - 12, 3, LINE, 1.5) for i in range(4)))
