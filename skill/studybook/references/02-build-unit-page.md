# 02 · Build a study unit (book page)

One unit = one HTML page with four in-page tabs sharing one audio engine and a fixed bottom control
bar. Build it with `templates/build_study.py`; this doc is the structure it must produce. For the
memory rationale behind each choice, load the `language-study-page` skill.

## The four tabs
1. **Speech (그림 카드).** Split the material into ~8–14 **beats** (one idea each, not one per
   sentence). Each card: **image on the left (~38%)**, a color chip for its section, the target line
   **large in a warm serif**, the translation muted, a one-word **keyword** bridge, and a **Listen**
   button. Above the cards, a **spine**: the sections as ordered, labeled steps mapped onto a
   real-world sequence the learner already owns (e.g. the parts run in the order of an ordinary day).
2. **Q&A.** Anticipated questions; question shown, answer hidden, tap to reveal, audio on answers.
   **Lead with traps and gaps** — places the script implies something it never states (an unnamed
   item, a shaky claim, an unkept promise); a real examiner probes exactly there. Flag any answer
   that asserts an unconfirmed personal fact so the learner verifies it.
3. **Vocab.** The topic words grouped by theme, audio each, and two-way hide (hide meaning / hide the
   word) for recall both directions.
4. **Full.** The whole speech, then all Q&A, then all vocab, as one continuous printable document
   (add a Print / Save-PDF button). This is also what feeds the RSS `content:encoded` (see 05).

## Fixed bottom control bar (docked, never scrolls away)
`position:fixed;bottom:0`, blurred surface, and `padding-bottom` on `body` so the last card clears
it. Per-tab controls: **Play all** (auto-advances, scrolls each card into view, highlights current),
**Hide target**, **Hide translation** on Speech; **Reveal all** on Q&A; **Hide meaning / Hide word**
on Vocab; **Hide English / Print** on Full. Add a **Home** button (links to `../`) on the web build.
The **Hide / active-recall** toggle is the single most important feature — never ship without it.

## Data the builder consumes
- **Lines + audio.** If a source/drill HTML already holds the lines (e.g. a `DATA=[{ko,k,en}]` array
  and an index-aligned `AUDIO=[{b:base64}]` array), parse both and reuse the audio so the voice
  matches what the learner shadows. Otherwise generate TTS per line (see 03).
- **Q&A** and **vocab** as small Python lists — see `templates/qa_data.example.py` and
  `templates/vocab_data.example.py` for the exact shapes.
- **Images** one per beat, `img/beatNN.jpg` (see 03).

## Build modes (in `build_study.py`)
- default → one self-contained HTML (images + audio embedded as base64). Good for offline / email.
- `lite` → smaller build for a claude.ai artifact (artifacts time out above ~6 MB, so Q&A audio is
  dropped to text there).
- `web` → separate `img/` + `audio/` files, ~100 KB HTML; **use this for GitHub Pages** (see 04).

## Must-dos
- `<meta charset="utf-8">` first in the file; `<!doctype html>`.
- When concatenating MP3 clips into one, strip each clip's ID3v2 header (and ID3v1 trailer) first, or
  players hiccup mid-stream. (`build_study.py` already does this.)
- Theme-aware (light + dark via tokens); target-language serif for the lines; Google Fonts with real
  fallbacks. See `06-style-and-sample.md`.
- Make ONE sample card first, confirm the image style with the user, then batch the rest.
