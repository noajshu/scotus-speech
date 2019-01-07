xcode-select --install; brew update; brew install sox ffmpeg espeak
pip install numpy
pip install aeneas
pip install -r requirements.txt
python scrape.py
bash download.sh
python parse_pdf.py
python to_words.py
python to_utterances.py
bash align.sh
python add_times.py
bash cut_audio.sh
python convert_corpus.py