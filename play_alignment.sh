PREFIX=$1 # e.g., downloads/2010/10-5400
jq -c '.fragments[]' $PREFIX.pdf.utts.txt.map.json | head -n500 | tail -n140 | while read -r fragment; do
    echo $(jq -r '.lines[0]' <<< $fragment) # | jq -r '.lines[0]'
    echo duration $(echo $(jq -r '.end' <<< $fragment) - $(jq -r '.begin' <<< $fragment) | bc)s
    play -q $PREFIX.mp3 trim $(jq -r '.begin' <<< $fragment) =$(jq -r '.end' <<< $fragment)
    sleep 0.25
done

# play aligned utterances from the middle of an audio file