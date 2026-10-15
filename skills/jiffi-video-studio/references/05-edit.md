# Stage 5: Sound and edit

Goal: a rough cut the user can react to, then final exports that pass the check.

## Setup

DaVinci Resolve Studio through the DaVinci Resolve MCP. Resolve must be open
with Preferences, System, General, External scripting set to Local. If the
MCP is not connected, drive the Resolve UI with computer control. If Resolve
is unavailable, assemble with ffmpeg and tell the user what is missing (styled
captions, grade, reframe).

## Tested Resolve compatibility

In Resolve Studio 21.1.0.17, loading the setup project in a separate call and
then using `MediaPool.ImportMedia([absolute_path])` worked. The dictionary
form returned `None` and the MediaStorage fallback timed out. Use the working
path-list form on this installation and read back the imported clips.
Verify the current project identity before editing. Save the user's project,
use a separate setup project for checks and restore the original afterwards.
If the current project is a new, empty Untitled Project, create a named test
project first. Calling SaveProject on the unnamed project opened a naming
dialogue and blocked the MCP call during the stress test.

The tested `AppendToTimeline` trim uses an exclusive end: source frames 30
to 330 produced 300 frames, while 30 to 329 produced 299. Read back clip and
timeline durations rather than assuming the convention is stable across versions.

Imported PNG stills used the default 150-frame duration even when a 120-frame
end was requested. For precise timed graphics, render each transparent PNG
as a fixed-length ProRes 4444 MOV with ffmpeg, then import it on V2. This route
was tested with 120 frames at 30 fps, alpha intact and a one-second start offset.
Use the actual timeline frame rate and read back the resulting duration.
Burned-in caption graphics work without FFmpeg's optional `subtitles` filter.
Prepare layouts separately for wide and portrait. Manual crop and Pan were
tested for portrait reframing. Smart Reframe still needs a shot-specific check.

For a local visual repair, compare decoded colours outside the edited region
before and after preparation, then inspect the actual Resolve export. In the
local eye repair, OpenCV's RGB decode of the 10-bit source shifted colour even
though the ProRes output carried Rec.709 tags. Decoding colour with FFmpeg,
specifying the RGB-to-Rec.709 conversion and writing ProRes colour metadata
reduced the measured preparation difference to less than half a value on an
8-bit channel. OpenCV remained useful for geometry tracking. This is a tested
compatibility issue with that path, not a universal rule about either decoder.
Use a new prepared filename when refreshing Resolve, then confirm every
affected timeline uses it. Output tags alone do not establish correct colour.

## Save and recovery

Save the named project and export a `.drp` before trying a media archive.
In the September 2026 stress test, `ArchiveProject` returned null twice,
left an empty `.dra` directory and Resolve stopped running. The `.drp`
recovery worked: relaunch, import under a separate verification name, check
timeline lengths and all media Online, then restore the working project.
Keep source media alongside the project. A `.drp` references media and is
not a self-contained archive. Never report an empty archive directory or
a successful method invocation without read-back as a verified backup.

## Sound

Read `09-scene-sound.md` and the project's sound choices before mixing. Match
dialogue and effects to the intended space and listening perspective. A clean
voice recording alone does not establish that it belongs in the visible scene.

- **Dialogue or narration, when required:** preserve supplied performances.
  For new speech, use the selected speaker's authorised recording, otherwise
  `text2speech_v2` (pick a voice with `higgsfield voices list` and keep it for
  that character in the registry). Check the performance against the visible
  acting, then place it acoustically in the scene. Keep suitable native dialogue
  when its voice, performance, timing and acoustic character fit the plan.
- **Effects and ambience:** keep native Seedance audio where it works. Add
  impacts (whoosh, pop, paper avalanche) from a library the user points you to.
- **Music:** use appropriately sourced and licensed tracks when the brief
  calls for music. If music is unnecessary, omit it without asking for a track.
- **Silent work:** omit audio when specified. Do not add a silent audio stream
  merely to satisfy a checker. The delivery specification records this choice.
- Record every audio source and its licence in `export/credits.md`.
- Preserve separate source and treated tracks where possible. Review a short
  representative passage with picture and an adjacent cut before applying a
  treatment across the project. Then review the complete final mix.

## Check actual dialogue timing

In CLI 1.1.26, `speech2text` and `clip_transcriber` appear in the model
catalogue but `generate create` rejects the data model type before issuing a
job ID. Do not retry that route or infer it works from a successful quote.
Use Resolve `MediaPoolItem.TranscribeAudio()` and `GetTranscription()` for
local word and timing checks. Open the Edit page first. Both exported MP4s
and decoded WAVs returned False/None for transcription while the Deliver page
was active, then transcribed successfully after `resolve.OpenPage("edit")`. Save the source and rendered transcripts.
Convert their timecodes using the relevant clip frame rate.

