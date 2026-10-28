# Recording and editing workflow

[繁體中文](workflow.zh-Hant.md)

## 1. Decide the deliverable

Keep a marketing demonstration and an App Store submission cut distinct. [Apple's preview guidance](https://developer.apple.com/app-store/app-previews/) emphasizes a cohesive story, actual in-app footage, localized previews and straightforward transitions. Re-check [current specifications](https://developer.apple.com/help/app-store-connect/reference/app-information/app-preview-specifications/) when submitting. At the recorded date: 15–30 seconds, up to 30 fps, 500 MB maximum; Duo supports 1920×886 landscape / 886×1920 portrait. Technical checks alone do not assess editorial or review eligibility.

Use the official-bezel mode for a marketing demonstration. For a store cut start from native app footage, follow current rules, and validate in App Store Connect. Apple-published promotional videos are not proof of what an ordinary app preview may contain.

## 2. Storyboard: one task, two displays

| Shot | Source duration | Visible benefit | English caption |
|---|---:|---|---|
| Closed talk | 4 s | Check details quickly | Closed. Your talk at a glance. |
| Open same talk | 5 s | Agenda and details together | Open. Agenda and details together. |
| Open note editor | 6 s | Reference and writing together | Refer and write, side by side. |
| Close unsaved note | 5 s | Draft retained | Close it. Your draft stays with you. |
| Reopen and save | 7 s | Reference returns; save succeeds | Reopen. Pick up where you left off. |

Four 0.4-second overlaps give 25.4 seconds. Keep UI text readable and captions outside the product. Native fold animation is not visible in `recordVideo`; transitions join separately captured displays. A screenshot hold is acceptable as an explicitly documented editorial choice, not evidence of continuous motion.

## 3. Prepare the app and session

- Use a test fixture/store, fictional data, consistent light/dark appearance and text size. Do not clear personal data to obtain a clean shot.
- In Acadenda, `-ScreenshotTestStore` used an isolated in-memory fixture and `-ScreenshotHideCloudSyncBanner` hid only the screenshot banner. These flags are **app-specific**, not general iOS settings.
- For English, set the app language/locale on launch, use an English sample note, and visually verify the keyboard language. App-language changes alone may not change the keyboard.
- Prefer a stable independently launched app for long capture sequences. A workspace debug session ending may terminate the app. Do not change app code merely to remove capture friction.
- Use fresh UI hierarchy/screenshot observations; verify taps at hierarchy hit points before falling back to screen estimates. After opening or closing, old coordinates and accessibility references are stale.

## 4. Capture a single display

Discover display IDs on your runtime. In our setup, outer was **1**, inner was **3**; do not hardcode these as universal IDs. Screenshot sizes were outer **1398×2034**, inner landscape **2853×2007**. Recording raster sizes could differ slightly due to codec even-dimension constraints and orientation metadata.

```sh
# Replace the UDID, and use the separately installed duoctl.
duoctl -d YOUR_UDID state
duoctl -d YOUR_UDID close
duoctl -d YOUR_UDID screenshot local-assets/before.png

# Run from one terminal; operate the app from another session/tool.
python3 scripts/record.py --device YOUR_UDID --display 1 --seconds 12 local-assets/recordings/outer.mov
```

Read `duoctl state` after folds; it must confirm measured posture and active screen. A completed command does not prove the app layout is correct. Half-fold readings around 91–95° in our runtime were not worth forcing to exactly 90° for this story.

Only one `simctl recordVideo` could own the device at a time. Recording both display IDs simultaneously returned `Resource busy`. Finish the first recorder, fold, verify the app, then record the active display. A recording of an inactive panel froze its previous frame. It did **not** capture a physical hinge movement.

The wrapper sends SIGINT only to the child recorder it created, then waits for container finalization. Never `pkill` all simctl processes. Keep logs and compare app PIDs around each continuity sequence. Permission to install duoctl does not grant future sessions permission to access CoreSimulator.

## 5. Select valid footage

Inspect a contact sheet AND key full-size frames from every source. One of our files encoded successfully but showed SpringBoard for its entire duration after a debugger session ended. We excluded it and used a genuine open-state screenshot hold. The talk and note demonstrations used different launches; the note open→close→open→save sequence remained in one process. Preserve this distinction in the evidence.

A visible keyboard must be real. Verify its presence after every fold and restore keyboard state when finished. Do not draw a keyboard into the app or publish a private helper as a supported Apple API.

Fill `examples/evidence.template.json`: app PID before/after, measured posture, active display, content identity, exact draft text, source files, checks and any restart.

## 6. Edit reproducibly

Use `examples/plan.en.json` or `plan.zh-Hant.json`. Replace paths, trim points and source language. `kind: still` loops a genuine screenshot; do not label it as recorded motion. Keep sources longer than the selected interval. The renderer does not silently fill a short recording to conceal missing footage.

- Apply `fps=30` **before** `trim`: simulator footage can be highly variable-frame-rate during static scenes.
- Let FFmpeg apply input rotation once, then remux the encoded segment with `-display_rotation 0 -c copy`. In our FFmpeg 7.1 run, `-metadata:s:v rotate=0` alone did not remove the retained display matrix.
- Explicitly use `-r 30 -fps_mode cfr` after concatenation/transitions; otherwise time bases produced an unintended output rate.
- Preserve aspect ratio; never stretch an open display into a closed shape. The official mapping is documented in the asset guide.
- H.264 High / Level 4, yuv420p, 11 Mbps target CBR, fast-start MP4; stereo AAC 48 kHz silent track. Silence can encode at a much lower measured bitrate than the requested 256 kbps. Check the applicable upload requirements rather than assuming the command-line target proves audio compliance.
- Captions are UTF-8 text files, with FFmpeg text expansion disabled. Paths are process arguments, not shell interpolation. No arbitrary shell commands in manifests.

## 7. Validate and deliver

Run `scripts/validate.py`. It fully decodes with error escalation, checks this preset's duration/rate/dimensions/rotation, calculates SHA-256 and creates a contact sheet. This is a technical screen, not certification.

Manually confirm: correct app; same selected item; unsaved text visibly retained; correct language and keyboard; captions legible; camera cutout aligned; no clipped controls; final saved note visible; no SpringBoard/dialogs; orientation upright. Inspect transitions in playback, not just still frames. Blank unused tiles at the end of a contact sheet are not necessarily blank frames in the movie.

Keep raw clips, manifests, sensor observations, final exports and reports locally. Publish reusable code/docs and links separately. Do not include Apple source assets or user data in an open-source release. End device interaction sessions and stop only your own recorders.
