# -*- coding: utf-8 -*-
"""Flat 2D drawings for the emotion words unit: one face per feeling, plus one object from the
book's example sentence. Rex, 2026-11-05: "redraw everything, from now we adopt the new UI".
Hand-authored SVG, no image generation. Run: python korean-emotion-words/draw.py"""
import io
import os

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'img')
NAVY, INK, WHITE, LINE = '#1C2A4A', '#23262D', '#FFFFFF', '#C9CED8'
GREEN, YELLOW, RED, BLUE, SKY, ORANGE, PINK = '#00A84D', '#F5B700', '#D7372B', '#0052A4', '#00A5DE', '#EF7C1C', '#F28CA6'
FACE, FACE_HOT, FACE_BLUE = '#FFD45C', '#F4866B', '#C9D8EA'
KFONT = 'Malgun Gothic, Apple SD Gothic Neo, Noto Sans KR, sans-serif'
CX, CY, R = 56, 52, 34


def svg(name, body, vb='0 0 160 100'):
    s = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}">{body}</svg>\n'
    io.open(os.path.join(OUT, name), 'w', encoding='utf-8', newline='\n').write(s)


def text(x, y, t, size=11, fill=INK, weight=700):
    return (f'<text x="{x}" y="{y}" font-family="{KFONT}" font-size="{size}" font-weight="{weight}" '
            f'fill="{fill}" text-anchor="middle">{t}</text>')


def heart(cx, cy, k=1.0, fill=RED):
    return (f'<path transform="translate({cx} {cy}) scale({k})" d="M0 6 C-10 -1 -9 -10 -4 -10 C-1.5 -10 0 -8 0 -6 '
            f'C0 -8 1.5 -10 4 -10 C9 -10 10 -1 0 6Z" fill="{fill}"/>')


def drop(x, y, k=1.0, fill=SKY):
    return f'<path transform="translate({x} {y}) scale({k})" d="M0 -8 Q6 0 6 3 A6 6 0 0 1 -6 3 Q-6 0 0 -8Z" fill="{fill}"/>'


S = f'fill="none" stroke="{INK}" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"'
EYES = {
    'dot': lambda: f'<circle cx="{CX - 12}" cy="{CY - 6}" r="3.6" fill="{INK}"/><circle cx="{CX + 12}" cy="{CY - 6}" r="3.6" fill="{INK}"/>',
    'happy': lambda: f'<path d="M{CX - 18} {CY - 4} q6 -8 12 0 M{CX + 6} {CY - 4} q6 -8 12 0" {S}/>',
    'closed': lambda: f'<path d="M{CX - 18} {CY - 6} q6 6 12 0 M{CX + 6} {CY - 6} q6 6 12 0" {S}/>',
    'wide': lambda: (f'<circle cx="{CX - 12}" cy="{CY - 7}" r="6.5" fill="{WHITE}" stroke="{INK}" stroke-width="2.4"/>'
                     f'<circle cx="{CX + 12}" cy="{CY - 7}" r="6.5" fill="{WHITE}" stroke="{INK}" stroke-width="2.4"/>'
                     f'<circle cx="{CX - 12}" cy="{CY - 7}" r="2.6" fill="{INK}"/><circle cx="{CX + 12}" cy="{CY - 7}" r="2.6" fill="{INK}"/>'),
    'half': lambda: (f'<path d="M{CX - 18} {CY - 6} h12 M{CX + 6} {CY - 6} h12" {S}/>'
                     f'<circle cx="{CX - 12}" cy="{CY - 3.5}" r="2.6" fill="{INK}"/><circle cx="{CX + 12}" cy="{CY - 3.5}" r="2.6" fill="{INK}"/>'),
    'side': lambda: (f'<circle cx="{CX - 12}" cy="{CY - 6}" r="5" fill="{WHITE}"/><circle cx="{CX + 12}" cy="{CY - 6}" r="5" fill="{WHITE}"/>'
                     f'<circle cx="{CX - 9}" cy="{CY - 6}" r="2.6" fill="{INK}"/><circle cx="{CX + 15}" cy="{CY - 6}" r="2.6" fill="{INK}"/>'),
    'down': lambda: f'<circle cx="{CX - 12}" cy="{CY - 3}" r="3" fill="{INK}"/><circle cx="{CX + 12}" cy="{CY - 3}" r="3" fill="{INK}"/>',
    'up': lambda: f'<circle cx="{CX - 10}" cy="{CY - 10}" r="3.4" fill="{INK}"/><circle cx="{CX + 14}" cy="{CY - 10}" r="3.4" fill="{INK}"/>',
    'heart': lambda: heart(CX - 12, CY - 5, .75) + heart(CX + 12, CY - 5, .75),
    'squeeze': lambda: f'<path d="M{CX - 18} {CY - 10} l9 4 l-9 4 M{CX + 18} {CY - 10} l-9 4 l9 4" {S}/>',
}
BROWS = {
    None: '',
    'worried': f'<path d="M{CX - 19} {CY - 15} l10 -5 M{CX + 19} {CY - 15} l-10 -5" {S}/>',
    'sad': f'<path d="M{CX - 20} {CY - 12} l11 -7 M{CX + 20} {CY - 12} l-11 -7" {S}/>',
    'angry': f'<path d="M{CX - 19} {CY - 19} l12 6 M{CX + 19} {CY - 19} l-12 6" {S}/>',
    'raised': f'<path d="M{CX - 19} {CY - 20} q6 -5 12 0 M{CX + 7} {CY - 20} q6 -5 12 0" {S}/>',
}
MOUTH = {
    'smile': f'<path d="M{CX - 11} {CY + 9} q11 11 22 0" {S}/>',
    'grin': f'<path d="M{CX - 14} {CY + 7} q14 18 28 0Z" fill="{INK}"/><path d="M{CX - 8} {CY + 13} q8 5 16 0" fill="none" stroke="{RED}" stroke-width="3" stroke-linecap="round"/>',
    'soft': f'<path d="M{CX - 7} {CY + 11} q7 5 14 0" {S}/>',
    'flat': f'<path d="M{CX - 9} {CY + 12} h18" {S}/>',
    'frown': f'<path d="M{CX - 11} {CY + 16} q11 -10 22 0" {S}/>',
    'wavy': f'<path d="M{CX - 12} {CY + 13} q3 -4 6 0 t6 0 t6 0 t6 0" {S}/>',
    'o': f'<ellipse cx="{CX}" cy="{CY + 13}" rx="5.5" ry="7" fill="{INK}"/>',
    'yawn': f'<ellipse cx="{CX}" cy="{CY + 14}" rx="9" ry="6" fill="{INK}"/>',
    'pout': f'<path d="M{CX - 5} {CY + 10} q5 -4 6 1 q1 5 -6 6" {S}/>',
    'grit': f'<rect x="{CX - 12}" y="{CY + 8}" width="24" height="9" rx="3" fill="{WHITE}" stroke="{INK}" stroke-width="2.6"/><path d="M{CX - 4} {CY + 8} v9 M{CX + 4} {CY + 8} v9" stroke="{INK}" stroke-width="1.8"/>',
}


