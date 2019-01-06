from tools import jsonl
from uuid import uuid4 as uuid
import os
import shutil


print('converting to KUR format')
with jsonl.JRZ('corpus_staging/corpus.utterances.jsonl.gz') as infile:
    os.system('mkdir -p outputs/kur/audio')
    with jsonl.JW('outputs/kur/scotusspeech.jsonl') as outfile:
        for utterance in infile:
            utterance_id = str(uuid())
            outfile.dump({
                'uuid': utterance_id ,
                'duration_s': round(float(utterance['duration']), 3),
                # leave punctuation for now
                'text': utterance['text'].lower()
            })
            shutil.copyfile(
                'audio/{}/{}'.format(utterance['utterance_dir'], utterance_file),
                'outputs/kur/audio/{}.mp3'.format(utterance_id)
            )
