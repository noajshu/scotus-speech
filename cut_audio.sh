gunzip -c corpus_staging/corpus.utterances.jsonl.gz | while read -r line; do
    mkdir -p audio/$(jq -r '.utterance_dir' <<< $line)/
    echo ffmpeg -y -i $(jq -r '.audiofile' <<< $line) \
        -ss $(jq -r '.start' <<< $line) \
        -t $(jq -r '.duration' <<< $line) \
        audio/$(jq -r '.utterance_dir' <<< $line)/$(jq -r '.utterance_file' <<< $line)
done | parallel