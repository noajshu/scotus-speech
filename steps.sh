# on mac:
xcode-select --install; brew update; brew install sox ffmpeg espeak
# on ubuntu:
sudo apt-get update
sudo apt-get install -y build-essential libpoppler-cpp-dev \
    pkg-config python-dev ffmpeg sox espeak jq parallel

pip install -r requirements.txt
pip install numpy bs4 pdftotext requests
pip install aeneas
python scrape.py
bash download.sh
python parse_pdf.py
python to_words.py
python to_utterances.py
bash align.sh
python add_times.py
bash cut_audio.sh
python convert_corpus.py