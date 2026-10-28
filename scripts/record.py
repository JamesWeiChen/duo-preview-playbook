#!/usr/bin/env python3
"""Record one explicitly selected display; SIGINT only the child recorder on completion."""
import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import signal
import subprocess

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--device", required=True, help="Explicit simulator UDID")
parser.add_argument("--display", type=int, required=True, help="Discover this ID; do not assume 1/3")
parser.add_argument("--seconds", type=float, default=12)
parser.add_argument("output", type=Path)
args = parser.parse_args()
if args.seconds <= 0 or args.output.exists():
    parser.error("Require positive seconds and a new output path")
args.output.parent.mkdir(parents=True, exist_ok=True)
command = ["xcrun", "simctl", "io", args.device, "recordVideo", "--codec=h264", f"--display={args.display}", str(args.output.resolve())]
start = datetime.now(timezone.utc).isoformat()
with args.output.with_suffix(".record.log").open("w") as log:
    child = subprocess.Popen(command, stdout=log, stderr=log)
    try:
        child.wait(timeout=args.seconds)
    except (subprocess.TimeoutExpired, KeyboardInterrupt):
        if child.poll() is None:
            child.send_signal(signal.SIGINT)
        try:
            child.wait(timeout=30)
        except subprocess.TimeoutExpired:
            raise SystemExit(f"Recorder PID {child.pid} did not finish; inspect before stopping it")
metadata = {"started_utc": start, "ended_utc": datetime.now(timezone.utc).isoformat(), "recorder_pid": child.pid, "device": args.device, "display": args.display, "returncode": child.returncode, "app_pid": "record separately before/after fold", "visual_review": "pending"}
args.output.with_suffix(".record.json").write_text(json.dumps(metadata, indent=2))
if child.returncode != 0 or not args.output.exists() or args.output.stat().st_size == 0:
    raise SystemExit("Recording failed; inspect .record.log")
print("Container written. Inspect actual frames before calling this valid app footage.")
