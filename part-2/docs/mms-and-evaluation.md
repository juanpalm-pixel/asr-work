# MMS fine-tuning, decoding and evaluation

This is the **research-oriented** track after the accessible Whisper demo.

## Core workflow

1. Begin with good audio and the correct aligned transcription tier in ELAN.
2. Prepare one audio segment + one target transcription per row.
3. Preserve original transcriptions; document every normalisation.
4. Create training, validation and held-out test splits, checking speakers and recordings.
5. Load an appropriate pretrained **MMS CTC** ASR checkpoint/processor.
6. Prefer **adapter fine-tuning** for a realistic low-resource Colab exercise; check the checkpoint, tokeniser, vocabulary and licence.
7. Start training; use a previously prepared model/checkpoint to demonstrate inference without waiting.
8. Decode held-out examples and compare hypotheses with reference transcriptions.
9. Report CER/WER and error categories; iterate on segmentation, target consistency, data balance, model and decoding.

The [student Colab notebook](../notebooks/Session_05_MMS_ASR_Colab.ipynb) demonstrates a short MMS adapter run; a trained checkpoint is not included. Students add a **read** Hugging Face token to Colab Secrets as `HF_TOKEN`, then uncomment exactly one FLEURS dataset and MMS language pair: English (`en_us`/`eng`), German (`de_de`/`deu`) or Maltese (`mt_mt`/`mlt`). They should state their chosen language, corpus and settings in their MMS work. The [FLEURS dataset](https://huggingface.co/datasets/google/fleurs) is public and does not itself require a token. Hugging Face's [MMS model documentation](https://huggingface.co/docs/transformers/model_doc/mms) and [MMS adapter fine-tuning tutorial](https://huggingface.co/blog/mms_adapters) provide the model details. Colab's free GPU allocations are variable and not guaranteed.

For larger English, German or Maltese ASR datasets, see [Mozilla Common Voice on Mozilla Data Collective](https://mozilladatacollective.com/datasets?q=common+voice). Mozilla now distributes Common Voice there, rather than from its former Hugging Face dataset repository. Check the chosen release's terms and transcript conventions before using it.

## CTC in one paragraph

Connectionist Temporal Classification (CTC) learns to connect many audio frames to a shorter sequence of target symbols without the researcher annotating the exact time of every symbol. A CTC-trained model can also support **forced alignment** of *known* transcripts to audio, provided the model and tokeniser represent the transcript reliably. Forced alignment is not the same thing as ASR and is not the required introductory task.

## CER and WER

Given reference length `N`, character error rate is:

```text
CER = (substitutions + deletions + insertions) / reference characters
```

WER uses reference words as the denominator instead. These scores may exceed 100% when there are many insertions, and they depend on the *evaluation transcription policy*.

```bash
python scripts/evaluate_cer.py --csv examples/evaluation.example.csv --ref-column reference --hyp-column hypothesis
```

The evaluator uses Unicode code points (not grapheme clusters), makes **no implicit text cleaning**, and computes corpus-level totals rather than averaging row percentages. If you change normalisation for evaluation, document the exact transformation.

**Example systematic failure:** almost all segmental characters are correct but tone letters are routinely omitted. CER might look reasonable, yet the output could be inadequate for tone research.

## Examples and boundary notes

- **Yonghe Qiang:** main teaching example for consistent transcript representation and tone encoding; project-specific source data and maps still need to be supplied.
- **Yongning Na:** DoReCo materials are a separate public resource, not the same corpus. Always cite the dataset correctly and follow its stated terms.
- **Allosaurus:** predicts a phone sequence; do not treat it as an ordinary orthographic ASR transcript or compute orthographic CER without an intentionally comparable reference representation.
- **Beam / language-model decoding:** can help select plausible token sequences, but cannot repair a fundamentally inconsistent target convention.

No private models, media or evaluation results are published here.
