import os
from pathlib import Path

from separate_simple_track import bash_separator
from test_basic_pitch import my_predict_and_save
from basic_pitch import ICASSP_2022_MODEL_PATH

from open_isolate_slowdown_midi import open_and_slow_down
import argparse

SONG_NAME = 'cheryl_colee_rain_on_me'
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

    args = parser.parse_args()
    input_audio = args.input_audio

    saving_folder = args.output_path
    song_name, _ = os.path.splitext(os.path.split(input_audio)[-1])
    print(song_name)

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
        onset_threshold=0.6,
        frame_threshold=0.3,
        minimum_note_length=100,
        minimum_frequency=None,
        maximum_frequency=None,
        melodia_trick=True,
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
