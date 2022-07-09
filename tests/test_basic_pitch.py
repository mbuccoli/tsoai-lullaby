import os
from pathlib import Path

from basic_pitch import ICASSP_2022_MODEL_PATH
#from basic_pitch.inference import predict_and_save
from inference import predict_and_save

SONG_NAME = 'test'
RES_DIR = Path(os.environ["TSOAI_HACK_LULLABY_RESOURCES"])
SONG_PATH = RES_DIR / SONG_NAME / 'vocals.wav'
OUTPUT_PATH = RES_DIR / 'vocals_basic_pitch.mid'

if __name__ == '__main__':
    if os.path.exists(OUTPUT_PATH):
        os.remove(OUTPUT_PATH)

    predict_and_save(
        # mandatory parameters
        audio_path_list=[str(SONG_PATH), ],
        output_directory=str(RES_DIR),
        save_midi=True,
        sonify_midi=False,
        save_model_outputs=False,
        save_notes=False,
        # optional parameters
        model_path=ICASSP_2022_MODEL_PATH,
        onset_threshold=0.6,
        frame_threshold=0.3,
        minimum_note_length=100,
        minimum_frequency=None,
        maximum_frequency=None,
        melodia_trick=True,
        debug_file=None,
    )
