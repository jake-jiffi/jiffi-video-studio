# Per-project delivery specification

Create `projects/<slug>/brief/delivery.json` from the agreed brief before
editing. Use `assets/delivery.template.json` as a schema example, not as a
default request. Set the filenames, aspect ratios, duration ranges and audio
requirements to this project's actual deliverables.

There is no fixed programme-length limit and no mandatory pair of formats.
A model's generation limit still applies to each source clip. Long work needs
sequence planning, storage, render time and enough budget; it does not become
feasible merely because the checker accepts its requested length.

Version 1 contains `version: 1` and a non-empty `exports` list. For each output:

- `file`: simple MP4 filename within the project's `export/` directory.
- `aspect_ratio`: positive integer pair, such as `1:1`, `16:9` or `9:16`.
- `duration_seconds`: positive finite `min` and `max`. For an exact duration,
  set both to that value. The checker allows one output frame of tolerance.
- `audio`: `required` for an audio stream, or `none` for no audio stream.
- Optional `width` and `height`: both positive integers for exact dimensions.
- Optional `frame_rate`: positive numeric frames per second.
- Optional `duration_group`: shared label only for variants that must match
  within one output frame. A main film and a shorter cutdown need not match.

The checker supports the standard MP4 profile: H.264 yuv420p, square pixels,
rotation baked in, and AAC 48 kHz when audio exists. Different master formats
need separate explicit validation; do not describe them as covered by this
checker. Full decode time scales with clip duration. It must finish successfully
before reporting a technical pass.

Unknown fields, malformed bounds, duplicate filenames and escaped paths are
rejected. Existing projects without a specification retain their old wide and
portrait filename checks, with a warning that the requested runtime and exact
resolution were not verified. Do not use this compatibility path for new work.

Keep an empty studio registry if there are no reusable characters or assets.
Credit actual source media, including recordings and generated components.
For intentional silence, write `Audio: Intentionally silent, no audio track.`
Do not invent a soundtrack to make a check pass.

The spec records requirements; it does not grant permission or prove quality.
Review relevant rights, factual fidelity, captions, story/communication and
continuous playback separately. Silent work still needs visual review.
