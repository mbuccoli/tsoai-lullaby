import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 
from pathlib import Path
from typing import Optional
from separate_simple_track import bash_separator

from open_isolate_slowdown_midi import open_and_slow_down
import argparse

from post_processing import post_process


SONG_NAME = 'baby_shark_cut'
EXTENSION = '.wav'
SONG_FILE = SONG_NAME + EXTENSION
RES_DIR = Path(os.environ["TSOAI_HACK_LULLABY_RESOURCES"])
SONG_DIR = RES_DIR / SONG_NAME
SONG_FILE = SONG_DIR / SONG_FILE
LULLABY_LP = SONG_DIR / "lullaby_lp.wav"
LULLABY_LP_REV = SONG_DIR / "lullaby_lp_rev.wav"
VOCALS_WAV_PATH = SONG_DIR / 'vocals.wav'
VOCALS_MIDI_PATH = SONG_DIR / 'vocals_basic_pitch.mid'
SLOW_VOCALS_MIDI_PATH = SONG_DIR / 'slow.wav'

if __name__ == '__main__':
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('--input_audio', '-ia', type=str,
                        help="Path to the audio file to be processed.", default=SONG_FILE)
    parser.add_argument('--output_path', '-o', type=str, help="Path where to save the final file; default is the same directory of the input_audio.",
                        default="")

    onset_threshold = parser.add_argument('--onset_threshold', '-ot', type=float, help="Onset threshold", default=0.6)
    frame_threshold = parser.add_argument('--frame_threshold', '-ft', type=float, help="Frame threshold", default=0.3)
    minimum_note_length = parser.add_argument('--minimum_note_length', '-mnl', type=int, help="Minimum note length", default=58)
    minimum_frequency = parser.add_argument('--minimum_frequency', '-mf', type=Optional[float], help="minimum frequecy", default=None)
    maximum_frequency = parser.add_argument('--maximum_frequency', '-Mf', type=Optional[float], help="Maximum frequency", default=None)
    include_pitch_bends = parser.add_argument('--include_pitch_bends', '-pb', type=Optional[float], help="Include pitch bends", default=None)
    melodia_trick = parser.add_argument('--melodia_trick', '-mt', type=bool, help="Melodia trick", default=None)


    slowdown_rate = parser.add_argument('--slowdown_rate', '-slow', type=float, help="Slowdown rate", default=2.)


    args = parser.parse_args()
    input_audio = args.input_audio

    saving_folder = args.output_path
    if saving_folder == "":
        saving_folder, song_name=os.path.split(input_audio)
    song_name, _ = os.path.splitext(song_name)
    print(song_name)
    onset_threshold = args.onset_threshold
    frame_threshold = args.frame_threshold
    minimum_note_length = args.minimum_note_length
    minimum_frequency = args.minimum_frequency
    maximum_frequency = args.maximum_frequency
    include_pitch_bends = args.include_pitch_bends
    melodia_trick = args.melodia_trick
    slowdown_rate = args.slowdown_rate

    # TODO check that stuff exists
    assert os.path.exists(input_audio), f"{input_audio} does not exist!" 
    assert os.path.exists(saving_folder), f"{saving_folder} does not exist!"

    print('Separating vocals👄 from accompaniement🎶...')
    out_spleeter_vocals=os.path.join(saving_folder, song_name, "vocals.wav")
    if not os.path.exists(out_spleeter_vocals):
        bash_separator(
            song_path=input_audio,
            output_path=saving_folder,
        )
    print('...done!☑️')



    print('Converting to midi🎼...')
    # move here to speed up the help
    from test_basic_pitch import my_predict_and_save
    from basic_pitch import ICASSP_2022_MODEL_PATH

    my_predict_and_save(
        audio_path_list=[out_spleeter_vocals, ],
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
    print('...done!☑️')
    print('Slowing down and synthetizing...👶💤')
    data_slow, voice_instr, sr = open_and_slow_down(
        midi_fn=os.path.join(saving_folder, 'vocals_basic_pitch.mid'),
        out_fn=os.path.join(saving_folder, 'lullaby_slow.wav'),
        id_instr="all",
        mid_out_fn=os.path.join(saving_folder, 'midi_synth.wav')
    )

    print('...done!☑️')
    print('Post-processing...')

    fn_in = os.path.join(saving_folder, 'lullaby_lp.wav')
    fn_out = os.path.join(saving_folder, 'lullaby_final.wav')

    data_slow_reverb = post_process(
        data_slow,
        sr,
        fn_in,
        fn_out,
        lowpass_rate=0.1,
    )

    print('...done!☑️')
    print('All done, bye!')
