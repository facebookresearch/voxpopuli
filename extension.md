# Extension

We provide additional scripts for customizing our data processing pipelines.

### [Experimental] Segmenting Unlabelled Data with Speaker Diarization 

Our current pipeline uses voice activity detection (VAD) algorithm to segment unlabelled data which has no awareness 
of the speakers. However, potential speaker changes inside the audio clips may not be favored by downstream applications. 
We propose 2-step segmentation (speaker diarization followed by VAD) to mitigate this issue.

First, apply speaker diarization (SD) model provided by pyannote:

```bash
python -m voxpopuli.segmentation.run_pyannote_sd \
  --root [ROOT] -l [LANGUAGE_LIST] \
  --segment-min [MIN_SEGMENT_DURATION_IN_SECONDS]
```

Then, apply VAD on top of SD outputs to segment the audios:
```bash
python -m voxpopuli.segmentation.get_segment_pyannote_speaker.py \
    --root [ROOT] --languages [LANGUAGE_LIST] -o [OUTPUT_DIR] \
    --max-dur-vad [MAX_SEGMENT_DURATION_IN_SECONDS]
```

We also provide pre-computed segments on the 10k subset. Apply the segmentation directly via
```bash
python -m voxpopuli.get_unlabelled_data --root [ROOT] --subset 10k_sd
```
which outputs to `${ROOT}/unlabelled_data_sd/[language]/[year]/[segment_id].ogg`

### Customizing Force-Alignment for Transcribed (ASR) Data

To segment the labelled data you will need the decoded text corresponding to each audio segment. 
They are available upon request: please contact us or post an issue. 

If you want to use the force-aligned text for any purpose (like VAD), 
they are available [here](https://dl.fbaipublicfiles.com/voxpopuli/align_data.tar.gz).

To segment paragraphs into utterances for the given language $LANG, run:

```bash
python -m voxpopuli.pipeline.cut_with_align_files \
    --dir_wer ${DIR_DOWNLOAD_WER}/${LANG}/wer \
    --dir_align ${DIR_DOWNLOAD_WER}/${LANG}/align/ \
    --dir_audio $VOX_POPULI_DIR \
    -o $OUTPUT_DIRECTORY \
    --path_chars ${DIR_DOWNLOAD}/${LANG}/${LANG}_grapheme.tokens \
    --lang $LANG
```
