import os
from pathlib import Path

from separate_simple_track import bash_separator
from test_basic_pitch import my_predict_and_save
from basic_pitch import ICASSP_2022_MODEL_PATH

from open_isolate_slowdown_midi import open_and_slow_down

SONG_NAME = 'test'
EXTENSION = '.mp3'
SONG_FILE = SONG_NAME + EXTENSION
RES_DIR = Path(os.environ["TSOAI_HACK_LULLABY_RESOURCES"])
SONG_DIR = RES_DIR / SONG_NAME
SONG_FILE = RES_DIR / SONG_FILE

VOCALS_WAV_PATH = SONG_DIR / 'vocals.wav'
VOCALS_MIDI_PATH = SONG_DIR / 'vocals_basic_pitch.mid'
SLOW_VOCALS_MIDI_PATH = SONG_DIR / 'slow.wav'


if __name__ == '__main__':
    print('Separating vocals...')
    bash_separator(
        song_path=SONG_FILE,
        output_path=RES_DIR,
    )

    print('...done!')
    print('Converting to midi...')
    my_predict_and_save(
        audio_path_list=[str(VOCALS_WAV_PATH), ],
        output_directory=str(SONG_DIR),
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
    print('...done!')
    print('Slowing down...')
    open_and_slow_down(
        midi_fn=VOCALS_MIDI_PATH,
        out_fn=SLOW_VOCALS_MIDI_PATH,
        id_instr="all",
        mid_out_fn="",
    )

    print('...done!')

    print('All done, bye!')
