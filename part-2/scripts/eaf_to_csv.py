#!/usr/bin/env python3
"""Export ALIGNABLE_ANNOTATION rows from one explicitly selected ELAN EAF tier."""
import argparse
import csv
from pathlib import Path
import xml.etree.ElementTree as ET

FIELDS = [
    "segment_id", "source_eaf", "audio_path", "start_ms", "end_ms",
    "dur_ms", "speaker", "tier", "text_original", "text_target",
]

def convert(eaf_path, tier_id, audio_path):
    root = ET.parse(eaf_path).getroot()
    slots = {}
    for elem in root.findall("./TIME_ORDER/TIME_SLOT"):
        value = elem.get("TIME_VALUE")
        if value is not None:
            slots[elem.get("TIME_SLOT_ID")] = int(value)
    tier = next((t for t in root.findall("./TIER") if t.get("TIER_ID") == tier_id), None)
    if tier is None:
        available = ", ".join(t.get("TIER_ID", "") for t in root.findall("./TIER"))
        raise ValueError(f"Unknown tier {tier_id!r}. Available: {available}")
    speaker = tier.get("PARTICIPANT") or tier_id
    rows = []
    for i, ann in enumerate(tier.findall("./ANNOTATION/ALIGNABLE_ANNOTATION"), 1):
        start = slots.get(ann.get("TIME_SLOT_REF1"))
        end = slots.get(ann.get("TIME_SLOT_REF2"))
        if start is None or end is None or end <= start:
            raise ValueError(f"Missing or invalid time interval in annotation {i}")
        value = ann.find("./ANNOTATION_VALUE")
        text = "".join(value.itertext()) if value is not None else ""
        if not text.strip():
            continue
        rows.append({
            "segment_id": f"{Path(eaf_path).stem}_{i:05d}",
            "source_eaf": str(Path(eaf_path).resolve()),
            "audio_path": str(Path(audio_path).resolve()),
            "start_ms": start, "end_ms": end, "dur_ms": end - start,
            "speaker": speaker, "tier": tier_id,
            "text_original": text, "text_target": text,
        })
    return rows

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--eaf", type=Path, required=True)
    ap.add_argument("--tier", required=True, help="Exact TIER_ID for aligned transcription")
    ap.add_argument("--audio", type=Path, required=True, help="Matching original recording")
    ap.add_argument("--output", type=Path, required=True)
    args = ap.parse_args()
    if not args.eaf.is_file():
        ap.error(f"EAF file missing: {args.eaf}")
    if not args.audio.is_file():
        ap.error(f"Audio file missing: {args.audio}")
    if args.output.resolve() == args.eaf.resolve():
        ap.error("Output cannot overwrite the EAF")
    try:
        rows = convert(args.eaf, args.tier, args.audio)
    except (ET.ParseError, ValueError) as e:
        ap.error(str(e))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)
    print(f"Exported {len(rows)} aligned nonempty annotations to {args.output}")

if __name__ == "__main__":
    main()
