# Validation status

This release separates packaging, local tool tests and production evidence. No paid generations are part of its automated test suite.

## Current release checks

Checked locally on 15 October 2026:

| Check | Result |
| --- | --- |
| Python setup, installer and actual-media delivery tests | 36 passed |
| Node audio-review tests with synthetic media and mocked API | 9 passed |
| Standalone installation in both host layouts, including spaces and collision protection | Passed |
| Fresh studio initialisation and repeated-run preservation | Passed |
| Guided setup: missing-tool actions, optional tools, retained setup progress and account-response privacy | Passed in automated helper tests |
| Synthetic H.264/AAC encode, full decode and delivery check | Passed |
| Claude Code 2.1.296 strict marketplace, manifest and skill validation | Passed |
| Codex CLI 0.155.1 local marketplace installation and enabled-plugin discovery | Passed |
| Higgsfield CLI 1.1.26 read-only account, workspace and model-catalogue checks | Passed; private responses suppressed |
| Public-package file, manifest, link and common-secret-pattern checks | Passed |

The live read-only checks used an existing authenticated account. They do not
prove a new user's login or model entitlement. No paid generation, media upload
or live Gemini review was performed for this packaging release. Remote GitHub
installation and CI results are recorded in the release notes after publication.

Version 0.2.0 adds Stage 0 and route-specific repair guidance. The instructions
were reviewed against a planning-only request without execution access, a
supplied-footage edit without paid accounts, a fresh generation setup, a returning
studio and a changed host/workspace. These are instruction reviews, not claims
that a live agent onboarding conversation or paid production was run on every host.
The executable checks cover missing dependencies, next actions, preserved setup
records, offline behaviour and suppression of both successful and failed private
account responses.

## Local transcription without Resolve

Checked on macOS with an Apple M4 Max on 30 October 2026, using whisper.cpp
1.9.5 from Homebrew and `ggml-large-v3-turbo-q5_0.bin`. The model's SHA-256
matched the hash Hugging Face lists. Both clips were synthetic macOS speech
with one clean speaker and no music.

| Check | Result |
| --- | --- |
| 5.2-second clip with a measured 1.5-second pause: words | 13 of 13 correct |
| Default settings: word timing after the pause | Failed: three words shared one timestamp, 0.37 s early |
| `-nfa --dtw large.v3.turbo`: word timing after the pause | First word 0.11 s after the measured onset; every word in order |
| 32.1-second narration: words and speed | 94 of 94 correct in 1.4 s, including model load |

Flash attention is on by default in this version and silently disables DTW.
Real dialogue with noise, accents or crosstalk is untested.

## Historical production evidence

The original private workflow was exercised on macOS through concept development, character references, local Blender planning, Higgsfield generation, Resolve Studio editing, locally rendered graphics, audio processing and final export/recovery. Feedback from those runs led to the continuity, acting, eyeline, sound and audio-review guidance retained here. Private production media and account records are not published.

That evidence does not establish that a fresh install, another host or another OS can run every integration without setup. The public version removes owner-specific assumptions, adds setup tooling and shares the same skill across hosts. Installation/discovery tests are distinct from a complete new paid film rendered separately by each host.

## Limits

- macOS is the historical full-production environment. Linux and Windows GUI/browser/Resolve integration need their own local tests. CI covers portable helpers on its declared platforms only after a run passes.
- This repository is not an approved listing in the OpenAI or Anthropic public directories. Its GitHub marketplace and downloadable package are separate distribution routes.
- No claim of direct agent hearing, universal browser control or automatically authenticated services is made.
- Human continuous review is still needed for each final video. An advisory model report or codec check does not approve a performance or music choice.
