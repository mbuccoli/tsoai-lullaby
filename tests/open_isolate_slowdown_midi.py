# %%
import os
from pathlib import Path

import numpy as np
import soundfile as sf
import matplotlib.pyplot as plt

import pretty_midi

# This environment variables point to the "resources" directory 
# in our google drive
RES_DIR=Path(os.environ["TSOAI_HACK_LULLABY_RESOURCES"])
MIDI_FN=RES_DIR/'Toms_Diner.mid'
OUT_FN=RES_DIR/"guitar_only_slow.wav"
ID_INSTR=2
# %%
SR=48000


#%%

# %%
def to_int16(x,gain):
    """
    From float x to np.int16 x, with a preliminary normalization
    gain can be used to scale the signal
    """
    return (gain*(x/np.max(np.abs(x)))*(2**15)).astype(np.int16)

def open_and_slow_down(midi_fn, out_fn,id_instr="all", mid_out_fn=""):
    """
    Open midi and slows it down, removing bending, writes the outout wav
    - midi fn: filename of the input midi
    - out_fn: filename of the output wav file
    - id_instr: the instrument track to take; if "ask" will ask the user, if "all" will combine all together. Define is all
    - mid_out_fn: outputs the wav file before the slowing

    """
    # Load MIDI file into PrettyMIDI object
    midi_data = pretty_midi.PrettyMIDI(str(midi_fn))
    
    if id_instr=="ask":
        print("The instruments are the following")
        for n, instr in enumerate(midi_data.instr):
            print(f"{n} - {instr}")
        ans= input("What instrument do you want to choose?\n")
        id_instr=int(ans)
        voice_instr=midi_data.instruments[id_instr]
    elif id_instr=="all":        
        voice_instr=midi_data.instruments[0]
        for instr in midi_data.instruments[1:]:
            voice_instr.notes.extend(instr.notes)
    else:
        voice_instr=midi_data.instruments[id_instr]
    # Starting from the beginning
    start_=np.min([note.start for note in voice_instr.notes])
    for note in voice_instr.notes:
        note.start=(note.start-start_)
        note.end=(note.end-start_)
        assert note.duration==note.end-note.start
    voice_instr.pitch_bends=[]
    
    # uncomment if you want to hear the normal version
    if mid_out_fn!="":
        data_normal=voice_instr.synthesize(SR)
        sf.write(mid_out_fn, to_int16(data_normal, 0.707), SR)

    # %% Slow everything down   

    for note in voice_instr.notes:
        note.start=2*note.start
        note.end=2*note.end
        assert note.duration==note.end-note.start

    data_slow=voice_instr.synthesize(SR)
    sf.write(out_fn, to_int16(data_slow, 0.707), SR)
    return data_slow, voice_instr

# %%
if __name__=="__main__":
    open_and_slow_down(MIDI_FN, ID_INSTR, OUT_FN)