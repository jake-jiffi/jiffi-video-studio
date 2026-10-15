# Image storyboards: use them when they answer a question

A board is useful when the written plan leaves uncertainty about composition,
visual storytelling, actor/object placement, a transition or a cut. Its value
is resolving that uncertainty before expensive production. It is not a required
deliverable or proof that motion and physics will work.

## Choose the smallest useful visual plan

| Uncertainty | Useful preparation |
|---|---|
| Simple trim, existing interview, straightforward screen capture | A selects/edit list, capture checklist or existing source frames; usually no generated board |
| One shot with a clear action | A composition sketch or reference frame if needed; no panel sequence by default |
| Several connected shots or a precise reveal | Rough image panels in edit order, including important changes and outcomes |
| Rhythm, narration, reading time or a difficult transition | A timed animatic using the panels and scratch audio where relevant |
| Camera travel, occlusion or interacting subjects in a shared space | A layout and, if useful, a short 3D rehearsal |
| Unproven generated motion, contact or a transformation | A short motion pilot after the layout is clear; still panels cannot validate it |

These can be combined where each adds information. For long work, outline the
whole programme and board the uncertain sequences. Do not pay for a polished
panel for every second, or duplicate planning already settled by source media.

## When in the workflow

During concept development, rough sketches or existing stills can resolve an
unclear visual idea. After treatment and visual direction are settled, plan
shot compositions before video generation or a staged shoot. Review adjacent
panels as a sequence and revise the shot plan when they reveal a problem.
Use a timed animatic only when timing is an open question.

Generate polished keyframes only for shots that need them as production inputs.
A style/mood board shows a look; a storyboard shows ordered events; a production
frame controls a particular shot. Do not substitute one for the other.

## Make the board drive production

Use `assets/storyboard-template.md`. Each useful panel has a sequence/shot ID,
frame shape, action phase and approximate time, camera/framing, relevant state,
and a specific visual question. Start, change and result panels may be needed
for one action. Keep notes and arrows separate from clean render inputs.

Derive connected panels from the scene layout and selected references rather
than inventing each composition independently. Inspect the sequence for identity,
geometry, screen direction and understandable changes. Do not preserve a bad
panel just because it looks attractive. Put narrative revisions back into the
shot list and mark dependent panels/prompts stale if a reference changes.

Carry the selected panel into its shot's production record: exact file/version,
intended role and model input field (or `planning-only`). Use a clean, separate
frame at the intended aspect ratio when supplying a start/end image. Do not
send a labelled collage or a rough drawing as a photoreal start frame unless
that is the intended result and the route supports it.

Check the live model schema. A general image reference guides appearance;
a start or end image specifies a different role. Do not promise equivalent
control. Seedance 2.5's CLI schema checked on 24 September 2026 exposes
`start_image` and `end_image` in `omni_reference` mode alongside general
references. Schema support is not proof of faithful motion or composition.
Confirm the current media format, limits and quote before submission.

Review the returned clip against the panel's intended composition and the
action's observable outcome. Also review the actual end state and next cut.
Even matching endpoints cannot establish that the movement between them works.

## Evidence and limits

[Adobe on storyboards](https://www.adobe.com/uk/creativecloud/animation/discover/animation-storyboarding.html)
describes visual planning of shots and events. [Adobe on animatics](https://www.adobe.com/uk/creativecloud/animation/discover/animatics.html)
describes testing timing and flow with a rough timed sequence.

[Runway's image-to-video guide](https://help.runwayml.com/hc/en-us/articles/48324313115155-Image-to-Video-Prompting-Guide)
documents how its input image sets the first frame, including composition and
style. This is evidence for that route, not a guarantee about Higgsfield and
not a recommendation to add a provider. Higgsfield input roles must be checked
through its current schema and observed outputs.

The optional workflow above is a practical application of these sources. It
has not established a measured quality gain or credit saving in this studio.
