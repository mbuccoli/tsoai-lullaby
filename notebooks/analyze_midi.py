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
def lp(x,rate):
    b= [rate]
    a= [1,rate-1]
    return lfilter(b, a, x)

re_synth_slow_lp=lp(re_synth_slow, rate)
sf.write(RES_DIR/"test_midi"/"lullaby_lp.wav", to_int16(re_synth_slow_lp, 0.7), sr)

# %%
fn_in=RES_DIR/"test_midi"/"lullaby_lp.wav"
fn_out=RES_DIR/"test_midi"/"lullaby_reverb.wav"
os.system(f"sox {fn_in} {fn_out} reverb 75 70 75 100 25 3")

i_l=int(1.75*sr)
i_r=int(1.85*sr)
t=np.arange(re_synth_slow[i_l:i_r].size)/sr
plt.plot(t,np.abs(re_synth_slow[i_l:i_r]), lw=5)
plt.plot(t,np.abs(re_synth_slow_lp[i_l:i_r]))

# %%
noise_pars={
    "SNR_range":[-30, -18],
    "dur_range":[3, 10],
    "overlap_secs":[0.2, 1],
    "lp_factor_range":[0.01, 0.2],
}
lullaby_lp_reverb, sr=sf.read(fn_out)
energy=np.std(lullaby_lp_reverb)
white_noise_array=np.zeros(lullaby_lp_reverb.size)
k=0
def rand_N(range_x, N):
    return np.random.randint(range_x[0]*N, range_x[1]*N)/N

while k < white_noise_array.size:
    dur_noise=rand_N(noise_pars["dur_range"],1000) 
    lp_rate=rand_N(noise_pars["lp_factor_range"],10000)
    target_SNR_dB=rand_N(noise_pars["SNR_range"],10)
    overlap_sec=rand_N(noise_pars["overlap_secs"],10)
    overlap_sample=int(overlap_sec*sr)
    print(dur_noise, target_SNR_dB, overlap_sec)

    noise_i=lp(np.random.normal(0, 1, int((1+dur_noise)*sr)), lp_rate)
    noise_i=noise_i[sr:] # add one second to avoid smoothing entrance
    N=noise_i.size
    ampl=np.sin(np.linspace(0,np.pi, N))    
    noise_i=noise_i*ampl
    energy_noise=np.std(noise_i)
    cur_SNR_dB=20*np.log10(energy/energy_noise)
    diff_SNR = np.power(10, (target_SNR_dB - cur_SNR_dB)/20)
    #assert diff_SNR<1, "Problem"
    noise_i=noise_i*diff_SNR
    max_N=min(white_noise_array.size-k, noise_i.size)
    white_noise_array[k:k+max_N]=white_noise_array[k:k+max_N]+noise_i[:max_N]
    k+=noise_i.size-overlap_sample

sf.write(RES_DIR/"test_midi"/"lullaby_lp_rev_sea.wav", 
        to_int16(lullaby_lp_reverb+white_noise_array, 0.7), sr)

# %%
