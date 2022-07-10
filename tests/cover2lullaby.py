"""
Ablate the Spleeter modules
"""
from pathlib import Path
from basic_pitch.inference import predict_and_save
from open_isolate_slowdown_midi import open_and_slow_down
import argparse
from typing import Optional
from basic_pitch import ICASSP_2022_MODEL_PATH
import os

def Cover2Lullaby(SONG_PATH=Path('/Users/vincent/PianoCover/'),
            audio_name="Life_and_Volition.wav",
            OUTPUT_PATH=Path('/Users/vincent/PianoCover/'),
            BACKEND='tensorflow',
            MODEL='spleeter:2stems'):



    predict_and_save(
        [str(SONG_PATH/audio_name), ],
        str(OUTPUT_PATH),
        True,  # save-midi,
        False,  # <sonify-midi>,
        False,  # <save-model-outputs>,
        False,  # <save-note-events>,
    )

    MIDI_FN = OUTPUT_PATH / 'Life_and_Volition_basic_pitch.mid'
    OUT_FN = OUTPUT_PATH / "vocals_basic_pitch_slow.wav"
    ID_INSTR = 2
    data_slow, voice_instr, _ = open_and_slow_down(
        midi_fn=MIDI_FN,
        out_fn=OUTPUT_PATH/'lullaby.wav',
        id_instr="all",
        mid_out_fn=OUTPUT_PATH/'midi_synth.wav'
    )

    return


if __name__ == '__main__':

    Cover2Lullaby()
    print("DONE")
