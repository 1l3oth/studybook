# -*- coding: utf-8 -*-
"""Flat 2D object drawings for the dating words unit. Replaces the older AI pictures
(Rex, 2026-11-05: "redraw everything, from now we adopt the new UI").
Hand-authored SVG, no image generation. Run: python korean-dating-words/draw.py"""
import io
import os

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'img')
NAVY, INK, WHITE, LINE = '#1C2A4A', '#23262D', '#FFFFFF', '#C9CED8'
GREEN, YELLOW, RED, BLUE, SKY, ORANGE, PINK = '#00A84D', '#F5B700', '#D7372B', '#0052A4', '#00A5DE', '#EF7C1C', '#F28CA6'
KFONT = 'Malgun Gothic, Apple SD Gothic Neo, Noto Sans KR, sans-serif'


def svg(name, body, vb='0 0 160 100'):
    s = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}">{body}</svg>\n'
    io.open(os.path.join(OUT, name), 'w', encoding='utf-8', newline='\n').write(s)


def text(x, y, t, size=11, fill=INK, weight=700):
    return (f'<text x="{x}" y="{y}" font-family="{KFONT}" font-size="{size}" font-weight="{weight}" '
            f'fill="{fill}" text-anchor="middle">{t}</text>')


def heart(cx, cy, k=1.0, fill=RED):
    return (f'<path transform="translate({cx} {cy}) scale({k})" d="M0 6 C-10 -1 -9 -10 -4 -10 C-1.5 -10 0 -8 0 -6 '
            f'C0 -8 1.5 -10 4 -10 C9 -10 10 -1 0 6Z" fill="{fill}"/>')


def cup(x, y, fill):
    return (f'<path d="M{x} {y} H{x + 28} L{x + 25} {y + 34} H{x + 3}Z" fill="{fill}"/>'
            f'<rect x="{x - 2}" y="{y - 6}" width="32" height="7" rx="3" fill="{WHITE}" stroke="{LINE}" stroke-width="1.5"/>'
            f'<rect x="{x + 2}" y="{y + 12}" width="24" height="10" fill="#E9D8BC"/>'
            f'<path d="M{x + 20} {y - 6} L{x + 26} {y - 20}" stroke="{RED}" stroke-width="3" stroke-linecap="round"/>')


os.makedirs(OUT, exist_ok=True)

# 01. blind dates (소개팅): two coffees on a cafe table
svg('d01-sogaeting.svg',
    f'<rect x="14" y="76" width="132" height="7" rx="3.5" fill="#B07A4A"/>'
    f'<rect x="76" y="83" width="8" height="14" fill="#8E6038"/>'
    + cup(40, 40, '#7A4E2D') + cup(92, 40, '#C98B4F')
    + heart(80, 26, 1.1, PINK))

# 02. a date with someone a senior introduced: two tickets
svg('d02-date.svg',
    ''.join(f'<g transform="rotate({r} 80 50) translate({dx} {dy})">'
            f'<path d="M30 30 H130 V44 A6 6 0 0 0 130 56 V70 H30 V56 A6 6 0 0 0 30 44Z" fill="{c}"/>'
            f'<path d="M104 32 V68" stroke="{WHITE}" stroke-width="2" stroke-dasharray="4 4"/>'
            f'<rect x="40" y="40" width="50" height="5" rx="2.5" fill="{WHITE}"/><rect x="40" y="52" width="34" height="5" rx="2.5" fill="{WHITE}" opacity=".7"/>'
            f'</g>' for r, dx, dy, c in [(-10, -4, -6, BLUE), (8, 4, 8, ORANGE)])
    + heart(118, 64, .9, WHITE))

# 03. the talking stage (썸): a phone, chat bubbles, a half-filled heart
svg('d03-sseom.svg',
    f'<rect x="20" y="6" width="50" height="88" rx="9" fill="{NAVY}"/>'
    f'<rect x="24" y="15" width="42" height="70" rx="3" fill="{WHITE}"/>'
    f'<rect x="28" y="22" width="26" height="10" rx="5" fill="#EEF0F4"/><rect x="36" y="38" width="26" height="10" rx="5" fill="{YELLOW}"/>'
    f'<rect x="28" y="54" width="20" height="10" rx="5" fill="#EEF0F4"/><rect x="40" y="70" width="22" height="10" rx="5" fill="{YELLOW}"/>'
    f'<defs><clipPath id="half"><rect x="84" y="20" width="36" height="70"/></clipPath></defs>'
    + heart(118, 52, 3.2, WHITE).replace('/>', f' stroke="{PINK}" stroke-width=".9"/>')
    + f'<g clip-path="url(#half)">{heart(118, 52, 3.2, PINK)}</g>'
    + text(118, 92, '?', 14, NAVY, 800))

