# -*- coding: utf-8 -*-
"""Flat 2D object drawings for the SQL injection review unit. Hand-authored SVG."""
import io
import os

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'img')
NAVY, INK, WHITE, LINE = '#1C2A4A', '#23262D', '#FFFFFF', '#C9CED8'
GREEN, YELLOW, RED, BLUE, ORANGE = '#00A84D', '#F5B700', '#D7372B', '#0052A4', '#EF7C1C'
F = 'font-family="Consolas, Menlo, monospace" font-weight="700"'


def svg(name, body, vb='0 0 160 100'):
    s = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}">{body}</svg>\n'
    io.open(os.path.join(OUT, name), 'w', encoding='utf-8', newline='\n').write(s)


def bars(x, y, n, w, c=LINE):
    return ''.join(f'<rect x="{x}" y="{y + i * 9}" width="{w - (i % 2) * 10}" height="4" rx="2" fill="{c}"/>' for i in range(n))


os.makedirs(OUT, exist_ok=True)

svg('c1-glue.svg',
    f'<rect x="8" y="30" width="62" height="40" rx="6" fill="{NAVY}"/>' + bars(16, 41, 3, 44, '#8FA3C8') +
    f'<circle cx="80" cy="50" r="11" fill="{RED}"/><rect x="74" y="48" width="12" height="4" fill="{WHITE}"/><rect x="78" y="44" width="4" height="12" fill="{WHITE}"/>'
    f'<rect x="90" y="30" width="62" height="40" rx="6" fill="{WHITE}" stroke="{RED}" stroke-width="2.5"/>' + bars(98, 41, 3, 44, '#F2B8B2'))

svg('c2-quote.svg',
    f'<rect x="12" y="34" width="136" height="32" rx="6" fill="{WHITE}" stroke="{LINE}" stroke-width="2.5"/>'
    + bars(20, 43, 2, 46, LINE) + bars(96, 43, 2, 46, '#F2B8B2') +
    f'<path d="M80 14 C92 14 92 30 82 40 L76 38 C82 30 80 26 74 26 C68 26 66 14 80 14Z" fill="{RED}"/>'
    f'<rect x="78" y="44" width="4" height="40" fill="{RED}"/>')

svg('c3-leak.svg',
    f'<ellipse cx="62" cy="20" rx="34" ry="10" fill="#4A5A80"/><rect x="28" y="20" width="68" height="56" fill="{NAVY}"/>'
    f'<ellipse cx="62" cy="76" rx="34" ry="10" fill="{NAVY}"/><ellipse cx="62" cy="20" rx="34" ry="10" fill="#4A5A80"/>'
    f'<path d="M28 40 Q62 50 96 40" fill="none" stroke="#4A5A80" stroke-width="2"/><path d="M28 58 Q62 68 96 58" fill="none" stroke="#4A5A80" stroke-width="2"/>'
    f'<rect x="104" y="30" width="44" height="9" rx="3" fill="{YELLOW}" transform="rotate(12 104 30)"/>'
    f'<rect x="108" y="50" width="40" height="9" rx="3" fill="{YELLOW}" transform="rotate(18 108 50)"/>'
    f'<rect x="104" y="70" width="36" height="9" rx="3" fill="{YELLOW}" transform="rotate(26 104 70)"/>')

svg('c4-door.svg',
    f'<rect x="50" y="8" width="60" height="88" fill="{LINE}"/><rect x="54" y="12" width="52" height="84" fill="#EEF0F4"/>'
    f'<path d="M54 12 L88 20 L88 100 L54 96Z" fill="{ORANGE}"/><circle cx="82" cy="58" r="3" fill="{INK}"/>'
    f'<rect x="114" y="52" width="16" height="14" rx="2" fill="none" stroke="{RED}" stroke-width="3"/>'
    f'<path d="M117 52 V44 A5 5 0 0 1 127 44" fill="none" stroke="{RED}" stroke-width="3"/>')