def face(eyes, mouth, brows=None, fill=FACE, blush=False, extra=''):
    b = (f'<ellipse cx="{CX - 20}" cy="{CY + 6}" rx="6" ry="4" fill="{PINK}"/>'
         f'<ellipse cx="{CX + 20}" cy="{CY + 6}" rx="6" ry="4" fill="{PINK}"/>') if blush else ''
    return f'<circle cx="{CX}" cy="{CY}" r="{R}" fill="{fill}"/>' + b + EYES[eyes]() + BROWS[brows] + MOUTH[mouth] + extra


def house(x, y, k=1.0, fill=WHITE):
    return (f'<g transform="translate({x} {y}) scale({k})"><path d="M-18 4 L0 -12 L18 4 V24 H-18Z" fill="{fill}" stroke="{LINE}" stroke-width="2.4" stroke-linejoin="round"/>'
            f'<path d="M-22 6 L0 -15 L22 6" fill="none" stroke="{ORANGE}" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>'
            f'<rect x="-5" y="10" width="10" height="14" fill="{NAVY}"/></g>')


def bubble(x, y, w, h):
    return (f'<path d="M{x} {y} h{w} a6 6 0 0 1 6 6 v{h - 12} a6 6 0 0 1 -6 6 h-{w - 14} l-10 8 l2 -8 h-6 a6 6 0 0 1 -6 -6 v-{h - 12} a6 6 0 0 1 6 -6Z" '
            f'fill="{WHITE}" stroke="{LINE}" stroke-width="2"/>')


def paper(x, y, w=30, h=40, lines=4):
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="3" fill="{WHITE}" stroke="{LINE}" stroke-width="2"/>'
            + ''.join(f'<rect x="{x + 6}" y="{y + 8 + i * 8}" width="{w - 12 - (i % 2) * 6}" height="3.5" rx="1.75" fill="{LINE}"/>' for i in range(lines)))


SWEAT = drop(CX + 30, CY - 22, .8)
TEARS = drop(CX - 13, CY + 6, .7) + drop(CX + 13, CY + 6, .7)
P = 124  # x centre of the object on the right

os.makedirs(OUT, exist_ok=True)

