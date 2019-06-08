# If this breaks (e.g., for 2019 dockets),
# I recommend opening a reproducible issue on github
# or writing from scratch using this as a guide.


import pdftotext
from tools import jsonl
from tqdm import tqdm


all_speakers = set()
def new_speaker_spec(line):
    # a variable amount of whitespace precedes a speaker
    if line.startswith('      ') and ':' in line:
        potential_speaker = line[:line.index(':')]
        if potential_speaker.isupper():
            return potential_speaker.strip()

with jsonl.JRZ('corpus_staging/manifest.jsonl.gz') as manifest:
    num_files = sum(1 for audiofile in manifest)

with jsonl.JRZ('corpus_staging/manifest.jsonl.gz') as manifest:
    with jsonl.JWZ('corpus_staging/corpus.raw.jsonl.gz') as corpus:
        pbar = tqdm(manifest, total=num_files)
        for audiofile in pbar:
            pbar.set_postfix(case=audiofile['case_title']+' '+audiofile['transcript_pdf_path'])
            with open(audiofile['transcript_pdf_path'], 'rb') as pdffile:
                # pdftotext.PDF does not support slicing
                pdf = pdftotext.PDF(pdffile)
                pdf = [page.replace('\xa0', ' ') for page in pdf]
                # some transcripts have a title page that shifts everything by 1
                key_opener = 'in the supreme court of the united states'
                opening_pages = [i for i in range(3) if key_opener in pdf[i].lower()]
                assert len(opening_pages) <= 2
                assert max(opening_pages) <= 1
                pdf = [pdf[i] for i in range(opening_pages[-1], len(pdf))]
                assert key_opener in pdf[0].lower()
                index_pgs = [
                    i for i in range(len(pdf))
                    if pdf[i].count(':') > 50
                ]
                if index_pgs:
                    assert all(index_pgs[i] == index_pgs[i+1] - 1 for i in range(len(index_pgs) - 1))
                content_lines = []
                speakers = []
                max_page = index_pgs[0] if index_pgs else len(pdf)
                page = '\n'.join([line for line in pdf[max_page - 1].split('\n') if line])
                page_number_lines = [
                    j
                    for j, line in enumerate(page.split('\n'))
                    if str(max_page) in line
                    # not a time
                    and line[line.index(str(max_page)) - 1] != ':'
                    # page numbers are at the top or bottom
                    and ((j <= 2) or (j >= len(page.split('\n')) - 2))
                ]
                assert len(page_number_lines) == 1
                page_number_line = page_number_lines[0]
                current_speaker = None
                for i in range(max_page):
                    page = '\n'.join([line for line in pdf[i].split('\n') if line])
                    page = '\n'.join([
                        line for j, line in enumerate(page.split('\n'))
                        if j != page_number_line
                    ])
                    assert len(page_number_lines) == 1, page_number_lines
                    for i, line in enumerate(page.split('\n')[1:-1]):
                        line = line.strip()[len(str(i+1)):]
                        new_speaker = new_speaker_spec(line)
                        if new_speaker is not None:
                            current_speaker = new_speaker
                            all_speakers.add(new_speaker)
                            # hide new speaker from line
                            line = line.replace(new_speaker + ':', '')
                        if line:
                            # print(line)
                            content_lines.append(' '.join(line.split()))
                            speakers.append(current_speaker)
                # closing parenthetical
                assert (')' in content_lines[-1]) or \
                    ('submitted' in content_lines[-1]) or \
                    ('adjourned' in content_lines[-1]) or \
                    ('Reporting Corporation' in content_lines[-1]), content_lines[-100:]
                parenthetical_start = len(content_lines) - next(
                    # typos such as forgotten '(' make this a fuzzy problem
                    k for k in range(1, 4)
                    if ('(' in content_lines[-k]) or ('whereupon' in content_lines[-k].lower())
                )
                assert (
                    content_lines[parenthetical_start].lower()[0] == '('
                    or content_lines[parenthetical_start].lower().split()[0].startswith('whereupon')
                ), content_lines[-100:]
                parenthetical = ' '.join(content_lines[parenthetical_start:])
                content_lines = content_lines[:parenthetical_start]
                speakers = speakers[:parenthetical_start]
                proceedings_line = next(i for i, line in enumerate(content_lines) if 'P R O C E E D I N G S' in line)
                front_matter = content_lines[:proceedings_line]
                content_lines = content_lines[proceedings_line + 2:]
                speakers = speakers[proceedings_line + 2:]
                assert len(speakers) == len(content_lines)
                assert all(speakers), (speakers, audiofile)
                audiofile['transcript'] = {
                    'end_parenthetical': parenthetical,
                    'proceedings': content_lines,
                    'proceedings_speakers': speakers,
                    'front_matter': front_matter
                }
                corpus.dump(audiofile)

with jsonl.JW('corpus_staging/all_speakers.jsonl') as outfile:
    for speaker in all_speakers:
        outfile.dump(speaker)
