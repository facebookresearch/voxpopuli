 VoxPopuli
=====
[https://arxiv.org/abs/2010.12829](https://arxiv.org/abs/2010.12829)

A large-scale multilingual speech corpus for representation learning, semi-supervised learning and interpretation.

# Overview

VoxPopuli provides 
- 100K hours of unlabelled speech data for 23 languages
- 1.8K hours of transcribed speech data for 16 languages
- 17.3K hours of speech-to-speech interpretation data for 16x15 directions

The raw data is collected from 2009-2020 [European Parliament event recordings](https://multimedia.europarl.europa.eu/en/home). 
We acknowledge the European Parliament for creating and sharing these materials.

#### Detailed statistics

<details><summary>Unlabelled and transcribed data</summary><p>

| Language | Code | Unlabelled Hours | Transcribed Hours | Transcribed Speakers | Transcribed Tokens | LM Tokens |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
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
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| En | - | 463 | 427 | 441 | 432 | 461 | 457 | 382 | 427 | 400 | 442 | 433 | 434 | 398 | 370 | 6.0K |
| De | 187 | - | 196 | 204 | 214 | 217 | 198 | 205 | 214 | 196 | 217 | 208 | 218 | 164 | 179 | 2.8K |
| Fr | 169 | 187 | - | 187 | 172 | 197 | 195 | 144 | 170 | 158 | 168 | 168 | 156 | 139 | 134 | 2.3K |
| Es | 130 | 138 | 135 | - | 118 | 148 | 128 | 93 | 118 | 115 | 124 | 114 | 108 | 83 | 86 | 1.6K |
| Pl | 68 | 66 | 54 | 55 | - | 67 | 55 | 43 | 67 | 42 | 55 | 62 | 57 | 50 | 34 | 775 |
| It | 69 | 77 | 76 | 79 | 72 | - | 75 | 61 | 68 | 64 | 71 | 66 | 70 | 53 | 60 | 961 |
| Ro | 60 | 59 | 59 | 58 | 49 | 61 | - | 38 | 50 | 43 | 48 | 50 | 46 | 38 | 29 | 688 |
| Hu | 30 | 38 | 25 | 27 | 29 | 30 | 27 | - | 27 | 20 | 31 | 29 | 26 | 21 | 18 | 378 |
| Cs | 39 | 35 | 29 | 30 | 36 | 32 | 31 | 23 | - | 23 | 29 | 55 | 29 | 25 | 18 | 434 |
| Nl | 31 | 43 | 35 | 29 | 27 | 38 | 24 | 25 | 25 | - | 32 | 25 | 23 | 19 | 25 | 401 |
| Fi | 15 | 18 | 15 | 13 | 13 | 13 | 13 | 12 | 13 | 11 | - | 14 | 12 | 11 | 9 | 182 |
| Hr | 31 | 27 | 27 | 24 | 27 | 28 | 24 | 22 | 24 | 22 | 24 | 26 | 37 | 21 | 20 | 384 |
| Sk | 21 | 22 | 14 | 16 | 19 | 16 | 16 | 14 | 32 | 13 | 16 | - | 17 | 13 | 10 | 239 |
| Sl | 6 | 6 | 4 | 5 | 5 | 6 | 5 | 4 | 5 | 4 | 5 | 6 | - | 4 | 3 | 68 |
| Lt | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | - | 0 | 13 |
| Total | 857 | 1.2K | 1.1K | 1.2K | 1.2K | 1.3K | 1.2K | 1.1K | 1.2K | 1.1K | 1.3K | 1.3K | 1.2K | 1.0K | 995 | 17.3K |

</p></details>

# Getting Data
We provide raw audios as well as scripts to segment and align them with transcription/interpretation. The output format 
is [Ogg Vorbis](https://en.wikipedia.org/wiki/Vorbis) (16000Hz, 16-bit, mono-channel), 
which is supported by common libraries such as `libsndfile` and `libsox` (they have Python frontends 
by [soundfile](https://github.com/bastibe/python-soundfile), [torchaudio](https://github.com/pytorch/audio), etc.).

As the first step, clone this repo for the processing scripts
```bash
git clone https://github.com/facebookresearch/voxpopuli.git
```
and install required PyPI packages:
```bash
pip install -r requirements.txt
```


### Unlabelled Data
First, download raw audios via
```bash
python -m voxpopuli.download_audios --root [ROOT] --subset [SUBSET]
```
which saves audios to `${ROOT}/raw_audios/[language]/[year]/[recording_id].ogg`.

`SUBSET` specifies the data subset to download:

|  --subset | # Languages | Hours | Years | Size | 
|:---:|:---:|:---:|:---:|:---:|
| en, de, fr, es, pl, it, ro, hu, cs, nl, fi, hr, sk, sl, et, lt, pt, bg, el, lv, mt, sv or da | 1 | 2.7K-4.6K | 2009-2020 | 44G-75G |
| 10k | 23 | 10K | 2019-2020 | 170G |
| 100k | 23 | 100K | 2009-2020 | 1.7T |

Then, segment these audios via
```bash
python -m voxpopuli.get_unlabelled_data --root [ROOT] --subset [SUBSET]
```
which outputs to `${ROOT}/unlabelled_data/[language]/[year]/[segment_id].ogg`

### Transcribed (ASR) Data
First, download raw audios via
```bash
python -m voxpopuli.download_audios --root [ROOT] --subset asr
```
which saves audios to `${ROOT}/raw_audios/original/[year]/[recording_id].ogg`.

Then, segment these audios and align them with transcripts via
```bash
python -m voxpopuli.get_asr_data --root [ROOT]
```
which outputs
- audios `${ROOT}/transcribed_data/[language]/[year]/[segment_id].ogg`
- per-split manifest (ID, transcript, speaker ID) `${ROOT}/transcribed_data/[language]/asr_[split].tsv` 

### Speech-to-Speech Interpretation Data
First, follow the instructions above to set up ASR data (source audios and transcripts).

Then, download target audios via
```bash
python -m voxpopuli.download_audios --root [ROOT] --subset [TARGET_LANGUAGE]
```
which saves audios to `${ROOT}/raw_audios/[target_language]/[year]/[recording_id].ogg`.

Finally, segment these audios and match them with source ones via
```bash
python -m voxpopuli.get_s2s_data --root [ROOT] --source-lang [SOURCE_LANGUAGE] --target-lang [TARGET_LANGUAGE]
```
which outputs
- target audios `${ROOT}/transcribed_data/[language]/[target_language]/[year]/[segment_id].ogg`
- manifest (source ID, transcript, speaker ID, target ID) `${ROOT}/transcribed_data/[language]/[target_language]/s2s.tsv`

We also human-transcribe part of the target audios (for English, French and Spanish only) to allow more accurate alignments. 
To use them instead of machine transcriptions in the alignments, add `--use-annotated-target` to the command line.

### Language Modeling (LM) Data
First, download both data ("source release") and tools ("tools") from the [EuroParl website](https://www.statmt.org/europarl/),
and pre-process the data with `tools/split-sentences.perl`.

Then, process the data with
```bash
python -m voxpopuli.get_lm_data --input [IN_TEXT_FILE] --lang [LANGUAGE] --output [OUT_TEXT_FILE]
```

#  Pre-trained Models
We provide pre-trained wav2vec 2.0 models 
(both [fairseq](https://github.com/pytorch/fairseq) and [wav2letter/flashlight](https://github.com/facebookresearch/flashlight) implementations):

| Language(s) | Pre-training Hours | Base Model (95M) |  Large Model (317M) |
|:---:|:---:|:---:|:---:|
| Es | 4.5K | [fairseq](https://dl.fbaipublicfiles.com/voxpopuli/models/wav2vec2_base_es.pt) | [fairseq](https://dl.fbaipublicfiles.com/voxpopuli/models/wav2vec2_large_es.pt) |
| Fr | 4.5K | [fairseq](https://dl.fbaipublicfiles.com/voxpopuli/models/wav2vec2_base_fr.pt) | [fairseq](https://dl.fbaipublicfiles.com/voxpopuli/models/wav2vec2_large_fr.pt) |
| It | 4.5K | [fairseq](https://dl.fbaipublicfiles.com/voxpopuli/models/wav2vec2_base_it.pt) | [fairseq](https://dl.fbaipublicfiles.com/voxpopuli/models/wav2vec2_large_it.pt) |
| Nl | 4.5K | [fairseq](https://dl.fbaipublicfiles.com/voxpopuli/models/wav2vec2_base_nl.pt) | [fairseq](https://dl.fbaipublicfiles.com/voxpopuli/models/wav2vec2_large_nl.pt) |
| Sv | 4.5K | [fairseq](https://dl.fbaipublicfiles.com/voxpopuli/models/wav2vec2_base_sv.pt) | [fairseq](https://dl.fbaipublicfiles.com/voxpopuli/models/wav2vec2_large_sv.pt) |
| All 23 languages | 100K | [fairseq](https://dl.fbaipublicfiles.com/voxpopuli/models/wav2vec2_base_100k.pt) [wav2letter](https://dl.fbaipublicfiles.com/voxpopuli/models/wav2vec2_base_100k_wav2letter.tar.gz) | [fairseq](https://dl.fbaipublicfiles.com/voxpopuli/models/wav2vec2_large_100k.pt) |

The wav2letter implementation follows [this paper](https://arxiv.org/abs/2011.00093). In [our paper](https://arxiv.org/pdf/2101.00390.pdf) (Section 4.3.1), we evaluated these models on the [Common Voice](https://commonvoice.mozilla.org/) corpus 
in the normal setting and the [few-shot phoneme recognition setting](https://github.com/facebookresearch/CPC_audio#cross-lingual-transfer).


# What's New
- __2021-03-02__: VoxPopuli released.

# License
|  | License |
|:---:|:---:|
| VoxPopuli Data | [CC0](https://creativecommons.org/share-your-work/public-domain/cc0/) (see also European Parliament's [legal notice](https://www.europarl.europa.eu/legal-notice/en/) for the raw data) |
| LM Data | (Please check out the [EuroParl website](https://www.statmt.org/europarl/) for the EuroParl portion) |
| Code | [CC BY-NC 4.0](https://github.com/facebookresearch/covost/blob/master/LICENSE) |

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
