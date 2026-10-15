# Setup and host capabilities

This skill uses a shared filesystem workflow. Keep the active studio separate
from the installed skill or plugin cache. In commands below, `<skill>` is the
folder containing this SKILL.md, not a guessed user-home path.

```sh
python3 <skill>/scripts/studio.py init /path/to/studio
python3 <skill>/scripts/studio.py doctor /path/to/studio --mode edit
python3 <skill>/scripts/studio.py smoke
```

`init` preserves existing policy and registry files. Review the generated
policy with the user. No budget or upload authority is created by installation.
`doctor` reports prerequisites; it cannot certify a host connection, account,
successful paid render or creative quality. `smoke` generates and fully decodes
a tiny synthetic H.264/AAC file locally, then runs the delivery checker.

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
- Blender for spatial rehearsal, Google Chrome/Chromium or Resolve titles for exact graphics, as the chosen project needs them.

For Higgsfield, run `higgsfield auth login` and let the user complete the
provider's browser flow. Inspect `workspace list`, select the intended
workspace with `workspace set`, then run `studio.py doctor ... --mode generate
--online`. This sends read-only account/workspace/model queries and suppresses
their private output. Use `--higgsfield-cli /absolute/path/to/wrapper` when the
CLI is not on PATH. Never run a token-display command.

Inspect live model schemas and text-only cost estimates before quoting. A
cost command with media paths may upload media, so clear those inputs first.
Paid tests need their own explicit cap. Preserve reservations and uncertain
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
