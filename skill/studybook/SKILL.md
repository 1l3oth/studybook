---
name: studybook
description: >
  Router skill for building a "studybook" — a self-hosted GitHub Pages site of interactive
  language-study units that follow one memory-first structure: picture cards with audio, a Q&A
  drill, a vocabulary tab, and a full read-through, plus an RSS feed an AI can read. Use this
  whenever the user wants to build a study site or add a study unit/book page, or says "make a
  studybook", "add a study unit", "create study cards for this speech", "study page like the sample".
  This is a ROUTER: do not improvise the structure — read the one reference below that matches the
  step and follow it, so every unit comes out in the same proven shape.
---

# Studybook (router)

A **studybook** is a static site (GitHub Pages) whose units all follow the same learning
structure, so a learner can *see it, hear it, say it* and an AI can read the whole thing as text.
Live sample to copy from: **https://1l3oth.github.io/studybook/** · feed **/feed.xml**.

Each **unit** is one self-contained study page with four in-page tabs sharing one audio engine:
1. **Speech / 그림 카드** — picture cards (one per idea) with per-line audio, a structural "spine", Play-all, and hide-to-recall.
2. **Q&A** — anticipated questions, answer hidden then revealed, audio on answers; traps and gaps first.
3. **Vocab** — the topic words in groups, audio each, two-way hide-to-recall.
4. **Full** — the whole speech + all Q&A + all vocab as one printable document.

A **hub** page (`index.html`) lists the units like a notebook table of contents. A **feed.xml**
exposes each unit's full text so an AI can ingest it without running the app.

## How to use this router
Figure out which step the user is on, then **read only that reference file and follow it**. Do not
generate your own structure — the whole point of this skill is that units come out consistent.

| The user wants to… | Read |
|---|---|
| Understand the whole pipeline first | this file, then the reference for the step you are on |
| Stand up a brand-new studybook site (repo + hub + Pages) | `references/01-create-site.md` |
| Add a study unit / book page from some material | `references/02-build-unit-page.md` |
| Generate the images and the voice audio | `references/03-media-generation.md` |
| Host it: separate audio/image assets, deploy to Pages | `references/04-hosting-and-assets.md` |
| Add or refresh the RSS feed (so an AI can read it) | `references/05-rss-feed.md` |
| Match the visual style / read the live sample | `references/06-style-and-sample.md` |

For the deep memory science behind the card design (dual coding, picture superiority, method of
loci, active recall, and the honest caveat about NLP "eye-accessing cues"), also load the standalone
**`language-study-page`** skill — this router's `02` reference is the operational summary of it.

## Reference implementation (bundled)
Working code lives in `templates/` (the live site uses the same files under `tools/` and `assets/`):
- `unit.example.json` is the data shape of one unit: sections (each a Seoul line colour), an optional
  `explain` block (eli5 style: big flat pictures, a few words each), cards, Q&A blocks
  (`trap` / `qa` / `surv`), vocab groups and full text. Write this file first.
- `gen_audio.py` gives every line, answer and word a native Korean voice (edge-tts, free, no key) and
  fills the Full text from the cards. Re-runnable; existing clips are kept.
- `render_unit.py` writes `<unit>/index.html` from `unit.json`. The page links the shared
  `assets/line.css`, `assets/unit.css`, `assets/unit.js`; never inline a per-unit design.
- `build_feed.py` builds `feed.xml` from every `*/unit.json`, newest `published` first.
- `draw_flat_objects.example.py` shows how unit pictures are drawn: flat 2D object SVGs, no image model.
- `hub_index.html` is the homepage (a subway line, one station per unit); `pwa/` holds the manifest,
  service worker, offline page and icon sources that make the site an installable app.
- `DESIGN.example.md` records the visual system (Seoul Metro wayfinding). Follow it.

Unit build, in order: write `unit.json` -> draw `img/*.svg` -> `python tools/gen_audio.py <slug>` ->
`python tools/render_unit.py <slug>` -> add a station to the homepage -> `python tools/build_feed.py`.

## What the user needs on their side
Do not assume these exist — check, and tell the user what is missing (full list in the repo README):
- **Python 3** (the builders are Python, standard library only).
- **`edge-tts`** (`pip install -U edge-tts`) for the native voice. Keep it updated: old versions get
  HTTP 403 from the speech service. fal.ai (`genmedia`) is optional, not required.
- **git + a GitHub account + `gh` CLI** to host on GitHub Pages.

## Non-negotiables (every unit)
- `<meta charset="utf-8">` first in the file, always (or non-Latin text becomes mojibake).
- A native voice in the target language, not a multilingual voice with a language flag.
- The **Hide / active-recall** toggle — never ship a unit without it.
- One HTML file with in-page tabs, never separate pages per tab; audio and images as files beside it.
- Focus mode (one card at a time, Korean hidden until tapped) and the shared dock stay on every unit.
- Never ask the learner to speak aloud: recall happens in their head (they study at work).
- Pictures are flat 2D objects, drawn as SVG.
