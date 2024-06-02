# Audio-component-classifier

## Repositiry structure
```
|- data/ <- directory can be used to store data during model training,
|   |       also it can be used to store example data needed for notebooks
|   |
|   |-- interim/ <- Intermediate data that has been transformed
|   |-- processed/ <- The final, canonical data sets for modeling
|   |--raw/ <- The original, immutable data dump
|
|- notebooks/ - stores jupyter notebooks with examples and implementation details
|  
|- src/ - stores python files (model implementation and data prep)
|   |-- audio_classifier
|   |-- audio_components_extractor
```

## Preparation (will be simplified in the future)
1. First init and update submodules:

  ```bash
  git submodule init && git submodule update
  ```
2. Create dir `src/AudioSep/checkpoint`
3. [Download weights](https://huggingface.co/spaces/Audio-AGI/AudioSep/tree/main/checkpoint) for Separate Anything You Describe model and place them inside `src/AudioSep/checkpoint/`.

4. In src/AudioSep/models/clap_encoder.py **replace line**:
``` python
pretrained_path='checkpoint/music_speech_audioset_epoch_15_esc_89.98.pt',
```
with
``` python
pretrained_path='AudioSep/checkpoint/music_speech_audioset_epoch_15_esc_89.98.pt',
```

5. Install requirements:
```bash
pip install -r requirements.txt
```

## Running the pipeline 
In `data/raw` place audiofiles to be tagged (mixed audio).

In `data/sound_classes.txt` write sound source classes you wish to be recognized in the audio. Place each class in a separate line.

Change directory to `src` and run `main.py`.