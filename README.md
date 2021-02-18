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

First, download and unzip the .tsv labels
```
cd $VOX_POPULI_DIR/ ; mkdir labels; cd labels
wget https://dl.fbaipublicfiles.com/voxpopuli/labels.tar.gz
tar xvf labels.tar.gz 
```

Then, to prepare the labelled data from the .tsv label files for a specific language run:
```
python voxpopuli/segmentation/cut_from_labels.py --root_original $VOX_POPULI_DIR/sd_segments \
                                                 --tsv_file $VOX_POPULI_DIR/labels/${LANG}_all.tsv \
                                                 --output $VOX_POPULI_DIR/segmented_output/$LANG \
                                                 --mode labelled
```

## Unlabelled data

### Rebuild the data using existing timestamps

For the 10k subset, you can use the existing timestamps to quickly rebuild the session segmented by speaker and voice activity.
To do so, you first need to download the timestamps:
```
cd $VOX_POPULI_DIR/ ; mkdir timestamps; cd timestamps
wget https://dl.fbaipublicfiles.com/voxpopuli/timestamps_10k.tsv
```

Then, run the reconstruction with:
```
python voxpopuli/segmentation/cut_from_labels.py --root_original $VOX_POPULI_DIR/sd_segments \
                                                 --tsv_file $VOX_POPULI_DIR/timestamps/timestamps_10k.tsv \
                                                 --output $VOX_POPULI_DIR/unlabelled \
                                                 --mode per_speaker_vad
```

If you don't want the voice activity detection to be applied, you can replace per_speaker_vad with per_speaker.

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
