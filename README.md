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

To prepare the labelled data from the .tsv label files for a specifica language run:
```
python voxpopuli/segmentation/cut_from_labels.py --root_original $VOX_POPULI_DIR/sd_segments --tsv_file $VOX_POPULI_DIR/labels/${LANG}_all.tsv --output $VOX_POPULI_DIR/ssegmented_output/$LANG
```

TODO: add a .sh script handling the download and all languages 


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
