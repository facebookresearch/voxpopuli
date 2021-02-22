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


## File segmentation

Once the speakers timestamps are built, you can run the file segmentation with:

```
python voxpopuli/segmentation/get_segment_pyannote_speaker.py --root $VOX_POPULI_DIR \
                                                              --languages $LANGUAGES_LIST \
                                                              -o $OUTPUT_DIR \
                                                              --max-dur-vad $MAX_SIZE
```

This command will segment each audio file using the sepaker timestamps detected with ```run_pyannote_sd.py``` above. Then it will use a voice activity dectetion (VAD) algorithm to remove non-speech parts of the resulting sequences. The resulting audio tracks won't be longer than ```MAX_SIZE``` seconds.
If you want to disable the  VAD use the flag ```--no-vad```.
