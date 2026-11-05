# -*- coding: utf-8 -*-
"""Flat 2D object drawings for the summer speech unit. Replaces the August AI paintings
(Rex, 2026-11-05: "redraw everything, from now we adopt the new UI").
Hand-authored SVG, no image generation. Run: python korean-summer-speech/draw.py"""
import io
import math
import os

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'img')
NAVY, INK, WHITE, LINE = '#1C2A4A', '#23262D', '#FFFFFF', '#C9CED8'
GREEN, YELLOW, RED, BLUE, SKY, ORANGE = '#00A84D', '#F5B700', '#D7372B', '#0052A4', '#00A5DE', '#EF7C1C'
KFONT = 'Malgun Gothic, Apple SD Gothic Neo, Noto Sans KR, sans-serif'


def svg(name, body, vb='0 0 160 100'):
    s = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}">{body}</svg>\n'
    io.open(os.path.join(OUT, name), 'w', encoding='utf-8', newline='\n').write(s)


def text(x, y, t, size=11, fill=INK, weight=700):
    return (f'<text x="{x}" y="{y}" font-family="{KFONT}" font-size="{size}" font-weight="{weight}" '
            f'fill="{fill}" text-anchor="middle">{t}</text>')


def sun(cx, cy, r):
    rays = ''.join(
        f'<rect x="{cx - 1.6}" y="{cy - r - 7}" width="3.2" height="5" rx="1.6" fill="{YELLOW}" '
        f'transform="rotate({a} {cx} {cy})"/>' for a in range(0, 360, 45))
    return rays + f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{YELLOW}"/>'


def drop(x, y, k=1.0, fill=SKY):
    return (f'<path transform="translate({x} {y}) scale({k})" d="M0 -8 Q6 0 6 3 A6 6 0 0 1 -6 3 Q-6 0 0 -8Z" '
            f'fill="{fill}"/>')


def pine(x, base, h, fill='#3E8E52'):
    w = h * .42
    return (f'<rect x="{x - 2.5}" y="{base - h * .22}" width="5" height="{h * .22}" fill="#7A4E2D"/>'
            f'<path d="M{x} {base - h} L{x + w * .7} {base - h * .5} H{x - w * .7}Z" fill="{fill}"/>'
            f'<path d="M{x} {base - h * .78} L{x + w} {base - h * .2} H{x - w}Z" fill="{fill}"/>')


def bowl(cx, top, w, broth):
    return (f'<path d="M{cx - w} {top} Q{cx - w + 2} {top + 44} {cx} {top + 46} Q{cx + w - 2} {top + 44} {cx + w} {top}Z" '
            f'fill="{WHITE}" stroke="{LINE}" stroke-width="2"/>'
            f'<ellipse cx="{cx}" cy="{top}" rx="{w}" ry="{w * .24:.1f}" fill="{broth}" stroke="{LINE}" stroke-width="2"/>')


def fan(px, py, r, rin, a0=165, a1=15):
    """Folding fan, pivot at px,py, opening upward from angle a0 to a1 (degrees)."""
    def pt(a, rr):
        return px + rr * math.cos(math.radians(a)), py - rr * math.sin(math.radians(a))
    (x0, y0), (x1, y1) = pt(a0, r), pt(a1, r)
    (u0, v0), (u1, v1) = pt(a0, rin), pt(a1, rin)
    ribs = ''.join(f'<path d="M{px} {py} L{pt(a, r)[0]:.1f} {pt(a, r)[1]:.1f}" stroke="{LINE}" stroke-width="1.6"/>'
                   for a in range(a1 + 15, a0, 15))
    return (f'<path d="M{px} {py} L{x0:.1f} {y0:.1f} A{r} {r} 0 0 1 {x1:.1f} {y1:.1f}Z" fill="{WHITE}" stroke="{LINE}" stroke-width="2"/>'
            + ribs +
            f'<path d="M{x0:.1f} {y0:.1f} A{r} {r} 0 0 1 {x1:.1f} {y1:.1f} L{u1:.1f} {v1:.1f} A{rin} {rin} 0 0 0 {u0:.1f} {v0:.1f}Z" fill="{RED}"/>')


