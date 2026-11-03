#!/usr/bin/env python3
"""Slice an existing aligned CSV with ffmpeg into 16 kHz mono WAV clips."""
import argparse
import csv
from pathlib import Path
import re
import shutil
import subprocess

AUDIO_COL_CANDIDATES = ["audio_path", "audio", "wav", "path", "file", "filename"]
START_COL_CANDIDATES = ["start_ms", "start_msec", "start_sec", "start"]
END_COL_CANDIDATES = ["end", "end_ms", "end_msec", "end_sec"]
DUR_COL_CANDIDATES = [
    "dur_ms", "dur_msec", "dur_sec",
    "duration_ms", "duration_msec", "duration_sec",
]

def choose(headers, candidates):
    return next((col for col in candidates if col in headers), None)

def seconds(value, name, unsuffixed):
    units = "ms" if name.endswith(("_ms", "_msec")) else "sec" if name.endswith("_sec") else unsuffixed
    return float(value) / 1000.0 if units == "ms" else float(value)

def safe_stem(text):
    stem = re.sub(r"[^A-Za-z0-9._-]+", "_", text).strip("._")
    return stem or "segment"

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--input", type=Path, required=True)
    ap.add_argument("--output", type=Path, required=True)
    ap.add_argument("--clips-dir", type=Path, required=True)
    ap.add_argument("--unsuffixed-unit", choices=["ms", "sec"], default="sec",
                    help="Unit for ambiguous start/end/dur headings; explicit suffixes override")
    args = ap.parse_args()
    if args.input.resolve() == args.output.resolve():
        ap.error("Input and output must differ")
    if not shutil.which("ffmpeg"):
        ap.error("ffmpeg was not found on PATH")
    with args.input.open(newline="", encoding="utf-8") as stream:
        reader = csv.DictReader(stream)
        headers = reader.fieldnames or []
        rows = list(reader)
    audio_col = choose(headers, AUDIO_COL_CANDIDATES)
    start_col = choose(headers, START_COL_CANDIDATES)
    end_col = choose(headers, END_COL_CANDIDATES)
    dur_col = choose(headers, DUR_COL_CANDIDATES)
    if not audio_col or not start_col or not (end_col or dur_col):
        ap.error(f"Missing audio/start/end-or-duration fields. Found: {headers}")
    args.clips_dir.mkdir(parents=True, exist_ok=True)
    produced = []
    for idx, row in enumerate(rows, 1):
        src = Path(row[audio_col])
        if not src.is_absolute():
            src = args.input.resolve().parent / src
        if not src.is_file():
            ap.error(f"Missing audio source on row {idx}: {src}")
        try:
            start = seconds(row[start_col], start_col, args.unsuffixed_unit)
            stop = seconds(row[end_col], end_col, args.unsuffixed_unit) if end_col and row.get(end_col) else None
            duration = seconds(row[dur_col], dur_col, args.unsuffixed_unit) if dur_col and row.get(dur_col) else None
        except (TypeError, ValueError) as e:
            ap.error(f"Invalid time on row {idx}: {e}")
        length = stop - start if stop is not None else duration
        if start < 0 or length is None or length <= 0:
            ap.error(f"Invalid interval on row {idx}: start={start}, duration={length}")
        identifier = safe_stem(row.get("segment_id") or f"segment_{idx:05d}")
        outfile = args.clips_dir / f"{idx:05d}_{identifier}.wav"
        cmd = ["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-ss", str(start),
               "-i", str(src), "-t", str(length), "-ac", "1", "-ar", "16000",
               "-c:a", "pcm_s16le", str(outfile)]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode:
            ap.error(f"ffmpeg failed on row {idx}: {result.stderr.strip()}")
        outputrow = dict(row)
        outputrow["source_audio_path"] = str(src.resolve())
        outputrow["audio_path"] = str(outfile.resolve())
        produced.append(outputrow)
    names = list(dict.fromkeys(headers + ["source_audio_path", "audio_path"]))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=names)
        writer.writeheader()
        writer.writerows(produced)
    print(f"Created {len(produced)} clips and {args.output}")

if __name__ == "__main__":
    main()
