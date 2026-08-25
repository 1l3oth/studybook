---
description: Build you a memory-first study unit on any topic — asks a couple of quick questions, then generates it (studybook)
argument-hint: "[topic, or pasted text, or a link — all optional]"
---

The user ran `/teach-me`. Their input (a topic, pasted text, or a link — may be empty):

$ARGUMENTS

You will build them a **studybook** study unit. **Load the `studybook` skill now and follow its
structure exactly** — picture cards with audio, a Q&A drill, a vocab tab, and a full read-through.
Do not invent a different structure; that consistency is the whole point.

Work through this flow, staying light and friendly (never interrogate — batch questions, ask few):

**1. Open with the study tip.** Before anything else, tell them warmly:
> Grab a snack or a drink to sip while you study. Tying new words to a taste or smell gives your
> brain an extra hook to pull them back later (context-dependent memory). It really does help.

**2. Read what they already gave you.** Look at `$ARGUMENTS`:
- If it contains **pasted text**, use it as the source material.
- If it contains a **link**, fetch and read it (defuddle / WebFetch) and use that as the source.
- If it is a **short topic** or **empty**, gather a little info in step 3.

**3. Ask about time FIRST** (one AskUserQuestion):
> "Do you have a couple of minutes to answer a few quick questions, or are you short on time?"
- **Short on time →** ask ONLY the one essential question, then proceed with sensible defaults for
  everything else:
  > "In one line: what do you want to be able to say or know by the end, and in which language
  > (and roughly your level)?"
- **A few minutes →** ask a small batched set (one AskUserQuestion, 2–4 items): target language +
  level; the goal/occasion (a speech, an exam, a conversation, or just a vocab set); roughly how much
  (a 2–3 minute speech / a short dialogue / ~50 words); and the support/translation language.

**4. If the topic is still thin**, ask 1–3 short clarifiers (angle, audience, any must-include
points). Then stop asking and build.

**5. Confirm the plan in one or two lines**, then BUILD via the `studybook` skill: split into beats,
generate ONE sample image and confirm the style with them, then batch the images and native-voice
audio, assemble the four tabs, and deliver.
- If they already have a studybook site, deploy the new unit and update the hub + `feed.xml`.
- If not, offer to set one up (skill reference `01`), or just hand them the self-contained HTML file.

**6. Close by keeping the habit alive:** remind them to study in short, spaced sessions, to say each
line out loud from the picture before revealing it, and to keep sipping that drink while they shadow.

Defaults when unsure: target-language native voice, ~12 beats, translation into the language they are
asking in, self-contained file first. Scale up (per-answer audio, more cards) only if they want it.
