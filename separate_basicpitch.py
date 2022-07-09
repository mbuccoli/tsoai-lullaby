'''
Input:audio file
output: MIDI file
'''
import sys
from pathlib import Path
from separator import bash_separator
from basic_pitch.inference import predict_and_save

def separate_MIDIconversion(SONG_PATH = Path('/Users/vincent/Desktop/tsoai-lullaby/audio/'),
                            audio_name = "test1.wav",
                            OUTPUT_PATH = '/Users/vincent/Desktop/tsoai-lullaby/audio/output/',
                            BACKEND = 'tensorflow',  # ["librosa"]
                            MODEL = 'spleeter:2stems'  # , 'spleeter:4stems', 'spleeter:5stems']
                            ):

    # separate vocals and accompaniment
    bash_separator(SONG_PATH/audio_name, OUTPUT_PATH)


    SONG_PATH = OUTPUT_PATH/audio_name[:-4]/"vocals.wav"
    
    predict_and_save(
        [str(SONG_PATH),],
        str(OUTPUT_PATH),
        True,# save-midi,
        False,#<sonify-midi>,
        False,#<save-model-outputs>,
        False,#<save-note-events>,
    )   


    return

