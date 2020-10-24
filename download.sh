mkdir -p downloads

gunzip -c corpus_staging/manifest.jsonl.gz | while read -r line; do    
    echo wget -N --retry-connrefused --waitretry=100 --read-timeout=20 --timeout=15 -t 0 -O \"$(jq -r '.audio_mp3_path' <<< $line)\" \"$(jq -r '.audio_mp3_url' <<< $line)\"
    echo wget -O \"$(jq -r '.transcript_pdf_path' <<< $line)\" \"$(jq -r '.transcript_pdf_url' <<< $line)\"
done | parallel
