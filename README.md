# VoxPopuli

## Download the data

TODO : the raw data will be downloaded to $VOX_POPULI_DIR

## Rebuild the dataset from raw data

Here are the detailled instructions to re-process the entire dataset.

## Setup instructions

First, install the project's dependencies by running:
```
pip install -r requirements.txt
```

Then just run:
```
python setup.py develop
```

## Labelled data

### Download the align / wer data

To segment the labelled data you will need the decoded text corresponding to each audio segment. They are available upon request: please contact mriviere@fb.com and post an issue. 

### Relaunch the segmentation from the decoded data

To segment the parargaph into smaller sequences for the given language $LANG run:

```
python voxpopuli/segmentation/cut_with_align_files.py --dir_wer ${DIR_DOWNLOAD_WER}/${LANG}/wer \
                                                      --dir_align ${DIR_DOWNLOAD_WER}/${LANG}/align/ \
                                                      --dir_audio $VOX_POPULI_DIR \
                                                      -o $OUTPUT_DIRECTORY \
                                                      --path_chars ${DIR_DOWNLOAD}/${LANG}/${LANG}_grapheme.tokens \
                                                      --lang $LANG
```

## Unlabelled data

### Speaker diarization

To build the speaker timestamps you will need to run pyannote on the unlabelled data. To do so, launch:

```
python voxpopuli/segmentation/run_pyannote_sd.py --root $VOX_POPULI_DIR -l $LANGUAGES_LIST --segment-min 30
```

Where $LANGUAGES_LIST is the list of languages you want to deal with. For example this command will run the segmentation for french and spanish:

```
python voxpopuli/segmentation/run_pyannote_sd.py --root $VOX_POPULI_DIR -l fr es --segment-min 30
```

After launching the script go grab a coffee, it will run for some time.
