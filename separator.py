import os
from spleeter.separator import Separator
from spleeter.audio.adapter import AudioAdapter
#
# To run the code, simply change the variables SONG_PATH and
# OUTPUT_PATH.


SONG_PATH = '/home/marta/Musica/007LIJOPQ4Sb98qV.mp3'
BACKEND = 'tensorflow'  # ["librosa"]
MODEL = 'spleeter:4stems'  # , 'spleeter:4stems', 'spleeter:5stems']
OUTPUT_PATH = '/home/marta/soundofAI/output/'


# Models need to be downloaded first

def bash_separator(song_path, output_path) -> None:
    """
    Wrapper for calling spleeter within python.
    It splits the input file into voice and accompainment
    and stores the two into the folder of output_path
    :param song_path: path to the file to split
    :param output_path: path to the directory where to store the splits
    """

    os.system(f"spleeter separate -o {output_path} {song_path}")


def python_separator(
        song_path=SONG_PATH,
        output_path=OUTPUT_PATH,
        backend=BACKEND,
        model=MODEL,
        to_file=True,
) -> dict:
    """
    Wrapper for the spleeter separator. It takes as input the path to the audio file
    and either stores the different sources or returns a dictionary storing the
    separated sources as np.array.

    :param song_path: path to the file to split
    :param output_path: path to the directory where to store the splits
    :param backend: the backend module to use for STFT
    :param model: the model to use for splitting, i.e. how many separate sources we want
    #TODO substitute with number of sources
    :param to_file: whether to save the split sources or to return them as a dictionary
    # TODO substitute with save_files instead

    """
    # Instantiate the separator
    separator = Separator(model, stft_backend=backend, multiprocess=False)

    if to_file:
        separator.separate_to_file(song_path, output_path)
        return {}
    else:
        audio_adapter = AudioAdapter.default()
        waveform, _ = audio_adapter.load(
            song_path,
        )

        return separator.separate(waveform)


if __name__ == '__main__':
    sources = python_separator(to_file=False)
    print(sources)