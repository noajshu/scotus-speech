gunzip -c corpus_staging/manifest.jsonl.gz | while read -r line; do
    echo python -m aeneas.tools.execute_task \
        \"$(jq -r '.audio_mp3_path' <<< $line)\" \
        \"$(jq -r '.transcript_pdf_path' <<< $line).utts.txt\" \
        "\"task_language=eng|os_task_file_format=json|is_text_type=plain\"" \
        \"$(jq -r '.transcript_pdf_path' <<< $line).utts.txt.map.json\" --presets-word -r="tts=espeak"
done | parallel