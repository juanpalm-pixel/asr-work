#!/usr/bin/env python3
"""Create a documented target transcription without destroying the source text."""
import argparse
import csv
import json
from pathlib import Path
import re
import unicodedata

def normalise(text, cfg):
    form = cfg.get("unicode_form", "NFC")
    if form not in ("NFC", "NFD", "NFKC", "NFKD"):
        raise ValueError(f"Unsupported unicode_form: {form}")
    text = unicodedata.normalize(form, text)
    if cfg.get("strip_outer_whitespace", True):
        text = text.strip()
    if cfg.get("collapse_internal_whitespace", False):
        text = re.sub(r"\s+", " ", text)
    if cfg.get("lowercase", False):
        text = text.lower()
    mapping = cfg.get("replacements", {})
    if not isinstance(mapping, dict) or not all(isinstance(k, str) and isinstance(v, str) and k for k, v in mapping.items()):
        raise ValueError("replacements must map nonempty strings to strings")
    # Literal replacements, longest first. Linguists must review overlapping rules.
    for old in sorted(mapping, key=len, reverse=True):
        text = text.replace(old, mapping[old])
    return text

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--input", type=Path, required=True)
    ap.add_argument("--output", type=Path, required=True)
    ap.add_argument("--config", type=Path, required=True)
    ap.add_argument("--source-column", default="text_original")
    ap.add_argument("--target-column", default="text_target")
    args = ap.parse_args()
    if args.input.resolve() == args.output.resolve():
        ap.error("Input and output must differ: preserve the original file")
    cfg = json.loads(args.config.read_text(encoding="utf-8"))
    with args.input.open(newline="", encoding="utf-8") as stream:
        reader = csv.DictReader(stream)
        if args.source_column not in (reader.fieldnames or []):
            ap.error(f"Missing source column: {args.source_column}")
        names = list(reader.fieldnames or [])
        if args.target_column not in names:
            names.append(args.target_column)
        rows = list(reader)
    for row in rows:
        row[args.target_column] = normalise(row[args.source_column] or "", cfg)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=names)
        writer.writeheader()
        writer.writerows(rows)
    print(f"Normalised {len(rows)} rows (original text retained): {args.output}")

if __name__ == "__main__":
    main()
