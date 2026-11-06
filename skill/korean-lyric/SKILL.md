---
name: korean-lyric
description: >
  Write Korean in English letters the way K-pop lyric sites and YouTube lyric videos do
  (ColorCodedLyrics style), so someone who cannot read Hangul can read or sing it out loud.
  Use whenever you add a "Lyric" or romanized line next to Korean text, build a studybook unit,
  make study cards, subtitles or song sheets with romanization, or when the user says the
  romanization "does not look like the lyrics I read when I sing". Comes with romanize.py.
---

# Korean Lyric

"Lyric" is Korean written in English letters, spelled the way it is **sung and spoken**, in the
style learners already see on lyric videos. It is not strict textbook Revised Romanization and not
letter-by-letter transliteration.

**Do not write it by hand.** Run `romanize.py` (in this folder; the studybook repo keeps the same file
at `tools/romanize.py` and `skill/studybook/templates/romanize.py` — keep all copies identical):

```python
from romanize import romanize
romanize('저는 사랑하는 사람과 결혼하고 싶어요.')
# 'jeoneun saranghaneun saramgwa gyeolhonhago shipeoyo.'
```

Standard library only. Hangul runs are converted; English, numbers without a counter, and
punctuation stay as they are.

## The rules (what romanize.py does)

1. **Spacing follows the Hangul.** One Korean word becomes one Latin word; particles and endings stay
   on the word: 우리를 *urireul*, 날씨가 *nalsshiga*. Never split into syllables, no hyphens inside words.
2. **All lowercase.** No capital at the start of a sentence. Commas, ? and ! stay.
3. **Spelled as spoken**:
   - linking: 먹어요 *meogeoyo*, 옷이 *oshi*
   - nasal sounds: 합니다 *hamnida*, 있는 *inneun*, 못 먹어요 *mon meogeoyo*
   - ㄹ: 연락 *yeollak*, 설날 *seollal*
   - ㅎ: 좋아요 *joayo*, 좋다 *jota*, 축하 *chuka*
   - 같이 *gachi*, 굳이 *guji*
   - finals are spoken p / t / k / n / m / ng / l: 없어 *eopseo*, 먹고 *meokgo*
4. **Tensing is not written.** Double letters only where the Hangul has ㄲ ㄸ ㅃ ㅆ ㅉ: 먹고 *meokgo*,
   not *meokkko*.
5. **sh**: ㅅ/ㅆ before an i or y sound is *sh* / *ssh*: 시간 *shigan*, 셔츠 *shyeocheu*, 날씨 *nalsshi*,
   쉬어요 *shwieoyo*.
6. **Vowels**: ㅓ *eo*, ㅡ *eu*, ㅐ *ae*, ㅔ *e*, ㅕ *yeo*, ㅝ **weo** (줘요 *jweoyo*), ㅚ and ㅞ **we**
   (회사 *hwesa*, 외국 *weguk*), ㅙ *wae*, ㅟ *wi*.
7. **의**: *ui* at the start of a word (의사 *uisa*), *e* as the possessive particle (우리의 *urie*),
   *i* after a consonant (희망 *himang*).
8. **Consonants at the start of a word** are g / d / b / j (그대 *geudae*); ㄹ is *r* before a vowel,
   *l* otherwise.
9. Numbers with a Sino-Korean counter (년 월 일 원 분 번 층…) are written out; native counters (살, 번째)
   stay as digits. Latin right before Hangul keeps a hyphen so it stays readable: AI를 *AI-reul*.

## When a word comes out wrong

Some spoken forms cannot be seen from the letters (맛없다 *madeopda*, ㄴ added in compounds like
한국요리 *hangungnyori*, 의 in 회의 *hwei*). Add the word to the `SPOKEN` dict in `romanize.py`
(spelling → spoken Hangul), re-run, and copy the file to every place it lives. Never fix Lyric by
hand in generated HTML; it will be overwritten.

## Checks

- Read a few lines aloud with no Hangul in front of you: they should sound right to a Korean ear.
- In a page, a long Lyric word is wider than the Hangul. Check narrow layouts (390px) for words broken
  in the middle or labels running into each other.
- Do not copy real song lyrics into examples, notes or tests; use invented phrases or the content
  you are building.

## Why this style

Most YouTube lyric videos take their romanization from ColorCodedLyrics, and several lyric sites copy
it: lowercase, Hangul word spacing, sound changes applied, *sh*, *weo*, *we*. Genius Romanizations
spells letter by letter (*issdamyeon*), which is harder to sing for anyone who cannot read Hangul.
Korean press has criticised romanizations that ignore sound changes (Star News, 2013).
Sources checked 2026-11: colorcodedlyrics.com, kpopchords.com, genius.com (Genius Romanizations),
tirto.id, koreantoolbox.com/korean-lyrics-romanizer, starnewskorea.com.
