from tools import jsonl
from tqdm import tqdm


exterior_punctuation = [
    '(',
    ')',
    '"',
    ';',
    ':',
    '?',
    '.',
    ','
]

remove_punctuation_on_these = [
    'Mr.', 'Ms.', 'Mrs.',
]
def remove_undesired_punctuation(text):
    for unit in remove_punctuation_on_these:
        text = text.replace(unit, unit[:-1])
    return text

def remove_commas_if_number(word_text):
    if word_text and all(not s.isalnum() for s in word_text) and \
        any(s.isdigit() for s in word_text):
            # likely a number, like $250,000,000
            if word_text[-1] == ',':
                return word_text.replace(',', '') + ','
            else:
                return word_text.replace(',', '')
    else:
        return word_text

def space_adorning_punctuation(word_text):    
    for mark in exterior_punctuation:
        word_text = word_text.replace(mark, ' ' + mark + ' ')
    return word_text

def replace_weird_hyphens(text):
    return text.replace('­', '').replace('-­', '--')

def contains_any(text, contents):
    for c in contents:
        if c in text:
            return True
    return False

procedure_keywords = [
    'BEHALF', 'ARGUMENT', 'REVERSAL',
    'SUPPORT', 'AMICUS', 'CURIAE', 'JUDGEMENT',
    'RESPONDENT', 'PETITIONER', 'APPOINTED', 'FOR',
    'APPELLEE', 'DEFENDING', 'JUDGMENT' # typo
]

standalone_punctuation = [
    '--'
]

with jsonl.JRZ('corpus_staging/manifest.jsonl.gz') as manifest:
    num_files = sum(1 for audiofile in manifest)

with jsonl.JRZ('corpus_staging/corpus.raw.jsonl.gz') as infile:
    with jsonl.JWZ('corpus_staging/corpus.tokenized.jsonl.gz') as outfile:
        pbar = tqdm(infile, total=num_files)
        for audiofile in pbar:
            procedure_keyword_distance_count = 10
            pbar.set_postfix(case=audiofile['case_title'])
            all_words = []
            speakers_to_ints = {
                speaker: i
                for i, speaker in enumerate(set(
                    audiofile['transcript']['proceedings_speakers']
                ))
            }
            ints_to_speakers = {
                i: speaker
                for i, speaker in enumerate(set(
                    audiofile['transcript']['proceedings_speakers']
                ))
            }
            for line, speaker in zip(
                audiofile['transcript']['proceedings'],
                audiofile['transcript']['proceedings_speakers']
            ):
                procedure_keyword_distance_count += 1
                if len(line.strip()) > 4 and line.isupper():
                    if contains_any(line, procedure_keywords):
                        procedure_keyword_distance_count = 0
                        continue
                    elif procedure_keyword_distance_count < 5:
                        print('ignoring due to prior procedural langugage:' + line)
                        procedure_keyword_distance_count += 1
                        continue
                    print('not ignoring:' + line)
                line = remove_undesired_punctuation(line)
                for word_text in replace_weird_hyphens(line).strip().split():
                    if word_text not in standalone_punctuation:
                        word_text = space_adorning_punctuation(
                            remove_commas_if_number(
                                word_text    
                            )
                        )

                    for word_unit_text in word_text.split():
                        all_words.append({
                            'text': word_unit_text,
                            'type': 'symbol' if all(not s.isalnum() for s in word_unit_text) else 'word',
                            'speaker_id': speakers_to_ints[speaker]
                        })

            # we no longer need these
            del audiofile['transcript']['end_parenthetical']
            del audiofile['transcript']['proceedings']
            del audiofile['transcript']['front_matter']
            del audiofile['transcript']['proceedings_speakers']

            audiofile['transcript']['words'] = all_words
            audiofile['transcript']['speaker_names'] = ints_to_speakers
            outfile.dump(audiofile)
