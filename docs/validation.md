# Validation status

This release separates packaging, local tool tests and production evidence. No paid generations are part of its automated test suite.

## Current release checks

Checked locally on 15 October 2026:

| Check | Result |
| --- | --- |
| Python setup, installer and actual-media delivery tests | 32 passed |
| Node audio-review tests with synthetic media and mocked API | 9 passed |
| Standalone installation in both host layouts, including spaces and collision protection | Passed |
| Fresh studio initialisation and repeated-run preservation | Passed |
| Synthetic H.264/AAC encode, full decode and delivery check | Passed |
| Claude Code 2.1.296 strict marketplace, manifest and skill validation | Passed |
| Codex CLI 0.155.1 local marketplace installation and enabled-plugin discovery | Passed |
| Higgsfield CLI 1.1.26 read-only account, workspace and model-catalogue checks | Passed; private responses suppressed |
| Public-package file, manifest, link and common-secret-pattern checks | Passed |

The live read-only checks used an existing authenticated account. They do not
prove a new user's login or model entitlement. No paid generation, media upload
or live Gemini review was performed for this packaging release. Remote GitHub
installation and CI results are recorded in the release notes after publication.

## Historical production evidence

The original private workflow was exercised on macOS through concept development, character references, local Blender planning, Higgsfield generation, Resolve Studio editing, locally rendered graphics, audio processing and final export/recovery. Feedback from those runs led to the continuity, acting, eyeline, sound and audio-review guidance retained here. Private production media and account records are not published.

That evidence does not establish that a fresh install, another host or another OS can run every integration without setup. The public version removes owner-specific assumptions, adds setup tooling and shares the same skill across hosts. Installation/discovery tests are distinct from a complete new paid film rendered separately by each host.

## Limits

- macOS is the historical full-production environment. Linux and Windows GUI/browser/Resolve integration need their own local tests. CI covers portable helpers on its declared platforms only after a run passes.
- This repository is not an approved listing in the OpenAI or Anthropic public directories. Its GitHub marketplace and downloadable package are separate distribution routes.
- No claim of direct agent hearing, universal browser control or automatically authenticated services is made.
- Human continuous review is still needed for each final video. An advisory model report or codec check does not approve a performance or music choice.
