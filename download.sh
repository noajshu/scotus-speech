gunzip -c corpus_staging/manifest.jsonl.gz | while read line; do    
    echo wget -O \"$(jq -r '.audio_mp3_path' <<< $line)\" \"$(jq -r '.audio_mp3_url' <<< $line)\"
    echo wget -O \"$(jq -r '.transcript_pdf_path' <<< $line)\" \"$(jq -r '.transcript_pdf_url' <<< $line)\"
done | parallel
