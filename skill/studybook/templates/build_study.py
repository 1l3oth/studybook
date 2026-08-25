# -*- coding: utf-8 -*-
import io, os, re, base64, html, sys, shutil
LITE = 'lite' in sys.argv   # phone artifact: keep speech-card audio, Q&A becomes text-only
WEB  = 'web' in sys.argv     # github pages: separate audio/img files, tiny HTML (full content)
if WEB: LITE = False
OUTDIR = r'F:/studybook/korean-summer-speech'
if WEB:
    for _sub in ('audio','img'):
        _d=OUTDIR+'/'+_sub
        if os.path.isdir(_d): shutil.rmtree(_d)
        os.makedirs(_d)
def _emit_audio(name, raw):
    if WEB:
        io.open(OUTDIR+'/audio/'+name+'.mp3','wb').write(raw); return 'audio/'+name+'.mp3'
    return 'data:audio/mpeg;base64,'+base64.b64encode(raw).decode()

BASE = r'F:/secondbrain/wiki/me/korean'
IMG  = BASE + '/img'
drill = io.open(BASE + '/k-specialist-speech-drill.html', encoding='utf-8').read()
LINES = [{'ko':k,'k':kk,'en':en} for (k,kk,en) in
         re.findall(r'ko:"([^"]*)",k:"([^"]*)",en:"([^"]*)"', drill)]
CLIPS = re.findall(r'"b":"([A-Za-z0-9+/=]+)"', drill)

def strip_id3(raw):
    if raw[:3]==b'ID3':
        sz=(raw[6]&0x7f)<<21|(raw[7]&0x7f)<<14|(raw[8]&0x7f)<<7|(raw[9]&0x7f)
        foot=10 if (raw[5]&0x10) else 0
        raw=raw[10+sz+foot:]
    if raw[-128:-125]==b'TAG': raw=raw[:-128]
    return raw
def audio_uri(idxs):
    buf=bytearray()
    for i in idxs: buf+=strip_id3(base64.b64decode(CLIPS[i]))
    return _emit_audio('ln'+'_'.join(str(i) for i in idxs), bytes(buf))
def img_uri(name):
    raw=io.open(IMG+'/'+name,'rb').read()
    if WEB:
        io.open(OUTDIR+'/img/'+name,'wb').write(raw); return 'img/'+name
    mime='image/jpeg' if raw[:2]==b'\xff\xd8' else 'image/png'
    return 'data:%s;base64,%s'%(mime, base64.b64encode(raw).decode())
def qa_audio(cid):
    p=IMG+'/qa/'+cid+'.mp3'
    if not os.path.exists(p): return None
    return _emit_audio('qa_'+cid, io.open(p,'rb').read())
def voc_audio(cid):
    p=IMG+'/voc/'+cid+'.mp3'
    if not os.path.exists(p): return None
    return _emit_audio('voc_'+cid, io.open(p,'rb').read())
def esc(s): return html.escape(s, quote=True)
def ko_of(i): return ' '.join(LINES[j]['ko'] for j in i)
def en_of(i): return ' '.join(LINES[j]['en'] for j in i)

# ---------------- CARDS panel ----------------
BEATS = [
  ('Opening','시작','beat01.jpg',[0,3]),
  ('Clothes','옷','beat03.jpg',[7]),
  ('Clothes','옷','beat04.jpg',[8,9]),
  ('Weather','날씨','beat05.jpg',[12,13]),
  ('Weather','날씨','beat06.jpg',[14]),
  ('Weather','날씨','beat07.jpg',[16,17]),
  ('Food','음식','beat08.jpg',[21]),
  ('Food','음식','beat09.jpg',[22]),
  ('Escaping the heat','더위 피하기','beat10.jpg',[25]),
  ('Escaping the heat','더위 피하기','beat11.jpg',[26,28]),
  ('Closing','마무리','beat12.jpg',[30,31]),
]
PART_COLOR={'시작':'#7d7566','옷':'#4f7a6f','날씨':'#5b7fa6','음식':'#c07a3a','더위 피하기':'#b0603f','마무리':'#7d7566'}
def playbtn(au,label='Listen'):
    return (f'<button class="play" data-au="{au}"><svg viewBox="0 0 24 24" width="17" height="17" aria-hidden="true">'
            f'<path d="M8 5v14l11-7z" fill="currentColor"/></svg><span>{label}</span></button>')
cards=[]
for en_part,ko_part,img,idxs in BEATS:
    col=PART_COLOR.get(ko_part,'#7d7566')
    cards.append(f'''
  <article class="card">
    <div class="pic"><img loading="lazy" src="{img_uri(img)}" alt="{esc(en_of(idxs))}"></div>
    <div class="body">
      <div class="chips"><span class="chip part" style="--pc:{col}">{esc(ko_part)} · {esc(en_part)}</span><span class="chip hook">{esc(LINES[idxs[0]]["k"])}</span></div>
      <p class="ko" lang="ko">{esc(ko_of(idxs))}</p>
      <p class="en">{esc(en_of(idxs))}</p>
      {playbtn(audio_uri(idxs))}
    </div>
  </article>''')
