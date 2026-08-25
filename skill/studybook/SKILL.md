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
Working, adaptable code lives in `templates/`:
- `build_study.py` — builds one unit's HTML in three modes: default (self-contained single file),
  `lite` (smaller, for a claude.ai artifact), `web` (separate `img/`+`audio/`, for GitHub Pages).
- `build_feed.py` — builds `feed.xml` with each unit's full text in `content:encoded`.
- `qa_data.example.py`, `vocab_data.example.py` — the data shapes the builder consumes.
- `hub_index.html` — the notebook-style hub landing page to adapt per studybook.

## What the user needs on their side
Do not assume these exist — check, and tell the user what is missing (full list in the repo README):
- **Python 3** (the builders are Python, standard library only).
- **`genmedia` CLI + a fal.ai API key** for images (`fal-ai/flux/schnell`) and audio
  (`fal-ai/bytedance/seed-speech/tts/v2`) — or the user supplies their own images/audio.
- **git + a GitHub account + `gh` CLI** to host on GitHub Pages.

## Non-negotiables (every unit)
- `<meta charset="utf-8">` first in the file, always (or non-Latin text becomes mojibake).
- A native voice in the target language, not a multilingual voice with a language flag.
- The **Hide / active-recall** toggle — never ship a unit without it.
- One HTML file with in-page tabs, never separate pages per tab.
- On GitHub Pages, prefer the `web` build (separate assets) so the page stays light.
