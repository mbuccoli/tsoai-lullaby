import os
from pathlib import Path
from typing import Optional
from separate_simple_track import bash_separator
from test_basic_pitch import my_predict_and_save
from basic_pitch import ICASSP_2022_MODEL_PATH

from open_isolate_slowdown_midi import open_and_slow_down
import argparse

SONG_NAME = 'hot_cold_short'
EXTENSION = '.mp3'
SONG_FILE = SONG_NAME + EXTENSION
RES_DIR = Path(os.environ["TSOAI_HACK_LULLABY_RESOURCES"])
SONG_DIR = RES_DIR / SONG_NAME
SONG_FILE = SONG_DIR / SONG_FILE

VOCALS_WAV_PATH = SONG_DIR / 'vocals.wav'
VOCALS_MIDI_PATH = SONG_DIR / 'vocals_basic_pitch.mid'
SLOW_VOCALS_MIDI_PATH = SONG_DIR / 'slow.wav'

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('--input_audio', '-ia', type=str,
                        help="Path to the audio file to be processed.", default=SONG_FILE)
    parser.add_argument('--output_path', '-o', type=str, help="Path where to save the final file.",
                        default=SONG_DIR)

    onset_threshold = parser.add_argument('--onset_threshold', '-ot', type=float, help="Onset threshold", default=0.6)
    frame_threshold = parser.add_argument('--frame_threshold', '-ft', type=float, help="Frame threshold", default=0.3)
    minimum_note_length = parser.add_argument('--minimum_note_length', '-mnl', type=int, help="Minimum note length", default=58)
    minimum_frequency = parser.add_argument('--minimum_frequency', '-mf', type=Optional[float], help="minimum frequecy", default=None)
    maximum_frequency = parser.add_argument('--maximum_frequency', '-Mf', type=Optional[float], help="Maximum frequency", default=None)
    include_pitch_bends = parser.add_argument('--include_pitch_bends', '-pb', type=Optional[float], help="Include pitch bends", default=None)
    melodia_trick = parser.add_argument('--melodia_trick', '-mt', type=bool, help="Melodia trick", default=None)


    args = parser.parse_args()
    input_audio = args.input_audio

    saving_folder = args.output_path
    song_name, _ = os.path.splitext(os.path.split(input_audio)[-1])
    print(song_name)
    onset_threshold = args.onset_threshold
    frame_threshold = args.frame_threshold
    minimum_note_length = args.minimum_note_length
    minimum_frequency = args.minimum_frequency
    maximum_frequency = args.maximum_frequency
    include_pitch_bends = args.include_pitch_bends
    melodia_trick = args.melodia_trick

    # TODO check that stuff exists
    print('Separating vocals...')
    bash_separator(
        song_path=input_audio,
        output_path=saving_folder,
    )

    print('...done!')
    print('Converting to midi...')
    my_predict_and_save(
        audio_path_list=[os.path.join(saving_folder, song_name, 'vocals.wav'), ],
        output_directory=saving_folder,
        save_midi=True,
        sonify_midi=False,
        save_model_outputs=False,
        save_notes=False,
        # optional parameters
        model_path=ICASSP_2022_MODEL_PATH,
        onset_threshold=onset_threshold,
        frame_threshold=frame_threshold,
        minimum_note_length=minimum_note_length,
        minimum_frequency=minimum_frequency,
        maximum_frequency=maximum_frequency,
        melodia_trick=melodia_trick,
        debug_file=None,
    )
    print('...done!')
    print('Slowing down and synthetizing...')
    data_slow, voice_instr = open_and_slow_down(
        midi_fn=os.path.join(saving_folder, 'vocals_basic_pitch.mid'),
        out_fn=os.path.join(saving_folder, 'lullaby.wav'),
        id_instr="all",
        mid_out_fn="",  # os.path.join(saving_folder, 'midi.wav')
    )

    print('...done!')

    print('All done, bye!')
