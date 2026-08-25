# 03 · Media generation (images + voice)

Both run through the `genmedia` CLI (fal.ai). Needs a configured fal.ai key. If the user has no key
or would rather supply their own media, skip generation and drop their files into `img/` and
`audio/` with the same names the builder expects.

## Images (one per beat)
- Endpoint: **`fal-ai/flux/schnell`** — fast, about $0.003/image, so ~12 images is a few cents.
- Use **one reusable style suffix** for every image (a consistent style is a stronger memory anchor
  than mixed stock photos). Depict the exact scene of the line.
- **Always append** `no text, no words, no letters, no logos` — diffusion models scribble gibberish
  text otherwise.
- Command:
  ```
  genmedia run fal-ai/flux/schnell --prompt "<STYLE>. Scene: <scene>" \
    --image_size landscape_4_3 --download img/beatNN.jpg --json
  ```
- Make ONE image first, show the user, lock the style, then batch the rest.
- Structural/labeled art (the spine) is built in **HTML**, not generated — diffusion can't carry
  reliable labels.

## Voice (per line, and per Q&A answer / per vocab word)
- Endpoint: **`fal-ai/bytedance/seed-speech/tts/v2`**.
- Use a **native voice in the target language**, not a multilingual voice with a language flag —
  native sounds far better. For Korean the sample uses voice `shane_ko`.
- Command:
  ```
  genmedia run fal-ai/bytedance/seed-speech/tts/v2 --text "<line>" \
    --voice <native_voice> --language <lang> --speed 0.95 \
    --output_format mp3 --sample_rate 24000 --download audio/<id>.mp3 --json
  ```
- These calls are ~5 s each. For dozens of clips, run the batch in the background and poll, or expect
  a 2-minute foreground tool to time out partway (the builder/gen loop is safe to re-run — it skips
  files that already exist).
- 24 kHz is a good default. Only drop to 8 kHz if you must shrink for the artifact `lite` build.
- Keep clip filenames deterministic (index- or id-based) so the builder can find and, in `web` mode,
  emit them.

## If reusing existing audio
When a drill HTML already carries index-aligned base64 audio, reuse it rather than regenerating — it
keeps the voice identical to what the learner already shadows, and costs nothing.