svg('c5-plus.svg',
    f'<rect x="10" y="24" width="96" height="52" rx="6" fill="{WHITE}" stroke="{LINE}" stroke-width="2.5"/>' + bars(18, 34, 4, 40) +
    f'<circle cx="80" cy="50" r="10" fill="{RED}"/><rect x="74" y="48" width="12" height="4" fill="{WHITE}"/><rect x="78" y="44" width="4" height="12" fill="{WHITE}"/>'
    f'<circle cx="80" cy="50" r="24" fill="none" stroke="{NAVY}" stroke-width="5"/><rect x="98" y="66" width="34" height="10" rx="4" fill="{NAVY}" transform="rotate(40 98 66)"/>')

svg('c6-trace.svg',
    f'<rect x="8" y="26" width="46" height="48" rx="5" fill="{WHITE}" stroke="{LINE}" stroke-width="2.5"/>'
    f'<rect x="14" y="36" width="34" height="9" rx="2" fill="#EEF0F4" stroke="{LINE}"/><rect x="14" y="54" width="22" height="9" rx="3" fill="{BLUE}"/>'
    f'<path d="M58 50 H104" stroke="#996CAC" stroke-width="3" stroke-dasharray="5 5"/><path d="M104 42 L114 50 L104 58Z" fill="#996CAC"/>'
    f'<rect x="116" y="34" width="38" height="32" rx="5" fill="{NAVY}"/><text x="135" y="55" {F} font-size="13" fill="{WHITE}" text-anchor="middle">var</text>')

svg('c7-bind.svg',
    f'<rect x="8" y="22" width="88" height="56" rx="6" fill="{NAVY}"/>' + bars(16, 32, 2, 44, '#8FA3C8') +
    f'<rect x="16" y="54" width="30" height="16" rx="3" fill="{GREEN}"/><text x="31" y="67" {F} font-size="14" fill="{WHITE}" text-anchor="middle">?</text>'
    f'<path d="M100 50 H112" stroke="{LINE}" stroke-width="2.5"/>'
    f'<path d="M114 36 H148 V64 H114 L104 50Z" fill="{WHITE}" stroke="{GREEN}" stroke-width="2.5"/><circle cx="114" cy="50" r="3" fill="{GREEN}"/>' + bars(122, 44, 2, 20, '#A8DCBE'))

svg('c8-list.svg',
    f'<rect x="44" y="6" width="72" height="88" rx="6" fill="{WHITE}" stroke="{LINE}" stroke-width="2.5"/>'
    + ''.join(f'<rect x="54" y="{20 + i * 24}" width="12" height="12" rx="2" fill="{GREEN}"/><path d="M57 {26 + i * 24} l3 3 l5 -6" fill="none" stroke="{WHITE}" stroke-width="2"/>'
              f'<rect x="72" y="{24 + i * 24}" width="34" height="5" rx="2.5" fill="{LINE}"/>' for i in range(3)))

svg('c9-lock.svg',
    f'<path d="M62 44 V30 A18 18 0 0 1 98 30 V44" fill="none" stroke="{NAVY}" stroke-width="7"/>'
    f'<rect x="48" y="44" width="64" height="48" rx="7" fill="{ORANGE}"/>'
    f'<circle cx="80" cy="62" r="7" fill="{WHITE}"/><path d="M68 84 A12 10 0 0 1 92 84Z" fill="{WHITE}"/>')

svg('c10-comment.svg',
    f'<path d="M22 12 H138 A12 12 0 0 1 150 24 V62 A12 12 0 0 1 138 74 H60 L40 92 L44 74 H22 A12 12 0 0 1 10 62 V24 A12 12 0 0 1 22 12Z" fill="{WHITE}" stroke="{LINE}" stroke-width="2.5"/>'
    f'<path d="M38 24 L54 52 H22Z" fill="{YELLOW}"/><rect x="36.5" y="32" width="3" height="11" fill="{INK}"/><rect x="36.5" y="46" width="3" height="3" fill="{INK}"/>'
    f'<rect x="64" y="28" width="64" height="6" rx="3" fill="{INK}"/><rect x="64" y="42" width="52" height="6" rx="3" fill="{LINE}"/><rect x="64" y="56" width="58" height="6" rx="3" fill="{LINE}"/>')
