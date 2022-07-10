# Pacifier
Pacifier is a tool for converting the melody of any song into a lullaby to put your baby to sleep. 

It was developed as a project for the [1st The Sound of AI Hackaton](https://musikalkemist.github.io/thesoundofaihackathon/).

## Requirements
To use Pacifier, first create a virtual environment by typing 
```
python3 -m  venv lullaby-venv
```
and then install the required packages as
```
python3 -m pip install -r requirements.txt
```
This will install the following packages to your virtual environment (and dependencies thereof):
- [numpy](https://numpy.org/)
- [scipy](https://scipy.org/)
- [ipykernel](https://pypi.org/project/ipykernel/)
- [pretty_midi](https://craffel.github.io/pretty-midi/)
- [spleeter](https://research.deezer.com/projects/spleeter.html)
- [basic-pitch](https://basicpitch.spotify.com/)

You also need to have `ffmpeg`, `libsndfile`, and `sox` installed on your computer.
Additionally, the first time you run pacifier, it needs download the spleeter pre-trained model
for isolating the melody. Those will be stored in a subfolder named `pretrained_models`.


## Usage and pipeline
The conversion to lullaby consists of several steps:
 - Separating the melody from the accompaniment
 - Converting the melody to midi
 - Slow-down the melody
 - Synthesize the melody
 - Add post-processing effect