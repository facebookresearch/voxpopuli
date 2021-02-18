# VoxPopuli : Wav2letter checkpoints

See https://github.com/facebookresearch/flashlight

Wav2letter implementation of wav2vec as described in https://arxiv.org/abs/2011.00093

A more updated version can be available in the wav2letter repository. 

The code included in this folder is a patched version of the original sample code developped by the [wav2letter team](https://github.com/facebookresearch/wav2letter/tree/masked_cpc) in order to include the pre-training.

## Loading the checkpoint

Wav2letter small wav2vec model : https://dl.fbaipublicfiles.com/voxpopuli/wav2letter_100k_small.tar.gz

Our checkpoint is using fl::ext::Serializer. The items are saved in the following order:

```
filename,     
FL_APP_ASR_VERSION, // std::string
config,             // std::unordered_map<std::string, std::string> 
network,            // fl::Sequential
criterion,          // CPCCriterion (Subclass of fl::app::asr::SequenceCriterion) : unsupervised CPC criterion
criterion2,         // fl::app::asr::SequenceCriterion : supervised CTC criterion
netoptim,           // fl::FirstOrderOptimizer : Optimizer for the unsupervised loss (adam)
netoptim2,          // fl::FirstOrderOptimizer : Optimizer for the supervised loss (adam)
critoptim,          // fl::FirstOrderOptimizer
critoptim2          // fl::FirstOrderOptimizer
```

The network consists in a base feature network topped with a classifier. 
To use it for fine-tuning, you need to load the network without its last layer:

```
void LoadFeatures(std::shared_ptr<fl::Sequential>  net0, std::shared_ptr<fl::Sequential> net){

    auto modules_0 = net0->modules();
    int n_layers = modules_0.size() - 1
    for (int i =0; i< n_layers; i++){
        net->add(modules_0[i]);
    }
}
```

## Building the Train and Decode binaries

First install flashlight https://github.com/facebookresearch/flashlight

Then:
```
mkdir build; cd build
cmake .. 
make -j40
```

## Building the Common Voice manifest files

First, download the datasets you're interested in from the [Common Voice website](https://commonvoice.mozilla.org/en/datasets).
Uncompress the data and copy them into $COMMON_VOICE_DIR/$LANG
Then run the following command:
```
cd prepare_data
bash build_cc_data.sh $COMMON_VOICE_DIR $LANG
```
The script will produce the manifest files associated with the validated, train, dev and test sets. As well as the lexicon and the token files.

## Results 

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