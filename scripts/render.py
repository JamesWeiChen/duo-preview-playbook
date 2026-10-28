#!/usr/bin/env python3
"""Render a manifest with real screen recordings; optional official product bezels."""
import argparse
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile


def ffmpeg_path():
    executable = os.environ.get("FFMPEG") or shutil.which("ffmpeg")
    if not executable:
        try:
            import imageio_ffmpeg
            executable = imageio_ffmpeg.get_ffmpeg_exe()
        except ImportError:
            raise SystemExit("Install FFmpeg, set FFMPEG, or pip install imageio-ffmpeg")
    return executable


def run(args, **kwargs):
    subprocess.run(args, check=True, **kwargs)


def render(plan_path, output, mode, font):
    plan_path = plan_path.resolve()
    plan = json.loads(plan_path.read_text())
    root = plan_path.parent
    shots = plan["shots"]
    fade = float(plan.get("transition_seconds", 0.4))
    if len(shots) < 2 or fade < 0 or any(float(s["duration"]) <= 2 * fade for s in shots):
        raise ValueError("Use at least two shots, each longer than twice the transition")
    if any(float(s.get("start", 0)) < 0 for s in shots):
        raise ValueError("Start times must be nonnegative")
    duration = sum(float(s["duration"]) for s in shots) - fade * (len(shots) - 1)
    if not 15 <= duration <= 30:
        raise ValueError(f"This preset requires 15–30 seconds; got {duration}")
    for s in shots:
        if not (root / s["file"]).is_file():
            raise FileNotFoundError(root / s["file"])
        if mode == "official" and not (root / plan["bezels"][s["display"]]["file"]).is_file():
            raise FileNotFoundError("Missing official bezel; see docs/assets.en.md")
    if not font.is_file():
        raise FileNotFoundError(font)
    if output.exists():
        raise FileExistsError(f"Choose a new output name: {output}")
    output.parent.mkdir(parents=True, exist_ok=True)
    ff = ffmpeg_path()
    with tempfile.TemporaryDirectory(prefix="duo-preview-") as temporary:
        work = Path(temporary)
        # Safe relative filter paths: no shell interpolation and no caption string in filters.
        shutil.copyfile(font, work / "font.ttf")
        clips = []
        for i, s in enumerate(shots):
            (work / "caption.txt").write_text(s["caption"], encoding="utf-8")
            cmd = [ff, "-hide_banner", "-loglevel", "error", "-y"]
            if s.get("kind") == "still":
                cmd += ["-loop", "1", "-framerate", "30"]
            cmd += ["-i", str((root / s["file"]).resolve())]
            pre = f"fps=30,trim=start={float(s.get('start', 0))}:duration={float(s['duration'])},setpts=PTS-STARTPTS"
            if mode == "official":
                b = plan["bezels"][s["display"]]
                bw, bh = map(int, b["canvas"])
                x, y, sw, sh = map(int, b["screen"])
                if min(bw, bh, sw, sh) <= 0 or min(x, y) < 0 or x + sw > bw or y + sh > bh:
                    raise ValueError("Invalid bezel screen rectangle")
                cmd += ["-loop", "1", "-i", str((root / b["file"]).resolve())]
                # Contain and pad rather than stretching a mismatched source aspect ratio.
                scale = float(plan.get("bezel_scale", 0.336))
                dw, dh = int(bw * scale) // 2 * 2, int(bh * scale) // 2 * 2
                if dw <= 0 or dh <= 0 or dw > 1920 or dh > 782:
                    raise ValueError("Bezel scale does not fit output canvas")
                filters = f"[0:v]{pre},scale={sw}:{sh}:force_original_aspect_ratio=decrease,format=rgba,pad={sw}:{sh}:(ow-iw)/2:(oh-ih)/2,setsar=1[v];color=c=0xeef1f5:s={bw}x{bh}:r=30[bg];[bg][v]overlay={x}:{y}:shortest=1[s];[s][1:v]overlay=0:0:shortest=1,scale={dw}:{dh}:flags=lanczos"
            else:
                filters = f"[0:v]{pre},scale=1800:760:force_original_aspect_ratio=decrease:force_divisible_by=2:flags=lanczos,setsar=1"
            filters += ",pad=1920:886:(ow-iw)/2:104:color=0xeef1f5,drawtext=fontfile=font.ttf:textfile=caption.txt:expansion=none:fontsize=44:fontcolor=0x17212f:x=(w-text_w)/2:y=26[out]"
            encoded = work / f"encoded-{i}.mp4"
            cmd += ["-filter_complex", filters, "-map", "[out]", "-t", str(s["duration"]), "-an", "-r", "30", "-fps_mode", "cfr", "-c:v", "libx264", "-preset", "fast", "-crf", "18", "-pix_fmt", "yuv420p", str(encoded)]
            run(cmd, cwd=work)
            normalized = work / f"clip-{i}.mp4"
            # Pixels have already been rotated by FFmpeg. Clear the inherited display matrix.
            run([ff, "-hide_banner", "-loglevel", "error", "-y", "-display_rotation", "0", "-i", str(encoded), "-c", "copy", str(normalized)])
            clips.append(normalized)
        cmd = [ff, "-hide_banner", "-loglevel", "warning", "-y"]
        for clip in clips:
            cmd += ["-i", str(clip)]
        cmd += ["-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo"]
        filters, last, offset = [], "0:v", float(shots[0]["duration"])
        if fade:
            for i in range(1, len(shots)):
                offset -= fade
                filters.append(f"[{last}][{i}:v]xfade=transition=fade:duration={fade}:offset={offset}[x{i}]")
                last = f"x{i}"
                offset += float(shots[i]["duration"])
        else:
            filters = ["".join(f"[{i}:v]" for i in range(len(shots))) + f"concat=n={len(shots)}:v=1:a=0[all]"]
            last = "all"
        result = work / "result.mp4"
        cmd += ["-filter_complex", ";".join(filters), "-map", f"[{last}]", "-map", f"{len(clips)}:a", "-t", str(duration), "-r", "30", "-fps_mode", "cfr", "-c:v", "libx264", "-preset", "medium", "-profile:v", "high", "-level:v", "4.0", "-b:v", "11M", "-minrate", "11M", "-maxrate", "11M", "-bufsize", "22M", "-x264-params", "nal-hrd=cbr", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "256k", "-ar", "48000", "-ac", "2", "-movflags", "+faststart", str(result)]
        run(cmd)
        shutil.copyfile(result, output)
    print(json.dumps({"file": str(output), "planned_seconds": duration, "mode": mode}))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("plan", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--mode", choices=["plain", "official"], default="plain")
    parser.add_argument("--font", type=Path, default=Path("/System/Library/Fonts/STHeiti Medium.ttc"))
    args = parser.parse_args()
    render(args.plan, args.output.resolve(), args.mode, args.font)
