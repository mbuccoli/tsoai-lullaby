# %%
import os

import numpy as np
from scipy.io import wavfile
from pathlib import Path

import pretty_midi

# This environment variables point to the "resources" directory 
# in our google drive
RES_DIR=Path(os.environ["TSOAI_HACK_LULLABY_RESOURCES"])
MIDI_FN=RES_DIR/'Toms_Diner.mid'
OUT_FN=RES_DIR/"guitar_only_slow.wav"
ID_INSTR=2
# %%
SR=48000

# %%
# Load MIDI file into PrettyMIDI object

def open_and_slow_down(midi_fn, id_instr, out_fn):
    midi_data = pretty_midi.PrettyMIDI(str(midi_fn))
    
    if id_instr=="ask":
        print("The instruments are the following")
        for n, instr in enumerate(midi_data.instr):
            print(f"{n} - {instr}")
        ans= input("What instrument do you want to choose?\n")
        id_instr=int(ans)
    
    voice_instr=midi_data.instruments[id_instr]

    # Starting from the beginning
    start_=voice_instr.notes[0].start
    for note in voice_instr.notes:
        note.start=(note.start-start_)
        note.end=(note.end-start_)
        assert note.duration==note.end-note.start

    # uncomment if you want to hear the normal version
    #data_normal=voice_instr.synthesize(SR)
    #wavfile.write(RES_DIR/"guitar_only.wav", SR, data_normal)

    # %% Slow everything down   

    for note in voice_instr.notes:
        note.start=2*note.start
        note.end=2*note.end
        assert note.duration==note.end-note.start

    data_slow=voice_instr.synthesize(SR)
    wavfile.write(out_fn, SR, data_slow)


# %%
if __name__=="__main__":
    open_and_slow_down(MIDI_FN, ID_INSTR, OUT_FN)