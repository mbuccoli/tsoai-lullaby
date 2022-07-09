'''
this file links all the functions we have
'''

from pathlib import Path
from tests.separate_simple_track import bash_separator
from basic_pitch.inference import predict_and_save
from tests.open_isolate_slowdown_midi import open_and_slow_down


def Lullaby(SONG_PATH=Path('/Users/vincent/Desktop/tsoai-lullaby/audio/'),
            audio_name="test1.wav",
            OUTPUT_PATH=Path('/Users/vincent/Desktop/tsoai-lullaby/audio/output/'),
            BACKEND='tensorflow',
            MODEL='spleeter:2stems'):
    # separate vocals and accompaniment
    bash_separator(SONG_PATH / audio_name, OUTPUT_PATH)

    SONG_PATH = Path(OUTPUT_PATH) / audio_name[:-4] / "vocals.wav"

    predict_and_save(
        [str(SONG_PATH), ],
        str(OUTPUT_PATH),
        True,  # save-midi,
        False,  # <sonify-midi>,
        False,  # <save-model-outputs>,
        False,  # <save-note-events>,
    )

    MIDI_FN = OUTPUT_PATH / 'vocals_basic_pitch.mid'
    OUT_FN = OUTPUT_PATH / "vocals_basic_pitch_slow.wav"
    ID_INSTR = 2
    open_and_slow_down(MIDI_FN, ID_INSTR, OUT_FN)

    return


if __name__ == '__main__':
    Lullaby()
    print("DONE")
