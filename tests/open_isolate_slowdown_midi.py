# %%
import os

import numpy as np
from scipy.io import wavfile
from pathlib import Path

import pretty_midi

# This environment variables point to the "resources" directory 
# in our google drive
RES_DIR=Path(os.environ["TSOAI-HACK-LULLABY-RESOURCES"])

# %%
SR=48000

# %%
# Load MIDI file into PrettyMIDI object
midi_data = pretty_midi.PrettyMIDI(str(RES_DIR/'Toms_Diner.mid'))
voice_instr=midi_data.instruments[2]
voice = pretty_midi.PrettyMIDI()

# %%
# Starting from the beginning
start_=voice_instr.notes[0].start
for note in voice_instr.notes:
    note.start=(note.start-start_)
    note.end=(note.end-start_)
    assert note.duration==note.end-note.start

data_normal=voice_instr.synthesize(SR)
wavfile.write(RES_DIR/"guitar_only.wav", SR, data_normal)

# %% Slow everything down

for note in voice_instr.notes:
    note.start=2*note.start
    note.end=2*note.end
    assert note.duration==note.end-note.start

data_slow=voice_instr.synthesize(SR)
wavfile.write(RES_DIR/"guitar_only_slow.wav", SR, data_slow)


# %%
