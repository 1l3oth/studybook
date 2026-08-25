# -*- coding: utf-8 -*-
# Build an RSS 2.0 feed for the studybook, with each study's full text embedded
# (content:encoded) so an AI or feed reader can read the material, not just link to it.
import io, re, html
from email.utils import format_datetime
from datetime import datetime, timezone
from qa_data import TRAPS, DEEP
from vocab_data import VOCAB

BASE = r'F:/secondbrain/wiki/me/korean'
OUT  = r'F:/studybook/feed.xml'
SITE = 'https://1l3oth.github.io/studybook/'
drill = io.open(BASE + '/k-specialist-speech-drill.html', encoding='utf-8').read()
LINES = [{'ko':k,'en':en} for (k,_kk,en) in re.findall(r'ko:"([^"]*)",k:"([^"]*)",en:"([^"]*)"', drill)]

def esc(s): return html.escape(s, quote=False)

# ---- full text content of the Korean summer speech study ----
SECTIONS=[('시작 · Opening',range(0,6)),('옷 · Clothes',range(6,11)),('날씨 · Weather',range(11,19)),
          ('음식 · Food',range(19,24)),('더위 피하기 · Escaping the heat',range(24,29)),('마무리 · Closing',range(29,32))]
c = ['<h2>여름 발표 스튜디오 (Korean Summer Speech)</h2>',
     '<p>A graded Korean speech comparing summer in Korea and Cambodia, with follow-up questions and topic vocabulary. Register: 습니다체. Level: about TOPIK 1 to 2.</p>',
     '<h3>발표 대본 (The speech)</h3>']
for title, rng in SECTIONS:
    ko = ' '.join(LINES[i]['ko'] for i in rng); en = ' '.join(LINES[i]['en'] for i in rng)
    c.append(f'<p><strong>{esc(title)}</strong><br>{esc(ko)}<br><em>{esc(en)}</em></p>')

c.append('<h3>예상 질문 (Q&amp;A)</h3>')
c.append('<p><strong>함정과 빈틈 · Traps</strong></p>')
for (q, qen, a, w) in TRAPS:
    c.append(f'<p>Q. {esc(q)}<br>A. {esc(a)}</p>')
c.append('<p><strong>핵심 질문 · Core</strong></p>')
for (qi, ai) in [(36,37),(38,39),(40,41),(42,43),(44,45),(46,47),(48,49),(50,51),(52,53)]:
    c.append(f'<p>Q. {esc(LINES[qi]["ko"])} ({esc(LINES[qi]["en"])})<br>A. {esc(LINES[ai]["ko"])} ({esc(LINES[ai]["en"])})</p>')
for title, items in DEEP:
    c.append(f'<p><strong>{esc(title)}</strong></p>')
    for (q, qen, a, aen, cf) in items:
        c.append(f'<p>Q. {esc(q)} ({esc(qen)})<br>A. {esc(a)} ({esc(aen)})</p>')

vcount = sum(len(items) for _t, items in VOCAB)
c.append(f'<h3>단어 (Vocabulary, {vcount})</h3>')
for title, items in VOCAB:
    words = '; '.join(f'{ko} = {en}' for (ko, en) in items)
    c.append(f'<p><strong>{esc(title)}</strong>: {esc(words)}</p>')

content_html = '\n'.join(c)
summary = ('A graded Korean speech comparing summer weather in Korea and Cambodia, with 32 speech lines, '
           '29 follow-up questions with model answers, and 89 topic words. Interactive study page with audio.')

# ---- RSS 2.0 ----
pub = format_datetime(datetime(2026, 8, 25, 12, 0, 0, tzinfo=timezone.utc))
items = [{
    'title': '여름 발표 스튜디오 (Korean Summer Speech)',
    'link': SITE + 'korean-summer-speech/',
    'summary': summary,
    'content': content_html,
    'pub': pub,
}]

parts = ['<?xml version="1.0" encoding="UTF-8"?>',
 '<rss version="2.0" xmlns:content="http://purl.org/rss/1.0/modules/content/" xmlns:atom="http://www.w3.org/2005/Atom">',
 '<channel>',
 '<title>다라봇 스터디북 (Studybook)</title>',
 f'<link>{SITE}</link>',
 f'<atom:link href="{SITE}feed.xml" rel="self" type="application/rss+xml"/>',
 '<description>A Korean study notebook. Each item is a self-study unit with its full text (speech, Q&amp;A, vocabulary) so it can be read directly. See it, hear it, say it.</description>',
 '<language>ko</language>',
 f'<lastBuildDate>{pub}</lastBuildDate>']
for it in items:
    parts += ['<item>',
      f'<title>{esc(it["title"])}</title>',
      f'<link>{it["link"]}</link>',
      f'<guid isPermaLink="true">{it["link"]}</guid>',
      f'<pubDate>{it["pub"]}</pubDate>',
      f'<description>{esc(it["summary"])}</description>',
      '<content:encoded><![CDATA[' + it['content'] + ']]></content:encoded>',
      '</item>']
parts += ['</channel>', '</rss>']
io.open(OUT, 'w', encoding='utf-8').write('\n'.join(parts))
print('feed written:', OUT, '| items:', len(items), '| content chars:', len(content_html))
