from tools import jsonl
from tqdm import tqdm


full_stops = {
    '?', '.', '!'
}

with jsonl.JRZ('corpus_staging/manifest.jsonl.gz') as manifest:
    num_files = sum(1 for audiofile in manifest)

with jsonl.JRZ('corpus_staging/corpus.tokenized.jsonl.gz') as infile:
    pbar = tqdm(infile, total=num_files)
    for audiofile in pbar:
        pbar.set_postfix(case=audiofile['case_title'])
        with open(
            audiofile['transcript_pdf_path'] + '.utts.txt',
            'w'
        ) as outfile:
            utt_count = 0
            current_utt = ''
            for i in range(len(audiofile['transcript']['words'])):
                word = audiofile['transcript']['words'][i]
                if not word['text']:
                    print('ERR')
                    exit(1)
                window = ' '.join(w['text'] for w in audiofile['transcript']['words'][max(0, i-3):i + 3]).lower()
                uninterrupted = ((i == len(audiofile['transcript']['words']) - 1) or ('-' not in audiofile['transcript']['words'][i+1]['text']))
                no_punctuated_atoms = all(
                    punctuated_atom not in window
                    for punctuated_atom in [
                        'i . e .',
                        'e . g .',
                        'u . s .'
                    ]
                )
                # we don't want to start next utt with punctuation
                if len(current_utt) > 16 and word['text'] in full_stops \
                        and uninterrupted and no_punctuated_atoms:
                    current_utt += ' ' + word['text']
                    outfile.write(current_utt.strip() + '\n')
                    utt_count += 1
                    current_utt = ''
                else:
                    current_utt += ' ' + word['text']
            if current_utt:
                outfile.write(current_utt.strip() + '\n')
                utt_count += 1