SPINE=[('👕','옷','Clothes','Get dressed','#4f7a6f'),('🌦️','날씨','Weather','Check the sky','#5b7fa6'),
       ('🍜','음식','Food','Eat','#c07a3a'),('🏞️','더위 피하기','Escape the heat','Go out','#b0603f')]
spine=''.join(f'''<div class="step" style="--pc:{c}"><span class="emoji">{e}</span><span class="s-ko" lang="ko">{esc(ko)}</span><span class="s-en">{esc(en)}</span><span class="s-day">{esc(day)}</span></div>''' for (e,ko,en,day,c) in SPINE)
roadmap_au=audio_uri([4])

# ---------------- Q&A panel ----------------
CORE=[(36,37),(38,39),(40,41),(42,43),(44,45),(46,47),(48,49),(50,51),(52,53)]
SURV=[32,33,34,35]
from qa_data import TRAPS, DEEP
from vocab_data import VOCAB
def qmini(au):
    return f'<button class="play mini qplay" data-au="{au}"><svg viewBox="0 0 24 24" width="14" height="14" aria-hidden="true"><path d="M8 5v14l11-7z" fill="currentColor"/></svg></button>' if au else ''
def qa_card(q,a,aen,au=None,confirm=False,trap=None,qen=None,qau=None):
    play=playbtn(au) if au else ''
    badge='<span class="confirm">확인 필요</span>' if confirm else ''
    why=f'<p class="why">{esc(trap)}</p>' if trap else ''
    aen_h=f'<p class="aen">{esc(aen)}</p>' if aen else ''
    qen_h=f'<span class="qen">{esc(qen)}</span>' if qen else ''
    cls='qa trap' if trap else 'qa'
    return f'''<article class="{cls}"><div class="qhead"><button class="q" type="button"><span class="qm">Q</span><span class="qtext"><span class="qko" lang="ko">{esc(q)}</span>{qen_h}</span><span class="tw">tap</span></button>{qmini(qau)}</div><div class="a"><p class="ako" lang="ko">{esc(a)}{badge}</p>{aen_h}{why}{play}</div></article>'''
traps_html=''.join(qa_card(q,a,None,au=(None if LITE else qa_audio('t%d'%i)),qen=qen,qau=(None if LITE else qa_audio('qt%d'%i)),trap=w) for i,(q,qen,a,w) in enumerate(TRAPS))
core_html=''.join(qa_card(LINES[qi]['ko'],LINES[ai]['ko'],LINES[ai]['en'],au=(None if LITE else audio_uri([ai])),qen=LINES[qi]['en'],qau=(None if LITE else audio_uri([qi]))) for (qi,ai) in CORE)
surv_html=''.join(f'<div class="surv"><span class="sko" lang="ko">{esc(LINES[i]["ko"])}</span><span class="sen">{esc(LINES[i]["en"])}</span><button class="play mini" data-au="{audio_uri([i])}"><svg viewBox="0 0 24 24" width="14" height="14" aria-hidden="true"><path d="M8 5v14l11-7z" fill="currentColor"/></svg></button></div>' for i in SURV)
deep_html=''; _dj=0
for title,items in DEEP:
    deep_html+=f'<h3 class="grp">{esc(title)}</h3>'
    for (q,qen,a,aen,c) in items:
        deep_html+=qa_card(q,a,aen,au=(None if LITE else qa_audio('d%d'%_dj)),qen=qen,qau=(None if LITE else qa_audio('qd%d'%_dj)),confirm=c); _dj+=1

vocab_html=''; _vj=0
for title, items in VOCAB:
    vocab_html+=f'<h3 class="grp">{esc(title)}</h3><div class="vocgrid">'
    for (ko, en) in items:
        au=voc_audio('v%d'%_vj); _vj+=1
        pb=f'<button class="play mini vplay" data-au="{au}"><svg viewBox="0 0 24 24" width="13" height="13" aria-hidden="true"><path d="M8 5v14l11-7z" fill="currentColor"/></svg></button>' if au else ''
        vocab_html+=f'<div class="voc">{pb}<span class="vko" lang="ko">{esc(ko)}</span><span class="ven">{esc(en)}</span></div>'
    vocab_html+='</div>'

# ---- Full (continuous document) panel: whole speech + all Q&A + all vocab as text ----
SECTIONS=[('시작 · Opening',range(0,6)),('옷 · Clothes',range(6,11)),('날씨 · Weather',range(11,19)),
          ('음식 · Food',range(19,24)),('더위 피하기 · Escaping the heat',range(24,29)),('마무리 · Closing',range(29,32))]