E = {
    # positive
    'e04': face('happy', 'grin', blush=True) + ''.join(
        f'<path d="M{x} {y} l3 -7 l3 7 l7 3 l-7 3 l-3 7 l-3 -7 l-7 -3Z" fill="{YELLOW}"/>' for x, y in [(116, 26), (136, 56), (112, 72)]),
    'e12': face('heart', 'smile', blush=True) + f'<circle cx="{P - 8}" cy="56" r="14" fill="none" stroke="{YELLOW}" stroke-width="5"/>'
           f'<circle cx="{P + 10}" cy="56" r="14" fill="none" stroke="#D99E00" stroke-width="5"/>' + heart(P + 2, 28, 1),
    'e13': face('closed', 'smile') + f'<path d="M{P - 6} 18 h18 a6 6 0 0 1 6 6 v6" fill="none" stroke="{LINE}" stroke-width="4" stroke-linecap="round"/>'
           f'<path d="M{P + 8} 32 h20 l-4 8 h-12Z" fill="#9AA3B2"/>' + ''.join(drop(P + 6 + dx, 52 + dy, .55) for dx, dy in [(4, 0), (14, 6), (24, 0), (8, 18), (20, 20)]),
    'e16': face('happy', 'grin') + f'<path d="M{P} 74 V44" stroke="{LINE}" stroke-width="2"/>'
           f'<ellipse cx="{P}" cy="30" rx="14" ry="17" fill="{RED}"/><path d="M{P - 3} 47 h6 l-3 -4Z" fill="{RED}"/>'
           f'<path d="M{P + 16} 80 V54" stroke="{LINE}" stroke-width="2"/><ellipse cx="{P + 16}" cy="44" rx="10" ry="12" fill="{SKY}"/>',
    'e22': face('happy', 'smile', blush=True) + text(P - 6, 44, '♪', 26, BLUE, 400) + text(P + 16, 70, '♫', 24, GREEN, 400),
    'e25': face('closed', 'soft') + paper(P - 16, 26, 32, 44, 3) + f'<circle cx="{P + 14}" cy="66" r="11" fill="{GREEN}"/>'
           f'<path d="M{P + 9} 66 l4 4 l7 -8" fill="none" stroke="{WHITE}" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>',
    'e26': face('happy', 'grin', blush=True) + heart(P + 2, 50, 2.4),
    # reaction
    'e02': face('up', 'soft') + bubble(P - 22, 14, 44, 38).replace('h-30', 'h-30') + house(P + 2, 32, .7),
    'e03': face('dot', 'flat') + text(CX + 28, CY - 24, '?', 18, BLUE, 800)
           + f'<path d="M{P - 14} 22 h28 v12 a14 14 0 0 1 -28 0Z" fill="{YELLOW}"/><rect x="{P - 3}" y="47" width="6" height="12" fill="#D99E00"/>'
           f'<rect x="{P - 12}" y="59" width="24" height="7" rx="2" fill="#D99E00"/>',
    'e06': face('wide', 'o', 'raised') + bubble(P - 22, 22, 44, 30) + text(P, 42, '한국말', 10, NAVY)
           + f'<path d="M{CX - 34} {CY - 32} l-6 -6 M{CX + 34} {CY - 32} l6 -6 M{CX} {CY - 42} v-7" stroke="{INK}" stroke-width="2.5" stroke-linecap="round"/>',
    # negative
    'e01': face('dot', 'wavy', 'worried', extra=SWEAT) + house(P, 54, .9) + text(P + 18, 34, '?', 16, RED, 800),
    'e08': face('half', 'flat', 'worried') + f'<rect x="{P - 22}" y="26" width="44" height="50" fill="#EEF0F4" stroke="{NAVY}" stroke-width="4"/>'
           f'<rect x="{P - 12}" y="36" width="24" height="18" fill="none" stroke="{LINE}" stroke-width="2" stroke-dasharray="4 3"/>',
    'e09': face('wide', 'wavy', 'worried', fill='#FFE08A', extra=SWEAT)
           + f'<path d="M{P - 16} 70 V40 a16 16 0 0 1 32 0 V70 l-6 -5 l-5 5 l-5 -5 l-5 5 l-5 -5Z" fill="{WHITE}" stroke="{LINE}" stroke-width="2"/>'
           f'<circle cx="{P - 6}" cy="40" r="3" fill="{INK}"/><circle cx="{P + 6}" cy="40" r="3" fill="{INK}"/><ellipse cx="{P}" cy="52" rx="4" ry="5" fill="{INK}"/>',
    'e10': face('side', 'pout') + bubble(P - 22, 20, 44, 30) + text(P, 40, '한국말', 10, NAVY)
           + f'<path d="M{P + 18} 62 l3 -7 l3 7 l7 3 l-7 3 l-3 7 l-3 -7 l-7 -3Z" fill="{YELLOW}"/>',
    'e11': face('dot', 'wavy', 'worried', extra=SWEAT) + paper(P - 20, 30, 30, 40) + f'<circle cx="{P + 16}" cy="34" r="12" fill="{WHITE}" stroke="{NAVY}" stroke-width="3"/>'
           f'<path d="M{P + 16} 27 v7 l5 3" fill="none" stroke="{NAVY}" stroke-width="2.5" stroke-linecap="round"/>',
    'e14': face('down', 'soft', 'sad') + f'<rect x="{P - 16}" y="40" width="34" height="36" rx="5" fill="{ORANGE}"/>'
           f'<path d="M{P - 6} 40 v-8 h14 v8" fill="none" stroke="#B85A12" stroke-width="3"/><rect x="{P - 16}" y="52" width="34" height="4" fill="#B85A12"/>'
           f'<path d="M{P + 24} 20 q6 4 2 10 M{P + 30} 16 q8 6 4 14" fill="none" stroke="{LINE}" stroke-width="2.5" stroke-linecap="round"/>',
    'e15': face('down', 'frown', 'sad', extra=TEARS) + f'<rect x="{P - 24}" y="26" width="48" height="34" rx="4" fill="{NAVY}"/>'
           f'<rect x="{P - 20}" y="30" width="40" height="26" rx="2" fill="#4A5B80"/>' + drop(P, 44, .9, SKY)
           + f'<path d="M{P - 8} 60 l-6 10 M{P + 8} 60 l6 10" stroke="{NAVY}" stroke-width="3" stroke-linecap="round"/>',
    'e17': face('half', 'flat') + f'<circle cx="{P}" cy="50" r="22" fill="{WHITE}" stroke="{LINE}" stroke-width="3"/>'
           f'<path d="M{P} 36 v14 l9 6" fill="none" stroke="{NAVY}" stroke-width="3" stroke-linecap="round"/>' + text(P + 26, 30, 'z', 12, BLUE, 800),
    'e18': face('down', 'soft', 'sad') + f'<path d="M{P + 10} 16 A16 16 0 1 0 {P + 24} 40 A12 12 0 1 1 {P + 10} 16Z" fill="{YELLOW}"/>'
           f'<rect x="{P - 18}" y="60" width="26" height="6" rx="3" fill="#B07A4A"/><rect x="{P - 16}" y="66" width="4" height="14" fill="#8E6038"/>'
           f'<rect x="{P + 2}" y="66" width="4" height="14" fill="#8E6038"/><rect x="{P - 18}" y="40" width="5" height="22" rx="2" fill="#B07A4A"/>',
    'e19': face('down', 'frown', 'sad', fill=FACE_BLUE) + f'<path d="M{CX - 26} 20 a10 10 0 0 1 14 -10 a13 13 0 0 1 24 2 a9 9 0 0 1 10 12 H{CX - 26}Z" fill="#8A93A6"/>'
           + drop(CX - 14, 30, .5) + drop(CX + 2, 32, .5) + drop(CX + 16, 30, .5)
           + paper(P - 14, 28, 30, 40) + text(P + 1, 62, 'X', 14, RED, 800),
    'e23': face('half', 'yawn') + ''.join(paper(P - 18 + i * 4, 22 + i * 6, 30, 40, 3) for i in range(3)),
    'e24': face('squeeze', 'wavy', blush=True, fill='#FFC864')
           + f'<path d="M{P - 4} 72 q-14 -2 -22 -14 q12 2 20 8Z M{P + 4} 72 q14 -2 22 -14 q-12 2 -20 8Z" fill="{YELLOW}" stroke="#D99E00" stroke-width="1.8" stroke-linejoin="round"/>'
           f'<path d="M{P - 8} 74 C{P - 8} 42 {P + 8} 42 {P + 8} 74Z" fill="{YELLOW}" stroke="#D99E00" stroke-width="1.8" stroke-linejoin="round"/>'
           f'<rect x="{P - 2}" y="44" width="4" height="7" rx="1" fill="#7A5A10"/>'
           f'<rect x="{P - 30}" y="76" width="62" height="4" rx="2" fill="{LINE}"/>',
    'e27': face('dot', 'grit', 'angry', fill=FACE_HOT)
           + f'<path d="M{CX - 34} 14 q-4 -6 0 -10 M{CX + 34} 14 q4 -6 0 -10" fill="none" stroke="{LINE}" stroke-width="3" stroke-linecap="round"/>'
           + bubble(P - 22, 24, 44, 30) + text(P, 44, '거짓말', 10, RED),
}
for k, body in E.items():
    svg(f'{k}.svg', body)
print('drawn:', len(E))
