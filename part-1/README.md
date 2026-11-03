# Practical walkthrough 1: From a Mandarin-class recording to a text file

This exercise uses five recordings from a Mandarin class. The speech is predominantly Mandarin, with some English. We will run the multilingual **Whisper `small`** model on one short recording, listen to the audio while checking its transcript, then inspect the other four transcripts. Use `small`, not the English-only `small.en` checkpoint.

Put permission-cleared `.m4a` recordings in `data/`. Recordings and generated transcripts are excluded from Git, and reference transcripts are not included. **`speaker_04.m4a` is an example name, not a supplied file:** replace it with the exact name shown by `ls data/*.m4a` when you run a single-file command. Whisper gives the text file the same base name as the audio file.

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

## 2. Check the recording

From `part-1`, confirm the filenames and inspect the short recording:

```bash
ls -lh data/*.m4a
ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1 "data/speaker_04.m4a"
```

`.m4a` works directly: FFmpeg reads the supplied AAC audio for Whisper, so conversion is not required. `ls` confirms the exact filename and extension, and `ffprobe` checks that the audio can be read. To add a file from Windows when using WSL, copy it into `data/` from its `/mnt/c/...` path. If another tool requires WAV, convert a file you are permitted to process to mono, 16 kHz audio:

```bash
ffmpeg -i "data/speaker_04.m4a" -vn -ac 1 -ar 16000 "data/speaker_04.wav"
```

If your source is a video, use the same conversion settings:

```bash
ffmpeg -i "class_video.mp4" -vn -ac 1 -ar 16000 "data/audio.wav"
```

## 3. Inspect the installed CLI, then transcribe

```bash
whisper --help
whisper "data/speaker_04.m4a" --model small --model_dir "results/models" --output_format txt --output_dir "results" --device cpu --fp16 False --task transcribe
```

The installed CLI help is the authority for available options. Look for `--model`, `--model_dir`, `--device`, `--output_format`, `--output_dir`, `--task`, and `--language` before running it. This installed version requires `False` with a capital F for `--fp16`.

| Part | What it asks Whisper to do |
| --- | --- |
| `whisper` | Launch the installed Whisper CLI. |
| `"data/speaker_04.m4a"` | Read this file after replacing the example name. Quotes protect paths containing spaces. |
| `--model small` | Use the multilingual `small` checkpoint. |
| `--model_dir "results/models"` | Keep downloaded model weights in the ignored results folder. |
| `--output_format txt` | Write a plain-text transcript. |
| `--output_dir "results"` | Write the transcript to this folder. |
| `--device cpu` | Run on the CPU. |
| `--fp16 False` | Disable FP16 inference; use the normal FP32 CPU path. |
| `--task transcribe` | Keep speech in its original language rather than translating it. |

With `--output_format txt`, Whisper writes a file such as `results/speaker_04.txt`. The standard CLI has no flag to pick an arbitrary output **filename**. To transcribe all five `.m4a` files without typing their names:

```bash
whisper data/*.m4a --model small --model_dir "results/models" --output_format txt --output_dir "results" --device cpu --fp16 False --task transcribe
```

`--output_format all` is also available if you need SRT, VTT, TSV and JSON alongside the text. Rename a result afterward if needed, for example `mv results/speaker_04.txt results/demo_review.txt`. If you specify `--language Chinese`, you guide detection toward Mandarin; that can also affect English stretches. Compare the output with and without that setting before deciding which is better for this recording.

## 4. Listen, read, and compare

Open the matching file in `results/` in a text editor. Listen to the recording while following the transcript. Check Mandarin words and characters, English phrases, code-switch points, omissions, repetitions, punctuation, and any text produced during silence. Record what you hear before editing the model output.

Whisper writes the generated transcripts to `results/`. If trusted reference transcripts become available, place them in `data/precomputed/` with a clear mapping to the recordings. Use [the comparison sheet](comparison-sheet.md) to note recurring mistakes. Only claim an error when you can check it against the audio or a trusted human transcript.

## Optional: run the large model on an NVIDIA GPU

The CPU environment above installs CPU-only PyTorch, so `torch.cuda.is_available()` returns `False` there even if your computer has an NVIDIA GPU. To use a GPU, create the separate environment from `part-1`:

```bash
conda env create --file environment-gpu.yml
conda activate mandarin-whisper-gpu
python -c "import torch; print(torch.cuda.is_available())"
whisper data/*.m4a --model large --model_dir "results/models" --output_format txt --output_dir "results/gpu" --device cuda --fp16 True --task transcribe
```

The check must print `True` before running Whisper. `--device cuda` selects the NVIDIA GPU. The GPU environment uses the [PyTorch CUDA 12.6 wheel](https://pytorch.org/get-started/previous-versions/), and `results/gpu/` is ignored by Git. The large model can sometimes repeat unrelated text; listen to the recording before using its transcript. If repetition occurs, try rerunning that file with `--condition_on_previous_text False`, then check the new result against the audio.

## Precision: FP32, FP16, and BF16

Floating-point formats trade memory and speed against range and precision. Smaller formats can be useful on supported hardware.

| Format | Size | Exponent / fraction bits | Practical meaning |
| --- | --- | --- | --- |
| FP32 | 32 bits | 8 / 23 | Broad range and relatively high precision; safe CPU choice here. |
| FP16 | 16 bits | 5 / 10 | More fraction precision than BF16, but a smaller numerical range; useful on compatible accelerators. |
| BF16 | 16 bits | 8 / 7 | Similar range to FP32, with less fraction precision than FP16; useful on supported hardware. |

The standard OpenAI Whisper CLI provides `--fp16`, not a `--bf16` switch. On CPU, `--fp16 False` uses FP32. Do not write `--fp16 bf16`.

## Files in this part

- `environment.yml` — complete Conda environment specification for this exercise.
- `environment-gpu.yml` — optional NVIDIA GPU environment for the large model.
- `comparison-sheet.md` — blank worksheet for listening and error analysis.
- `data/README.md` — suggested placement for local recordings and precomputed transcripts.
- `.gitignore` — keeps recordings, transcripts and outputs out of Git.

The [official Whisper README](https://github.com/openai/whisper) documents installation, model choices, and CLI use. Always check your local `whisper --help` for the exact installed options.
