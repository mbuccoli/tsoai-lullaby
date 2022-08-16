from pathlib import Path
import os

SONG_NAME = 'baby_shark_cut'
EXTENSION = '.wav'
SONG_FILE = SONG_NAME + EXTENSION
# RES_DIR = Path(os.environ["TSOAI_HACK_LULLABY_RESOURCES"])
# RES_DIR = Path(os.getcwd()).parent.absolute() / 'resources'
RES_DIR = Path(os.path.dirname(os.path.realpath(__file__))) / 'resources'
SONG_DIR = RES_DIR / SONG_NAME
SONG_FILE = SONG_DIR / SONG_FILE
LULLABY_LP = SONG_DIR / "lullaby_lp.wav"
LULLABY_LP_REV = SONG_DIR / "lullaby_lp_rev.wav"
VOCALS_WAV_PATH = SONG_DIR / 'vocals.wav'
VOCALS_MIDI_PATH = SONG_DIR / 'vocals_basic_pitch.mid'
SLOW_VOCALS_MIDI_PATH = SONG_DIR / 'slow.wav'

