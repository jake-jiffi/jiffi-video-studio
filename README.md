# Jiffi Video Studio

Turn a concept, handoff, script or existing footage into a scoped video production, then carry it through visuals, sound, editing and delivery checks.

This is an agent skill and installable plugin, with small local setup and validation tools. The agent does the production work using tools you connect. It is not a video model, hosted render service or one-click promise of a finished film.

The same skill files serve **Codex, ChatGPT and Claude Code**. Full production requires a host with usable file and command execution, plus the tools needed for your chosen route. In ChatGPT without those capabilities, use it for concepts, scripts and production planning. Installing a plugin does not connect your desktop apps or sign you into paid services.

## What it does

- Develops a short concept or detailed handoff into a treatment, timed audiovisual script, shot records, asset list and estimate.
- Supports generated footage, supplied recordings, screen capture where tools permit it, or a mixture. There is no fixed genre, cast, style, length or aspect ratio.
- Plans character attention, body language, props, geography, camera framing and continuity across shots.
- Uses image boards or Blender/3D rehearsal when they answer a useful visual question.
- Preserves character voice identity and matches dialogue, ambience, effects and music to the scene.
- Tracks credit quotes, reservations, uncertain jobs and refunds before another submission.
- Produces an edit and technical evidence, while keeping model opinions and human audiovisual approval separate.

```mermaid
flowchart LR
  A[Concept, handoff or footage] --> S[Guided setup and missing details]
  S --> B[Scope, timed script and budget]
  B --> G1{Treatment review}
  G1 --> C[Select assets and visual direction]
  C --> G2{Visual review if needed}
  G2 --> D[Boards or Blender / 3D rehearsal if useful]
  D --> E[Higgsfield generation or supplied / captured media]
  E --> F[Scene sound and edit in Resolve or FFmpeg]
  F --> G3{Rough-cut review}
  G3 -->|Notes| F
  G3 --> H[Technical checks and continuous audiovisual review]
  H --> I[Final exports, sources and edit handoff]
```

Review gates honour decisions and waivers you have already given. Script-only work stops at the production plan and does not start paid jobs.

## Install

Choose **one** installation route per host. Installing both the standalone skill and plugin can expose duplicate entries.

### Codex plugin

With a current Codex CLI:

```sh
codex plugin marketplace add jake-jiffi/jiffi-video-studio
codex plugin add jiffi-video-studio@jiffi-video-studio-marketplace
```

