# Stage 3: Previz

Use 3D rehearsal only when camera travel, spatial relationships or occlusion
need testing. Choose the planning method with `07-storyboarding.md` first.
For connected scenes, use `06-direction-and-continuity.md`. A wide shot or
camera move alone does not make a 3D build worthwhile. Direct shots can skip
3D while retaining the continuity checks relevant to their sequence.

## Choose the scene tool

Choose for the required result, rather than making one application mandatory.
For exact placement, persistent objects, repeatable cameras or contact-sensitive
action, prefer an editable local scene when Blender is available. Its geometry,
animation and frame checks can be inspected and repaired without Higgsfield
credits. This still uses local compute and the assistant's service allowance.
Higgsfield 3D Jutsu remains an option for its scene assistant and browser workflow.
Use a small representative pilot when the better route is uncertain. Compare
actual exports before committing a long sequence or dependent shots.

Keep scene construction, export and final generation distinct. A Higgsfield-built
scene rendered in local Blender is a hybrid route. Label it that way. A successful
hybrid does not establish that the browser export worked. Likewise, precise 3D
motion does not prove that a generative video will preserve it. Choose the final
look from inspected outputs, not credit cost alone. Assess visual realism and
performance separately from spatial accuracy. Better framing or lower cost
does not by itself make a route the best-looking result.

## Local Blender

1. Find the installed executable, check its version and verify background rendering
   with a small frame. Use headless Blender where practical; use its GUI or an
   available MCP when inspection or interaction needs it. Do not overwrite an
   unrelated open project.
2. Keep a reproducible scene script and editable `.blend` inside the project.
   Use one coordinate system, stable object names, explicit camera settings and
   a frame-to-time convention. Reuse the scene state across connected shots.
3. For articulated subjects, keep limb lengths fixed. Validate contact constraints,
   support surfaces, release times and settled state where relevant. Simplified
   proxies and animated effects are useful guides, not proof of realistic anatomy
   or a physical simulation. State what they simplify.
4. Render inexpensive opening, interaction and cut-boundary previews. Check the
   image projection: separate floor marks can still produce overlapping silhouettes.
   Repair framing and motion before rendering the full guide. Keep earlier attempts.
   Use the performance guidance in `06-direction-and-continuity.md`. Animate
   weight, preparation, contact, release and recovery where the action needs
   them, plus motivated reactions from other visible characters. If the proxies
   only establish blocking, explicitly let the final generator add appropriate
   gaze, facial expression and small body adjustments within those constraints.
   Avoid asking it to copy rigid proxy poses frame for frame. Use credible scale
   for effects and props: oversized proxy droplets, exaggerated reflections or
   stiff poses can be copied into the final generation. Better preview visibility
   is not a reason to distort an effect that must look natural in the final shot.
5. Audit the saved scene and the encoded guide separately. Check every required
   object's frame margin, state across cuts and the actual visible result. Preserve
   the source when importing a file written by a different Blender version; record
   compatibility warnings and verify recovered animation before relying on it.

## Higgsfield 3D Jutsu

Higgsfield's browser 3D workspace at higgsfield.ai/3d-jutsu. You drive it
with computer control. Its own chat agent builds and edits the scene.

1. Open 3D Jutsu. Inspect the live model and cost controls before submitting a
   scene. Prefer Auto when suitable, but do not assume it is free. Include any
   scene or export charges in the approved budget.
2. Build one master layout for each continuous setting that needs spatial
   rehearsal, with fixed landmarks and action targets. Reuse its geometry
   across connected shots. Different locations or times can use other scenes.
3. Add named proxies for the subjects and relevant objects, if any.
4. For each previz shot, set the camera path and timing. Prompt shape:
   `[duration]s, [required aspect ratio]. [Subject] at [position] does [action].
   CAMERA: [move], starting [position], ending [position], [speed].
   FRAMING: [shot size] throughout.`
5. Press Export to render the camera timeline as video. Move the download
   to `projects/<slug>/previz/<shot id>.mp4`.
6. Check clips in sequence: actor spacing, prop state, eyelines, camera side
   and action outcome match the scene plan. The gesture, target and result must
   read with sound off in each requested format. Inspect the settled result,
   not just the movement towards it. Reject a plan that hides essential evidence.

Keep the 3D Jutsu chat open. Stage 4 may render the final shot in it.

## Tested export path

The setup test needed camera animation directly on the camera object. A
parented orbit with a constraint produced an invalid shared-edit warning and
no usable camera clip in the web editor. After repair, select Camera view,
open Animation and add the camera clip if the timeline is empty. Confirm its
duration and framing before Export. A warning alone does not establish whether
the resulting clip is valid, inspect the exported movement.

Chrome successfully downloaded the MP4 when the in-app browser did not.
Use the user's authorised browser. The automation download event timed out
even though Chrome's download history showed Done, so check the actual file
before repeating an export. Choose Download for the viewport preview, not
Generate for a paid AI video. A nominal five-second preview yielded 149 frames
at 30 fps. Probe the result and normalise to the exact required frame count
before using it as a timed reference. Previz may intentionally have no audio.
Avoid a slow server-side photoreal scene render for a simple blockout when
the browser viewport export is sufficient.

The scene comparison also found that a saved `.blend` could contain correct
camera markers while the web MP4 retained one view and much darker lighting.
Solid studio-shaded internal previews did not validate the lit web export.
Check the downloaded first frame, action, each cut and last frame. Inspect
the browser's actual camera clips, not just `scene.camera` or backend markers.
If the web bridge cannot preserve them, download the editable scene and test
a local Blender export. Keep the failed web file and disclose the hybrid route.
Do not repeatedly spend credits trying to repair a web state that the scene
assistant cannot access because its separate browser is signed out.

A credit limit written in a scene prompt is not a provider-enforced spending
limit. The tested paid agent explicitly could not enforce one. Keep the planned
final-generation budget aside, track settled charges and temporary reservations,
and stop open-ended scene work before it consumes that allowance. Prefer local
construction or a live-verified free mode when paid scene work cannot be bounded
reliably. Reconcile reservations before submitting dependent video jobs.

## Stress-test findings

The September 2026 Blender 5.2 scene agent encountered a legacy
`action.fcurves` error. It repaired the scene through the layered animation
API, using the action layer, strip and channel bag. Ask the scene agent to
inspect its installed API rather than repeatedly running legacy snippets.

Adding a camera clip can preserve an older look-at target or trajectory even
after the scene agent says a new camera is active. Inspect the downloaded
clip, especially its last frame and the prop landing. In the three-character
test, the bucket motion exported but the camera cropped its landing. The
photoreal render therefore used inspected start/end images instead. Do not
feed a known-bad camera guide into a paid render.

If the Chrome extension loses its connection, the authorised native Chrome
controls may still work. Inspect the existing task window, avoid unrelated
tabs, and continue there. For long scene prompts, paste the full text and
verify the visible input and enabled Send control. Setting the value of a
contenteditable field did not update the app, and simulated typing truncated
a long prompt. Confirm a real download exists before repeating an export.

## Fallbacks

- 3D Jutsu unavailable: use the Higgsfield for Blender plugin if installed and
  cleared under the setup requirements. Check current charges before use.
- No 3D: use suitable source frames, sketches or selected keyframes if they
  answer the remaining question. Generate start/end images only when useful
  and supported by the render route. Stills do not establish camera travel
  or physical action. Record what remains untested in `brief.md`.
