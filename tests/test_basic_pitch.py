import os
from pathlib import Path
import sys
print(sys.executable)
from basic_pitch.inference import predict_and_save

RES_DIR=Path(os.environ["TSOAI_HACK_LULLABY_RESOURCES"])
SONG_PATH = RES_DIR/'baby_one_more_time/vocals.wav'
OUTPUT_PATH = RES_DIR


predict_and_save(
    [str(SONG_PATH),],
    str(OUTPUT_PATH),
    True,# save-midi,
    False,#<sonify-midi>,
    False,#<save-model-outputs>,
    False,#<save-note-events>,
)