Start a fresh session, then use `$jiffi-video-studio` or choose the skill from the host's selector. The repository includes the OpenAI marketplace and plugin manifests. For desktop setup, clone/open the repository and use its local marketplace, or follow your app's plugin installation flow. See [OpenAI plugin packaging](https://developers.openai.com/plugins/build/plugins).

### Claude Code plugin

```sh
claude plugin marketplace add jake-jiffi/jiffi-video-studio
claude plugin install jiffi-video-studio@jiffi-video-studio-marketplace
```

Start a fresh session and invoke:

```text
/jiffi-video-studio:jiffi-video-studio Turn this concept into a production scope and timed script.
```

For a session-local checkout test: `claude --plugin-dir /absolute/path/to/jiffi-video-studio`. See [Claude Code plugins](https://code.claude.com/docs/en/plugins).

### Standalone skill for either local host

```sh
git clone https://github.com/jake-jiffi/jiffi-video-studio.git
cd jiffi-video-studio
python3 scripts/install.py --host both --scope project --root ../my-video-studio
```

This installs into `.agents/skills/` for Codex and `.claude/skills/` for Claude Code. Use `--host codex` or `--host claude` for one host, or `--scope user` for your home-directory install. Existing installs are never overwritten. Back up or move an existing version before replacing it. Start a fresh session in the studio folder. Standalone invocation is `$jiffi-video-studio` in Codex or `/jiffi-video-studio` in Claude Code.

### ChatGPT

Use the OpenAI-compatible plugin package in a supported desktop/local execution environment. A versioned ZIP is available under [Releases](https://github.com/jake-jiffi/jiffi-video-studio/releases). The package also retains the Claude manifest accepted by OpenAI's [skills-only import flow](https://developers.openai.com/plugins/guides/submit-claude-plugin).

Public GitHub availability is separate from listing in OpenAI's universal plugin directory. This repository does not claim directory approval. Import/install options depend on the account and surface. For a web or mobile session without the required execution access, develop the plan there and continue production in a connected local environment. See the [host compatibility notes](docs/compatibility.md).

## Set up the production tools

You can ask the skill to guide this step:

```text
Use jiffi-video-studio. Check what already works in this environment, ask me
only for the details you still need, and help me set up the tools for my video.
```

**Stage 0 runs on first use**, even if you start with a video concept. The agent
checks the host and existing setup, identifies the production route, then asks
for missing choices such as the project folder, source media, target outputs,
provider/workspace and budget. It explains how to install or connect anything
missing and verifies the result. Returning users resume from local setup records.

Only relevant tools need setup. A script needs no paid account; an edit of your
own footage needs no generation service. Optional Blender, Resolve and Gemini
routes are checked when selected. If execution is unavailable, the agent can
still develop the scope and explain where to continue production.

**Never paste API keys, passwords or tokens into the conversation.** Account
setup uses the provider's sign-in flow or private environment settings. The skill
records whether access works, not your credentials. See the
[guided setup steps](skills/jiffi-video-studio/references/00-setup-and-hosts.md).

| Requirement | Needed for | Setup |
| --- | --- | --- |
| Python 3.9+ | Installer, studio setup, delivery checker | Install Python and ensure `python3` is on PATH. On Windows use `py -3` where appropriate. |
| FFmpeg + ffprobe | Local edit and verification | Install an FFmpeg build with libx264 and AAC support. Both executables must be on PATH. |
| Node.js 22+ and npm | Gemini adapter and documented Higgsfield install | Install an active supported Node release. The core Python helpers have no pip dependencies. |
| Higgsfield CLI + account | Higgsfield image, video, voice or music jobs | Install, log in, choose a workspace, check available models and approve a project cap. |
| DaVinci Resolve Studio | Resolve editing route | Install separately, enable local scripting where supported, verify your host's MCP or official Python API connection. |
| whisper.cpp + GGML model | Dialogue transcription and word timing without Resolve | Install whisper.cpp (Homebrew formula `whisper.cpp`), download a GGML model and check its SHA-256. Run it with `-nfa` when using `--dtw`, or word timing is silently skipped. |
| Blender | Optional 3D planning | Install separately; put `blender` on PATH or provide its absolute executable path. |
| Chrome/Chromium or Resolve titles | Exact typography and graphics | Use an available local rendering route. Signed-in browsing needs a separate host browser connection. |
| Gemini API access | Optional advisory audio/video analysis | Configure a key in the execution process environment, outside chat. Costs are separate from Higgsfield credits. |
| Your source assets and permissions | Every real production | Supply footage/references, brand files, music licences and consent where needed. None are bundled here. |

For example, on macOS with Homebrew already installed:

```sh
brew install python node ffmpeg
npm install -g @higgsfield/cli@1.1.26
higgsfield auth login
higgsfield workspace list
higgsfield workspace set YOUR_WORKSPACE_ID
higgsfield account status --json
higgsfield model list --json
```

Version 1.1.26 is the tested Higgsfield CLI baseline, not a promise that model availability stays fixed. Use `higgsfield model get MODEL_ID` for the current input schema, then check the quote before submitting. Website login does not authenticate the CLI. Never print or paste an authentication token. The provider's [official CLI setup](https://higgsfield.ai/cli) covers installation alternatives.

For Linux or Windows, install the same prerequisites using your normal package manager or the vendors' installers. The portable Python helpers do not require Homebrew. Those operating systems need their own host/GUI integration checks; see [validation status](docs/validation.md).

## Create a studio and run the checks

From a clone of this repository:

```sh
python3 skills/jiffi-video-studio/scripts/studio.py init ../my-video-studio
python3 skills/jiffi-video-studio/scripts/studio.py doctor ../my-video-studio --mode edit
python3 skills/jiffi-video-studio/scripts/studio.py smoke
```

The agent helps record the actual budget, allowed providers and data policy in
`../my-video-studio/AGENTS.md`. `CLAUDE.md` points Claude Code to that shared policy.
`setup/status.md` keeps non-secret setup results and the next unresolved step.
The initial budget is unset, so setup does **not** authorise paid jobs.

For generation, after login:

```sh
python3 skills/jiffi-video-studio/scripts/studio.py doctor ../my-video-studio --mode generate --online
```

Use `--higgsfield-cli /absolute/path/to/higgsfield` for a local wrapper. Without `--online`, the doctor makes no provider requests. Online mode only reads the account, workspace list and model catalogue, suppressing private output. The smoke test encodes and decodes synthetic media locally. Neither command uploads media or starts paid generation. A successful doctor is a prerequisite check, not a production approval.

The doctor's `next_steps` explain how to fix failed checks and which unchecked
items need human or host verification. Optional items are labelled, so missing
Blender or Gemini access does not block an unrelated edit or script.

Resolve, browser and Blender connections still need a small real execution check. The [setup reference](skills/jiffi-video-studio/references/00-setup-and-hosts.md) explains what to test and how to preserve an existing Resolve project. The [setup checklist](docs/setup-checklist.md) covers first-run evidence, audio calibration and paid tests.

## Start a project

Open your host in the studio folder and give it what you know:

```text
Use jiffi-video-studio. Turn this handoff into a production-ready script first.
Audience: first-home buyers. Style: dry comedy. Length: 25–30 seconds.
Deliverable: 1080 × 1920 at 24 fps. Use the attached brand assets.
Propose the sound treatment and cost before generating anything.
```

For an edit-only job:

```text
Make a 60-second product demo from these recordings. No generated footage,
no paid services. Keep the original narration and deliver 16:9 with captions.
```

The agent asks about consequential gaps and proposes a scope. Model clip limits do not set the overall film length. Long projects are broken into sequences and shots, with a total estimate and continuity records.

The studio keeps briefs, source media, renders, audio, edits and exports under `projects/<slug>/`. Tell the agent to “carry on with [slug]” to resume from the brief and gate log. See [workflow and files](docs/workflow.md).

## Audio review is advisory

The optional Gemini helper sends only explicitly selected media and prompts to Google's API. It reads `GEMINI_API_KEY` or `GOOGLE_API_KEY` from the process environment. It does not load private CLI modules or read your host's credential files. OAuth-only Gemini CLI login is not supported. Never put keys in this repository, a prompt or a report.

```sh
node skills/jiffi-video-studio/scripts/gemini-review.mjs --check
node skills/jiffi-video-studio/scripts/gemini-review.mjs \
  --media /path/to/source.wav \
  --prompt skills/jiffi-video-studio/assets/audio-review-prompt.md \
  --model YOUR_AVAILABLE_GEMINI_MODEL \
  --out /path/to/studio/projects/example/brief/qa/review-01 \
  --dry-run
```

Choose a currently available model from the account check. `--dry-run` validates locally without credentials or network use. Removing it makes an API request, requiring media-upload permission and a separate review budget. Each request needs a new output directory; timeouts are recorded as uncertain and are not automatically retried.

This helper can describe audio, but it can also misidentify instruments or miss quiet music. It measures exact digital silence before calling the model. Human feedback, actual playback, signal measurements and model reports remain separate evidence. Read the [review guide](skills/jiffi-video-studio/references/12-audio-video-review.md).

## Development and checks

```sh
python3 -m unittest discover -s tests -v
node --test skills/jiffi-video-studio/scripts/gemini-review.test.mjs
python3 scripts/check_package.py
claude plugin validate . --strict
```

The tests use local synthetic media and mocked API responses. They do not consume generation credits. CI runs the portable tests on macOS and Linux. See [validation status](docs/validation.md) for what was actually exercised, and [security and data handling](SECURITY.md) for publishing boundaries.

MIT licence for this repository's skill, scripts and documentation. Third-party services, applications, source assets and generated outputs retain their own terms. No paid binaries, proprietary fonts, client footage or working-account credentials are included.