speech_full=''
for title,rng in SECTIONS:
    ko=' '.join(LINES[i]['ko'] for i in rng); en=' '.join(LINES[i]['en'] for i in rng)
    speech_full+=f'<h3 class="fh">{esc(title)}</h3><p class="fko" lang="ko">{esc(ko)}</p><p class="fen">{esc(en)}</p>'
def fqa(q,qen,a,aen):
    ae=f'<p class="fae">{esc(aen)}</p>' if aen else ''
    return f'<div class="fqa"><p class="fq" lang="ko">Q. {esc(q)}</p><p class="fqe">{esc(qen)}</p><p class="fa" lang="ko">A. {esc(a)}</p>{ae}</div>'
qa_full='<h3 class="fh">함정과 빈틈 · Traps</h3>'+''.join(fqa(q,'',a,None) for (q,qen,a,w) in TRAPS)
qa_full+='<h3 class="fh">핵심 질문 · Core</h3>'+''.join(fqa(LINES[qi]['ko'],LINES[qi]['en'],LINES[ai]['ko'],LINES[ai]['en']) for (qi,ai) in CORE)
for title,items in DEEP:
    qa_full+=f'<h3 class="fh">{esc(title)}</h3>'+''.join(fqa(q,qen,a,aen) for (q,qen,a,aen,c) in items)
voc_full=''
for title,items in VOCAB:
    voc_full+=f'<h3 class="fh">{esc(title)}</h3><div class="fvoc">'+''.join(f'<div class="fv"><span class="fvko" lang="ko">{esc(ko)}</span><span class="fven">{esc(en)}</span></div>' for (ko,en) in items)+'</div>'
VCOUNT=sum(len(items) for _,items in VOCAB)

