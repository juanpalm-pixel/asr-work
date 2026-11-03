# Working data are local only

This folder is excluded from Git, apart from this README.

Suggested local layout:

- `data/source_audio/` — original permission-cleared recordings, never modified
- `data/source_eaf/` — original ELAN annotations
- `data/segments.csv` — exported aligned segments
- `data/segments_normalised.csv` — text_original + text_target
- `data/clips/` — derived 16 kHz mono WAV excerpts
- `data/clip_manifest.csv` — one row per clip
- `data/train/`, `data/validation/`, `data/test/` — split manifests

**Do not commit real speech, participant IDs, unpublished transcripts or paths containing personal information without informed permission.** Public teaching examples live in `examples/` and contain invented data.
