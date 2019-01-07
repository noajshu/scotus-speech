PREFIX=$1 # e.g., downloads/2010/10-5400
BLUE='\033[0;34m'
CYAN='\033[0;36m'
GREEN='\033[0;32m'
SET='\033[0m'
jq -c '.fragments[]' $PREFIX.pdf.utts.txt.map.json | tail -n115 | while read -r fragment; do
    echo
    # echo "I ${CYAN}love${SET} github."
    echo -e "${BLUE}$(jq -r '.lines[0]' <<< $fragment)${SET}" # | jq -r '.lines[0]'
    echo -e "${CYAN}duration${SET} ${GREEN}$(echo $(jq -r '.end' <<< $fragment) - $(jq -r '.begin' <<< $fragment) | bc)s"
    play -q $PREFIX.mp3 trim $(jq -r '.begin' <<< $fragment) =$(jq -r '.end' <<< $fragment)
    # sleep 0.10
done

# These may be helpful for previewing alignments along the other stages of the pipeline
# # play aligned utterances from the middle of an audio file
# 
# gunzip -c corpus_staging/corpus.utterances.jsonl.gz | head -n100 | tail -50 | while read -r fragment; do
#     echo $(jq -r '.text' <<< $fragment) # | jq -r '.lines[0]'
#     echo duration $(jq -r '.duration' <<< $fragment)s
#     play -q audio/$(jq -r '.utterance_dir' <<< $fragment)/$(jq -r '.utterance_file' <<< $fragment)
#     sleep 0.25
# done
# 
# 
# # KUR CORPUS
# cat kur/scotusspeech.jsonl | tail -10 | while read -r fragment; do
#     echo $(jq -r '.text' <<< $fragment) # | jq -r '.lines[0]'
#     echo duration $(jq -r '.duration_s' <<< $fragment)s
#     play -q kur/audio/$(jq -r '.uuid' <<< $fragment).mp3
#     sleep 0.25
# done
# # play aligned utterances from the middle of an audio file