Compare the exact words and actual performance interval for every speaker.
If using the original preset recording in the edit, align it to that interval
and check its internal word timing. Keep time stretching modest, preserve
short breaths/tails and avoid cutting words at shot boundaries. Large timing
changes need a revised edit or shot, not a forced dub. Remove the replaced
native dialogue so two voices do not overlap. Recheck the exact final export.
Transcription and level measurements do not replace listening or lip-sync
review. Keep their status separate.

The stress test needed phrase-level alignment around a long inserted pause.
Do not stretch that silence into the words. FFmpeg 9.0.2 also produced
untimestamped leading silence after atempo/resampling and adelay, which a
downstream atrim discarded. Adding `asetpts=N/SR/TB` immediately after
adelay restored the delay. Independently assert the output duration and
measure its first sound, then transcribe the corrected file. Use a new media
filename or explicitly refresh Resolve when replacing an imported file, since
it may retain the old duration or transcription.

A narrow full-height portrait crop can lose another speaker or the prop.
Inspect every shot. A deliberate wider picture window with brand-coloured
space for titles and captions is a valid alternative when the story needs
more horizontal space. Verify the actual Resolve export, not just a crop mockup.

## Rough cut

1. Create a Resolve project named `<slug>` with the agreed dimensions and
   frame rate. Normalise mixed sources deliberately. For long work, use
   sequence timelines and a programme timeline, with stable source IDs.
2. Import supplied/captured footage, renders, graphics and audio into bins.
3. Assemble from the shot or edit list. For connected scenes, use the scene
   plan's cut review to check continuity and whether each action reads. For
   other forms, check information order, transitions and factual fidelity.
   Trim excess waiting, while keeping
   the time needed to understand the gesture, physical result and reaction.
   Do not trim away the only proof that an action worked.
4. Lay graphics on V2 where the shot list calls for them. Keep them on their
   own tracks so any alternate formats can be laid out separately.
5. Render `edit/<slug>_rough.mp4`.

## Gate 3 message

Give the user the rough cut's file path and at most three questions about the
actual purpose, pacing or unresolved choices. For long work, checkpoint
representative sequences before assembling the full rough cut, without adding
approval gates unless requested. Ask for missing branding or music only when
the agreed deliverable requires it. Apply his notes. Re-render a shot only if
a note requires it. If the notes
change more than trims and swaps, send a new rough cut before the final.

## Final

1. Meet the delivery specification. Upscaling cannot recover missing detail;
   inspect the result. Match shots in grade where the intended style needs it.
2. Create only the requested variants. For reframed outputs, inspect every
   shot and join; independent edits or cutdowns may have different runtimes.
3. Add only required graphics, captions, branding and end cards. Lay them out
   separately for each shape and keep essential visual evidence clear.
4. Export the files named in `brief/delivery.json`. The standard checked
   profile is MP4, H.264 yuv420p and AAC 48 kHz when sound is required. See
   `08-delivery.md` for duration, shape and silent-output configuration.
5. Finish `export/credits.md`, run the check, and review every actual output.
   For long videos, cover the full runtime in logged ranges and check joins.

## Newly generated music and media format

When original music is within the brief, the existing Higgsfield account can
provide a short cue without adding a separate service. A production test used
`sonilo_music` via the CLI, with prompt and duration parameters. Check its live
schema, quote and current output terms before reuse. Keep the prompt, job ID,
original file and source terms. An original cue is not an existing brand jingle;
record that choice. Avoid requesting a copy of a named artist or composition.
Audio generation and decoding do not establish musical fit or a listening pass.

Probe every downloaded asset before importing it. The tested music job returned
AAC in an MP4/M4A container at 44.1 kHz, despite a planned local WAV filename.
Use the actual container/codec to name or convert the working media; preserve
the original, and export to the delivery sample rate. Do not trust a suffix or
requested duration. Opaque graphic PNGs may be RGB; require alpha only for an
overlay that actually needs transparency.

## Validate prepared media before editor import

Mixed containers can report the same frame rate but use different timebases.
For a local FFmpeg transition, normalise both frame rates and timebases before
`xfade`. In a production revision, native MP4 and prepared ProRes MOV were both
24fps, but 1/90000 versus 1/12288 timebases made the transition encode fail.
Normalising with `fps=24,settb=AVTB` on both inputs repaired that case.

Check the preparation command's exit status before any dependent import. A
failed encode may leave an empty or incomplete file. Probe dimensions, frame
count and timing, and decode a new intermediate before passing it to the
editor. Keep the prior working timeline and sources until the revised project
can be recovered. These are technical checks, not evidence of a convincing
transition or performance.
