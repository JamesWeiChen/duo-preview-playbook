# Duo Preview Playbook

[繁體中文](README.zh-Hant.md) · [Workflow](docs/workflow.en.md) · [Official assets](docs/assets.en.md) · [AI instructions](AGENTS.md)

A reproducible field guide for recording and editing foldable iPhone Duo app demonstrations. Developed while making Acadenda's preview on **2026-10-28**, using **Xcode 27.2 RC (27B48), iOS 27.2 Simulator, Apple Silicon macOS 27**. It records what actually worked, what failed, and what future AI assistants should verify.

Show one task continuing across **closed → open → closed → open**. Show what the larger display enables, and prove that an unsaved draft survives. A long recording of an already-open screen does not communicate this benefit.

## Included

- English and Traditional Chinese production guides, pitfalls, licensing/source notes, and a five-shot storyboard.
- Python scripts for single-display capture, manifest-driven FFmpeg editing, full decoding, and contact sheets.
- English and Chinese caption manifests, plus an evidence template for continuity checks.
- AI handoff instructions. No app source code or personal simulator data.

**Apple product images, fonts, FFmpeg binaries, and duoctl are not redistributed.** Official links and exact placement instructions are included. Local recordings and downloaded assets belong in ignored `local-assets/`.

## Quick start

Requirements: Python 3, FFmpeg **7.1 or newer** with `libx264`, `drawtext`, `xfade`, and `-display_rotation`; a font covering the caption language. Capture additionally requires macOS, Xcode, a booted Duo, and a separately installed [duoctl compatibility fork](https://github.com/JamesWeiChen/duoctl).

```sh
# Option A: use an existing FFmpeg on PATH.
# Option B: isolated Python dependency (no vendored executable).
python3 -m venv .venv
.venv/bin/pip install imageio-ffmpeg==0.6.0

# Place your five clips in local-assets/recordings/zh-Hant/.
# Download the two official PNGs as explained in docs/assets.en.md.
.venv/bin/python scripts/render.py examples/plan.zh-Hant.json output/demo-zh-Hant.mp4 --mode official
.venv/bin/python scripts/validate.py output/demo-zh-Hant.mp4 --report output/demo-zh-Hant.validation.json --expected-seconds 25.4
```

`FFMPEG=/absolute/path/to/ffmpeg` overrides discovery. The default font is macOS's STHeiti Medium; use `--font /path/to/font.ttf` elsewhere. Paths in a plan are relative to the plan file. The renderer refuses to overwrite an existing final output. `--mode plain` omits product images; it is not automatic App Store approval.

For English, record the app UI, sample text and keyboard in English, then use `examples/plan.en.json`. Translating captions alone does not create a fully English preview.

## Marketing video versus App Store preview

The official-bezel export is a **marketing demonstration**. Apple's App Preview guidance calls for content within the app. Matching duration, resolution and codec is not proof of review compliance. Maintain a separate app-footage cut for store submission and check current requirements. No export in this project has been represented as approved by App Store review.

## Evidence and limits

The original five-shot cut is 25.4 seconds: 4 + 5 + 6 + 5 + 7 seconds, less four 0.4-second overlaps. The talk's open shot was an actual screenshot hold because its video recorded SpringBoard after a debug session ended. The draft sequence was captured in a separate uninterrupted app process. These are documented rather than concealed.

See [the complete workflow](docs/workflow.en.md), [sources and assets](docs/assets.en.md), and [validation notes](docs/validation.md). Device IDs, private API behavior and bezel dimensions are observations from this setup, not guarantees for future runtimes.

## Credits and license

Original documentation and scripts: Copyright 2026 JamesWeiChen, MIT. [Credits](CREDITS.md) distinguish our work from Apple assets, FFmpeg and duoctl. This is a production playbook, **not a fork of duoctl**. It invokes separately installed tools and includes none of their implementation. Not affiliated with or endorsed by Apple.
