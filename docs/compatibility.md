# Host compatibility

The shared part is `skills/jiffi-video-studio`: the workflow, templates, Python verifier, setup helper and optional Node audio reviewer. Host metadata changes discovery, not the production rules.

| Host | Package route | Execution boundary |
| --- | --- | --- |
| Codex CLI and desktop local work | OpenAI marketplace/plugin, or `.agents/skills` standalone install | Local CLI/media tools plus whichever browser/MCP tools are actually connected |
| Codex IDE integration | Standalone skill route | Uses that host's terminal/files/tool permissions; do not assume desktop plugins are loaded |
| ChatGPT with local execution | OpenAI-compatible plugin/import route supported by the account | Needs usable local files/commands for this production toolchain, plus explicit desktop app connections |
| ChatGPT web/mobile without execution | Installed skills where supported, or supplied workflow for planning | Concept/script work; no claim of local Resolve, Blender or authenticated CLI access |
| Claude Code local | `.claude-plugin` marketplace or standalone `.claude/skills` | Same local CLI/media tools; configure browser/Resolve access separately |
| Hosted coding sessions | Skill files and installed prerequisites in the hosted environment | Can run tools present there; cannot reach a user's desktop merely because it can run a shell |

No required model brand or model version is hard-coded into the host. Use a capable host model with the tools needed for the work. Historical image/video model names in production notes are examples that require live schema verification.

## Manifest layout

- `plugin.json`: portable Agent Plugins identity, with skills at the standard `skills/` path.
- `.codex-plugin/plugin.json`: OpenAI-compatible presentation and skill-path metadata.
- `.agents/plugins/marketplace.json`: OpenAI repository marketplace.
- `.claude-plugin/plugin.json`: Claude Code plugin identity.
- `.claude-plugin/marketplace.json`: Claude Code repository marketplace.
- `skills/jiffi-video-studio/agents/openai.yaml`: Codex skill display metadata.

No automatic hooks or bundled MCP server are required. The plugin does not claim that Codex's native Resolve tool is a portable server that Claude can install. Claude can use its own trusted MCP connection or Resolve's official local Python scripting API. FFmpeg remains the alternate editing route.

## Updating and uninstalling

For plugin installations, use the host's marketplace refresh/update command and start a fresh session. Codex CLI exposes `codex plugin marketplace upgrade` and `codex plugin add`; Claude Code exposes `claude plugin marketplace update` and `claude plugin update`. Inspect current `--help` if your version differs.

For standalone installs, back up the existing skill folder, remove or move only that installed copy, and rerun the installer. It refuses to merge or overwrite an existing installation. Keep your studio elsewhere, so uninstalling the skill cannot delete your video projects. For a user installation, the skill directories are `~/.agents/skills/jiffi-video-studio` and `~/.claude/skills/jiffi-video-studio`.

GitHub publication does not enrol the plugin in either vendor's reviewed directory. The public repository marketplace is independently installable. OpenAI directory submission and account-dependent import flows are separate steps.

Official references checked for this release: [OpenAI skills](https://learn.chatgpt.com/docs/build-skills), [OpenAI package and marketplace format](https://developers.openai.com/plugins/build/plugins), [OpenAI Claude archive import](https://developers.openai.com/plugins/guides/submit-claude-plugin), [Claude Code plugin discovery](https://code.claude.com/docs/en/plugins).
