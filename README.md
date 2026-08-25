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
| **Node.js 14+** | running the `npx` install | that is all Node is used for |
| **An AI that reads skills** (Claude Code, or an agent that loads `.claude/skills`) | doing the actual building | the skill is instructions + reference code, not a standalone program |
| **Python 3** | the page and feed builders | standard library only, nothing to `pip install` |
| **`genmedia` CLI + a fal.ai API key** | generating the pictures and the voice audio | images via `fal-ai/flux/schnell` (~$0.003 each), audio via `fal-ai/bytedance/seed-speech/tts/v2`. **Optional:** if you have no key, supply your own images/audio and skip generation. |
| **git + a GitHub account + the `gh` CLI** | hosting on GitHub Pages | the repo must be **public** for free Pages; `gh` must be logged into the account that owns it |
| **The study material itself** | the content | a speech, script, dialogue, or word list, in the target language — plus its translation if you want one |

Costs are tiny: a full unit (about 12 images + ~150 short audio clips) runs a few cents of fal.ai
usage. GitHub Pages hosting is free.

You do **not** need: any server, a database, a paid host, a build server, or npm-publish rights.

---

## Complete feature list

- **Four-tab study unit** — speech cards, Q&A, vocab, full read-through — in one HTML file with
  in-page tabs and a shared audio engine.
- **Audio on everything** — every speech line, every Q&A answer, every vocab word, in a native
  target-language voice.
- **Active recall** — hide the target / translation / meaning / word and reveal on tap; Play-all runs
  the whole thing hands-free with auto-scroll.
- **Memory-first layout** — image-left cards, a structural spine mapped to a real-world order,
  color-coded sections, consistent spatial layout.
- **Three build modes** — self-contained single file (offline/email), `lite` (claude.ai artifact),
  and `web` (separate `img/`+`audio/` assets for Pages, ~100 KB page, clips load on demand).
- **Notebook-style hub** — a table of contents that lists every unit as a numbered card.
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
    templates/               build_study.py, build_feed.py, hub_index.html, example data
```

---

## How it fits together

1. `npx github:1l3oth/studybook` installs the skill.
2. You ask your AI to build a unit from your material.
3. It follows the skill: splits the material into beats, generates images and audio, builds the page,
   updates the hub and the feed, and pushes to GitHub Pages.
4. Your learners open the site; any AI can read it through the feed.

License: MIT.