os.makedirs(OUT, exist_ok=True)

# 01. opening: lived in Busan, now Seoul, a subway-style route under the summer sun
svg('s01-route.svg',
    sun(30, 24, 9)
    + f'<path d="M34 76 Q70 76 86 56 T130 32" fill="none" stroke="{BLUE}" stroke-width="7" stroke-linecap="round"/>'
    f'<circle cx="34" cy="76" r="7" fill="{WHITE}" stroke="{BLUE}" stroke-width="4"/>'
    f'<circle cx="130" cy="32" r="9" fill="{WHITE}" stroke="{YELLOW}" stroke-width="5"/>'
    + text(34, 96, '부산', 12) + text(130, 58, '서울', 12)
    + f'<rect x="64" y="54" width="28" height="15" rx="7.5" fill="{NAVY}"/>' + text(78, 65, '2년', 10, WHITE))

# 03. Korean office: shorts and a company ID badge
svg('s03-shorts.svg',
    f'<path d="M34 24 H102 L110 88 H78 L68 50 L58 88 H26Z" fill="#3B6EA8"/>'
    f'<rect x="34" y="20" width="68" height="10" rx="2" fill="#2C5687"/>'
    f'<path d="M68 30 V46" stroke="#2C5687" stroke-width="2.5"/>'
    f'<path d="M120 4 Q128 22 129 30 M138 4 Q130 22 129 30" stroke="{RED}" stroke-width="3" fill="none"/>'
    f'<rect x="112" y="30" width="36" height="48" rx="5" fill="{WHITE}" stroke="{LINE}" stroke-width="2"/>'
    f'<rect x="112" y="30" width="36" height="9" rx="4" fill="{NAVY}"/>'
    f'<rect x="120" y="44" width="20" height="18" rx="3" fill="#EEF0F4"/>'
    f'<circle cx="130" cy="50" r="4.5" fill="{NAVY}"/><path d="M122 62 Q130 52 138 62Z" fill="{NAVY}"/>'
    f'<rect x="119" y="67" width="22" height="3.5" rx="1.75" fill="{INK}"/>'
    f'<rect x="122" y="73" width="16" height="2.5" rx="1.25" fill="{LINE}"/>')

# 04. Cambodian office: a long-sleeved uniform under a hot sun
svg('s04-uniform.svg',
    sun(20, 18, 9)
    + f'<path d="M62 18 L44 26 L28 44 L24 92 H38 L44 54 L48 52 V96 H112 V52 L116 54 L122 92 H136 L132 44 L116 26 L98 18Z" '
    f'fill="{WHITE}" stroke="{LINE}" stroke-width="2.5" stroke-linejoin="round"/>'
    f'<path d="M62 18 L72 34 L80 24 L88 34 L98 18" fill="none" stroke="{NAVY}" stroke-width="3" stroke-linejoin="round"/>'
    f'<path d="M80 26 V96" stroke="{LINE}" stroke-width="2"/>'
    + ''.join(f'<circle cx="80" cy="{44 + i * 14}" r="2.3" fill="{NAVY}"/>' for i in range(4))
    + f'<rect x="90" y="40" width="16" height="7" rx="2" fill="{NAVY}"/>'
    f'<rect x="24" y="86" width="14" height="6" fill="{NAVY}"/><rect x="122" y="86" width="14" height="6" fill="{NAVY}"/>'
    + drop(52, 38, .8) + drop(110, 66, .7))

