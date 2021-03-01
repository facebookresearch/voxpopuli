 VoxPopuli
=====
[https://arxiv.org/abs/2010.12829](https://arxiv.org/abs/2010.12829)

A large-scale multilingual speech corpus for representation learning, semi-supervised learning and interpretation.

# Overview

VoxPopuli provides 
- 100K hours of unlabelled speech data for 23 languages
- 1.8K hours of transcribed speech data for 16 languages
- 16.3K hours of speech-to-speech interpretation data for 16x15 directions

The raw data is collected from 2009-2020 European Parliament event recordings. 
We acknowledge the European Parliament for creating and sharing these materials.

#### Detailed statistics

<details><summary>Unlabelled and transcribed data</summary><p>

| Language | Code | Unlabelled Hours | Transcribed Hours | Transcribed Speakers | Transcribed Tokens | LM Tokens |
|---|---|---|---|---|---|---|
| English | En | 4.5K | 543 | 1313 | 4.8M | 60.0M |
| German | De | 4.5K | 282 | 531 | 2.3M | 49.8M |
| French | Fr | 4.5K | 211 | 534 | 2.1M | 58.6M |
| Spanish | Es | 4.4K | 166 | 305 | 1.6M | 57.3M |
| Polish | Pl | 4.5K | 111 | 282 | 802K | 7.6M |  
| Italian | It | 4.6K | 91 | 306 | 757K | 52.0M |
| Romanian | Ro | 4.5K | 89 | 164 | 739K | 10.3M |
| Hungarian | Hu | 4.4K | 63 | 143 | 431K | 12.9M |
| Czech | Cs | 4.5K | 62 | 138 | 461K | 13.5M |
| Dutch | Nl | 4.5K | 53 | 221 | 488K | 54.6M |
| Finnish | Fi | 4.4K | 27 | 84 | 160K | 34.5M |
| Croatian | Hr | 2.7K | 43 | 83 | 337K | 347K |
| Slovak | Sk | 4.4K | 35 | 96 | 270K | 13.3M | 
| Slovene | Sl | 4.4K | 10 | 45 | 76K | 12.6M |
| Estonian | Et | 4.3K | 3 | 29 | 18K | 11.3M |
| Lithuanian | Lt | 4.3K | 2 | 21 | 10K | 11.5M |
| Portuguese | Pt | 4.4K | - | - | - | - |
| Bulgarian | Bg | 4.3K | - | - | - | - |
| Greek | El | 4.4K | - | - | - | - | 
| Latvian | Lv | 4.4K | - | - | - | - |
| Maltese | Mt | 4.4K | - | - | - | - |
| Swedish | Sv | 4.5K | - | - | - | - |
| Danish | Da | 4.3K | - | - | - | - |
| Total | | 100K | 1791 | 4295 | 15.3M | 460.1M |

</p></details>

<details><summary>Speech-to-speech interpretation data</summary><p>

| Source/Target | En | De | Fr | Es | Pl | It | Ro | Hu | Cs | Nl | Fi | Sk | Sl | Lt | Da | Total |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| En | - | 426 | 374 | 401 | 407  | 426 | 431 | 359 | 401 | 375 | 417 |  406 | 410 | 378 | 344 | 5.6K |
| De | 171 | - | 171 | 184 | 203 | 201 | 189 | 195 | 203 | 186 | 206 |  198 | 207 | 158 | 169 | 2.6K |
| Fr | 154 | 173 | - | 170 | 164 | 185 | 186 | 137 | 162 | 149 | 161 |  160 | 149 | 133 | 126 | 2.2K |
| Es | 119 | 129 | 121 | - | 114 | 140 | 124 | 90 | 114 | 110 | 121 |  111 | 105 | 82 | 83 | 1.6K |
| Pl | 62 | 62 | 48 | 50 | - | 63 | 53 | 42 | 64 | 42 | 54 | 60 | 56 | 50 | 32 | 738 |
| It | 58 | 67 | 61 | 69 | 65 | - | 68 | 56 | 61 | 57 | 64 | 60 | 64 | 49 | 54 | 853 |
| Ro | 55 | 54 | 52 | 53 | 46 | 56 | - | 37 | 47 | 41 | 46 | 48 | 44 | 37 | 27 | 643 |
| Hu | 28 | 36 | 23 | 25 | 29 | 29 | 27 | - | 26 | 20 | 31 | 28 | 26 | 21 | 17 | 366 |
| Cs | 37 | 34 | 27 | 29 | 36 | 31 | 31 | 23 | - | 23 | 30 | 54 | 30 | 26 | 17 | 428 |
| Nl | 28 | 40 | 30 | 26 | 26 | 35 | 23 | 24 | 25 | - | 31 | 24 | 22 | 19 | 24 | 377 |
| Fi | 14 | 17 | 13 | 12 | 13 | 12 | 13 | 12 | 12 | 10 | - | 14 | 12 | 11 | 9 | 174 |
| Hr | 31 | 27 | 24 | 24 | 28 | 28 | 26 | 23 | 26 | 22 | 26 | 28 | 38 | 22 | 20 | 393 |
| Sk | 20 | 22 | 13 | 14 | 19 | 16 | 16 | 14 | 31 | 13 | 16 | - | 17 | 13 | 10 | 234 |
| Sl | 5 | 6 | 4 | 5 | 5 | 6 | 5 | 4 | 5 | 4 | 5 | 6 | - | 4 | 3 | 67 |
| Et | 2 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 16 |
| Lt | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | - | 0 | 13 |
| Total | 785 | 1.1K | 963 | 1.1K | 1.2K | 1.2K | 1.2K | 1.0K | 1.2K | 1.1K | 1.2K | 1.2K | 1.2K | 1.0K | 936 | 16.3K |

</p></details>

# Getting Data
We provide raw audios and scripts to process them. The output format 
is [Ogg Vorbis](https://en.wikipedia.org/wiki/Vorbis) (16000Hz, 16-bit, mono-channel), 
which is supported by common libraries such as `libsndfile` and `libsox`.

As the first step, clone this repo for the scripts
```bash
git clone https://github.com/facebookresearch/voxpopuli.git
```
and install required PyPI packages:
```bash
pip install tqdm torchaudio num2words
```


### Unlabelled Data
First, download raw audios via
```bash
python -m voxpopuli.download_audios --root ROOT --subset SUBSET
```
where `SUBSET` specifies the data subset to download:

|  --subset | # Languages | Hours | Years | Size | 
|---|---|---|---|---|
| en, de, fr, es, pl, it, ro, hu, cs, nl, fi, hr, sk, sl, et, lt, pt, bg, el, lv, mt, sv or da | 1 | 2.7K-4.6K | 2009-2020 | 44G-75G |
| 10k | 23 | 10K | 2019-2020 | 170G |
| 100k | 23 | 100K | 2009-2020 | 1.7T |
It saves audios to `${ROOT}/raw_audios/[language]/[year]/[recording_id].ogg`.

Then, segment these audios via
```bash
python -m voxpopuli.segment_unlabelled --root ROOT --subset SUBSET
```
which outputs to `${ROOT}/unlabelled_data/[language]/[year]/[segment_id].ogg`

### Transcribed (ASR) Data
First, download raw audios via
```bash
python -m voxpopuli.download_audios --root ROOT --subset asr
```
which saves audios to `${ROOT}/raw_audios/original/[year]/[recording_id].ogg`.

Then, segment these audios and align them with transcripts via
```bash
python -m voxpopuli.get_asr_data --root ROOT
```
which outputs
- audios `${ROOT}/transcribed_data/[language]/[year]/[segment_id].ogg`
- per-data-split example list (ID, transcript, speaker ID) `${ROOT}/transcribed_data/[language]/asr_[split].tsv` 

### Speech-to-Speech Interpretation Data
First, follow the instructions above to set up ASR data (source data).

Then, download target audios via
```bash
python -m voxpopuli.download_audios --root ROOT --subset [TARGET_LANGUAGE]
```
which saves audios to `${ROOT}/raw_audios/[target_language]/[year]/[recording_id].ogg`.

Finally, segment these audios and match them with source ones via
```bash
python -m voxpopuli.get_s2s_data --root ROOT --source-lang [SOURCE_LANGUAGE] --target-lang [TARGET_LANGUAGE]
```
which outputs
- target audios `${ROOT}/transcribed_data/[language]/[target_language]/[year]/[segment_id].ogg`
- example list (source ID, transcript, speaker ID, target ID) `${ROOT}/transcribed_data/[language]/[target_language]/s2s.tsv`

### Language Modeling (LM) Data
First, download both data ("source release") and tools ("tools") from the [EuroParl website](https://www.statmt.org/europarl/),
and pre-process the data with `tools/split-sentences.perl`.

Then, process the data with
```bash
python -m voxpopuli.get_lm_data --input [IN_TEXT_FILE] --lang [LANG] --output [OUT_TEXT_FILE]
```

#  Pre-trained Models
We provide pre-trained wav2vec 2.0 (fairseq) models:

| Language(s) | Pre-training Hours | Base Model (95M) |  Large Model (317M) |
|---|---|---|---|
| Es | 4.5K | [Download](s3://dl.fbaipublicfiles.com/voxpopuli/models/wav2vec2_base_es.pt) | [Download](s3://dl.fbaipublicfiles.com/voxpopuli/models/wav2vec2_large_es.pt) |
| Fr | 4.5K | [Download](s3://dl.fbaipublicfiles.com/voxpopuli/models/wav2vec2_base_fr.pt) | [Download](s3://dl.fbaipublicfiles.com/voxpopuli/models/wav2vec2_large_fr.pt) |
| It | 4.5K | [Download](s3://dl.fbaipublicfiles.com/voxpopuli/models/wav2vec2_base_it.pt) | [Download](s3://dl.fbaipublicfiles.com/voxpopuli/models/wav2vec2_large_it.pt) |
| Nl | 4.5K | [Download](s3://dl.fbaipublicfiles.com/voxpopuli/models/wav2vec2_base_nl.pt) | [Download](s3://dl.fbaipublicfiles.com/voxpopuli/models/wav2vec2_large_nl.pt) |
| Sv | 4.5K | [Download](s3://dl.fbaipublicfiles.com/voxpopuli/models/wav2vec2_base_sv.pt) | [Download](s3://dl.fbaipublicfiles.com/voxpopuli/models/wav2vec2_large_sv.pt) |
| All 23 languages | 100K | [Download](s3://dl.fbaipublicfiles.com/voxpopuli/models/wav2vec2_base_100k.pt) | [Download](s3://dl.fbaipublicfiles.com/voxpopuli/models/wav2vec2_large_100k.pt) |

We evaluated these models on the [Common Voice](https://commonvoice.mozilla.org/) corpus 
in the [few-shot phoneme recognition setting](https://github.com/facebookresearch/CPC_audio#cross-lingual-transfer) 
(see also Section 4.3.1 of [our paper](https://arxiv.org/pdf/2101.00390.pdf)).


# What's New
- __2021-03-02__: VoxPopuli released.

# License
|  | License |
| ------------- |:-------------:|
| VoxPopuli data | [Legal notice](https://www.europarl.europa.eu/legal-notice/en/) [CC0](https://creativecommons.org/share-your-work/public-domain/cc0/) |
| Anything else | [CC BY-NC 4.0](https://github.com/facebookresearch/covost/blob/master/LICENSE) |

# Contact
Changhan Wang (changhan@fb.com), Morgane Rivière (mriviere@fb.com), Ann Lee (annl@fb.com)

# Citation
```
@article{wang2021voxpopuli,
  title={VoxPopuli: A Large-Scale Multilingual Speech Corpus for Representation Learning, Semi-Supervised Learning and Interpretation},
  author={Wang, Changhan and Rivi{\`e}re, Morgane and Lee, Ann and Wu, Anne and Talnikar, Chaitanya and Haziza, Daniel and Williamson, Mary and Pino, Juan and Dupoux, Emmanuel},
  journal={arXiv preprint arXiv:2101.00390},
  year={2021}
}
```
