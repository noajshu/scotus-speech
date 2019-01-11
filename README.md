# scotus-speech
Corpus of oral arguments (recorded speech + official transcripts) of the Supreme Court of the United States (SCOTUS).

[Demo video here](https://youtu.be/UK5c_uxvUgU)

<!-- ### Identifier: SCOTUS -->
### Summary: Medium-scale (594 hours 42 minutes 13 seconds) corpus of professionally transcribed formal conversational English speech
### Category: Speech
### Lincese: MIT
<!-- ### Download mirrors: TBD -->

## Get the data:
Download the corpus manifest and all utterance audio files
- [default format here](https://drive.google.com/drive/folders/1cX_xf1F01l82dz59X2cIx0NPW5pAkatl?usp=sharing) (download only corpus.uterances.jsonl.gz (16 MB) for corpus text, audio.tar.gz (16 GB) contains all utterances)
- in [kur format here](https://drive.google.com/drive/folders/1OEz5q8Vx_6FQZ6GZlp5PlZbi5yHhYiwf?usp=sharing)

## Regenerate the data:
`bash steps.sh` will run the pipeline (takes a few days 4 cores). It is recommended to run the steps.sh lines one-by-one to make sure there are no intermediate errors.

1. scrape the SCOTUS website
2. download all transcript PDFs and recording MP3s
3. parse PDF transcripts into conversation text, extracting speaker information
4. tokenize transcripts to the word and punctuation level


## About this resource:
Scotus Speech is a collection of oral arguments presented before SCOTUS between 2010 and 2018. The conversations (arguments) are formal dialogues between attorneys (counsel) and justices.

Although the conversations follow some procedural rules and formalities, they are fairly straightforward.

Scotus Speech is inspired by the [LibriSpeech][(http://www.openslr.org/12) project, which produced a free ASR corpus from Project Gutenberg audiobooks.

As all recordings and transcripts are in the public domain [see SCOTUS website](https://www.supremecourt.gov/oral_arguments/availabilityoforalargumenttranscripts.aspx),the <strike>sky</strike> law is the limit for use cases. Here are a few possibilities:

- training & benchmarking:
    - automatic speech recognition (ASR)
    - speaker diarisation 
    - biometric speaker recognition
    - voice synthesis
- full-transcript search of SCOTUS oral arguments
- language modeling of legal dialogue
- academic study of SCOTUS oral arguments
- chatbots / AI

Forced alignment the transcripts to audio is achieved by the [aeneas package](https://www.readbeyond.it/aeneas/).


## Format notes
Each step manipulates data in the [JSON Lines](http://jsonlines.org/) structured data format.
For simple parsing tasks, JSONL format enables...

- fast debugging using [jq](https://stedolan.github.io/jq/)
- small file size (as long as compression is enabled)
- schema flexibility
- portability

It is very easy to export this corpus to formats supported by [Kur](https://kur.deepgram.com/in_depth_examples.html#deepgram10-speech-recognition) and  [Kaldi](http://kaldi-asr.org/doc/data_prep.html). A script `convert_corpus.py` is included that does the job for Kur corpus format.


## Benefits:
- Named (and mostly gendered) speaker labels
- High-quality audio and transcripts
- Punctuation and capitalization
- Public domain data
- Historically significant data
- Some audio contains multiple speakers when the courtroom is rowdy (this may be a disadvantage depending on your ASR goals)

## Disadvantages:
- unaligned transcripts (no word-level timestamps) (coming soon!)
- low diversity in:
    - accents
    - conversation topics
    - conversation styles
- often repeated speakers (the justices)
- some repeated utterances (formal procedure)


## Next Steps
The alignment is very good but not 100% perfect. Espeak gives known failure cases. I would like to configure festival and see if it overcomes these failure cases.
I've tried AWS Polly as the STT backend and found it to work extremely well with no failure cases yet, however the corpus is 35,652,395 characters which would cost about $140 for Polly STT on the whole thing. Before spending on that I want to do some benchmarks / training / data analysis of the corpus to make sure it's ready.
