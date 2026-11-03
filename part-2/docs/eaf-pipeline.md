# From ELAN EAF to a clean ASR manifest

## What the steps mean

```text
source recording + ELAN .eaf
  → choose aligned transcription tier and speaker
  → extract time boundaries and the matching text
  → segments.csv
  → documented target normalisation
  → segment-level audio WAV files
  → split by recording / speaker into train, validation, test
```

An `.eaf` can contain multiple annotation tiers for speaker turns, transcriptions, translations and notes. The script here exports **time-aligned annotations on one explicitly selected tier**. It does not infer which tier is correct, resolve reference annotations, transcribe audio, or diarise speakers.

```bash
python scripts/eaf_to_csv.py --eaf data/source_eaf/sample.eaf --tier transcription --audio data/source_audio/sample.wav --output data/segments.csv
```

Always inspect `TIER_ID` inside the EAF file before choosing `--tier`. The source audio path must refer to the matching recording.

## Schema

The default exported table has `segment_id, source_eaf, audio_path, start_ms, end_ms, dur_ms, speaker, tier, text_original, text_target`.

Time boundaries from ELAN are in **milliseconds**. Each aligned annotation must correspond to exactly the speech in its intended segment. The exported `text_target` is initially an exact copy of `text_original` and can be changed only by a later, documented normalisation pass.

Common external duration headers:

```python
DUR_COL_CANDIDATES = [
    "dur_ms", "dur_msec", "dur_sec",
    "duration_ms", "duration_msec", "duration_sec",
]
END_COL_CANDIDATES = ["end", "end_ms", "end_msec"]
```

Some evaluation exports use `hyp`, `hypothesis`, `pred`, `prediction`, `hyp_text`, `hypothesis_text`, `pred_text`, `prediction_text` for **model hypotheses**, whereas `targ`, `target`, `targ_text`, `target_text` usually identify **references**. A parser may recognise several headings, but **reference and hypothesis are not interchangeable**.

Our slicer can recognise common audio, start, duration and end headings; the `--unsuffixed-unit` option specifies whether plain `start`/`end` values are in seconds or milliseconds. Explicit suffixes always take priority.

```bash
python scripts/prepare_segments.py --input data/segments_normalised.csv --output data/clip_manifest.csv --clips-dir data/clips
```

This uses ffmpeg to create 16 kHz mono PCM WAV files. It does not perform VAD or infer speaker turns.

## Normalisation is a linguistic decision

Do **not** globally remove tone markers, aspiration signs or IPA symbols. Ask whether each variation represents a meaningful distinction or an inconsistent encoding practice.

For example, `ma555` and `ma5` may be different encodings of similar tonal information **in a particular project's conventions**. There is no universal rule equating them. Map forms to a controlled tone alphabet only after reviewing the actual transcription policy.

The example configuration is conservative by default:

```bash
python scripts/normalise_manifest.py --input data/segments.csv --output data/segments_normalised.csv --config config/normalisation.example.json
```

It preserves `text_original` and writes `text_target`. Set literal replacements in the JSON only after checking intended meanings; keep the script, config and experiment ID together.

## Quality checks before MMS training

1. Does each clip contain the words in its target transcription?
2. Have recordings, speakers and sessions been split to avoid leakage?
3. Are sampling rate, mono conversion, volume and clipping understood?
4. Are Unicode forms, spaces, tone notation and punctuation consistent and justified?
5. Is the held-out test material genuinely unseen?

**Note:** No supplied CSV or example file contains a real participant recording or transcription.
