# Audio and video review

Use actual media input when an authorised model is available. The tool adds
audio-derived reports to this workflow; it does not give the calling text
agent direct hearing or guarantee musical judgement. No additional creative
approval gate is introduced. Existing user feedback remains authoritative.

## Available adapter

`scripts/gemini-review.mjs` calls Google's Gemini API with local media bytes,
without agent tools, browsing or project-directory access. It sends only the
chosen media, neutral numbered labels, the review prompt and system guidance.
Source paths, hashes, usage and prompts are kept in the local review record.
No API keys or media base64 are written to the report.

Requirements: Node.js 22 or later, ffmpeg, ffprobe, and Gemini API access
configured outside chat. The adapter reads `GEMINI_API_KEY` or `GOOGLE_API_KEY`
from its process environment. It does not read a host config, keychain or
Gemini CLI internals. OAuth-only CLI login is not supported. Never ask for a
key in chat, print one, or copy credentials into the project.

Run `node <skill>/scripts/gemini-review.mjs --check` to verify access and list
current models. This does not prove audio quality. Select an available model
explicitly; do not silently change models to make a review agree.

Example, with paths replaced for the current project:

```sh
node <skill>/scripts/gemini-review.mjs \
  --media <project>/audio/source.wav \
  --prompt <skill>/assets/audio-review-prompt.md \
  --model "$GEMINI_REVIEW_MODEL" \
  --out <project>/brief/qa/audio-review/source-01
```

Add `--dry-run` to validate the input without authentication or network use.
Each paid request requires a new output directory, preventing accidental
overwrites or repeat submission into the same record. A completed API call
retains `analysis_verdict: unverified`. An incomplete response is not a pass;
a transport timeout remains uncertain, with no automatic retry. Check existing
records and spending before creating another request directory.

MP4, WAV and M4A were exercised. Other listed containers need validation with
the actual codec. Video defaults to four sampled frames per second, configurable
with `--fps`. Record this: sampling is not continuous human playback or
frame-accurate sync judgement. Inline media is limited to 90 MiB after base64
encoding. For longer work, use documented proxies or overlapping scene ranges,
retain source offsets and review joins; never silently shorten the requested
film. Keep original audio when making a picture proxy.

## Review sequence

1. Review a new music, voice or sound source before assembly. Use the blind
   audio prompt and withhold generation prompts, desired instruments and prior
   model verdicts. Record what it appears to contain and its uncertainty.
2. Compare that evidence with the source specification. A no-vocals request
   does not mean the generated file contains no vocals. Resolve a mismatch
   before spending time on a polished mix.
3. Review the actual full mix with picture and the intended audience experience.
   Use the video prompt, adding the project's purpose, dramatic arc, sound
   roles and relevant constraints. Do not reveal which alternative must win.
4. Use isolated tracks to diagnose a quiet or masked cue. Their level is not
   evidence of their level in the film. Prefer separate requests for each
   asset, with numbered, uninformative filenames/labels. For comparisons,
   preserve each independent report before synthesising a choice.
5. Reconcile model claims against local signal measurements, edit records and
   user feedback. Ask the user about a small number of concrete observations
   or style judgements, not the whole report. Save their corrections.

A model can rationalise the available music as intentional contrast. Evaluate
fit against the actual brief and references rather than merely asking whether
the result works. Keep the blind description distinct from the brief-aware
judgement, and record contradictory opinions instead of selecting only praise.

## Guardrails established by live tests

In September 2026 tests, Gemini 3.8 Flash and 3.1 Pro Preview both invented
music in digital silence. They agreed on a real cue's vocal/piano character,
which the user confirmed, but that did not make every other claim reliable.
One tone test identified electronic beeps yet miscounted and mistimed them.
Do not treat model self-reported confidence as calibrated accuracy.

The adapter decodes audio locally before submitting. Exact digital silence
is a measured result, with no model call for an audio-only silent request.
For video with a missing/silent track, it supplies that verified fact to the
model. Faint sound and room tone are not digital silence. This guard prevents
the observed zero-signal failure; it does not solve hallucination in general.

A quiet cue may be missed. Distinguish where an editor placed music from
where the model first noticed it. Check the isolated stem, automation and
levels before moving the cue. Use source waveforms and frame positions for
precise sync. Do not apply invented reverb, foley or music corrections merely
because the model suggests them.

In a later live comparison, full-video reports misidentified instruments,
called a measured scored ending silent, and described whistling across
different cues whose audio-only descriptions disagreed. Adding a louder audio
excerpt beside the video did not reliably resolve this. Treat a scene-fit
verdict built on contradicted sound descriptions as unreliable, even when it
praises the requested direction. Do not keep requesting reviews until praise
appears or choose a winner by counting positive model verdicts.

When this happens, extract the actual export audio and compare it with the
intended stem in a suitable music-only interval. Account for codecs and sample
alignment. This checks routing, not musical style. An audio-only diagnostic
copy with documented gain can help expose quiet detail. Retain the original,
record the source time offset and gain, verify the copy does not clip, and
never use its louder level to judge the film's balance. Keep blind source
descriptions separate from scene-fit opinions and take unresolved timbre or
taste questions to the director using a small, level-matched comparison.

For those comparisons, measure the same dramatic sections, not just whole-file
loudness. Match the sections relevant to the decision and preserve the approved
scene tracks. A single transient peak should not force every alternative to be
inaudible. If dynamics processing is needed, document it and check the actual
exports for peak overshoot, timing and audible pumping. Use project-specific
targets drawn from audience feedback, not fixed levels copied from another film.

Gemini processes a representation of the media and may downmix audio. It does
not certify the original stereo image, mastering quality, exact note/tempo
analysis or a human listening experience. Run normal delivery checks and
preserve the audience's approval/rejection status.

## Evidence and cost

Keep `record.json`, `prompt.txt` and `review.md` with the project. Record the
model returned, exact media hashes, sampling, token usage, factual checks and
which findings the user confirmed. Preserve raw failed calibration reports.
Review requests use the configured Gemini account, not Higgsfield credits.
Use current provider pricing for an estimate; do not label estimates as a
verified account charge or invent a bill from token counts alone.

The adapter tests exercise malformed/corrupt inputs, size limits, actual media
payloads, signal detection, no-audio video, credential redaction, duplicate
output protection, incomplete responses and uncertain failures. Run:

```sh
node --test <skill>/scripts/gemini-review.test.mjs
```

Sources: [Gemini audio input](https://ai.google.dev/gemini-api/docs/audio),
[video input](https://ai.google.dev/gemini-api/docs/video-understanding),
[pricing](https://ai.google.dev/gemini-api/docs/pricing). Model documentation
supports capability selection; the project's live calibration establishes
what was actually tested.
