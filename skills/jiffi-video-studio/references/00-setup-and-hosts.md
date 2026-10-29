# Setup and host capabilities

This skill uses a shared filesystem workflow. Keep the active studio separate
from the installed skill or plugin cache. In commands below, `<skill>` is the
folder containing this SKILL.md, not a guessed user-home path.

## Stage 0: guide the user through setup

Run this before the first production, when the host changes, or when a required
integration fails. Do not make a returning user complete onboarding again.

1. **Inspect before asking.** Read the current request, studio policy, project
   brief and `setup/status.md` if present. Detect the operating system, working
   folder and actual file/shell tools. Check available integrations without
   opening unrelated signed-in services. Do not infer desktop access from a
   cloud shell, or a CLI login from a signed-in website.
2. **Choose the minimum route.** Planning needs no generation account, editor
   or media tools. Supplied-footage editing needs local media tools and the
   chosen editor. Generation adds the approved provider account and workspace.
   Blender, browser capture and Gemini review are conditional choices, not
   prerequisites for every video. If the route is unclear, ask whether the user
   wants a script, an edit of their footage, new generated footage or a mixture.
3. **Ask only for consequential gaps.** Use one short batch of up to three
   questions, then follow up only where the answer creates a real dependency.
   A concept can be enough to start planning. Do not demand a completed form.

| Missing detail | What to ask or do |
| --- | --- |
| Studio folder or execution access | Use the selected folder if suitable. Otherwise ask where to keep the project. If file/command access is absent, explain how to continue in a connected local Codex or Claude Code session. Keep developing the script in the meantime. |
| Creative inputs | Ask for the concept or source footage, audience, target length and destination only when not supplied. Propose sensible creative defaults at Gate 1. Request brand files, references or captions only when relevant. |
| Tool preference | Offer the available edit route. Ask about an existing Resolve installation or browser preference only if the project needs it and inspection cannot settle it. |
| Provider or workspace | Ask which approved service and workspace to use if ambiguous. Offer to start its sign-in flow. Do not request email addresses, passwords, cookies, recovery codes or tokens. |
| Spending and media authority | Resolve missing provider permissions, source rights and a cap before the action they authorise. State currency or credits and what the cap covers. Existing explicit approval counts; available account balance is not a budget. |
| Optional audio/video reviewer | Explain the extra provider, selected-media upload and separate cost before enabling it. If chosen, guide private key configuration and verify access without displaying the key. |

4. **Repair what is missing.** Initialise a separate studio and run `doctor`
   for the chosen route. Turn each relevant `next_steps` item into a concrete
   instruction with its purpose, who acts and the verification to run next.
   Perform authorised local setup yourself where tools permit it. Give the
   user only the steps that need their sign-in, administrator access or host
   configuration. Do not buy software, change a subscription or launch a paid
   job as an implicit setup repair. If installation is blocked, keep useful
   planning work moving and record the specific dependency.
5. **Verify and remember.** Run the relevant checks below after each repair.
   Update local `setup/status.md`, created by `init` from
   `../assets/setup-status-template.md`. Keep versions, route choices, workspace
   selection confirmation and pass/fail/not-tested evidence, never raw account
   responses or secret values. On later runs, reuse that record and recheck
   affected capabilities when the host, tool version, workspace or route changes,
   or authentication fails. Budgets remain project-specific.

End setup with a short account of what works, what needs the user's action and
what happens next. Distinguish “ready to plan”, “local edit checked” and “selected
generation route checked”. Do not label everything ready because `doctor`
exited successfully. Pause only work that depends on a missing prerequisite;
Stage 0 is not an additional creative approval gate.

## Local checks and repair steps

Substitute the actual installed skill and selected studio paths. Quote paths
containing spaces. On Windows, use the available Python launcher, such as
`py -3`, in place of `python3`. If Python is absent, help install it before
attempting these commands. When the provider CLI is a local wrapper, substitute
its quoted executable path in the login and workspace commands too.

