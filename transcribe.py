import base64
import urllib.request
import json
import os
import asyncio
import aiohttp
from aiohttp_retry import RetryClient
from numpy.random import random
from tqdm.auto import tqdm
from tools import jsonl



creds = (os.environ['DGUSER'], os.environ['DGPASS'])

semaphore = asyncio.Semaphore(100)
async def get_transcript(url):
    async with semaphore:
        async with RetryClient(raise_for_status=False) as client:
            async with client.post(
                'https://brain.deepgram.com/v2/listen',
                headers={
                    'Content-type': 'application/json',
                    'Authorization': 'Basic {}'.format(
                        base64.b64encode('{}:{}'.format(*creds).encode('utf-8')).decode('utf-8')
                    )
                },
                data=json.dumps({
                    'url': url
                }).encode('utf-8')
            ) as response:
                response_content = await response.text()
                return json.loads(response_content)


if __name__ == '__main__':
    coroutines = []
    with jsonl.JRZ('corpus_staging/manifest.jsonl.gz') as manifest:
        for case in manifest:
            coroutines.append(get_transcript(case['audio_mp3_url']))

    loop = asyncio.get_event_loop()
    outputs = loop.run_until_complete(asyncio.gather(*coroutines))
    with jsonl.JRZ('corpus_staging/manifest.jsonl.gz') as manifest:
        with jsonl.JWZ('corpus_staging/dg_transcripts.jsonl.gz') as transcripts:
            for case, output in zip(manifest, outputs):
                transcripts.dump({
                    'case': case,
                    'dg_transcript': output
                })
