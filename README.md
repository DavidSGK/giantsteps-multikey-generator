# GiantSteps MultiKey Generator
Generative augmenting tool for the GiantSteps Key data set. Allows random generation of duplicate audio files with local key changes.

Generates 5 variations of each audio track in the data set, with at most 2 pitch shifts of up to one octave at least 5 seconds apart. Annotations for each generated track are also saved in JSON format.

These parameters can be changed easily. See `generator.py` for more details.

# Usage
Download the audio files using the script provided by GiantSteps. It will take a while as it is ~850MB.
```
cd giantsteps-key-dataset
./audio_dl.sh
cd ..
```

Build and run the docker image. The scripts should be sufficient, but can be modified for various purposes.
```
bash build.sh
bash run.sh
```

# Annotation Format
```
[
  {
    "start": 0.0,
    "key": F minor
  },
  {
    "start": 15.78,
    "key": Bb minor
  },
  {
    "start": 64.22,
    "key": G minor
  }
]
```
