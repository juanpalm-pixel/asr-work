# Session 05 — Data Creation II: ASR

**Duration:** 120 minutes. **Audience:** linguists with no assumed prior ML experience.

## Learning outcomes

Participants should be able to (1) explain ASR versus phone recognition, VAD, diarisation and forced alignment; (2) run a pretrained model from the CLI; (3) see how `.eaf` annotations become segment-level training data; (4) reason about tone, orthography and normalisation; (5) inspect CER and systematic errors; and (6) use AI critically for model discovery and debugging.

## Timetable

| Time | Activity |
| --- | --- |
| 0:00–0:10 | Welcome: practical uses of ASR in documentation and learning |
| 0:10–0:25 | **Lecture 1:** ASR, recognition errors, speech/noise, Whisper and code-switching |
| 0:25–0:45 | **Practical 1:** `whisper --help`, transcribe a short Mandarin/English recording; compare transcript with audio |
| 0:45–1:00 | **Task 1:** Discuss use cases, code-switching and predicted errors |
| 1:00–1:15 | **BREAK** |
| 1:15–1:30 | **Lecture 2:** VAD, diarisation, EAF, data cleaning, tone normalisation, MMS and CER |
| 1:30–1:45 | **Practical 2:** EAF → CSV → normalise → prepare clips → show MMS training configuration/pretrained model |
| 1:45–1:55 | **Task 2:** Find systematic errors, propose fixes, evaluate CER responsibly |
| 1:55–2:00 | Troubleshooting, documentation sources and next steps |

This is a **cooking-show demonstration**: start a training process with prepared material and then evaluate a previously fine-tuned model, rather than waiting during class. A separately tested Colab notebook and checkpoint must be prepared before teaching the full MMS demo.

## Practical 1 — Whisper

Instructor sample: one short, authorized recording from a set of five Mandarin-class audio files, mostly Mandarin with occasional English. The audio is **not stored in this repository**.

```bash
whisper --help
whisper "audio.wav" --model small --output_format txt --output_dir outputs/whisper --device cpu --fp16 False
```

See [Whisper demo](whisper-demo.md) to understand each option. On long recordings or weak CPUs, use a short excerpt or a previously generated output. Compare English insertions, Chinese characters, punctuation and omitted words with the original audio.

### Task 1 — after the practical

1. Where have you already encountered ASR, and when is it useful to a linguist?
2. Did the model keep both Mandarin and English accurately? What did it omit, translate or hallucinate?
3. What evidence suggests an error came from audio quality, model choice, language switching or transcription conventions?
4. What can an AI assistant do for us here, and what decisions must a researcher still check?

## Lecture and practical 2 — low-resource ASR

Explain **VAD** (where speech occurs), **segmentation** (utterance boundaries), **diarisation** (who spoke when), and **forced alignment** (where known text matches the audio). These are related but distinct tasks.

Instructor uses a prepared **Yonghe Qiang pipeline** example. `.eaf` stores time-aligned annotations, an export selects a transcription tier, a CSV manifest maps clips to text, and documented normalisation creates a consistent output inventory. Tone digits and Chao/letter notation should be treated as a linguistic decision, not globally stripped.

```bash
python scripts/eaf_to_csv.py --eaf path/to/recording.eaf --tier transcription --audio path/to/recording.wav --output data/segments.csv
python scripts/normalize_manifest.py --input data/segments.csv --output data/segments_normalized.csv --config config/normalization.example.json
python scripts/prepare_segments.py --input data/segments_normalized.csv --output data/clip_manifest.csv --clips-dir data/clips
```

Show the **MMS CTC adapter training configuration** in a pre-prepared Colab notebook (to be added), explain held-out data, then use a completed model to generate hypotheses and compare CER.

### Task 2 — after the practical

1. Why does the choice of transcription tier matter?
2. What would be the effect of inconsistent `ma5` and `ma555` representations if they were intended to encode the same tone?
3. Which reference/hypothesis errors are systematic? Would you fix audio, segmentation, transcription, data balance, decoding or the model first?
4. If a low CER still masks incorrect tone marking, is the result useful for tone research?

## Post-session reflection (200–500 words)

Preferred: fine-tune an MMS adapter in the **provided/verified** Colab notebook, if a GPU is available. Alternative: run and critically evaluate pretrained Whisper or Allosaurus (note Allosaurus is **phone recognition**, not orthographic ASR). Report the language, source/permissions, transcription method, exact commands, data and normalization, problems, attempted solutions, and error patterns. For ASR, report CER if a valid reference exists; **do not report an orthographic CER between Allosaurus phones and spelling**. Explain what would improve the workflow.

Free Colab GPU access is not guaranteed; assessment should focus on reasoning and reproducibility, not whether a GPU was granted.

Reading list: [references](references.md) and [MMS workflow](mms-and-evaluation.md).