# 05. weather: lotion and dry skin
svg('s05-lotion.svg',
    f'<rect x="40" y="36" width="38" height="58" rx="9" fill="#E6F4FB" stroke="{LINE}" stroke-width="2"/>'
    f'<rect x="52" y="22" width="14" height="14" rx="2" fill="{NAVY}"/>'
    f'<rect x="60" y="18" width="20" height="6" rx="3" fill="{NAVY}"/>'
    f'<rect x="46" y="54" width="26" height="22" rx="3" fill="{WHITE}"/>' + text(59, 69, '로션', 9)
    + drop(88, 30, .6, WHITE).replace('/>', f' stroke="{LINE}" stroke-width="1.5"/>')
    + f'<rect x="96" y="44" width="52" height="46" rx="12" fill="#F2D3B5"/>'
    f'<path d="M106 56 l8 6 l-4 8 l9 5 M132 52 l-6 9 l7 5 l-3 9 M118 80 l7 -4 l8 4" fill="none" stroke="#C4936A" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>')

# 06. sleep: hot night, pillow, moon and a high thermometer
svg('s06-sleep.svg',
    f'<path d="M118 12 A16 16 0 1 0 136 34 A12 12 0 1 1 118 12Z" fill="{YELLOW}"/>'
    f'<rect x="20" y="58" width="92" height="30" rx="15" fill="{WHITE}" stroke="{LINE}" stroke-width="2.5"/>'
    f'<path d="M34 66 Q66 60 98 66" fill="none" stroke="{LINE}" stroke-width="2"/>'
    + drop(46, 50, .7) + drop(70, 44, .55) + drop(92, 50, .7)
    + f'<rect x="136" y="40" width="10" height="44" rx="5" fill="{WHITE}" stroke="{LINE}" stroke-width="2"/>'
    f'<rect x="139" y="48" width="4" height="36" rx="2" fill="{RED}"/>'
    f'<circle cx="141" cy="88" r="7" fill="{RED}"/>')

# 07. air conditioner set to 24 degrees: cool for Koreans, cold for Cambodians
svg('s07-aircon.svg',
    f'<rect x="20" y="10" width="120" height="36" rx="9" fill="{WHITE}" stroke="{LINE}" stroke-width="2.5"/>'
    f'<path d="M30 38 H96" stroke="{LINE}" stroke-width="2.5" stroke-linecap="round"/>'
    f'<rect x="102" y="18" width="30" height="16" rx="3" fill="{NAVY}"/>' + text(117, 30, '24°', 11, WHITE)
    + ''.join(f'<path d="M{40 + i * 22} 52 q-5 6 0 12 t0 12" fill="none" stroke="{SKY}" stroke-width="3" stroke-linecap="round"/>' for i in range(4))
    + f'<rect x="12" y="78" width="44" height="18" rx="9" fill="{SKY}"/>' + text(34, 91, '시원', 10, WHITE)
    + f'<rect x="104" y="78" width="44" height="18" rx="9" fill="{NAVY}"/>' + text(126, 91, '추워', 10, WHITE))

# 08. Cambodian soups: a steaming noodle bowl
svg('s08-soup.svg',
    ''.join(f'<path d="M{62 + i * 18} 30 q-5 -6 0 -12 t0 -12" fill="none" stroke="{LINE}" stroke-width="3" stroke-linecap="round"/>' for i in range(3))
    + bowl(80, 46, 58, '#E9C88A')
    + ''.join(f'<path d="M{44 + i * 10} 44 q4 4 8 0 t8 0" fill="none" stroke="#FFF4D6" stroke-width="2.4" stroke-linecap="round"/>' for i in range(6))
    + f'<rect x="58" y="40" width="12" height="5" rx="2.5" fill="#9C5A3C"/><rect x="92" y="47" width="12" height="5" rx="2.5" fill="#9C5A3C"/>'
    f'<path d="M76 50 l8 -3 M44 49 l7 2 M108 41 l8 2" stroke="#5F9C5E" stroke-width="3" stroke-linecap="round"/>'
    f'<g transform="rotate(-18 128 30)"><rect x="98" y="26" width="60" height="4" rx="2" fill="#B07A4A"/><rect x="98" y="33" width="60" height="4" rx="2" fill="#B07A4A"/></g>')