footer_txt=('Pictures generated for study · speech cards have shane_ko audio · Q&amp;A is text here (the full-audio version is your desktop file).' if LITE else 'Pictures generated for study · every line and answer has shane_ko audio.')
home_btn=('<a class="tbtn homebtn" href="../" title="Studybook home"><svg viewBox="0 0 24 24" width="15" height="15" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M3 10.5 12 3l9 7.5"/><path d="M5 9.5V21h14V9.5"/></svg><span>Home</span></a>' if WEB else '')
DOC=f'''<!doctype html>
<html lang="ko"><head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Summer Speech Studio</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Hahmlet:wght@400;500;600;700&family=Gowun+Batang:wght@400;700&family=IBM+Plex+Sans:wght@400;500;600&display=swap">
<style>
:root{{
  --bg:#EFE7D6;--surface:#FBF7EF;--sunken:#F2EADB;--ink:#2C2620;--ink-2:#6B5F50;--ink-3:#948674;
  --line:#E4D9C6;--accent:#C4703A;--on-accent:#fff;--warn:#B0603F;
  --f-ko:'Gowun Batang','Hahmlet',serif;--f-disp:'Hahmlet',serif;--f-ui:'IBM Plex Sans',system-ui,sans-serif;
  --shadow:0 1px 2px rgba(60,46,28,.06),0 8px 24px rgba(60,46,28,.08);
}}
@media (prefers-color-scheme:dark){{:root:not([data-theme="light"]){{
  --bg:#211D18;--surface:#2A241D;--sunken:#241F19;--ink:#F1EADC;--ink-2:#C3B7A3;--ink-3:#8E8271;
  --line:#3A3227;--accent:#E0965F;--on-accent:#241f19;--warn:#E0965F;
  --shadow:0 1px 2px rgba(0,0,0,.3),0 10px 28px rgba(0,0,0,.34);
}}}}
*{{box-sizing:border-box}}html,body{{margin:0}}
body{{background:var(--bg);color:var(--ink);font-family:var(--f-ui);line-height:1.5;-webkit-font-smoothing:antialiased;padding:0 1.1rem 5.5rem}}
.wrap{{max-width:900px;margin:0 auto}}
header{{padding:2rem 0 .7rem;text-align:center}}
.eyebrow{{font-size:.72rem;letter-spacing:.18em;text-transform:uppercase;color:var(--accent);font-weight:600}}
h1{{font-family:var(--f-disp);font-weight:700;font-size:clamp(1.8rem,5vw,2.6rem);margin:.45rem 0 .3rem;letter-spacing:-.01em}}
.sub{{color:var(--ink-2);max-width:46ch;margin:0 auto;font-size:.95rem}}
/* sticky tabs */
.tabs{{position:sticky;top:0;z-index:50;display:flex;gap:.35rem;justify-content:center;flex-wrap:nowrap;overflow-x:auto;scrollbar-width:none;-webkit-overflow-scrolling:touch;padding:.7rem .3rem .8rem;margin:.9rem 0 1.4rem;background:linear-gradient(var(--bg) 72%,transparent)}}
.tabs::-webkit-scrollbar{{display:none}}
.tabs button{{font-family:var(--f-ui);font-size:.92rem;font-weight:600;color:var(--ink-2);background:var(--surface);border:1px solid var(--line);border-radius:999px;padding:.5rem 1.1rem;cursor:pointer;display:flex;gap:.35rem;align-items:baseline;white-space:nowrap;flex:0 0 auto}}
.tabs button .ko{{font-family:var(--f-ko);font-weight:700}}
.tabs button.on{{background:var(--accent);color:var(--on-accent);border-color:transparent}}
.tabs button:focus-visible{{outline:2px solid var(--accent);outline-offset:2px}}
.panel{{display:none}} .panel.on{{display:block}}
/* spine */
.spine-wrap{{background:var(--surface);border:1px solid var(--line);border-radius:18px;padding:1.15rem 1.1rem 1.25rem;box-shadow:var(--shadow);margin:0 0 1.6rem}}
.spine-hd{{display:flex;align-items:baseline;justify-content:space-between;gap:1rem;margin:0 .2rem .9rem}}
.spine-hd h2{{font-family:var(--f-disp);font-size:1.02rem;margin:0;font-weight:600}}
.spine-hd .note{{color:var(--ink-2);font-size:.82rem}}
.spine{{display:grid;grid-template-columns:repeat(4,1fr);gap:.55rem}}
.step{{position:relative;background:var(--sunken);border:1px solid var(--line);border-top:3px solid var(--pc);border-radius:13px;padding:.85rem .6rem;text-align:center;display:flex;flex-direction:column;gap:.15rem}}
.step .emoji{{font-size:1.5rem;line-height:1.1}}
.step .s-ko{{font-family:var(--f-ko);font-weight:700;font-size:1.06rem;color:var(--pc)}}
.step .s-en{{font-size:.74rem;color:var(--ink-2);font-weight:500}}
.step .s-day{{font-size:.7rem;color:var(--ink-3);margin-top:.15rem;font-style:italic}}
.step:not(:last-child)::after{{content:"→";position:absolute;right:-.46rem;top:50%;transform:translateY(-50%);color:var(--ink-3);font-size:.9rem;z-index:2}}
.spine-foot{{display:flex;align-items:center;gap:.7rem;margin:1rem .2rem 0;color:var(--ink-2);font-size:.85rem}}
.method{{display:flex;flex-wrap:wrap;gap:.6rem 1.5rem;justify-content:center;align-items:center;margin:0 0 1.3rem;color:var(--ink-2);font-size:.86rem}}
.method b{{color:var(--ink)}} .method .n{{display:inline-grid;place-items:center;width:1.35rem;height:1.35rem;border-radius:50%;background:var(--accent);color:var(--on-accent);font-size:.72rem;font-weight:700;margin-right:.42rem}}
/* cards */
.cards{{display:flex;flex-direction:column;gap:1.15rem}}
.card{{background:var(--surface);border:1px solid var(--line);border-radius:18px;overflow:hidden;box-shadow:var(--shadow);display:grid;grid-template-columns:minmax(0,38%) 1fr;transition:box-shadow .25s,transform .25s}}
.card.now{{box-shadow:0 0 0 3px var(--accent),var(--shadow);transform:translateY(-2px)}}
.pic{{position:relative;background:var(--sunken)}} .pic img{{display:block;width:100%;height:100%;object-fit:cover;aspect-ratio:4/3}}
.body{{padding:1.15rem 1.25rem 1.2rem;display:flex;flex-direction:column;gap:.5rem;min-width:0}}
.chips{{display:flex;flex-wrap:wrap;gap:.4rem}}
.chip{{font-size:.68rem;font-weight:600;border-radius:999px;padding:.16rem .6rem}}
.chip.part{{color:#fff;background:var(--pc)}}
.chip.hook{{color:var(--ink-2);background:var(--sunken);border:1px solid var(--line);font-family:var(--f-ko);font-weight:700}}
.ko{{font-family:var(--f-ko);font-weight:700;font-size:clamp(1.15rem,2.4vw,1.5rem);line-height:1.55;margin:.1rem 0 0;word-break:keep-all}}
.en{{color:var(--ink-2);font-size:.9rem;margin:0}}
.play{{align-self:flex-start;margin-top:.35rem;display:inline-flex;align-items:center;gap:.45rem;font-family:var(--f-ui);font-size:.85rem;font-weight:600;color:var(--on-accent);background:var(--accent);border:none;border-radius:999px;padding:.5rem .95rem;cursor:pointer}}
.play:hover{{filter:brightness(1.05)}} .play:focus-visible{{outline:2px solid var(--accent);outline-offset:2px}}
.play.playing{{background:var(--warn);animation:plpulse 1s ease-in-out infinite}}
@keyframes plpulse{{0%,100%{{box-shadow:0 0 0 2px color-mix(in srgb,var(--warn) 45%,transparent)}}50%{{box-shadow:0 0 0 8px color-mix(in srgb,var(--warn) 6%,transparent)}}}}
body.hide-ko .ko{{filter:blur(7px);opacity:.55;cursor:pointer;transition:filter .15s,opacity .15s}}
body.hide-ko .ko.reveal{{filter:none;opacity:1}} body.hide-en .en{{display:none}}
/* qa */
.strategy{{background:var(--sunken);border:1px solid var(--line);border-left:3px solid var(--accent);border-radius:12px;padding:.85rem 1rem;margin:0 0 1.4rem;color:var(--ink-2);font-size:.9rem}}
.strategy b{{color:var(--ink)}}
h2.sec{{font-family:var(--f-disp);font-size:1.15rem;margin:2rem 0 .4rem;display:flex;align-items:baseline;gap:.5rem}}
h2.sec .cnt{{font-family:var(--f-ui);font-size:.75rem;color:var(--ink-3);font-weight:500}}
.secnote{{color:var(--ink-2);font-size:.85rem;margin:0 0 1rem}}
h3.grp{{font-size:.78rem;letter-spacing:.06em;text-transform:uppercase;color:var(--accent);font-weight:600;margin:1.5rem 0 .55rem}}
.qa{{background:var(--surface);border:1px solid var(--line);border-radius:14px;box-shadow:var(--shadow);margin:0 0 .7rem;overflow:hidden}}
.qhead{{display:flex;align-items:flex-start}}
.qa .q{{flex:1;min-width:0;text-align:left;background:none;border:none;cursor:pointer;display:flex;align-items:flex-start;gap:.65rem;padding:.95rem 1.05rem;font-family:inherit}}
.qa .qm{{flex:none;width:1.5rem;height:1.5rem;border-radius:50%;background:var(--accent);color:var(--on-accent);font-size:.78rem;font-weight:700;display:grid;place-items:center;margin-top:.05rem}}
.qa.trap .qm{{background:var(--warn)}}
.qa .qtext{{flex:1;min-width:0;display:flex;flex-direction:column;gap:.14rem}}
.qa .qko{{font-family:var(--f-ko);font-weight:700;font-size:1.08rem;color:var(--ink);line-height:1.45;word-break:keep-all}}
.qa .qen{{font-size:.82rem;color:var(--ink-2);line-height:1.4}}
.qa .tw{{flex:none;font-size:.66rem;color:var(--ink-3);border:1px solid var(--line);border-radius:999px;padding:.05rem .45rem;margin-top:.2rem}}
.qa.open .tw{{display:none}}
.qplay{{flex:none;margin:.85rem .85rem 0 0}}
.qa .a{{display:none;padding:0 1.05rem 1.05rem 3.2rem;border-top:1px solid var(--line);padding-top:.8rem}}
.qa.open .a,body.reveal .qa .a{{display:block}}
.ako{{font-family:var(--f-ko);font-weight:700;font-size:1.05rem;line-height:1.6;margin:.15rem 0 .3rem;word-break:keep-all}}
.confirm{{font-family:var(--f-ui);font-size:.62rem;font-weight:700;color:var(--warn);border:1px solid var(--warn);border-radius:999px;padding:.05rem .4rem;margin-left:.5rem;vertical-align:middle}}
.aen{{color:var(--ink-2);font-size:.88rem;margin:0 0 .35rem}}
.why{{color:var(--warn);font-size:.82rem;font-style:italic;margin:.2rem 0 .35rem;line-height:1.5}}
.surv{{display:flex;align-items:center;gap:.6rem;background:var(--surface);border:1px solid var(--line);border-radius:12px;padding:.6rem .8rem;margin:0 0 .5rem;box-shadow:var(--shadow)}}
.surv .sko{{font-family:var(--f-ko);font-weight:700;font-size:.98rem;flex:1;word-break:keep-all}}
.surv .sen{{color:var(--ink-3);font-size:.78rem;flex:none;max-width:42%}}
.play.mini{{padding:.35rem;border-radius:50%;margin-top:0}}
/* vocab */
.vocgrid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(210px,1fr));gap:.5rem;margin:0 0 1.3rem}}
.voc{{display:flex;align-items:center;gap:.55rem;background:var(--surface);border:1px solid var(--line);border-radius:12px;padding:.5rem .65rem;box-shadow:var(--shadow)}}
.voc .vplay{{flex:none;margin:0}}
.voc .vko{{font-family:var(--f-ko);font-weight:700;font-size:1.08rem;color:var(--ink);word-break:keep-all}}
.voc .ven{{color:var(--ink-2);font-size:.8rem;margin-left:auto;text-align:right;padding-left:.4rem}}
body.hide-vko .voc .vko{{filter:blur(6px);opacity:.5;cursor:pointer}} body.hide-vko .voc .vko.reveal{{filter:none;opacity:1}}
body.hide-ven .voc .ven{{filter:blur(6px);opacity:.5;cursor:pointer}} body.hide-ven .voc .ven.reveal{{filter:none;opacity:1}}
/* full (continuous document) */
.fsec{{font-family:var(--f-disp);font-size:1.35rem;margin:2rem 0 .5rem;padding-bottom:.3rem;border-bottom:2px solid var(--accent)}}
.fsec:first-of-type{{margin-top:.6rem}}
.fh{{font-size:.8rem;letter-spacing:.05em;text-transform:uppercase;color:var(--accent);font-weight:600;margin:1.3rem 0 .4rem}}
.fko{{font-family:var(--f-ko);font-size:1.12rem;line-height:1.95;margin:0 0 .35rem;word-break:keep-all}}
.fen{{color:var(--ink-2);font-size:.9rem;line-height:1.6;margin:0 0 .7rem}}
.fqa{{margin:0 0 .85rem}}
.fq{{font-family:var(--f-ko);font-weight:700;font-size:1.02rem;margin:0;word-break:keep-all}}
.fqe{{color:var(--ink-3);font-size:.82rem;margin:.05rem 0 .15rem}}
.fa{{font-family:var(--f-ko);font-size:1rem;line-height:1.6;margin:.1rem 0 0;word-break:keep-all}}
.fae{{color:var(--ink-2);font-size:.84rem;margin:.05rem 0 0}}
.fvoc{{display:grid;grid-template-columns:repeat(auto-fill,minmax(230px,1fr));gap:0 1rem;margin:0 0 .5rem}}
.fv{{display:flex;gap:.5rem;align-items:baseline;padding:.2rem 0;border-bottom:1px dotted var(--line)}}
.fvko{{font-family:var(--f-ko);font-weight:700;font-size:1rem;flex:none;min-width:5.5rem}}
.fven{{color:var(--ink-2);font-size:.85rem;margin-left:auto;text-align:right}}
body.hide-fen .fen,body.hide-fen .fqe,body.hide-fen .fae,body.hide-fen .fven{{display:none}}
@media print{{
  .tabs,.bar,.method,.spine-wrap,header .eyebrow{{display:none!important}}
  body{{padding:0}} .panel{{display:none!important}} #panel-full{{display:block!important}}
  .fko,.fen,.fa,.fae,.fq,.fqe,.fvko,.fven{{color:#000}}
  .fsec{{border-color:#000}} .fh{{color:#333}}
}}
/* fixed bottom bar */
.bar{{position:fixed;left:0;right:0;bottom:0;z-index:60;display:flex;flex-wrap:wrap;gap:.45rem;align-items:center;justify-content:center;background:color-mix(in srgb,var(--surface) 92%,transparent);backdrop-filter:blur(8px);border-top:1px solid var(--line);padding:.6rem .8rem;box-shadow:0 -6px 22px rgba(40,30,20,.12)}}
.acts{{display:flex;flex-wrap:wrap;gap:.45rem;align-items:center;justify-content:center}}
.acts[hidden]{{display:none}}
.tbtn{{font-family:var(--f-ui);font-size:.83rem;font-weight:500;color:var(--ink-2);background:var(--surface);border:1px solid var(--line);border-radius:999px;padding:.42rem .95rem;cursor:pointer}}
.tbtn.on{{background:var(--accent);color:var(--on-accent);border-color:transparent}}
.tbtn.play-all{{color:var(--accent);border-color:var(--accent);font-weight:600}} .tbtn.play-all.on{{color:var(--on-accent)}}
.homebtn{{display:inline-flex;align-items:center;gap:.35rem;text-decoration:none;color:var(--ink-2);flex:none}}
.homebtn:hover{{color:var(--accent);border-color:var(--accent)}}
.tbtn:focus-visible{{outline:2px solid var(--accent);outline-offset:2px}}
footer{{text-align:center;color:var(--ink-3);font-size:.8rem;margin-top:2.4rem;line-height:1.7}}
@media (max-width:640px){{.card{{grid-template-columns:1fr}} .pic img{{aspect-ratio:16/9}} .spine{{grid-template-columns:repeat(2,1fr);gap:.7rem}} .step:nth-child(2)::after,.step:last-child::after{{content:none}} .surv .sen{{display:none}} .qa .a{{padding-left:1.05rem}}
  .tabs{{justify-content:flex-start;gap:.3rem}} .tabs button{{font-size:.82rem;padding:.45rem .8rem}}
  .vocgrid{{grid-template-columns:1fr 1fr}} .fvoc{{grid-template-columns:1fr}} header{{padding-top:1.6rem}} h1{{margin-bottom:.25rem}}}}
@media (max-width:400px){{.spine{{grid-template-columns:1fr}} .step:not(:last-child)::after{{content:none}} .vocgrid{{grid-template-columns:1fr}}}}
</style></head>
<body>
<div class="wrap">
  <header>
    <div class="eyebrow">K-Specialist · 2026-08-28</div>
    <h1>여름 발표 스튜디오</h1>
    <p class="sub">Study the talk from pictures, then drill the questions the judges may ask.</p>
  </header>

  <nav class="tabs">
    <button data-tab="cards" class="on"><span class="ko">그림 카드</span> · Speech</button>
    <button data-tab="qa"><span class="ko">예상 질문</span> · Q&amp;A</button>
    <button data-tab="voc"><span class="ko">단어</span> · Vocab</button>
    <button data-tab="full"><span class="ko">전체</span> · Full</button>
  </nav>

  <section class="panel on" id="panel-cards">
    <section class="spine-wrap">
      <div class="spine-hd"><h2>The spine · 하루의 순서</h2><span class="note">Your four parts run like one day</span></div>
      <div class="spine">{spine}</div>
      <div class="spine-foot">{playbtn(roadmap_au,'Hear the four parts')}<span>옷 → 날씨 → 음식 → 더위. Get dressed, check the sky, eat, go out.</span></div>
    </section>
    <p class="method"><span><span class="n">1</span><b>See</b> the picture</span><span><span class="n">2</span><b>Say</b> the Korean out loud</span><span><span class="n">3</span><b>Tap</b> to check &amp; <b>Listen</b></span></p>
    <div class="cards">{''.join(cards)}</div>
  </section>

  <section class="panel" id="panel-qa">
    <h2 class="sec">함정과 빈틈 <span class="cnt">Traps &amp; gaps · close these first</span></h2>
    <p class="secnote">Three doors the script opens but never walks through. A returning judge will find them.</p>
    {traps_html}
    <h2 class="sec">핵심 질문 <span class="cnt">Core · these have audio</span></h2>
    <p class="secnote">The nine from the drill. Answer aloud, then tap Listen to compare.</p>
    {core_html}
    <h2 class="sec">심화 꼬리 질문 <span class="cnt">Deeper follow-ups · by section</span></h2>
    <p class="secnote"><span class="confirm">확인 필요</span> means confirm it is true for you before you rely on it.</p>
    {deep_html}
    <h2 class="sec">막힐 때 <span class="cnt">Survival lines · when you get stuck</span></h2>
    {surv_html}
  </section>

  <section class="panel" id="panel-voc">
    <p class="secnote" style="margin-top:.4rem">The words behind the five topics. Tap ▶ to hear each one. Use <b>Hide English</b> to test the meaning, or <b>Hide Korean</b> to produce the word yourself.</p>
    {vocab_html}
  </section>

  <section class="panel" id="panel-full">
    <p class="secnote" style="margin-top:.4rem">Everything in one place for reading or printing. Use <b>Hide English</b> to read the Korean alone.</p>
    <h2 class="fsec">발표 대본 · The speech</h2>
    {speech_full}
    <h2 class="fsec">예상 질문 · Q&amp;A</h2>
    {qa_full}
    <h2 class="fsec">단어 · Vocabulary ({VCOUNT})</h2>
    {voc_full}
  </section>

  <footer>{footer_txt}</footer>
</div>

<div class="bar">
  {home_btn}
  <div class="acts" id="acts-cards">
    <button class="tbtn play-all" id="playAll" type="button">▶ Play all</button>
    <button class="tbtn" id="tKo" type="button">Hide Korean</button>
    <button class="tbtn" id="tEn" type="button">Hide English</button>
  </div>
  <div class="acts" id="acts-qa" hidden>
    <button class="tbtn" id="revealAll" type="button">Reveal all answers</button>
  </div>
  <div class="acts" id="acts-voc" hidden>
    <button class="tbtn" id="vKo" type="button">Hide Korean</button>
    <button class="tbtn" id="vEn" type="button">Hide English</button>
  </div>
  <div class="acts" id="acts-full" hidden>
    <button class="tbtn" id="fEn" type="button">Hide English</button>
    <button class="tbtn" id="fPrint" type="button">Print / Save PDF</button>
  </div>
</div>

<script>
var cur=null,curBtn=null,seq=null;
var paBtn=document.getElementById('playAll');
var cardBtns=[].slice.call(document.querySelectorAll('#panel-cards .card .play'));
function mark(btn,on){{if(!btn)return;btn.classList.toggle('playing',on);var s=btn.querySelector('span');if(s){{if(on){{if(btn.getAttribute('data-l')===null)btn.setAttribute('data-l',s.textContent);s.textContent='Playing…';}}else{{var l=btn.getAttribute('data-l');if(l!==null)s.textContent=l;}}}}}}
function stopCur(){{if(cur){{cur.pause();}}mark(curBtn,false);cur=null;curBtn=null;}}
function clearNow(){{var n=document.querySelector('.card.now');if(n)n.classList.remove('now');}}
function playOne(btn,onEnd){{stopCur();cur=new Audio(btn.getAttribute('data-au'));curBtn=btn;mark(btn,true);cur.onended=function(){{mark(btn,false);if(onEnd)onEnd();}};cur.play().catch(function(){{mark(btn,false);if(onEnd)onEnd();}});}}
function stopSeq(){{if(seq!==null){{seq=null;stopCur();clearNow();paBtn.classList.remove('on');paBtn.textContent='▶ Play all';}}}}
function step(){{if(seq===null)return;if(seq>=cardBtns.length){{stopSeq();return;}}var btn=cardBtns[seq],card=btn.closest('.card');clearNow();card.classList.add('now');card.scrollIntoView({{block:'center',behavior:'smooth'}});playOne(btn,function(){{if(seq!==null){{seq++;setTimeout(step,380);}}}});}}
paBtn.addEventListener('click',function(){{if(seq!==null){{stopSeq();return;}}seq=0;paBtn.classList.add('on');paBtn.textContent='■ Stop';step();}});
document.addEventListener('click',function(e){{
  var p=e.target.closest('.play');
  if(p){{e.stopPropagation();stopSeq();if(curBtn===p&&cur&&!cur.ended){{stopCur();return;}}playOne(p);return;}}
  var q=e.target.closest('.qa .q'); if(q){{q.closest('.qa').classList.toggle('open');return;}}
  var ko=e.target.closest('.ko'); if(ko&&document.body.classList.contains('hide-ko')){{ko.classList.toggle('reveal');return;}}
  var vko=e.target.closest('.vko'); if(vko&&document.body.classList.contains('hide-vko')){{vko.classList.toggle('reveal');return;}}
  var ven=e.target.closest('.ven'); if(ven&&document.body.classList.contains('hide-ven')){{ven.classList.toggle('reveal');}}
}});
function tog(id,cls,onL,offL){{var b=document.getElementById(id);b.addEventListener('click',function(){{var on=document.body.classList.toggle(cls);b.classList.toggle('on',on);b.textContent=on?offL:onL;if(cls==='hide-ko'&&!on){{[].forEach.call(document.querySelectorAll('.ko.reveal'),function(k){{k.classList.remove('reveal');}});}}}});}}
tog('tKo','hide-ko','Hide Korean','Show Korean');
tog('tEn','hide-en','Hide English','Show English');
tog('vKo','hide-vko','Hide Korean','Show Korean');
tog('vEn','hide-ven','Hide English','Show English');
tog('fEn','hide-fen','Hide English','Show English');
document.getElementById('fPrint').addEventListener('click',function(){{window.print();}});
var rb=document.getElementById('revealAll');
rb.addEventListener('click',function(){{var on=document.body.classList.toggle('reveal');rb.classList.toggle('on',on);rb.textContent=on?'Hide all answers':'Reveal all answers';}});
// tabs
var tabs=document.querySelectorAll('.tabs button');
var panels={{cards:document.getElementById('panel-cards'),qa:document.getElementById('panel-qa'),voc:document.getElementById('panel-voc'),full:document.getElementById('panel-full')}};
var acts={{cards:document.getElementById('acts-cards'),qa:document.getElementById('acts-qa'),voc:document.getElementById('acts-voc'),full:document.getElementById('acts-full')}};
function showTab(name){{stopSeq();stopCur();for(var k in panels){{panels[k].classList.toggle('on',k===name);acts[k].hidden=(k!==name);}}tabs.forEach(function(t){{t.classList.toggle('on',t.getAttribute('data-tab')===name);}});window.scrollTo({{top:0,behavior:'smooth'}});}}
tabs.forEach(function(t){{t.addEventListener('click',function(){{showTab(t.getAttribute('data-tab'));}});}});
</script>
</body></html>'''

out=(OUTDIR+'/index.html') if WEB else BASE+('/k-specialist-speech-study-lite.html' if LITE else '/k-specialist-speech-study.html')
io.open(out,'w',encoding='utf-8').write(DOC)
print('cards:',len(cards),'| traps:',len(TRAPS),'core:',len(CORE),'deep:',sum(len(x[1]) for x in DEEP),'surv:',len(SURV))
print('written:',out,'| %.2f MB'%(len(DOC.encode('utf-8'))/1048576))
