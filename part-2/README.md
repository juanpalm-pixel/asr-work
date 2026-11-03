# ASR Work

A reproducible starter repository for **automatic speech recognition in linguistic research and teaching**. Developed around Session 05 (Data Creation II: Automatic Speech Recognition), with a focus on data preparation, transcription conventions, inference, evaluation, and responsible use of AI assistants.

> **Status:** Teaching/research starter. The local scripts below work without model training, but the MMS fine-tuning notebook and project-specific audio, transcriptions, and checkpoints are **not included yet**. The repo is public: never commit confidential or participant-identifiable recordings.

## Student Google Colab notebook

[**Open Session 05 — MMS ASR in Google Colab**](https://colab.research.google.com/github/juanpalm-pixel/asr-work/blob/main/notebooks/Session_05_MMS_ASR_Colab.ipynb)

The interactive workbook covers environment setup, browsing Hugging Face FLEURS data, your own audio/CSV option, baseline MMS inference, language-specific character vocabularies, basic MMS adapter fine-tuning on a GPU, CER, and saving the adapter. **The GPU training section is opt-in**; check the notebook's data-use warnings before uploading recordings.

## Three connected workflows

1. **Whisper: accessible CLI demo.** Transcribe a Mandarin-dominant class recording with occasional English, inspect the output and its errors. See [Whisper demo](docs/whisper-demo.md).
2. **ELAN → training examples.** Export an aligned transcription tier from `.eaf`, preserve source text, apply *documented* normalisation, and optionally slice audio. See [EAF pipeline](docs/eaf-pipeline.md).
3. **MMS/CTC research workflow.** Fine-tune an existing multilingual speech model using prepared data, evaluate CER/WER on held-out material, and investigate systematic errors. This is the [MMS roadmap](docs/mms-and-evaluation.md), not yet a turnkey fine-tuning script.

The teaching session follows **Welcome → Lecture 1 → Practical 1 → Task 1 → break → Lecture 2 → Practical 2 → Task 2 → troubleshooting** in [Session 05](docs/session-05.md).

## Quick start (Ubuntu / WSL)

```bash
git clone https://github.com/juanpalm-pixel/asr-work.git
cd htr-work
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m unittest discover -s tests -v
```

The EAF export, normalisation and CER evaluation scripts use the Python standard library. To run Whisper, install **ffmpeg** on your system and the optional package:

```bash
sudo apt-get update && sudo apt-get install -y ffmpeg
python -m pip install -r requirements-whisper.txt
whisper --help
whisper "audio.wav" --model small --task transcribe --output_format txt --output_dir outputs/whisper --device cpu --fp16 False
```

Whisper names the result from the input file stem (for example, `outputs/whisper/audio.txt`). To choose a different name, rename/copy it afterward. On a CPU, `small` may be slow. Do not upload classroom recordings without permission.

## From an EAF file to an evaluation

```bash
# Select the precise aligned transcription tier and the matching source WAV.
python scripts/eaf_to_csv.py --eaf "/path/to/recording.eaf" --tier "transcription" --audio "/path/to/recording.wav" --output data/segments.csv

# Inspect the headers and edit the project-specific normalisation config first.
python scripts/normalize_manifest.py --input data/segments.csv --output data/segments_normalized.csv --config config/normalization.example.json

# Requires ffmpeg; creates 16 kHz, mono PCM WAV clips and a new manifest.
python scripts/prepare_segments.py --input data/segments_normalized.csv --output data/clip_manifest.csv --clips-dir data/clips

# Evaluate an already prepared CSV with reference and hypothesis columns.
python scripts/evaluate_cer.py --csv examples/evaluation.example.csv --ref-column reference --hyp-column hypothesis
```

The demonstration data under `examples/` is **synthetic**, not speech recordings or a scientifically meaningful test set. EAF tier names differ by project: replace `transcription` with a real `TIER_ID`.

## Repository map

| Path | Purpose |
| --- | --- |
| `docs/session-05.md` | 120-minute session plan and exercises |
| `docs/whisper-demo.md` | Model selection, CLI flags, CPU/FP16/BF16, Mandarin/English code-switching |
| `docs/eaf-pipeline.md` | Annotation tiers, CSV schema, time units, segmentation and normalisation |
| `docs/mms-and-evaluation.md` | MMS adapter/CTC workflow, dataset splitting, CER and forced alignment |
| `docs/ai-troubleshooting.md` | Error diagnosis with manuals, README, model cards, forums and AI assistants |
| `scripts/` | Local data-preparation and evaluation utilities |
| `config/` | Conservative, explicit normalisation example |
| `examples/` | Fictitious, non-sensitive sample tables |
| `data/` | Local-only working area (contents ignored by Git) |
| `tests/` | Small standard-library regression tests |

## Principles

- **Data quality before model scale.** Check recording quality, segment boundaries, matched transcript, Unicode and tone representation.
- **No destructive cleaning.** Keep `text_original`; create separate `text_target`. Do not remove tone, aspiration, punctuation or capitalization without a research reason.
- **No leakage.** Reserve independent validation/test data and consider speaker/recording overlap.
- **Inspect the actual mistakes.** CER is not sufficient if a low-error model systematically loses a meaningful tone or segment contrast.
- **Human remains responsible.** AI can help discover models or explain commands, but check permissions, model cards, licenses, scripts and suggested shell commands.

## Still to add

- The instructor's permission-cleared Mandarin/English demonstration clips, if they may be shared.
- Specific tier selection and tone mappings for Yonghe Qiang; never guess them from another corpus.
- A tested shared Google Colab notebook for **MMS adapter fine-tuning** and a small pre-trained “finished cake” model.
- Dataset provenance, speaker-safe splits, a model card and error-analysis results.
- A license once the owner chooses one. **No license is granted by default.**

Maintainer: repository owner. Contributions and research practices can be revised as the course develops.
