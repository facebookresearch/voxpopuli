 VoxPopuli
=====
[https://aclanthology.org/2021.acl-long.80](https://aclanthology.org/2021.acl-long.80)

A large-scale multilingual speech corpus for representation learning, semi-supervised learning and interpretation.

# Overview

VoxPopuli provides
- 400K hours of unlabelled speech data for 23 languages
- 1.8K hours of transcribed speech data for 16 languages
- 17.3K hours of speech-to-speech interpretation data for 15x15 directions
- 29 hours of transcribed speech data of non-native English intended for research in ASR for accented speech (15 L2 accents)

The raw data is collected from 2009-2020 [European Parliament event recordings](https://multimedia.europarl.europa.eu/en/home).
We acknowledge the European Parliament for creating and sharing these materials.

#### Detailed statistics

<details><summary>Unlabelled and transcribed data</summary><p>

| Language | Code | Unlabelled Hours (v1/v2) | Transcribed Hours | Transcribed Speakers | Transcribed Tokens | LM Tokens |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| English | En | 4.5K/24.1K | 543 | 1313 | 4.8M | 60.1M |
| German | De | 4.5K/23.2K | 282 | 531 | 2.3M | 50.0M |
| French | Fr | 4.5K/22.8K | 211 | 534 | 2.1M | 58.6M |
| Spanish | Es | 4.4K/21.4K | 166 | 305 | 1.6M | 57.4M |
| Polish | Pl | 4.5K/21.2K | 111 | 282 | 802K | 13.6M |
| Italian | It | 4.6K/21.9K | 91 | 306 | 757K | 52.1M |
| Romanian | Ro | 4.5K/17.9K | 89 | 164 | 739K | 10.3M |
| Hungarian | Hu | 4.4K/17.7K | 63 | 143 | 431K | 13.0M |
| Czech | Cs | 4.5K/18.7K | 62 | 138 | 461K | 13.5M |
| Dutch | Nl | 4.5K/19.0K | 53 | 221 | 488K | 54.6M |
| Finnish | Fi | 4.4K/14.2K | 27 | 84 | 160K | 34.5M |
| Croatian | Hr | 2.7K/8.1K | 43 | 83 | 337K | 285K |
| Slovak | Sk | 4.4K/12.1K | 35 | 96 | 270K | 13.3M |
| Slovene | Sl | 4.4K/11.3K | 10 | 45 | 76K | 12.6M |
| Estonian | Et | 4.3K/10.6K | 3 | 29 | 18K | 11.3M |
| Lithuanian | Lt | 4.3K/14.4K | 2 | 21 | 10K | 11.5M |
| Portuguese | Pt | 4.4K/17.5K | - | - | - | - |
| Bulgarian | Bg | 4.3K/17.6K | - | - | - | - |
| Greek | El | 4.4K/17.7K | - | - | - | - |
| Latvian | Lv | 4.4K/13.1K | - | - | - | - |
| Maltese | Mt | 4.4K/9.1K | - | - | - | - |
| Swedish | Sv | 4.5K/16.3K | - | - | - | - |
| Danish | Da | 4.3K/13.6K | - | - | - | - |
| Total | | 100K/384K | 1791 | 4295 | 15M | 467M |

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

<details><summary>Accented speech transcribed data</summary><p>

| Accent | Code | Transcribed Hours | Transcribed Speakers |
|:---:|:---:|:---:|:---:|
| Dutch | en_nl | 3.52 | 45 |
| German | en_de | 3.52 | 84 |
| Czech | en_cs | 3.30 | 26 |
| Polish | en_pl | 3.23 | 33 |
| French | en_fr | 2.56 | 27 |
| Hungarian | en_hu | 2.33 | 23 |
| Finnish | en_fi | 2.18 | 20 |
| Romanian | en_ro | 1.85 | 27 |
| Slovak | en_sk | 1.46 | 17 |
| Spanish | en_es | 1.42 | 18 |
| Italian | en_it | 1.11 | 15 |
| Estonian | en_et | 1.08 | 6 |
| Lithuanian | en_lt | 0.65 | 7 |
| Croatian | en_hr | 0.42 | 9 |
| Slovene | en_sl | 0.25 | 7 |

</p></details>

# What's New
- __2022-02-01__: New labelled accented English speech data released.
- __2022-01-15__: New [wav2vec 2.0 pre-trained models](https://github.com/facebookresearch/voxpopuli#wav2vec-20) released.
- __2021-07-26__: New unlabelled data (additional 300K hours) released.
- __2021-03-03__: VoxPopuli released.

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
| en_v2, de_v2, fr_v2, es_v2, pl_v2, it_v2, ro_v2, hu_v2, cs_v2, nl_v2, fi_v2, hr_v2, sk_v2, sl_v2, et_v2, lt_v2, pt_v2, bg_v2, el_v2, lv_v2, mt_v2, sv_v2 or da_v2 | 1 | 8.1K-24.1K | 2009-2020 | 130G-385G |
| 10k | 23 | 10K | 2019-2020 | 170G |
| 100k | 23 | 100K | 2009-2020 | 1.7T |
| 400k | 23 | 400K | 2009-2020 | 6.4T |

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
python -m voxpopuli.get_asr_data --root [ROOT] --lang [LANGUAGE]
```
which outputs
- audios `${ROOT}/transcribed_data/[language]/[year]/[segment_id].ogg`
- per-split manifest (ID, transcript, speaker ID) `${ROOT}/transcribed_data/[language]/asr_[split].tsv`

**Accented transcribed data**
To retrieve the transcribed accented speech data, follow the above steps with `--lang [LANGUAGE]_accented` (e.g. `--lang en_accented`).
Note that the accented speech data is only composed of a test set for now.

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
We combine VoxPopuli transcripts and text data from [Europarl](https://www.statmt.org/europarl/) for LM training.

Download VoxPopuli and Europarl text data, process the raw text and generate the vocabulary via
```bash
python -m voxpopuli.get_lm_data --root [ROOT] --lang [LANGUAGE]
```
which outputs
- sentences `${ROOT}/lm_data/[language]/sentences.txt`
- vocabulary `${ROOT}/lm_data/[language]/vocabulary.txt`

To train an n-gram LM with [KenLM](https://github.com/kpu/kenlm), run
```bash
${KENLM_PATH}/lmplz -o ${n} --limit_vocab_file [OUT_VOCAB_FILE] < [OUT_TEXT_FILE] > ${n}gram_lm.arpa
${KENLM_PATH}/build_binary ${n}gram_lm.arpa ${n}gram_lm.bin
```

#  Pre-trained Models
## wav2vec 2.0
We provide pre-trained wav2vec 2.0 models
(implemented in [fairseq](https://github.com/pytorch/fairseq) and [wav2letter/flashlight](https://github.com/facebookresearch/flashlight))
for downstream speech tasks. Each language is covered by a monolingual _Base_ model and multilingual _Large_ models that
combine languages in the same family or all languages. See also [XLS-R](https://github.com/pytorch/fairseq/tree/main/examples/wav2vec/xlsr)
for larger-scale (up to 2B) multilingual models trained on VoxPopuli (400K hours).

<details><summary><b>Download</b></summary><p>

|   Language(s)    |     Family     |  PT Hours  |                                                                             Base Model (95M)                                                                              |                                                                                      Large Model (317M)                                                                                       |
|:----------------:|:--------------:|:----------:|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------:|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------:|
|    Es (V1/V2)    |    Romance     | 4.4K/21.4K |     fairseq [V1](https://dl.fbaipublicfiles.com/voxpopuli/models/wav2vec2_base_es.pt) / [V2](https://dl.fbaipublicfiles.com/voxpopuli/models/wav2vec2_base_es_v2.pt)      |        fairseq [V1](https://dl.fbaipublicfiles.com/voxpopuli/models/wav2vec2_large_es.pt) / [V2 Romance](https://dl.fbaipublicfiles.com/voxpopuli/models/wav2vec2_large_romance_v2.pt)        |
|    Fr (V1/V2)    |    Romance     | 4.5K/22.8K |     fairseq [V1](https://dl.fbaipublicfiles.com/voxpopuli/models/wav2vec2_base_fr.pt) / [V2](https://dl.fbaipublicfiles.com/voxpopuli/models/wav2vec2_base_fr_v2.pt)      |        fairseq [V1](https://dl.fbaipublicfiles.com/voxpopuli/models/wav2vec2_large_fr.pt) / [V2 Romance](https://dl.fbaipublicfiles.com/voxpopuli/models/wav2vec2_large_romance_v2.pt)        |
|    It (V1/V2)    |    Romance     | 4.6K/21.9K |     fairseq [V1](https://dl.fbaipublicfiles.com/voxpopuli/models/wav2vec2_base_it.pt) / [V2](https://dl.fbaipublicfiles.com/voxpopuli/models/wav2vec2_base_it_v2.pt)      |        fairseq [V1](https://dl.fbaipublicfiles.com/voxpopuli/models/wav2vec2_large_it.pt) / [V2 Romance](https://dl.fbaipublicfiles.com/voxpopuli/models/wav2vec2_large_romance_v2.pt)        |
|     Pt (V2)      |    Romance     |   17.5K    |                                             [fairseq](https://dl.fbaipublicfiles.com/voxpopuli/models/wav2vec2_base_pt_v2.pt)                                             |                                              [fairseq V2 Romance](https://dl.fbaipublicfiles.com/voxpopuli/models/wav2vec2_large_romance_v2.pt)                                               |
|     Ro (V2)      |    Romance     |   17.9K    |                                             [fairseq](https://dl.fbaipublicfiles.com/voxpopuli/models/wav2vec2_base_ro_v2.pt)                                             |                                              [fairseq V2 Romance](https://dl.fbaipublicfiles.com/voxpopuli/models/wav2vec2_large_romance_v2.pt)                                               |
|    Nl (V1/V2)    | West Germanic  | 4.5K/19.0K |     fairseq [V1](https://dl.fbaipublicfiles.com/voxpopuli/models/wav2vec2_base_nl.pt) / [V2](https://dl.fbaipublicfiles.com/voxpopuli/models/wav2vec2_base_nl_v2.pt)      |  fairseq [V1](https://dl.fbaipublicfiles.com/voxpopuli/models/wav2vec2_large_nl.pt) / [V2 West Germanic](https://dl.fbaipublicfiles.com/voxpopuli/models/wav2vec2_large_west_germanic_v2.pt)  |
|     En (V2)      | West Germanic  |   24.1K    |                                             [fairseq](https://dl.fbaipublicfiles.com/voxpopuli/models/wav2vec2_base_en_v2.pt)                                             |                                        [fairseq V2 West Germanic](https://dl.fbaipublicfiles.com/voxpopuli/models/wav2vec2_large_west_germanic_v2.pt)                                         |
|     De (V2)      | West Germanic  |   23.2K    |                                             [fairseq](https://dl.fbaipublicfiles.com/voxpopuli/models/wav2vec2_base_de_v2.pt)                                             |                                        [fairseq V2 West Germanic](https://dl.fbaipublicfiles.com/voxpopuli/models/wav2vec2_large_west_germanic_v2.pt)                                         |
|    Sv (V1/V2)    | North Germanic | 4.5K/16.3K |     fairseq [V1](https://dl.fbaipublicfiles.com/voxpopuli/models/wav2vec2_base_sv.pt) / [V2](https://dl.fbaipublicfiles.com/voxpopuli/models/wav2vec2_base_sv_v2.pt)      | fairseq [V1](https://dl.fbaipublicfiles.com/voxpopuli/models/wav2vec2_large_sv.pt) / [V2 North Germanic](https://dl.fbaipublicfiles.com/voxpopuli/models/wav2vec2_large_north_germanic_v2.pt) |
|     Da (V2)      | North Germanic |   13.6K    |                                             [fairseq](https://dl.fbaipublicfiles.com/voxpopuli/models/wav2vec2_base_da_v2.pt)                                             |                                       [fairseq V2 North Germanic](https://dl.fbaipublicfiles.com/voxpopuli/models/wav2vec2_large_north_germanic_v2.pt)                                        |
|     Bg (V2)      |     Slavic     |   17.6K    |                                             [fairseq](https://dl.fbaipublicfiles.com/voxpopuli/models/wav2vec2_base_bg_v2.pt)                                             |                                                 [fairseq V2 Slavic](https://dl.fbaipublicfiles.com/voxpopuli/models/wav2vec2_large_slavic_v2.pt)                                                 |
|     Cs (V2)      |     Slavic     |   18.7K    |                                             [fairseq](https://dl.fbaipublicfiles.com/voxpopuli/models/wav2vec2_base_cs_v2.pt)                                             |                                                 [fairseq V2 Slavic](https://dl.fbaipublicfiles.com/voxpopuli/models/wav2vec2_large_slavic_v2.pt)                                                 |
|     Hr (V2)      |     Slavic     |    8.1K    |                                             [fairseq](https://dl.fbaipublicfiles.com/voxpopuli/models/wav2vec2_base_hr_v2.pt)                                             |                                                 [fairseq V2 Slavic](https://dl.fbaipublicfiles.com/voxpopuli/models/wav2vec2_large_slavic_v2.pt)                                                 |
|     Pl (V2)      |     Slavic     |   21.2K    |                                             [fairseq](https://dl.fbaipublicfiles.com/voxpopuli/models/wav2vec2_base_pl_v2.pt)                                             |                                                 [fairseq V2 Slavic](https://dl.fbaipublicfiles.com/voxpopuli/models/wav2vec2_large_slavic_v2.pt)                                                 |
|     Sk (V2)      |     Slavic     |   12.1K    |                                             [fairseq](https://dl.fbaipublicfiles.com/voxpopuli/models/wav2vec2_base_sk_v2.pt)                                             |                                                 [fairseq V2 Slavic](https://dl.fbaipublicfiles.com/voxpopuli/models/wav2vec2_large_slavic_v2.pt)                                                 |
|     Sl (V2)      |     Slavic     |   11.3K    |                                             [fairseq](https://dl.fbaipublicfiles.com/voxpopuli/models/wav2vec2_base_sl_v2.pt)                                             |                                                 [fairseq V2 Slavic](https://dl.fbaipublicfiles.com/voxpopuli/models/wav2vec2_large_slavic_v2.pt)                                                 |
|     Et (V2)      |     Uralic     |   10.6K    |                                             [fairseq](https://dl.fbaipublicfiles.com/voxpopuli/models/wav2vec2_base_et_v2.pt)                                             |                                                 [fairseq V2 Uralic](https://dl.fbaipublicfiles.com/voxpopuli/models/wav2vec2_large_uralic_v2.pt)                                                 |
|     Fi (V2)      |     Uralic     |   14.2K    |                                             [fairseq](https://dl.fbaipublicfiles.com/voxpopuli/models/wav2vec2_base_fi_v2.pt)                                             |                                                 [fairseq V2 Uralic](https://dl.fbaipublicfiles.com/voxpopuli/models/wav2vec2_large_uralic_v2.pt)                                                 |
|     Hu (V2)      |     Uralic     |   17.7K    |                                             [fairseq](https://dl.fbaipublicfiles.com/voxpopuli/models/wav2vec2_base_hu_v2.pt)                                             |                                                 [fairseq V2 Uralic](https://dl.fbaipublicfiles.com/voxpopuli/models/wav2vec2_large_uralic_v2.pt)                                                 |
|     Lv (V2)      |     Baltic     |   13.1K    |                                             [fairseq](https://dl.fbaipublicfiles.com/voxpopuli/models/wav2vec2_base_lv_v2.pt)                                             |                                                 [fairseq V2 Baltic](https://dl.fbaipublicfiles.com/voxpopuli/models/wav2vec2_large_baltic_v2.pt)                                                 |
|     Lt (V2)      |     Baltic     |   14.4K    |                                             [fairseq](https://dl.fbaipublicfiles.com/voxpopuli/models/wav2vec2_base_lt_v2.pt)                                             |                                                 [fairseq V2 Baltic](https://dl.fbaipublicfiles.com/voxpopuli/models/wav2vec2_large_baltic_v2.pt)                                                 |
|     El (V2)      |     Greek      |   17.7K    |                                             [fairseq](https://dl.fbaipublicfiles.com/voxpopuli/models/wav2vec2_base_el_v2.pt)                                             |                                                      [fairseq](https://dl.fbaipublicfiles.com/voxpopuli/models/wav2vec2_large_el_v2.pt)                                                       |
|     Mt (V2)      |    Semitic     |    9.1K    |                                             [fairseq](https://dl.fbaipublicfiles.com/voxpopuli/models/wav2vec2_base_mt_v2.pt)                                             |                                                      [fairseq](https://dl.fbaipublicfiles.com/voxpopuli/models/wav2vec2_large_mt_v2.pt)                                                       |
| All 23 languages |       -        |    10K     |                                              [fairseq](https://dl.fbaipublicfiles.com/voxpopuli/models/wav2vec2_base_10k.pt)                                              |                                                       [fairseq](https://dl.fbaipublicfiles.com/voxpopuli/models/wav2vec2_large_10k.pt)                                                        |
| All 23 languages |       -        |    100K    | [fairseq](https://dl.fbaipublicfiles.com/voxpopuli/models/wav2vec2_base_100k.pt) / [wav2letter](https://dl.fbaipublicfiles.com/voxpopuli/vox_populi_100k_500iters.tar.gz) |                                                       [fairseq](https://dl.fbaipublicfiles.com/voxpopuli/models/wav2vec2_large_100k.pt)                                                       |

</p></details>

In [our paper](https://arxiv.org/pdf/2101.00390.pdf) (Section 4.3.1), we evaluated part of these models on the [Common Voice](https://commonvoice.mozilla.org/) corpus
in the normal setting and the [few-shot phoneme recognition setting](https://github.com/facebookresearch/CPC_audio#cross-lingual-transfer).

## Wav2letter C++ implementation

A wav2letter implementation as well as a checkpoint pretrained on VoxPopuli 100k (base model) is also available in the [Wav2letter respository](https://github.com/flashlight/wav2letter/tree/master/recipes/joint_training_vox_populi).

The complete fine-tuned ASR baselines for this codebase shoulda come soon.
The wav2letter implementation follows [this paper](https://arxiv.org/abs/2011.00093).

## ASR and LM
For the VoxPopuli ASR task, we provide Transformer baselines, fine-tuned wav2vec2 models (Base 10K) as well as n-gram LMs (trained with [KenLM](https://github.com/kpu/kenlm)) and their lexicons.

<details><summary><b>Download</b></summary><p>

|  Language | ASR (fairseq) | LM (kenLM) | Lexicon |
|:---:|:---:|:---:|:---:|
| Cs | [baseline](https://dl.fbaipublicfiles.com/voxpopuli/models/vp_asr/s2t_transformer_s_cs.tar), [fine-tuned wav2vec2](https://dl.fbaipublicfiles.com/voxpopuli/models/vp_asr/wav2vec2_base_10k_ft_cs.tar) | [3-gram](https://dl.fbaipublicfiles.com/voxpopuli/lm/cs/cs_3gram_lm.bin), [5-gram](https://dl.fbaipublicfiles.com/voxpopuli/lm/cs/cs_5gram_lm.bin) | [lexicon](https://dl.fbaipublicfiles.com/voxpopuli/lm/cs/cs_lm.lexicon) |
| De | [baseline](https://dl.fbaipublicfiles.com/voxpopuli/models/vp_asr/s2t_transformer_s_de.tar), [fine-tuned wav2vec2](https://dl.fbaipublicfiles.com/voxpopuli/models/vp_asr/wav2vec2_base_10k_ft_de.tar) | [3-gram](https://dl.fbaipublicfiles.com/voxpopuli/lm/de/de_3gram_lm.bin), [5-gram](https://dl.fbaipublicfiles.com/voxpopuli/lm/de/de_5gram_lm.bin) | [lexicon](https://dl.fbaipublicfiles.com/voxpopuli/lm/de/de_lm.lexicon) |
| En | [baseline](https://dl.fbaipublicfiles.com/voxpopuli/models/vp_asr/s2t_transformer_s_en.tar), [fine-tuned wav2vec2](https://dl.fbaipublicfiles.com/voxpopuli/models/vp_asr/wav2vec2_base_10k_ft_en.tar) | [3-gram](https://dl.fbaipublicfiles.com/voxpopuli/lm/en/en_3gram_lm.bin), [5-gram](https://dl.fbaipublicfiles.com/voxpopuli/lm/en/en_5gram_lm.bin) | [lexicon](https://dl.fbaipublicfiles.com/voxpopuli/lm/en/en_lm.lexicon) |
| Es | [baseline](https://dl.fbaipublicfiles.com/voxpopuli/models/vp_asr/s2t_transformer_s_es.tar), [fine-tuned wav2vec2](https://dl.fbaipublicfiles.com/voxpopuli/models/vp_asr/wav2vec2_base_10k_ft_es.tar) | [3-gram](https://dl.fbaipublicfiles.com/voxpopuli/lm/es/es_3gram_lm.bin), [5-gram](https://dl.fbaipublicfiles.com/voxpopuli/lm/es/es_5gram_lm.bin) | [lexicon](https://dl.fbaipublicfiles.com/voxpopuli/lm/es/es_lm.lexicon) |
| Et | [baseline](https://dl.fbaipublicfiles.com/voxpopuli/models/vp_asr/s2t_transformer_s_et.tar), [fine-tuned wav2vec2](https://dl.fbaipublicfiles.com/voxpopuli/models/vp_asr/wav2vec2_base_10k_ft_et.tar) | [3-gram](https://dl.fbaipublicfiles.com/voxpopuli/lm/et/et_3gram_lm.bin), [5-gram](https://dl.fbaipublicfiles.com/voxpopuli/lm/et/et_5gram_lm.bin) | [lexicon](https://dl.fbaipublicfiles.com/voxpopuli/lm/et/et_lm.lexicon) |
| Fi | [baseline](https://dl.fbaipublicfiles.com/voxpopuli/models/vp_asr/s2t_transformer_s_fi.tar), [fine-tuned wav2vec2](https://dl.fbaipublicfiles.com/voxpopuli/models/vp_asr/wav2vec2_base_10k_ft_fi.tar) | [3-gram](https://dl.fbaipublicfiles.com/voxpopuli/lm/fi/fi_3gram_lm.bin), [5-gram](https://dl.fbaipublicfiles.com/voxpopuli/lm/fi/fi_5gram_lm.bin) | [lexicon](https://dl.fbaipublicfiles.com/voxpopuli/lm/fi/fi_lm.lexicon) |
| Fr | [baseline](https://dl.fbaipublicfiles.com/voxpopuli/models/vp_asr/s2t_transformer_s_fr.tar), [fine-tuned wav2vec2](https://dl.fbaipublicfiles.com/voxpopuli/models/vp_asr/wav2vec2_base_10k_ft_fr.tar) | [3-gram](https://dl.fbaipublicfiles.com/voxpopuli/lm/fr/fr_3gram_lm.bin), [5-gram](https://dl.fbaipublicfiles.com/voxpopuli/lm/fr/fr_5gram_lm.bin) | [lexicon](https://dl.fbaipublicfiles.com/voxpopuli/lm/fr/fr_lm.lexicon) |
| Hr | [baseline](https://dl.fbaipublicfiles.com/voxpopuli/models/vp_asr/s2t_transformer_s_hr.tar), [fine-tuned wav2vec2](https://dl.fbaipublicfiles.com/voxpopuli/models/vp_asr/wav2vec2_base_10k_ft_hr.tar) | [3-gram](https://dl.fbaipublicfiles.com/voxpopuli/lm/hr/hr_3gram_lm.bin), [5-gram](https://dl.fbaipublicfiles.com/voxpopuli/lm/hr/hr_5gram_lm.bin) | [lexicon](https://dl.fbaipublicfiles.com/voxpopuli/lm/hr/hr_lm.lexicon) |
| Hu | [baseline](https://dl.fbaipublicfiles.com/voxpopuli/models/vp_asr/s2t_transformer_s_hu.tar), [fine-tuned wav2vec2](https://dl.fbaipublicfiles.com/voxpopuli/models/vp_asr/wav2vec2_base_10k_ft_hu.tar) | [3-gram](https://dl.fbaipublicfiles.com/voxpopuli/lm/hu/hu_3gram_lm.bin), [5-gram](https://dl.fbaipublicfiles.com/voxpopuli/lm/hu/hu_5gram_lm.bin) | [lexicon](https://dl.fbaipublicfiles.com/voxpopuli/lm/hu/hu_lm.lexicon) |
| It | [baseline](https://dl.fbaipublicfiles.com/voxpopuli/models/vp_asr/s2t_transformer_s_it.tar), [fine-tuned wav2vec2](https://dl.fbaipublicfiles.com/voxpopuli/models/vp_asr/wav2vec2_base_10k_ft_it.tar) | [3-gram](https://dl.fbaipublicfiles.com/voxpopuli/lm/it/it_3gram_lm.bin), [5-gram](https://dl.fbaipublicfiles.com/voxpopuli/lm/it/it_5gram_lm.bin) | [lexicon](https://dl.fbaipublicfiles.com/voxpopuli/lm/it/it_lm.lexicon) |
| Lt | [baseline](https://dl.fbaipublicfiles.com/voxpopuli/models/vp_asr/s2t_transformer_s_lt.tar), [fine-tuned wav2vec2](https://dl.fbaipublicfiles.com/voxpopuli/models/vp_asr/wav2vec2_base_10k_ft_lt.tar) | [3-gram](https://dl.fbaipublicfiles.com/voxpopuli/lm/lt/lt_3gram_lm.bin), [5-gram](https://dl.fbaipublicfiles.com/voxpopuli/lm/lt/lt_5gram_lm.bin) | [lexicon](https://dl.fbaipublicfiles.com/voxpopuli/lm/lt/lt_lm.lexicon) |
| Nl | [baseline](https://dl.fbaipublicfiles.com/voxpopuli/models/vp_asr/s2t_transformer_s_nl.tar), [fine-tuned wav2vec2](https://dl.fbaipublicfiles.com/voxpopuli/models/vp_asr/wav2vec2_base_10k_ft_nl.tar) | [3-gram](https://dl.fbaipublicfiles.com/voxpopuli/lm/nl/nl_3gram_lm.bin), [5-gram](https://dl.fbaipublicfiles.com/voxpopuli/lm/nl/nl_5gram_lm.bin) | [lexicon](https://dl.fbaipublicfiles.com/voxpopuli/lm/nl/nl_lm.lexicon) |
| Pl | [baseline](https://dl.fbaipublicfiles.com/voxpopuli/models/vp_asr/s2t_transformer_s_pl.tar), [fine-tuned wav2vec2](https://dl.fbaipublicfiles.com/voxpopuli/models/vp_asr/wav2vec2_base_10k_ft_pl.tar) | [3-gram](https://dl.fbaipublicfiles.com/voxpopuli/lm/pl/pl_3gram_lm.bin), [5-gram](https://dl.fbaipublicfiles.com/voxpopuli/lm/pl/pl_5gram_lm.bin) | [lexicon](https://dl.fbaipublicfiles.com/voxpopuli/lm/pl/pl_lm.lexicon) |
| Ro | [baseline](https://dl.fbaipublicfiles.com/voxpopuli/models/vp_asr/s2t_transformer_s_ro.tar), [fine-tuned wav2vec2](https://dl.fbaipublicfiles.com/voxpopuli/models/vp_asr/wav2vec2_base_10k_ft_ro.tar) | [3-gram](https://dl.fbaipublicfiles.com/voxpopuli/lm/ro/ro_3gram_lm.bin), [5-gram](https://dl.fbaipublicfiles.com/voxpopuli/lm/ro/ro_5gram_lm.bin) | [lexicon](https://dl.fbaipublicfiles.com/voxpopuli/lm/ro/ro_lm.lexicon) |
| Sk | [baseline](https://dl.fbaipublicfiles.com/voxpopuli/models/vp_asr/s2t_transformer_s_sk.tar), [fine-tuned wav2vec2](https://dl.fbaipublicfiles.com/voxpopuli/models/vp_asr/wav2vec2_base_10k_ft_sk.tar) | [3-gram](https://dl.fbaipublicfiles.com/voxpopuli/lm/sk/sk_3gram_lm.bin), [5-gram](https://dl.fbaipublicfiles.com/voxpopuli/lm/sk/sk_5gram_lm.bin) | [lexicon](https://dl.fbaipublicfiles.com/voxpopuli/lm/sk/sk_lm.lexicon) |
| Sl | [baseline](https://dl.fbaipublicfiles.com/voxpopuli/models/vp_asr/s2t_transformer_s_sl.tar), [fine-tuned wav2vec2](https://dl.fbaipublicfiles.com/voxpopuli/models/vp_asr/wav2vec2_base_10k_ft_sl.tar) | [3-gram](https://dl.fbaipublicfiles.com/voxpopuli/lm/sl/sl_3gram_lm.bin), [5-gram](https://dl.fbaipublicfiles.com/voxpopuli/lm/sl/sl_5gram_lm.bin) | [lexicon](https://dl.fbaipublicfiles.com/voxpopuli/lm/sl/sl_lm.lexicon) |

</p></details>
 
We also provide [CoVoST 2](https://github.com/facebookresearch/covost) +
[EuroParl-ST](https://www.mllp.upv.es/europarl-st/) ASR Transformer models that are self-trained on 3000h VoxPopuli
unlabelled data.

<details><summary><b>Download</b></summary><p>

|  Language | CoVoST 2 Test (WER) | EuroParl-ST Test (WER) | Model (fairseq) |
|:---:|:---:|:---:|:---:|
| De | 17.3 | 21.4 | [s2t_transformer_l](https://dl.fbaipublicfiles.com/voxpopuli/models/cvst_epst/s2t_transformer_l_de.tar) |
| Es | 13.2 | 15.3 | [s2t_transformer_l](https://dl.fbaipublicfiles.com/voxpopuli/models/cvst_epst/s2t_transformer_l_es.tar) |
| Fr | 17.0 | 19.0 | [s2t_transformer_l](https://dl.fbaipublicfiles.com/voxpopuli/models/cvst_epst/s2t_transformer_l_fr.tar) |
 
</p></details>

Please refer to the [S2T examples](https://github.com/pytorch/fairseq/tree/master/examples/speech_to_text) for the use
of Transformer model checkpoints.

## Speech-to-Text Translation (ST)
We provide [CoVoST 2](https://github.com/facebookresearch/covost) +
[EuroParl-ST](https://www.mllp.upv.es/europarl-st/) ST Transformer models that are jointly trained with 400h VoxPopuli
weakly labelled data.

<details><summary><b>Download</b></summary><p>

| Direction | CoVoST 2 Test (BLEU) | EuroParl-ST Test (BLEU) | Model (fairseq) |
|:---:|:---:|:---:|:---:|
| De-En | 23.4 | 24.4 | [s2t_transformer_l](https://dl.fbaipublicfiles.com/voxpopuli/models/cvst_epst/s2t_transformer_l_de-en.tar) |
| Es-En | 29.7 | 28.4 | [s2t_transformer_l](https://dl.fbaipublicfiles.com/voxpopuli/models/cvst_epst/s2t_transformer_l_es-en.tar) |
| Fr-En | 30.3 | 31.1 | [s2t_transformer_l](https://dl.fbaipublicfiles.com/voxpopuli/models/cvst_epst/s2t_transformer_l_fr-en.tar) |

</p></details>
 
Please refer to the
[S2T examples](https://github.com/pytorch/fairseq/tree/master/examples/speech_to_text) for the use of these checkpoints.

# License
|  | License |
|:---:|:---:|
| VoxPopuli Data | [CC0](https://creativecommons.org/share-your-work/public-domain/cc0/) (see also European Parliament's [legal notice](https://www.europarl.europa.eu/legal-notice/en/) for the raw data) |
| LM Data | (Please check out the [Europarl website](https://www.statmt.org/europarl/) for the Europarl portion) |
| Pre-trained Models | [CC BY-NC 4.0](https://github.com/facebookresearch/covost/blob/master/LICENSE) |
| Code | [CC BY-NC 4.0](https://github.com/facebookresearch/covost/blob/master/LICENSE) |

# Contact
Changhan Wang (changhan@fb.com), Morgane Rivière (mriviere@fb.com), Ann Lee (annl@fb.com)

# Citation
```
@inproceedings{wang-etal-2021-voxpopuli,
    title = "{V}ox{P}opuli: A Large-Scale Multilingual Speech Corpus for Representation Learning, Semi-Supervised Learning and Interpretation",
    author = "Wang, Changhan  and
      Riviere, Morgane  and
      Lee, Ann  and
      Wu, Anne  and
      Talnikar, Chaitanya  and
      Haziza, Daniel  and
      Williamson, Mary  and
      Pino, Juan  and
      Dupoux, Emmanuel",
    booktitle = "Proceedings of the 59th Annual Meeting of the Association for Computational Linguistics and the 11th International Joint Conference on Natural Language Processing (Volume 1: Long Papers)",
    month = aug,
    year = "2021",
    address = "Online",
    publisher = "Association for Computational Linguistics",
    url = "https://aclanthology.org/2021.acl-long.80",
    pages = "993--1003",
}
```
