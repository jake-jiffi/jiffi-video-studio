# Stage 4: Render

Use this stage for missing generated shots, in the style specified by the
brief. Supplied footage, graphics and direct capture do not need a paid video
generation. Check captured or supplied media against the same shot purpose.

## Choose the route per shot

Before submission, check connected shots against their scene plan using
`06-direction-and-continuity.md`. Test uncertain high-risk motion before paying
for dependent shots. If a storyboard was useful, carry the selected frame and
its input role into the request using `07-storyboarding.md`. Each connected
shot must continue the intended scene state, including any planned change.

1. Check the live Seedance 2.5 parameters (`higgsfield model list`, then
   `higgsfield model get <model>`). Note the limits on duration,
   image references and video references. They differ by route.
2. **Direct shots:** render with the CLI.
3. **Previz shots:** if the CLI model accepts a reference video, render with
   the CLI and the previz clip attached. If it does not, render in the 3D
   Jutsu chat where the previz lives (drop the cast and location images next
   to the previz and ask it to combine them), or in Higgsfield's web video
   page with the same references.

On the tested CLI schema, Seedance 2.5 uses `mode=t2v` for text only and
`mode=omni_reference` when supplying reference media. The reference mode
accepts image, video and audio references, including existing Higgsfield job
IDs. Check the current schema before reuse. Both an image-reference generation
and a combined 3D-preview-plus-image generation completed during setup.
For several CLI image references, repeat `--image-references <UUID-or-path>` for each item. A comma-joined list was rejected before quoting in the production test.
A text-only cube test returned
`ip_detected` without an output. Record such a result as a failed attempt,
not evidence that authentication or the plan is broken. Do not loop on it.

Probe each downloaded source. The five-second test delivered 121 frames at
24 fps (5.041667 seconds) with 32 kHz AAC audio. Trim to the intended timeline
length and export 48 kHz audio. Do not assume requested duration, sample rate
or image dimensions are delivered exactly. The native 1080p stress test
returned HEVC, while the earlier 720p test used H.264. Probe the codec too.
An audio reference does not guarantee the requested start time. The stress
test moved one line from 0.5s to 3.75s. Build captions and any replacement
dialogue from the actual rendered performance, not the prompt timestamps.

## Shot rules

- Choose shot length for the beat or information. Short generated clips can
  make retries cheaper, but 3 to 8 seconds is a tactic, not a universal rule.
  Check the live model's clip limits. Longer scenes need suitable coverage,
  supported extension or recording, not arbitrary repeated five-second cuts.
- Match the number and type of subjects to the brief. Crowds and many moving
  subjects are harder to control; test or plan coverage that preserves the
  requested content rather than imposing a three-person cap.
- Stage subjects naturally around the action. Check each requested output
  composition before rendering. Use separate coverage or a wider
  portrait picture window if necessary. Do not crowd the cast into the centre
  third just to make one crop work.
- Use real-time or slow motion according to the intent. If fast action fails,
  simplify coverage or choose a better source route within budget. Do not hide
  an essential event or change a factual demonstration to make a render pass.
- Keep native ambience and effects when they sound right. Dialogue is
  handled in Stage 5.
- Prefer real capture or controlled graphics for exact UI, documents, labels
  and instructional text. Do not rely on a generative video to reproduce facts
  or readable interfaces accurately.

## Prompt template

Declare every reference in prose with its tag, and scope it to exactly what
it should control:

```
@image1 is [SUBJECT]: identity, design and surface details only.
@image2 is [SETTING]: layout, landmarks and light only.
@image3 is [OBJECT]: geometry, markings and condition only.
@video1 sets [the specific camera, action or timing it should control].

[Scene in one line.] First frame: [who is where].
Fixed landmarks and action target: [positions that cannot change].
Prop entering: [owner, hand/support, position and condition].
0.0s to 2.0s: [action]. 2.0s to 4.0s: [action].
Visible result: [what proves the action succeeded, with time to read it].
Final state: [actor marks and prop owner, hand/support, position and condition].
Camera: [move]. Light: [look].
Performance: [each relevant character's intention, attention and response to events].
Guide constraints, if used: [marks, contacts, timing and result that must hold].
Performance freedom: [small motivated gestures, gaze and posture the model may add].
Sound, if required: [in-scene or narration, listening perspective, acoustic
setting, continuous ambience and timed effects].
Speech, if required: [established voice, intention, effort and delivery].
[Continuous shot or explicitly planned cuts]. [Required style and exclusions].
```

