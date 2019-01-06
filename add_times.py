from tools import jsonl
import json
from tqdm import tqdm


with jsonl.JRZ('corpus_staging/manifest.jsonl.gz') as manifest:
    num_files = sum(1 for audiofile in manifest)

with jsonl.JRZ('corpus_staging/manifest.jsonl.gz') as infile:
    pbar = tqdm(infile, total=num_files)
    with jsonl.JWZ('corpus_staging/corpus.utterances.jsonl.gz') as outfile:
        for j, audiofile in enumerate(pbar):
            pbar.set_postfix(case=audiofile['case_title'])
            with open(
                audiofile['transcript_pdf_path'] + '.utts.txt.map.json',
                'rb'
            ) as alignmentfile:
                utterances = json.load(alignmentfile)['fragments']
            for i, utterance in enumerate(utterances):
                outfile.dump({
                    'audiofile': audiofile['audio_mp3_path'],
                    'audiourl': audiofile['audio_mp3_url'],
                    'duration': str(round(float(utterance['end']) - float(utterance['begin']), 4)),
                    'start': utterance['begin'],
                    'end': utterance['end'],
                    'utterance_dir': str(j),
                    'utterance_file': str(i) + '.mp3',
                    'text': utterance['lines'][0]
                })
