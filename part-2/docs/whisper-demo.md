# Whisper CLI — Mandarin/English demonstration

## Why this demonstration?

A set of five Mandarin-class audio recordings (mostly Mandarin, with passages in English) gives a concrete example of **multilingual ASR and code-switching**. The recordings are not in this public repository. Work with a short, permission-cleared excerpt during class.

One role for AI is **model discovery**: describe the task ("transcribe Mandarin with some English, from a local WAV, save a TXT, run on CPU") and ask for candidate models. Verify the answer in the actual model documentation, installed CLI help and model card, rather than installing an unverified script.

## Run the model

Open a terminal in the directory containing the audio:

```bash
whisper --help
mkdir -p outputs/whisper
whisper "audio.wav" --model small --task transcribe --output_format txt --output_dir outputs/whisper --device cpu --fp16 False
```

| Part | Function |
| --- | --- |
| `whisper` | Run the OpenAI Whisper command-line program |
| `"audio.wav"` | The input recording; quote paths with spaces |
| `--model small` | Choose a multilingual model size; larger often needs more resources |
| `--task transcribe` | Produce transcription, rather than English translation |
| `--output_format txt` | Save a plain-text transcription |
| `--output_dir outputs/whisper` | Save results in this directory |
| `--device cpu` | Use the CPU even if a GPU is not configured |
| `--fp16 False` | Disable half-precision FP16 inference (important for CPU compatibility) |

**Output naming:** Whisper's standard CLI chooses the base filename from the input (e.g., `audio.txt`) and lets you set the output **directory** and **format**, not an arbitrary output filename. Rename afterward if needed: `mv outputs/whisper/audio.txt outputs/whisper/mandarin_demo.txt`.

**Language choice:** without `--language`, Whisper detects a language, but code-switching is still difficult. Forcing `--language zh` assumes Mandarin and might harm English spans. Compare the outputs and audio rather than assuming either setting is automatically correct.

## FP16 versus BF16 versus FP32

| Format | Bits | Exponent bits | Fraction bits | General consequence |
| --- | --- | --- | --- | --- |
| FP32 | 32 | 8 | 23 | Wider range and finer precision; more memory/compute |
| FP16 | 16 | 5 | 10 | Less memory; narrower numerical range; often fast on compatible accelerators |
| BF16 | 16 | 8 | 7 | Less memory; FP32-like exponent range but less precision than FP16 |

`--fp16 False` in Whisper selects the non-FP16 inference path (normally FP32 on CPU). **It does not enable BF16.** The standard `whisper` CLI does not expose an interchangeable `--bf16` switch. BF16 support depends on the framework, hardware and implementation.

## Teaching questions

- Which Mandarin words and English phrases were recognised correctly?
- Were words omitted, translated, repeated or hallucinated during silence?
- What happens if we change `small` to `base` and compare time and output?
- Are punctuation and word breaks part of the signal or decisions made by the system?
- What should be corrected by listening again, rather than by blindly asking AI to rewrite the text?

Read the [official Whisper repository](https://github.com/openai/whisper), including installation requirements, and the local `whisper --help` output.
