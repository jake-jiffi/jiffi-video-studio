# First-run setup checks

Use this as an evidence checklist. Installed tools and successful logins do not prove the full production route works.

1. Install one skill/plugin copy per host. Confirm the host can discover it and read a referenced file from the installed skill folder.
2. Initialise a separate studio. Set the real provider/data policy, budget and browser preference. Do not assert a clean profile or training-off arrangement without evidence. If your organisation requires them, resolve them before uploads.
3. Run `studio.py doctor` in the intended execution environment. Fix missing dependencies for the route, then run the local `smoke` test. Keep the output in the studio's `setup/` folder.
4. If using Higgsfield, complete its browser login, choose the workspace, and use the online doctor. Then inspect the actual image, video and audio model schemas. Select models available to this account rather than copying historic IDs blindly.
5. If using Resolve, test a separate synthetic project: import a clip, trim to a known frame count, add sound and a graphic, export, decode the whole output, save a DRP and reopen it with its media. Check actual source ranges and frame counts, since API endpoint conventions can vary. Preserve the user's existing project and restore it afterwards.
6. If using Blender, run a small headless render and inspect it. Check scale, camera, lighting and output paths. Installing a Blender MCP does not replace a render check.
7. If using browser capture, verify that the host can read/control the intended browser and save a local output. Login is completed by the user in the provider's flow. Restrict browsing to the authorised sites and task.
8. For the optional Gemini adapter, use its `--check` for model access and `--dry-run` for input validation. Any live review requires clearance for the selected media and a review budget. Calibrate with known material and retain disagreements with the user.
9. If paid generation is needed, ask for a specific setup cap, quote the small synthetic test and reserve the amount before submission. Test the exact reference-media route you intend to use, download and decode the result, then reconcile actual charges/refunds. Do not treat a slow job or transport timeout as a reason to submit a duplicate.
10. Record which routes passed, failed or remain untested. Keep technical checks, source/consent review, continuity, sound fit and continuous playback as separate verdicts.

## What you need to provide for a video

- The concept/handoff or footage, intended audience and communication goal.
- Desired runtime and delivery formats, or permission to propose them.
- Style references and brand assets when relevant.
- Whether dialogue, narration, music and captions are wanted.
- Source permissions, consent for real people, and any provider/data restrictions.
- A project budget for each paid service, plus the review decisions you want to retain or waive.

The skill can develop missing creative details with you. It cannot infer upload authority, a paid budget or authentic consent from a brief attachment.
