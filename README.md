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

## Preparation
1. First init and update submodules:

  ```bash
  git submodule init && git submodule update
  ```
2. [Download weights](https://huggingface.co/spaces/Audio-AGI/AudioSep/tree/main/checkpoint) for Separate Anything You Describe model and place them inside `src/AudioSep/checkpoint/`.

3. Install requirements:
```bash
pip install -r requirements.txt
```
