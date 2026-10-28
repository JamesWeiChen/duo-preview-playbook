#!/usr/bin/env python3
"""Decode every frame and produce evidence; this is not an App Store approval check."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess
from render import ffmpeg_path

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("video", type=Path)
parser.add_argument("--report", type=Path, required=True)
parser.add_argument("--expected-seconds", type=float, help="Compare to storyboard duration (tolerance: one frame)")
args = parser.parse_args()
video = args.video.resolve()
ff = ffmpeg_path()
probe = subprocess.run([ff, "-hide_banner", "-i", str(video)], capture_output=True, text=True)
decode = subprocess.run([ff, "-hide_banner", "-v", "error", "-xerror", "-i", str(video), "-f", "null", "-"], capture_output=True, text=True)
duration = re.search(r"Duration: (\d+):(\d+):([\d.]+)", probe.stderr)
seconds = sum(float(v) * m for v, m in zip(duration.groups(), [3600, 60, 1])) if duration else None
fps_match = re.search(r"([\d.]+) fps", probe.stderr)
fps = float(fps_match.group(1)) if fps_match else None
rotation = re.search(r"rotation of ([\d.-]+) degrees", probe.stderr)
checks = {
    "full_decode": decode.returncode == 0,
    "duration_15_to_30": seconds is not None and 15 <= seconds <= 30,
    "fps_30": fps == 30,
    "size_1920x886": "1920x886" in probe.stderr,
    "no_nonzero_rotation": rotation is None or abs(float(rotation.group(1))) < 0.01,
}
if args.expected_seconds is not None:
    checks["matches_storyboard_duration"] = seconds is not None and abs(seconds - args.expected_seconds) <= 1 / 30 + 0.001
args.report.parent.mkdir(parents=True, exist_ok=True)
digest = hashlib.sha256()
with video.open("rb") as handle:
    for chunk in iter(lambda: handle.read(1024 * 1024), b""):
        digest.update(chunk)
report = {"file": video.name, "seconds": seconds, "fps": fps, "sha256": digest.hexdigest(), "checks": checks, "probe": probe.stderr, "decode_errors": decode.stderr, "manual_review_required": ["correct app", "language", "same draft across folds", "readable captions", "final saved state"], "app_store_approval": "not assessed"}
args.report.write_text(json.dumps(report, indent=2, ensure_ascii=False))
subprocess.run([ff, "-hide_banner", "-loglevel", "error", "-y", "-i", str(video), "-vf", "fps=1/3,scale=640:-1,tile=3x4", "-frames:v", "1", "-update", "1", str(args.report.with_suffix(".jpg"))], check=True)
print(json.dumps(checks))
raise SystemExit(0 if all(checks.values()) else 1)
