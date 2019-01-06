from tools import jsonl
from uuid import uuid4 as uuid
import os
import shutil


def strip_non_alphanum(string):
    return ''.join(
        c
        for c in string
        if c.isalnum() or c == ' ' or c == "'"
    )

def strip_non_ascii(string):
    return ''.join(c for c in string if 0 < ord(c) < 127)

print('converting to KUR format')
with jsonl.JRZ('corpus_staging/corpus.utterances.jsonl.gz') as infile:
    os.system('mkdir -p outputs/kur/audio')
    with jsonl.JW('outputs/kur/scotusspeech.jsonl') as outfile:
        for utterance in infile:
            utterance_id = str(uuid())
            shutil.copyfile(
                'audio/{}/{}'.format(utterance['utterance_dir'], utterance['utterance_file']),
                'outputs/kur/audio/{}.mp3'.format(utterance_id)
            )
            if any(c.isdigit() for c in utterance['text']):
                continue
            utterance['text'].lower()
            outfile.dump({
                'uuid': utterance_id ,
                'duration_s': round(float(utterance['duration']), 3),
                # leave punctuation for now
                'text': ' '.join(strip_non_ascii(strip_non_alphanum(
                    utterance['text'].lower()
                )).split())
            })