# 09. the soup in summer too, and an energy drink can all year
svg('s09-drink.svg',
    bowl(46, 52, 34, '#C8472B')
    + ''.join(f'<path d="M{38 + i * 14} 42 q-4 -5 0 -10 t0 -10" fill="none" stroke="{LINE}" stroke-width="2.5" stroke-linecap="round"/>' for i in range(2))
    + f'<rect x="100" y="14" width="38" height="78" rx="7" fill="{RED}"/>'
    f'<rect x="100" y="14" width="38" height="9" rx="4" fill="#9AA3B2"/><rect x="100" y="83" width="38" height="9" rx="4" fill="#9AA3B2"/>'
    f'<path d="M123 30 L108 56 H118 L114 76 L130 48 H120Z" fill="{YELLOW}"/>')

# 10. Han River park pool: water, ladder and a swim ring
svg('s10-pool.svg',
    sun(24, 18, 8)
    + f'<rect x="10" y="46" width="140" height="48" rx="7" fill="{SKY}"/>'
    + ''.join(f'<path d="M{18 + i * 28} {60 + (i % 2) * 14} q7 -5 14 0 t14 0" fill="none" stroke="{WHITE}" stroke-width="2.5" stroke-linecap="round"/>' for i in range(4))
    + f'<circle cx="60" cy="62" r="13" fill="none" stroke="{RED}" stroke-width="8"/>'
    f'<circle cx="60" cy="62" r="13" fill="none" stroke="{WHITE}" stroke-width="8" stroke-dasharray="10.2 10.2"/>'
    f'<path d="M118 24 V62 M134 24 V62" stroke="#9AA3B2" stroke-width="3.5" stroke-linecap="round"/>'
    f'<path d="M118 24 Q118 16 112 16 M134 24 Q134 16 128 16" fill="none" stroke="#9AA3B2" stroke-width="3.5" stroke-linecap="round"/>'
    + ''.join(f'<path d="M118 {34 + i * 10} H134" stroke="#9AA3B2" stroke-width="3"/>' for i in range(3)))

# 11. Kirirom: a tent between pine trees, wind blowing the heat away
svg('s11-camp.svg',
    ''.join(f'<path d="M{50 + i * 8} {12 + i * 9} h{30 - i * 4} q8 0 8 -6 q0 -5 -5 -5" fill="none" stroke="{LINE}" stroke-width="2.5" stroke-linecap="round"/>' for i in range(2))
    + pine(22, 92, 58) + pine(140, 92, 64) + pine(118, 92, 40)
    + f'<path d="M44 92 L78 40 L112 92Z" fill="{ORANGE}"/>'
    f'<path d="M78 56 L68 92 H88Z" fill="#B85A12"/>'
    f'<rect x="8" y="90" width="144" height="5" rx="2.5" fill="#9BC08A"/>')

# 12. closing: two ways to fan away the heat, one feeling
svg('s12-fans.svg',
    f'<rect x="38" y="58" width="6" height="36" rx="3" fill="#B07A4A"/>'
    f'<circle cx="41" cy="38" r="26" fill="{YELLOW}"/>'
    + ''.join(f'<path d="M41 62 L{41 + 24 * c:.1f} {38 - 24 * s:.1f}" stroke="#D99E00" stroke-width="1.6"/>'
              for c, s in [(-.9, .4), (-.5, .85), (0, 1), (.5, .85), (.9, .4)])
    + fan(120, 86, 40, 30)
    + f'<circle cx="120" cy="86" r="3.5" fill="{NAVY}"/>'
    f'<path d="M80 80 C80 74 72 72 70 78 C68 72 60 74 60 80 C60 86 70 92 70 92 C70 92 80 86 80 80Z" fill="{RED}"/>')

print('drawn:', sorted(f for f in os.listdir(OUT) if f.endswith('.svg')))
