import os
from pathlib import Path
import sys

from basic_pitch import ICASSP_2022_MODEL_PATH

print(sys.executable)
from basic_pitch.inference import predict_and_save

RES_DIR=Path(os.environ["TSOAI_HACK_LULLABY_RESOURCES"])
SONG_PATH = RES_DIR/'baby_one_more_time/vocals.wav'
OUTPUT_PATH = RES_DIR


predict_and_save(
# mandatory parameters
    audio_path_list= [str(SONG_PATH),],
    output_directory=str(OUTPUT_PATH),
    save_midi=True,
    sonify_midi=False,
    save_model_outputs=False,
    save_notes=False,
# optional parameters
    model_path=ICASSP_2022_MODEL_PATH,
    onset_threshold=0.5,
    frame_threshold=0.3,
    minimum_note_length=58,
    minimum_frequency=None,
    maximum_frequency=None,
    melodia_trick=True,
    debug_file=None,
)
