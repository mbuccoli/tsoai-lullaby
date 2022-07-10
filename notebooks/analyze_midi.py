# %%
import os
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
import soundfile as sf
import sys
sys.path.append("../tests")
from open_isolate_slowdown_midi import to_int16

import pretty_midi

# %%
RES_DIR = Path(os.environ["TSOAI_HACK_LULLABY_RESOURCES"])
MIDI_FN = RES_DIR / 'baby_shark' / "vocals_basic_pitch.mid"

# %%

sample_directory = RES_DIR / "24Samples"
sample_format = "samples{0:02d}.wav"

midi_data = pretty_midi.PrettyMIDI(str(MIDI_FN))
# %%
def write_debug(midi_data, fn_out, path_out=".", sr=48000, ):
    audio_data = midi_data.synthesize(sr)
    audio_fn = os.path.join(path_out, fn_out+".wav")    
    sf.write(audio_fn, to_int16(audio_data, 0.707), sr)

    midi_fn =  os.path.join(path_out, fn_out+".mid")
    midi_data.write(midi_fn)

# %%

midi_data = pretty_midi.PrettyMIDI(str(MIDI_FN))
new_instr=midi_data.instruments[0]
for instr in midi_data.instruments[1:]:
    new_instr.notes.extend(instr.notes)
    new_instr.pitch_bends.extend(instr.pitch_bends)
midi_data.instruments=midi_data.instruments[:1]
write_debug(midi_data, "join_midi", RES_DIR /"test_midi")

