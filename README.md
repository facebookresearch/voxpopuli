# Vox Populi

## ASR models

### Wav2letter

Wav2letter model trained on 100k of data: https://dl.fbaipublicfiles.com/voxpopuli/wav2letter_100k_small.tar.gz

Performances on CommonVoices without language model:

| Language        | Fine-tuning size |                 Dev      |       Test        |
| --------------- |:----------------:|:------------------------:|:-----------------:|
| De              | 314h             | CER 3.83 WER: 15.0       | CER 4.70 WER: 17.0|
| Es              | 203h             | CER 3.49 WER: 10.7       | CER 4.04 WER: 11.9|
| Fr              | 364h             | CER 4.9 WER: 16.9        | CER 5.89 WER: 18.8|

Performances on CommonVoices using a language model built out from CommonVoices data (excluding dev / test):

| Language        | Fine-tuning size |                 Dev      |       Test        |
| --------------- |:----------------:|:------------------------:|:-----------------:|
| De              | 314h             | CER 2.36 WER: 6.76       | CER 2.98 WER: 7.82|
| Es              | 203h             | CER 3.11 WER: 8.93       | CER 3.60 WER: 10.0|
| Fr              | 364h             | CER 2.73 WER: 8.31       | CER 3.57 WER: 9.56|



