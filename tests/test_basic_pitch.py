import os
from pathlib import Path

from basic_pitch import ICASSP_2022_MODEL_PATH
# from basic_pitch.inference import predict_and_save
from inference import predict_and_save

SONG_NAME = 'test'
RES_DIR = Path(os.environ["TSOAI_HACK_LULLABY_RESOURCES"])
SONG_PATH = RES_DIR / SONG_NAME / 'vocals.wav'
OUTPUT_PATH = RES_DIR / 'vocals_basic_pitch.mid'


def my_predict_and_save(
        # mandatory parameters
        audio_path_list,
        output_directory,
        save_midi,
        sonify_midi,
        save_model_outputs,
        save_notes,
        # optional parameters
        model_path,
        onset_threshold,
        frame_threshold,
        minimum_note_length,
        minimum_frequency,
        maximum_frequency,
        melodia_trick,
        debug_file,
):
    if os.path.exists(OUTPUT_PATH):
        os.remove(OUTPUT_PATH)

    predict_and_save(
        audio_path_list=audio_path_list,
        output_directory=output_directory,
        save_midi=save_midi,
        sonify_midi=sonify_midi,
        save_model_outputs=save_model_outputs,
        save_notes=save_notes,
        # optional parameters
        model_path=model_path,
        onset_threshold=onset_threshold,
        frame_threshold=frame_threshold,
        minimum_note_length=minimum_note_length,
        minimum_frequency=minimum_frequency,
        maximum_frequency=maximum_frequency,
        melodia_trick=melodia_trick,
        debug_file=debug_file,
    )


if __name__ == '__main__':
    my_predict_and_save(
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
