#!/usr/bin/env python3
"""Corpus-level character and whitespace-token word error rates for paired rows."""
import argparse
import csv
from pathlib import Path

REFERENCE_CANDIDATES = ["reference", "ref", "target", "targ", "target_text", "targ_text", "text_target"]
HYPOTHESIS_CANDIDATES = ["hyp", "hypothesis", "pred", "prediction", "hyp_text", "hypothesis_text", "pred_text", "prediction_text"]

def edit_distance(ref, hyp):
    prev = list(range(len(hyp) + 1))
    for i, ch in enumerate(ref, 1):
        curr = [i]
        for j, other in enumerate(hyp, 1):
            curr.append(min(curr[j - 1] + 1, prev[j] + 1, prev[j - 1] + (ch != other)))
        prev = curr
    return prev[-1]

def evaluate(rows, ref_key, hyp_key):
    total_chars = errors_chars = total_words = errors_words = 0
    count = 0
    for row in rows:
        ref, hyp = row[ref_key] or "", row[hyp_key] or ""
        if not ref:
            raise ValueError("Empty reference found; cannot compute reliable CER")
        count += 1
        total_chars += len(ref)
        errors_chars += edit_distance(ref, hyp)
        rwords, hwords = ref.split(), hyp.split()
        total_words += len(rwords)
        errors_words += edit_distance(rwords, hwords)
    if not count:
        raise ValueError("No rows to evaluate")
    return count, errors_chars / total_chars, errors_words / total_words if total_words else None

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--csv", type=Path, required=True)
    ap.add_argument("--ref-column", required=True, help="Human reference column; never swap with hypothesis")
    ap.add_argument("--hyp-column", required=True, help="Model output column")
    args = ap.parse_args()
    with args.csv.open(newline="", encoding="utf-8") as stream:
        reader = csv.DictReader(stream)
        cols = reader.fieldnames or []
        for key in (args.ref_column, args.hyp_column):
            if key not in cols:
                ap.error(f"Column {key!r} not in {cols}")
        rows = list(reader)
    try:
        count, cer, wer = evaluate(rows, args.ref_column, args.hyp_column)
    except ValueError as e:
        ap.error(str(e))
    print(f"Rows: {count}")
    print(f"Corpus CER: {cer:.4f} ({cer * 100:.2f}%)")
    if wer is not None:
        print(f"Corpus whitespace-token WER: {wer:.4f} ({wer * 100:.2f}%)")
    print("No implicit punctuation, case, tone or Unicode normalisation was applied.")

if __name__ == "__main__":
    main()
