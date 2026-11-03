# Getting unstuck: a reproducible troubleshooting ladder

In class, keep **Terminal 1** for real commands and **Terminal 2** for an AI coding assistant (for example, OpenCode with Ollama). The researcher decides what to do and checks changes before running them.

## Start with the evidence

Record: the exact command, the full error, Python version, current directory (`pwd`), file names (`ls -lah`), environment, and `--help` output. Do not paste private recordings, tokens or confidential transcript contents into public forums or untrusted hosted AI services.

| Symptom | First check |
| --- | --- |
| `whisper: command not found` | Activate the environment; check `python -m pip show openai-whisper` and PATH |
| `ffmpeg not found` or failed audio decoding | Install ffmpeg, run `ffmpeg -version`; check file format |
| Cannot find `audio.wav` | Run `pwd` and `ls`; quote paths containing spaces; remember WSL's `/mnt/c/...` paths |
| `FP16 is not supported on CPU` | Use `--device cpu --fp16 False`; this is FP32, not BF16 |
| Very slow inference | Smaller model, a short clip, and confirmed CPU/GPU choice |
| Whisper misses English insertions | Examine language detection, clip context and code-switching; listen rather than rewriting predictions blindly |
| Empty EAF export / unknown tier | Inspect actual `TIER_ID` values, alignable annotations and time slots |
| Duration out of range | Verify milliseconds vs seconds, the audio length and segment boundaries |
| High CER | Listen to audio, check matching targets, consistent tone symbols, segmentation and held-out speaker overlap |
| Colab session terminates | Save checkpoints frequently where permitted; consider the fallback exercise |

## Where to ask, in order

1. **Local help:** `whisper --help`, `python scripts/eaf_to_csv.py --help` and tracebacks.
2. **README / manuals:** the project repository and package documentation.
3. **Model cards / dataset cards:** on [Hugging Face](https://huggingface.co/models), verify language, licence, intended use, hardware and known limitations.
4. **GitHub Issues / Discussions:** look for version-specific reports; search before opening an issue.
5. **Stack Overflow / relevant Stack Exchange:** for reproducible Python, command-line and OS questions.
6. **Your AI assistant:** ask it to explain the evidence and propose *minimal, reversible* fixes; verify against the above sources.

### Useful AI prompts

- “Explain each argument in this command and which ones affect output format, accuracy or device.”
- “Here is the traceback without private data. What are the three most likely causes? Give read-only checks first.”
- “Find the authoritative README or model card that supports this recommendation.”
- “Suggest a patch that preserves `text_original` and changes only `text_target`.”
- “Why might a corpus show good CER but systematic tone errors?”

Do not pipe unfamiliar internet scripts to a shell without examining what they do. Be wary of AI-suggested `rm -rf`, overwriting files, credential requests and uploading materials.
