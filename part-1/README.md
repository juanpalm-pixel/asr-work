# Practical walkthrough 1: From a Mandarin-class recording to a text file

This exercise uses five recordings from a Mandarin class. The speech is predominantly Mandarin, with some English. We will run the multilingual **Whisper `small`** model on one short excerpt, listen to the audio while checking its transcript, then inspect precomputed transcripts for the other four recordings. Use `small`, not the English-only `small.en` checkpoint.

The recordings and precomputed transcripts are **not included** in this repository. Supply your own permission-cleared files. The commands below use `audio.wav` as an example filename; replace it with the exact name of your excerpt.

## 1. Create the environment (Ubuntu or WSL)

From the repository root:

```bash
cd part-1
conda env create --file environment.yml
conda activate mandarin-whisper-cpu
python --version
python -c "import torch; print(torch.__version__, torch.cuda.is_available())"
ffmpeg -version
whisper --help
```

The Conda specification creates `mandarin-whisper-cpu` in Conda's usual environments directory. It installs Python 3.10, FFmpeg, Whisper and a CPU-only PyTorch build. The [Whisper installation guide](https://github.com/openai/whisper#setup) documents compatibility through Python 3.11. The [PyTorch CPU wheel index](https://pytorch.org/get-started/locally/) avoids downloading GPU runtime packages for this CPU exercise. The version check should print `False` for CUDA availability. If `conda activate` is unavailable in your shell, run `conda init bash`, restart the shell, and retry.

When you return to the exercise later, run `conda activate mandarin-whisper-cpu`. Run `conda deactivate` when finished. The first run of `small` downloads its model weights if they are not already cached, so an internet connection is needed then. CPU transcription may take a while.

## 2. Put the short excerpt in the working directory

Copy the short demo file into `part-1`, without altering the original. In WSL, Windows drives are usually under `/mnt/`; for example:

```bash
cp "/mnt/c/Users/YOUR_NAME/path/to/short_excerpt.wav" "audio.wav"
ls -lh "audio.wav"
ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1 "audio.wav"
```

Replace the source path with your actual file. `ls` confirms the exact filename and extension, and `ffprobe` checks that the audio can be read. An MP3 or other format supported by FFmpeg can also be used; keep its real extension in the Whisper command. If you have a video instead, extract mono, 16 kHz WAV audio from a file you are permitted to process:

```bash
ffmpeg -i "class_video.mp4" -vn -ac 1 -ar 16000 "audio.wav"
```

## 3. Inspect the installed CLI, then transcribe

```bash
whisper --help
whisper "audio.wav" --model small --output_format txt --device cpu --fp16 false
```

The installed CLI help is the authority for available options. Look for `--model`, `--device`, `--output_format`, `--output_dir`, `--task`, and `--language` before running it.

| Part | What it asks Whisper to do |
| --- | --- |
| `whisper` | Launch the installed Whisper CLI. |
| `"audio.wav"` | Read this file. Quotes protect paths containing spaces. |
| `--model small` | Use the multilingual `small` checkpoint. |
| `--output_format txt` | Write a plain-text transcript. |
| `--device cpu` | Run on the CPU. |
| `--fp16 false` | Disable FP16 inference; use the normal FP32 CPU path. |

With `--output_format txt`, Whisper normally writes `audio.txt` in the current directory. The standard CLI has no flag to pick an arbitrary output **filename**. To choose a folder and produce all available formats, including text, SRT, VTT, TSV, and JSON:

```bash
whisper "audio.wav" --model small --output_format all --output_dir "results" --device cpu --fp16 false --task transcribe
```

`--task transcribe` requests speech in the original language rather than English translation. To give the result a different filename, rename it afterward, for example `mv results/audio.txt results/short_excerpt_review.txt`. If you specify `--language Chinese`, you guide detection toward Mandarin; that can also affect English stretches. Compare the output with and without that setting before deciding which is better for this recording.

## 4. Listen, read, and compare

Open `audio.txt` (or `results/audio.txt`) in a text editor. Listen to the short excerpt while following the transcript. Check Mandarin words and characters, English phrases, code-switch points, omissions, repetitions, punctuation, and any text produced during silence. Record what you hear before editing the model output.

Place the four precomputed transcripts in `data/precomputed/`, with a clear mapping to their original recordings. Use [the comparison sheet](comparison-sheet.md) to note recurring mistakes across all five recordings. Only claim an error when you can check it against the audio or a trusted human transcript. The other four transcripts cannot be reviewed here until those files are supplied.

## Precision: FP32, FP16, and BF16

Floating-point formats trade memory and speed against range and precision. Smaller formats can be useful on supported hardware.

| Format | Size | Exponent / fraction bits | Practical meaning |
| --- | --- | --- | --- |
| FP32 | 32 bits | 8 / 23 | Broad range and relatively high precision; safe CPU choice here. |
| FP16 | 16 bits | 5 / 10 | More fraction precision than BF16, but a smaller numerical range; useful on compatible accelerators. |
| BF16 | 16 bits | 8 / 7 | Similar range to FP32, with less fraction precision than FP16; useful on supported hardware. |

The standard OpenAI Whisper CLI provides `--fp16`, not a `--bf16` switch. On CPU, `--fp16 false` uses FP32. Do not write `--fp16 bf16`.

## Files in this part

- `environment.yml` — complete Conda environment specification for this exercise.
- `comparison-sheet.md` — blank worksheet for listening and error analysis.
- `data/README.md` — suggested placement for local recordings and precomputed transcripts.
- `.gitignore` — keeps recordings, transcripts and outputs out of Git.

The [official Whisper README](https://github.com/openai/whisper) documents installation, model choices, and CLI use. Always check your local `whisper --help` for the exact installed options.
