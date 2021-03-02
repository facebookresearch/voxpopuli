# Processing Pipeline Customization

We provide additional scripts for customizing our processing pipelines.

## Transcribed (ASR) Data

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
