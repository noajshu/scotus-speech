import requests
from bs4 import BeautifulSoup
import os
from tools import jsonl



base_url = 'https://www.supremecourt.gov/oral_arguments'

with jsonl.JWZ('corpus_staging/manifest.jsonl.gz') as manifest:
    year = 2010
    while True:
        page = requests.get('{}/argument_audio/{}'.format(base_url, year))
        soup = BeautifulSoup(page.text, 'html.parser')
        counter = 0
        for link in soup.find_all('a'):
            if 'href' not in link.attrs or not link.attrs['href'].startswith('../audio/'):
                continue
            os.system('mkdir -p ./downloads/{}'.format(year))
            counter += 1
            case_title = link.parent.parent.find_all('span')[-1].text
            docket_number = link.text
            print('found Docket Number: {} ({})'.format(docket_number, case_title))
            docket_page = requests.get('{}/audio/{}'.format(
                base_url,
                link.attrs['href'][len('../audio/'):]
            ))
            docket_soup = BeautifulSoup(docket_page.text, 'html.parser')

            mp3_urls = [
                link.attrs['href'] for link in docket_soup.find_all('a')
                if 'href' in link.attrs
                and link.attrs['href'].endswith('mp3')
            ]
            assert len(mp3_urls) == 1
            audio_mp3_path = './downloads/{}/{}.mp3'.format(year, docket_number)
            mp3_url = mp3_urls[0]
            
            pdf_urls = [
                link.attrs['href'] for link in docket_soup.find_all('a')
                if 'href' in link.attrs
                and link.attrs['href'].endswith('pdf')
                and 'argument_transcripts' in link.attrs['href']
            ]
            assert len(pdf_urls) == 1
            transcript_pdf_path = './downloads/{}/{}.pdf'.format(year, docket_number)
            pdf_url = '{}/{}'.format(base_url, pdf_urls[0][len('/oral_arguments/'):])

            description = {
                'docket_number': docket_number,
                'case_title': case_title,
                'audio_mp3_url': mp3_url,
                'audio_mp3_path': audio_mp3_path,
                'transcript_pdf_url': pdf_url,
                'transcript_pdf_path': transcript_pdf_path
            }
            manifest.dump(description)

        if counter == 0:
            # caught up to the most recent records
            break

        year += 1