```sh
python3 "<skill>/scripts/studio.py" init "/path/to/studio"
python3 "<skill>/scripts/studio.py" doctor "/path/to/studio" --mode edit
python3 "<skill>/scripts/studio.py" smoke
```

`init` preserves existing policy and registry files. Review the generated
policy with the user. No budget or upload authority is created by installation.
`doctor` reports prerequisites; it cannot certify a host connection, account,
successful paid render or creative quality. `smoke` generates and fully decodes
a tiny synthetic H.264/AAC file locally, then runs the delivery checker.
For planning-only work use `--mode plan` and skip `smoke`. Do not install media
dependencies just to write a script. For generation, start offline, then use
`--mode generate --online` after the intended provider's login is complete.

| Problem | Specific setup help | Verify afterwards |
| --- | --- | --- |
| Python missing or too old | Use the [official Python installer](https://www.python.org/downloads/) or the user's existing package manager. Ensure the chosen launcher is available to the execution host. | Python version is 3.9+; `doctor` runs in that host. |
| FFmpeg or ffprobe missing | Follow an OS-appropriate build/package route on [FFmpeg's download page](https://ffmpeg.org/download.html), including libx264 and AAC. Add the directory containing both executables to PATH. Restart the host if its PATH is stale. | Both version commands succeed, then `smoke` passes. |
| Node missing or below 22 | If selected tools need it, install a supported Node release, version 22 or newer, from [Node.js](https://nodejs.org/en/download). Restart the host if needed. | `node --version` and `doctor`; adapter tests/check when relevant. |
| Higgsfield CLI missing | Use the [official CLI instructions](https://higgsfield.ai/cli). The tested npm route is `npm install -g @higgsfield/cli@1.1.26`. A local wrapper can be passed with `--higgsfield-cli`. | CLI version command, provider login, workspace selection, then online doctor. |
| Higgsfield signed out or wrong workspace | Start `higgsfield auth login`; the user completes browser authentication. Inspect workspace choices locally and confirm the intended one when ambiguous. Use `higgsfield workspace set WORKSPACE_ID`. | Read-only online doctor, followed by current model/schema checks. |
| Gemini key unavailable | Follow Google's [API-key setup](https://ai.google.dev/gemini-api/docs/api-key). Have the user configure `GEMINI_API_KEY` or `GOOGLE_API_KEY` through the host's private environment/secret settings, or their local secret manager. Provide host-specific guidance if asked. Do not put the value in a chat message, command argument, shell history, studio file or repository. | Run `gemini-review.mjs --check` in the actual execution process. Do not use `echo`, `printenv` or inspect credential files. |
| whisper.cpp missing for an edit without Resolve | Install it from the [official project](https://github.com/ggml-org/whisper.cpp) or a package manager (the Homebrew formula is `whisper.cpp`). Download a GGML model such as `ggml-large-v3-turbo-q5_0.bin` from the [model repository](https://huggingface.co/ggerganov/whisper.cpp) to a folder outside the studio and skill. Compare its SHA-256 with the hash Hugging Face lists for that file. | `whisper-cli --help` runs. A short clip with known words and a measured pause transcribes correctly, with `t_dtw` values present (see `05-edit.md`). |
| Resolve, Blender or browser integration unavailable | Use the selected route's connection checks below. If the host cannot reach the user's desktop, explain that limitation and continue planning or offer an available route. | A small real execution check, not just an executable or MCP listing. |

## Host routing

| Capability | Codex / ChatGPT with local execution | Claude Code |
| --- | --- | --- |
| Skill invocation | `$jiffi-video-studio` in Codex; choose the installed skill/plugin in ChatGPT | `/jiffi-video-studio:jiffi-video-studio` for plugin; `/jiffi-video-studio` for standalone |
| Shared commands | Available shell tool | Bash or host shell tool |
| File and image inspection | Available file/image tools | Read and image-aware file tools |
| Browser | Connected host browser tool; prefer user-selected profile | Configured browser integration, or user-assisted login/capture |
| Paid image/video/audio generation | Higgsfield CLI and explicit cap | Same CLI and cap |
| Blender | Headless executable or configured local Blender MCP | Same, if installed |
| Resolve | Native MCP if present, or official local scripting API | Configured MCP or official local scripting API |
| Audio review | Bundled Gemini adapter if authorised; human listening remains necessary | Same adapter and listening requirement |

Tool names are discovered at runtime. No hooks, MCP servers, authentication,
browser extensions or third-party binaries are auto-installed by this plugin.
Do not pretend to have tools that exist only on a different host. A ChatGPT
session without usable execution/file access can develop the brief and script,
but must request a suitable execution environment for rendering. Cloud shell
access alone does not provide access to the user's desktop apps or sign-ins.

## Required and conditional dependencies

- Python 3.9+ for setup, installer and verification. No Python packages are required for these helpers.
- FFmpeg and ffprobe with H.264/AAC support for local editing, smoke tests and technical verification.
- Node.js 22+ for the optional Gemini review adapter and its tests; npm for the documented Higgsfield installation route.
- Higgsfield CLI and a signed-in account/workspace for Higgsfield generation. No account is needed for supplied-footage editing or script-only work.
- Resolve Studio with a verified connection for Resolve edits. FFmpeg is an explicit alternate edit route; do not claim it produced a Resolve project.
- whisper.cpp and a GGML model for dialogue transcription and word timing when Resolve is not the editor.
- Blender for spatial rehearsal, Google Chrome/Chromium or Resolve titles for exact graphics, as the chosen project needs them.

For Higgsfield, run `higgsfield auth login` and let the user complete the
provider's browser flow. Inspect `workspace list`, select the intended
workspace with `workspace set`, then run `studio.py doctor ... --mode generate
--online`. This sends read-only account/workspace/model queries and suppresses
their private output. Use `--higgsfield-cli /absolute/path/to/wrapper` when the
CLI is not on PATH. Never run a token-display command.

Inspect live model schemas and text-only cost estimates before quoting. A
cost command with media paths may upload media, so clear those inputs first.
Paid tests need an explicit cap covering those tests. Reuse an existing setup
or project cap only when its authorisation includes the proposed test. Preserve
reservations and uncertain
jobs in the project ledger rather than resubmitting after a timeout.

## Resolve check

Open Resolve Studio. Follow that installation's bundled Developer/Scripting
README and set external scripting to Local where supported. For Python, use
the official `DaVinciResolveScript.py` module, `scriptapp('Resolve')`, and
`GetProjectManager()`. The scripting module normally lives under:

- macOS: `/Library/Application Support/Blackmagic Design/DaVinci Resolve/Developer/Scripting/Modules`
- Windows: `%PROGRAMDATA%/Blackmagic Design/DaVinci Resolve/Support/Developer/Scripting/Modules`
- Linux: `/opt/resolve/Developer/Scripting/Modules`

Use the README shipped with the installed version for library paths, Python
compatibility and API signatures. A host-native MCP connection is not bundled
for other hosts. Do not invent a package name or silently install a random
bridge. Test import, trim/source endpoints, audio routing, one small export,
full decoding and project reopening in a separate synthetic project. Save and
restore the user's working project. See `05-edit.md` for observed pitfalls.

## Review and evidence

Use `12-audio-video-review.md` for the optional Gemini adapter. Configure keys
outside chat in the execution process environment; the adapter does not reuse
an unrelated CLI's private credential loader. Model IDs are selected from the
current account's available models. No model response establishes final approval.

Write local evidence in `setup/`: versions, executed checks, missing features,
and what still requires a real account, GUI connection or human listening.
Never claim a complete production test from package validation alone.
