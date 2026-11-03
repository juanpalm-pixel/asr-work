# ASR audio and transcripts

Three approximately one-minute examples, one per language. Each clip joins complete recordings from the [FLEURS test mirror](https://huggingface.co/datasets/rasgaard/fleurs_test), derived from [Google FLEURS](https://huggingface.co/datasets/google/fleurs). There is 0.25 seconds of silence between source recordings. The source audio and transcripts are licensed [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/); credit: Conneau et al., *FLEURS: Few-shot Learning Evaluation of Universal Representations of Speech* (2022).

The **reference transcript** below is the dataset’s `raw_transcription` text, in the same order as the joined recordings. It is a published reference, rather than a fresh word-for-word verification by a listener. The **Whisper output** is from the multilingual `small` model; bold text marks recognition errors compared with the reference. Formatting aside, the model text is unchanged.

| Language | Audio | Length | Source recording IDs |
| --- | --- | ---: | --- |
| English | [Play or download English audio](part-1/task-audio/english.wav) | 64.58 s | `en_us_0000`, `en_us_0001`, `en_us_0002`, `en_us_0003`, `en_us_0004`, `en_us_0005`, `en_us_0006` |
| German | [Play or download German audio](part-1/task-audio/german.wav) | 63.10 s | `de_de_0000`, `de_de_0001`, `de_de_0002`, `de_de_0003`, `de_de_0004` |
| Maltese | [Play or download Maltese audio](part-1/task-audio/maltese.wav) | 60.94 s | `mt_mt_0000`, `mt_mt_0001`, `mt_mt_0002`, `mt_mt_0003`, `mt_mt_0004` |

## Whisper settings

OpenAI Whisper `small` (multilingual; `openai-whisper` 20250625), `--task transcribe`, CPU, FP32 (`--fp16 False`), automatic language detection. Each assembled clip was transcribed once as a whole. No text was corrected or removed.

```bash
whisper part-1/task-audio/english.wav part-1/task-audio/german.wav part-1/task-audio/maltese.wav --model small --model_dir part-1/results/models --task transcribe --device cpu --fp16 False --output_format txt --output_dir /tmp/asr-task-whisper
```

## Character error rate

| Language | Character edits | Reference characters | CER |
| --- | ---: | ---: | ---: |
| English | 124 | 818 | 15.16% |
| German | 13 | 715 | 1.82% |
| Maltese | 529 | 588 | 89.97% |

CER is the character-level Levenshtein edit distance divided by the number of reference characters. Both texts were Unicode NFC-normalised and lowercased; punctuation was replaced with spaces, except apostrophes, which were removed. Repeated whitespace was collapsed to one space. Spaces are counted as characters. Each score covers the whole assembled clip.

The Maltese result has no correctly recognised Maltese words, despite its CER being below 100%. One optimal character alignment contains 59 matching characters (including spaces and incidental Latin letters), 178 substitutions, 351 deletions, and no insertions: `(178 + 351) / 588 = 89.97%`. A substitution counts as one edit; CER does not measure whole-word correctness.

## English

**Audio:** [Play or download the English clip](part-1/task-audio/english.wav)

**Whisper `small` output** (recognition errors in bold)

However, due to the slow communication channels, styles in the west could lag behind by 25 to 30 **years**.<br>
All nouns alongside the **world's say** for you always begin with a capital letter, even in the middle of a sentence.<br>
To the north, and within easy reach, is **a** romantic and fascinating town of **Cintra** and which was made famous to foreigners after a **growing** account of its **splinters** recorded by Lord Byron.<br>
The cabbage juice changes color depending on how acidic, **basic, alkaline** the chemical is.<br>
Many people don't think about them as dinosaurs because they have feathers and can **fall**.<br>
The hospital has followed protocol for infection control, including separating the patient from others to prevent possible infection of others.

**Reference transcript** (FLEURS `raw_transcription`, one line per source recording)

```text
However, due to the slow communication channels, styles in the west could lag behind by 25 to 30 year.
All nouns, alongside the word Sie for you, always begin with a capital letter, even in the middle of a sentence.
To the north and within easy reach is the romantic and fascinating town of Sintra and which was made famous to foreigners after a glowing account of its splendours recorded by Lord Byron.
The cabbage juice changes color depending on how acidic or basic (alkaline) the chemical is.
Many people don't think about them as dinosaurs because they have feathers and can fly.
The hospital has followed protocol for infection control, including separating the patient from others to prevent possible infection of others.
The Northern Marianas emergency management office said that there were no damages reported in the nation.
```

**Omitted by Whisper:** **The Northern Marianas emergency management office said that there were no damages reported in the nation.**

## German

**Audio:** [Play or download the German clip](part-1/task-audio/german.wav)

**Whisper `small` output** (recognition errors in bold)

Für die besten Aussichten auf Hongkong sollten sie die Insel verlassen und zum gegenüberliegenden<br>
Ufer von Kowloon fahren.<br>
Er griff auch alles an, was ins Wasser kam. Selbst ein großer Dinosaurier wie der T-Rex war ihm nicht gewachsen.<br>
Wenn Sie den Film Das Vermächtnis der Tempelritter gesehen haben, denken Sie vielleicht, dass auf **der** Rückseite der Unabhängigkeitserklärung eine Schatzkarte gezeichnet wurde.<br>
Es leben noch viele Männer und Frauen, die ihre Zeit überlebt haben und viele weitere mit Angehörigen, die dort ermordet wurden oder sich zu Tode arbeiteten, Juden und nicht Juden gleichermaßen.<br>
Die Höhle befindet sich auf der Spitze eines der Berge nördlich von **Mecca** und ist vom Rest der Welt völlig **insudiert**.

**Reference transcript** (FLEURS `raw_transcription`, one line per source recording)

```text
Für die besten Aussichten auf Hongkong sollten Sie die Insel verlassen und zum gegenüberliegenden Ufer von Kowloon fahren.
Er griff auch alles an, was ins Wasser kam; selbst ein großer Dinosaurier wie der T. Rex war ihm nicht gewachsen.
Wenn Sie den Film „Das Vermächtnis der Tempelritter“ gesehen haben, denken Sie vielleicht, dass auf die Rückseite der Unabhängigkeitserklärung eine Schatzkarte gezeichnet wurde.
Es leben noch viele Männer und Frauen, die ihre Zeit hier überlebt haben, und viele weitere mit Angehörigen, die dort ermordet wurden oder sich zu Tode arbeiteten, Juden und Nichtjuden gleichermaßen.
Die Höhle befindet sich auf der Spitze eines der Berge nördlich von Mekka und ist vom Rest der Welt völlig isoliert.
```

**Omitted by Whisper:** **hier** after “ihre Zeit” in the fourth reference sentence. The reference also writes **Nichtjuden** as one word, while Whisper writes “nicht Juden”.

## Maltese

**Audio:** [Play or download the Maltese clip](part-1/task-audio/maltese.wav)

**Whisper `small` output** (the entire output fails to match the Maltese reference)

**تبع التأكذا يا اسفر لا يشحب الأثنت ستافكم مع مخترتاقة تأكأل، شرف و بورumuгuger**<br>
**Soon after, اقوم بالعمال**<br>
**في شرطة الرج ان تفتحها بقاتل أووقف**<br>
**لكي نريد اطلاق كانت ا Johar**<br>
**كذلك الدان اللقاف**<br>
**السocar**<br>
**س을 تفوق았 الناس**<br>
**الكروطة وحفنة مدهورة الترازبورت**

**Reference transcript** (FLEURS `raw_transcription`, one line per source recording)

```text
Ġeneralment huma jkollhom offerti ta' ikel, xorb u divertiment speċjali, biex iżommu lill-mistiednin f'burdata tajba, u jżommuhom fuq il-post.
Fil-klima sħuna tal-Lvant Nofsani, id-dar ma kinitx daqshekk importanti.
L-iscaffolding mhuwiex metodu ta’ tagħlim iżda, pjuttost, għajnuna li tipprovdi appoġġ lil individwi li għaddejjin minn esperjenza ta’ tagħlim ġdida bħall-użu ta’ programm ġdid tal-kompjuter jew il-bidu ta’ proġett ġdid.
Apparti mill-avveniment ta’ nhar l-Erbgħa, Carpanedo kkompeta f’żewġ tlielaq individwali fil-Kampjonati.
Ġab miegħu l-ferrovija, il-karozza, u ħafna mezzi oħra tat-trasport.
```

The Maltese run was automatically identified by Whisper as Arabic; its output above is shown exactly as produced.

## Source and licence

Source rows are the IDs listed in the table, from the `train` split of the [FLEURS test mirror](https://huggingface.co/datasets/rasgaard/fleurs_test). The mirror retains FLEURS audio and text and cites the [original FLEURS dataset](https://huggingface.co/datasets/google/fleurs). The assembled clips contain 0.25-second silent joins; no source speech was trimmed or reordered. Audio and text: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).
