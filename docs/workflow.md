# Production workflow and files

The production pipeline is the skill. The helper scripts make setup and technical checks repeatable; they do not run a hidden autonomous production daemon.

| Step | Decisions and outputs | Tools where needed |
| --- | --- | --- |
| Guided setup and intake | Inspect what works, ask for missing choices, guide required installs/sign-ins, verify the chosen route and retain non-secret setup evidence | Host capability inspection, studio.py doctor and its next_steps, local smoke and selected integration checks |
| Scope | Purpose, claims, audience, runtime, outputs, treatment, timed script, asset dependencies and estimate | Host reasoning, file tools, authorised research |
| Select assets | Supplied-media selects, reusable cast/location/prop references, consent/source records | Image inspection, Higgsfield image route or host image generation if available |
| Plan visuals | Scene geography, prop state, eyelines, framing, performance intention, optional boards/animatic | Images, headless Blender, configured Blender MCP or Higgsfield 3D route |
| Acquire shots | Approved generated takes or actual capture/supplied footage, with source inspection | Higgsfield CLI, verified capture tools, FFmpeg/ffprobe |
| Sound and edit | Native dialogue, voice identity, scene acoustics, foley, music spotting, caption timing, final sequence | Resolve or FFmpeg; optional Gemini source/mix review |
| Review and deliver | Rough-cut notes, technical checks, continuous picture/sound review, exports, credits, recoverable edit | Delivery checker, actual playback, source and budget review |

Typical studio:

```text
my-video-studio/
  AGENTS.md                 shared project policy and budget rules
  CLAUDE.md                 loads the same policy in Claude Code
  cast-registry.json        reusable assets and consent records
  cast/ locations/ props/   only when the project needs them
  brand/                    supplied project branding, not bundled defaults
  setup/status.md           local setup choices, evidence and next action, no secrets
  projects/example/
    brief/                  scope, script, delivery.json, gates, ledger, QA
    source/ storyboard/ previz/ renders/
    graphics/ audio/ edit/ export/
```

Templates live in the installed skill's `assets/`. Use a stable slug and shot IDs. The current `brief/brief.md` is the session handoff: status, approved decisions, unresolved issues and next work. It is separate from the host's conversation history.

For concept-only requests, deliver the scope, script and production breakdown without rendering. For supplied-footage edits, skip paid casting and generation. For long videos, track sequence dependencies and review complete contiguous ranges, including joins. Image storyboards and 3D rehearsal are optional tools for specific problems.

The final checker reads `brief/delivery.json`, so duration, aspect ratio, resolution, frame rate and audio policy come from the project. It validates H.264/yuv420p delivery MP4s and AAC/48 kHz sound where present. Other master formats, such as ProRes, need their own technical checks; do not claim that this checker verifies every codec.

Source and consent records describe evidence. A well-formed registry field is not proof the consent is real. Likewise, a technically valid export can still fail acting, continuity, joke timing, music fit or caption accuracy. Keep those results explicit.