# 04. aegyo: a sticker-style cute face with a heart and sparkle
svg('d04-aegyo.svg',
    f'<circle cx="72" cy="52" r="34" fill="#FFD45C"/>'
    f'<path d="M56 46 q5 -6 10 0 M78 46 q5 -6 10 0" fill="none" stroke="{INK}" stroke-width="3" stroke-linecap="round"/>'
    f'<ellipse cx="54" cy="60" rx="7" ry="4.5" fill="{PINK}"/><ellipse cx="90" cy="60" rx="7" ry="4.5" fill="{PINK}"/>'
    f'<path d="M64 64 q4 6 8 0 q4 6 8 0" fill="none" stroke="{INK}" stroke-width="2.6" stroke-linecap="round"/>'
    + heart(126, 30, 1.4, PINK) + heart(138, 64, .9, RED)
    + f'<path d="M120 80 l3 -7 l3 7 l7 3 l-7 3 l-3 7 l-3 -7 l-7 -3Z" fill="{YELLOW}"/>')

# 05. I wanted to confess but was too nervous: a love letter and sweat drops
svg('d05-gobaek.svg',
    f'<rect x="30" y="28" width="86" height="58" rx="5" fill="{WHITE}" stroke="{LINE}" stroke-width="2.5"/>'
    f'<path d="M30 32 L73 62 L116 32" fill="none" stroke="{LINE}" stroke-width="2.5"/>'
    + heart(73, 62, 1.3)
    + ''.join(f'<path transform="translate({x} {y}) scale({k})" d="M0 -8 Q6 0 6 3 A6 6 0 0 1 -6 3 Q-6 0 0 -8Z" fill="{SKY}"/>'
              for x, y, k in [(132, 30, .9), (144, 48, .7), (128, 60, .6)])
    + f'<path d="M20 20 l6 5 M14 34 l8 1" stroke="{LINE}" stroke-width="2.5" stroke-linecap="round"/>')

# 06. confessed yesterday, dating from today: a calendar with day 1 ringed
svg('d06-sagwida.svg',
    f'<rect x="38" y="12" width="84" height="80" rx="8" fill="{WHITE}" stroke="{LINE}" stroke-width="2"/>'
    f'<path d="M38 20 A8 8 0 0 1 46 12 H114 A8 8 0 0 1 122 20 V32 H38Z" fill="{PINK}"/>'
    f'<rect x="56" y="6" width="6" height="14" rx="3" fill="#C9637D"/><rect x="98" y="6" width="6" height="14" rx="3" fill="#C9637D"/>'
    + ''.join(f'<rect x="{48 + i * 23}" y="{44 + j * 22}" width="17" height="16" rx="4" fill="#EEF0F4"/>' for i in range(3) for j in range(2) if (i, j) != (1, 0))
    + f'<circle cx="80" cy="52" r="12" fill="none" stroke="{RED}" stroke-width="3"/>' + text(80, 57, '1', 13, RED, 800))

# 07. our hundredth day: a gift box tagged 100
svg('d07-100days.svg',
    f'<rect x="40" y="44" width="70" height="48" rx="4" fill="{RED}"/>'
    f'<rect x="34" y="34" width="82" height="14" rx="3" fill="#E65A4E"/>'
    f'<rect x="69" y="34" width="12" height="58" fill="{YELLOW}"/>'
    f'<path d="M75 34 Q58 14 52 26 Q50 34 75 34 Q92 14 98 26 Q100 34 75 34Z" fill="{YELLOW}"/>'
    f'<path d="M116 52 L128 46 H152 V70 H128Z" fill="{WHITE}" stroke="{LINE}" stroke-width="2"/>'
    + text(139, 63, '100', 10, RED, 800) + f'<path d="M110 54 L118 56" stroke="{LINE}" stroke-width="2"/>')

# 08. together a long time, but in the end we broke up: a broken heart
svg('d08-breakup.svg',
    f'<path d="M78 30 C70 14 40 12 36 34 C32 54 56 70 74 84 L70 66 L80 54 L70 42Z" fill="{RED}"/>'
    f'<path d="M88 30 C96 14 126 12 130 34 C134 54 110 70 92 84 L96 66 L86 54 L96 42Z" fill="#E86A5E"/>'
    f'<path transform="translate(150 70) scale(.7)" d="M0 -8 Q6 0 6 3 A6 6 0 0 1 -6 3 Q-6 0 0 -8Z" fill="{SKY}"/>')

print('drawn:', sorted(f for f in os.listdir(OUT) if f.startswith('d')))
