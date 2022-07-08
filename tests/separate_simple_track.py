import os
from pathlib import Path
from spleeter.separator import Separator
from spleeter.audio.adapter import AudioAdapter


# This environment variables point to the "resources" directory 
# in our google drive
RES_DIR=Path(os.environ["TSOAI_HACK_LULLABY_RESOURCES"])

SONG_PATH = RES_DIR/'baby_one_more_time.mp3'
BACKEND = 'tensorflow'  # ["librosa"]
MODEL = 'spleeter:2stems'  # , 'spleeter:4stems', 'spleeter:5stems']
OUTPUT_PATH = RES_DIR

# Check just if separator works
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



if __name__ == '__main__':
    bash_separator(SONG_PATH, OUTPUT_PATH)