Use only the fields and references relevant to this shot. A landscape may
have no character or prop state. Use the tag format the route shows (for
example `@image1` or `@Image 1`).
Do not attach a competing room or layout image merely because it is available.
Separate identity, surface design, geometry, motion and lighting roles. If the
3D guide controls geography, another reference must not silently replace it.
Use the reference sheet images for identity. Attach only the references the
shot needs, within the route's limits.
For performing characters, use `06-direction-and-continuity.md` to distinguish
essential action constraints from acting the model can supply. Specify what
listeners notice and how they respond. "Stay on the same mark" must not become
"hold the same pose". A motion guide can define geography and contact while
allowing individual performance; its rigid proxy joints need not be copied.
Use `09-scene-sound.md` for audible shots. Prompted sound treatment is a target,
not evidence the model achieved it; assess the generated audio before deciding
what to retain, replace or mix.

## Review every take

Check the action's required result first, then continuity with the neighbouring
shots: subject positions, eyelines, object ownership and location as applicable.
A plausible movement fails if it does not achieve the required visible result.
Then check faces, hands, object shape, physics, unwanted text/logos, morphing
and timing. Review body language in motion, including waiting and listening
characters. Apply the performance checks in `06-direction-and-continuity.md`.
Compare actual cut-boundary frames, not only individual takes.

A correct 3D guide and an explicit camera prompt do not lock the generated
camera. Compare the final take with the guide at the interaction and settled
result, including the edges of the frame. Reject a take that enlarges subjects
or crops the evidence the shot must show. Check effect scale and material
continuity too: a model can faithfully copy an unrealistic proxy effect while
changing it in the following shot. Repair the guide or reference strategy
before spending on more dependent takes; repeated wording alone is not a fix.

- Small fault in one area: region edit.
- A controlled local composite can preserve an otherwise useful generated
  performance when the fault is confined to a small, trackable area. Keep the
  original take and the edited asset, record the frame range, and compare the
  result with the source. Check tracking, feathered edges, colour, grain,
  blinks and occlusions throughout the affected interval and at the cut.
  Reject the composite if it replaces needed movement with a frozen feature
  or cannot follow the surface naturally. It is a shot-specific option, not
  a substitute for directing the whole performance.
- Bigger fault: re-render with one change to the prompt at a time.
- A completed targeted video edit may preserve the original fault almost
  unchanged. Compare the exact problem interval with its source at useful
  detail. If the edit route cannot alter the relevant performance, record the
  failure and change the reference or performance approach within the budget;
  do not count a new file or successful job as a successful correction.
- Refused by moderation: do not resend the same wording. Describe the
  physical event plainly ("the bottle bursts into foam", "lobs it over the
  partition") and drop violent words like grenade or explosion from the
  prompt. The joke lives in the graphics and edit, not the render prompt.
  A refusal counts as an attempt.
- After at most 4 attempts within the remaining authorised budget, simplify
  the shot (fewer people, slower action, clearer coverage) and note it for the user
  at Gate 3. Tighter framing must still show the action and its required result.

Save the approved take as `renders/<shot id>.mp4`. Log attempts and credits
in `brief.md`.

## Graphics (in parallel)

Build required text, diagrams and overlays as controlled graphics in `graphics/`.
Write them as HTML and render to PNG with headless Chrome
(`--headless --screenshot --window-size=3840,2160`), or build them as Resolve
titles in Stage 5. Use the brief's dimensions and style. Viewer-facing lines
follow the tone and factual requirements in SKILL.md and the project brief.

## Leave useful editorial handles

Requested speech times may be ignored even when the exact line is correct.
In the production pilot a five-second take put the line at 2.75–3.75 seconds; a
six-second repair with an immediate-line instruction put it at 0.71–1.71
seconds. This is observed timing, not a guarantee for another prompt. Quote
a slightly longer source when an important response needs room, then select
the actual performance and update source in-points, captions and joins. Do
not preserve a long empty hold just to match the first timing estimate. Keep
the agreed total runtime unless the user authorises a scope change.

## Compare continuation routes when a join fails

A start-image field can still yield a recomposed first frame. In the production
build, a start/end-image reveal made the background sharp immediately. A
forward `video_extension` request used the actual selected preceding edit as
`--video-references` and the intended wider composition as an image reference.
It returned six seconds of new footage, preserving the prior soft background
at the join and revealing the room gradually. This was better for that take.

Use this as a repair option, not a universal preference. Inspect the live
schema and quote, preserve the accepted input edit, and probe whether the
result contains just the extension or also the input clip. Compare actual
boundary frames, identity, action and final state. Do not hide a visible
continuity fault behind a dissolve without checking the result.
