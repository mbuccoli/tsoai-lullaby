# %%
import os
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
import soundfile as sf
from scipy.signal import lfilter
import sys
sys.path.append("../tests")
from open_isolate_slowdown_midi import to_int16, synthesize_samples, slowdown

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

# %% Joining data
full_data = pretty_midi.PrettyMIDI(str(MIDI_FN))

midi_data = pretty_midi.PrettyMIDI(str(MIDI_FN))
new_instr=midi_data.instruments[0]
for instr in midi_data.instruments[1:]:
    new_instr.notes.extend(instr.notes)
    new_instr.pitch_bends.extend(instr.pitch_bends)
midi_data.instruments=midi_data.instruments[:1]
write_debug(midi_data, "join_midi", RES_DIR /"test_midi")

# %% removing bending

midi_data.instruments[0].pitch_bends=[]
write_debug(midi_data, "without_bending", RES_DIR /"test_midi")

# %% With real samples
re_synth, sr=synthesize_samples(midi_data.instruments[0].notes)
sf.write(RES_DIR/"test_midi"/"mid_synth_samples.wav", to_int16(re_synth, 0.5), sr)
# %% Slowing everything down

midi_data.instruments[0].notes=slowdown(midi_data.instruments[0].notes)
re_synth_slow, sr=synthesize_samples(midi_data.instruments[0].notes)
sf.write(RES_DIR/"test_midi"/"mid_synth_samples_slow.wav", to_int16(re_synth_slow, 0.5), sr)

# %%
rate = 0.1
b= [rate]
a= [1,rate-1]


re_synth_slow_lp=lfilter(b, a, re_synth_slow)
sf.write(RES_DIR/"test_midi"/"lullaby_lp.wav", to_int16(re_synth_slow_lp, 0.7), sr)

# %%
fn_in=RES_DIR/"test_midi"/"lullaby_lp.wav"
fn_out=RES_DIR/"test_midi"/"lullaby_reverb.wav"
os.system(f"sox {fn_in} {fn_out} reverb 75 70 75 100 25 3")

# %%
i_l=int(1.75*sr)
i_r=int(1.85*sr)
t=np.arange(re_synth_slow[i_l:i_r].size)/sr
plt.plot(t,np.abs(re_synth_slow[i_l:i_r]), lw=5)
plt.plot(t,np.abs(re_synth_slow_lp[i_l:i_r]))

# %%

piano_roll=full_data.get_piano_roll()
plt.imshow(piano_roll[80:40:-1,:1700], aspect="auto", interpolation="none")


# %%


