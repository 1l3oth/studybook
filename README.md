# studybook

A **studybook** is a self-hosted study site where every unit follows one memory-first structure, so
a learner can *see it, hear it, say it* — and an AI can read the whole thing as text.

**Live sample:** https://1l3oth.github.io/studybook/
· a unit: https://1l3oth.github.io/studybook/korean-summer-speech/
· feed: https://1l3oth.github.io/studybook/feed.xml

This repo is two things at once:
1. The **live sample site** (served by GitHub Pages).
2. A **Claude skill** (`studybook`) that teaches an AI to build more sites and units exactly like it —
   installable with one `npx` command, no files to pass around.

---

## Start from zero (free AI apps, no GitHub account needed)

Open a free AI app that can work on your computer: **Antigravity** (free with a Google account),
the **ChatGPT desktop app** in Codex mode (free plan included), or Claude Code. Open an empty folder
in it and paste:

```
Set up my studybook from zero. Read https://1l3oth.github.io/studybook/START.md and follow it step by step. Talk to me in Khmer.
```

The AI installs what is missing (Git, Python, the GitHub tool, the free voice), helps you make a
GitHub account, logs your computer in, starts **your own** site in any language (Korean, English,
Japanese, Chinese, ...), builds your first unit and puts it online at `https://<you>.github.io/studybook/`.
You only make the account, type your own password and click Authorize. Everything is free.

A normal chat (chatgpt.com, gemini.google.com) cannot do this: it cannot run programs on your computer.

---

## What each study unit gives the learner

Four in-page tabs, one shared audio engine, one fixed control bar:

| Tab | What it does |
|-----|--------------|
| **Speech** (picture cards) | One card per idea: image on the left, the target line, translation, a keyword, and audio. A "spine" at the top fixes the order onto a real-world sequence. **Play-all** and **hide-to-recall**. |
| **Q&A** | The questions an examiner might ask; answer hidden, tap to reveal, audio on answers. Leads with the script's **traps and gaps**. |
| **Vocab** | Topic words in groups, audio each, hide the meaning *or* the word for two-way recall. |
| **Full** | The whole speech + all Q&A + all vocab as one printable document (Print / Save PDF). Also what the RSS feed exposes. |

Design follows evidence-based memory research (dual coding, picture superiority, method of loci,
active recall), not folklore.

---

## Install the skill (via npx)

No file transfer. From any machine with Node:

```bash
# install globally (~/.claude) — usable in every project
npx github:1l3oth/studybook

# or install into just the current project (./.claude)
npx github:1l3oth/studybook --project

# or a .claude directory you name
npx github:1l3oth/studybook --dir /path/to/.claude

# Antigravity or Codex: this project's .agents/skills
npx github:1l3oth/studybook --agents

# Antigravity + Codex, every project
npx github:1l3oth/studybook --agents-global
```

This installs two things: the **`studybook` skill** and a **`/teach-me` command**. Restart Claude
Code so it loads them.

### The easy way: `/teach-me`

Just type the command:

```
/teach-me                       it asks what you want to learn
/teach-me Korean weather small talk
/teach-me <paste your text, or a link>
```

`/teach-me` first asks whether you have a couple of minutes or are short on time (if short, it asks
only the one essential question), reads any text or link you paste, then builds the whole unit for
you. It also reminds you to grab a snack or a drink to sip while you study — tying new words to a
taste gives your brain an extra way to recall them.

### Or just ask

The skill also works from a plain request, e.g. *"make a studybook unit for this speech"* or *"add a
study page to my studybook and deploy it"*. Either way the skill is a **router**: it dispatches the AI
to the right step-by-step reference (site, unit, media, hosting, feed, style) so units come out
consistent instead of improvised.

---

## What you need on your side (important)

The skill drives the work, but it uses tools on **your** machine and **your** accounts. Have these
ready; the AI will tell you which are missing when it starts.

| Need | For | Notes |
|------|-----|-------|
| **Node.js 14+** (optional) | the `npx` install | not needed when the AI follows START.md |
| **An AI that reads skills** (Claude Code, Antigravity, or Codex in the ChatGPT app) | doing the actual building | the skill is instructions + reference code, not a standalone program |
| **Python 3.12+** | the page and feed builders | standard library only |
| **edge-tts** | the free native voice | `pip install -U edge-tts`, no key |
| **git + a GitHub account + the `gh` CLI** | hosting on GitHub Pages | the repo must be **public** for free Pages; `gh` must be logged into the account that owns it |
| **The study material itself** | the content | a speech, script, dialogue, or word list, in the target language — plus its translation if you want one |

Everything is free: the pictures are drawn as SVG, the voice is edge-tts, and GitHub Pages hosting is free.

You do **not** need: any server, a database, a paid host, a build server, or npm-publish rights.

---

## Complete feature list

- **Four-tab study unit** — speech cards, Q&A, vocab, full read-through — in one HTML file with
  in-page tabs and a shared audio engine.
- **Audio on everything** — every speech line, every Q&A answer, every vocab word, in a native
  target-language voice.
- **Active recall** — hide the target / translation / meaning / word and reveal on tap; Play-all runs
  the whole thing hands-free with auto-scroll.
- **Memory-first layout** — flat 2D picture cards, big picture tiles, a line map of the sections in a
  real-world order; a card feed on phones and a platform display (one big stage plus the route list)
  on desktop.
- **One data file per unit** — `unit.json` holds every line, answer, word and audio path;
  `tools/render_unit.py` builds the page with the shared `assets/` styles and script.
- **Subway-line hub** — the homepage lists every unit as a station on one line, with a Continue panel;
  installable as an app (PWA, online only).
- **AI-readable RSS feed** — `feed.xml` carries each unit's full text in `content:encoded`, so an AI
  or feed reader ingests the material without running the app; auto-discoverable from the site root.
- **Print / Save-PDF** of the full document.
- **Responsive and theme-aware** — works on phones, respects light/dark.
- **Reusable, adaptable code** — Python builders and an HTML hub template bundled in the skill.

---

## Repo layout

```
studybook/
  index.html                 hub (table of contents) — the live sample
  feed.xml                   RSS feed with every unit's full text
  .nojekyll
  korean-summer-speech/      the sample unit
    index.html  img/  audio/
  package.json               npx installer manifest
  bin/install.js             copies the skill + command into your .claude dir
  command/teach-me.md        the /teach-me command (interview, then build)
  skill/studybook/           the skill payload
    SKILL.md                 the router
    references/              step-by-step sub-guides (site, unit, media, hosting, feed, style)
    templates/               render_unit.py, gen_audio.py, build_stations.py, build_feed.py, assets/, pwa/, hub_index.html, unit.example.json
```

---

## How it fits together

1. `npx github:1l3oth/studybook` installs the skill.
2. You ask your AI to build a unit from your material.
3. It follows the skill: splits the material into beats, generates images and audio, builds the page,
   updates the hub and the feed, and pushes to GitHub Pages.
4. Your learners open the site; any AI can read it through the feed.

License: MIT.
