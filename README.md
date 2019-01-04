# scotus-speech
Corpus of oral arguments (recorded speech + official transcripts) of the Supreme Court of the United States (SCOTUS).

**Identifier:** SCOTUS
**Summary:** Medium-scale (594 hours 42 minutes 13 seconds) corpus of professionally transcribed formal conversational English speech
**Category:** Speech
**Lincese:** MIT
**Download mirrors:** TBD

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

## How to generate the data
The script `steps.sh` will run the three steps of the pipeline:

1. scrape the SCOTUS website
2. download all transcript PDFs and recording MP3s
3. parse PDF transcripts into conversation text, extracting speaker information
4. tokenize transcripts to the word and punctuation level


## Format notes
Each step manipulates data in the [JSON Lines](http://jsonlines.org/) structured data format.
For simple parsing tasks, this format enables...

- fast debugging using [jq](https://stedolan.github.io/jq/)
- small file size (as long as compression is enabled)
- schema flexibility
- portability

In the future I would like to export this corpus to formats supported by [Kaldi](http://kaldi-asr.org/doc/data_prep.html) and [Kur](https://kur.deepgram.com/in_depth_examples.html#deepgram10-speech-recognition). First we need to run forced alignment and break down the 1 hour oral arguments into 4 - 25 second chunks.

## Benefits:
- Named (and mostly gendered) speaker labels
- High-quality audio and transcripts
- Punctuation and capitalization
- Public domain data
- Historically significant data

## Disadvantages:
- unaligned transcripts (no word-level timestamps) (coming soon!)
- low diversity in:
    - accents
    - conversation topics
    - conversation styles
- often repeated speakers (the justices)
- often repeated utterances (formal proceedings)

## To-dos
The most important next step is to run forced alignment to elucidate word timings. This will enable many of the applications mentioned above.
