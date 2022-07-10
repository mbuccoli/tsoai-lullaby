# %%
import os
from pathlib import Path

import numpy as np
import soundfile as sf
# import matplotlib.pyplot as plt

import pretty_midi

# This environment variables point to the "resources" directory 
# in our google drive
RES_DIR = Path(os.environ["TSOAI_HACK_LULLABY_RESOURCES"])
MIDI_FN = RES_DIR / 'Toms_Diner.mid'
OUT_FN = RES_DIR / "guitar_only_slow.wav"
ID_INSTR = 2
# %%
SR = 48000


# %%

# %%
def to_int16(x, gain):
    """
    From float x to np.int16 x, with a preliminary normalization
    gain can be used to scale the signal
    """
    return (gain * (x / np.max(np.abs(x))) * (2 ** 15)).astype(np.int16)


# def synthesize(notes, sample_directory, sample_format)

def slowdown(notes, slowdown_rate=2):
    new_notes = []
    for note in notes:
        new_note = pretty_midi.Note(note.velocity, note.pitch,
                                    slowdown_rate * note.start, slowdown_rate * note.end)
        new_notes.append(new_note)
        assert new_note.duration == new_note.end - new_note.start
    return new_notes


def synthesize_samples(notes, sample_directory=RES_DIR / "24Samples",
                       sample_format="samples{0:02d}.wav"):
    pitches_unique = np.unique([note.pitch for note in notes])

    if np.max(pitches_unique) - np.min(pitches_unique) < 24:
        print("Sorry but I'm going to do some wrapping here")

    notes_rescaled = []
    min_pitch = np.min(pitches_unique)
    max_end = 0
    for note in notes:
        new_note = pretty_midi.Note(note.velocity, ((note.pitch - min_pitch) % 24) + 1, note.start, note.end)
        notes_rescaled.append(new_note)
        if new_note.pitch == 25:
            print(note.pitch, new_note.pitch)

        max_end = max(max_end, new_note.end)
    pitches_unique = np.unique(np.mod(pitches_unique - min_pitch, 24) + 1)

    samples = {}
    max_peak = {}

    # loading samples...
    for pitch in pitches_unique:
        samples[pitch], sr = sf.read(sample_directory / sample_format.format(pitch))
        if samples[pitch].ndim > 1:  # multichannel
            samples[pitch] = samples[pitch][:, 0]  # consider left channel
        max_peak[pitch] = np.max(np.abs(samples[pitch]))

    y = np.zeros([int(sr * (max_end + 1)), ])

    for note in notes_rescaled:
        i_l = int(sr * (note.start))
        i_r = i_l + samples[note.pitch].size
        y[i_l:i_r] = y[i_l:i_r] + samples[note.pitch]
    return y, sr


def open_and_slow_down(midi_fn, out_fn, id_instr="all", mid_out_fn="", slowdown_rate=2):
    """
    Open midi and slows it down, removing bending, writes the outout wav
    - midi fn: filename of the input midi
    - out_fn: filename of the output wav file
    - id_instr: the instrument track to take; if "ask" will ask the user, if "all" will combine all together. Define is all
    - mid_out_fn: outputs the wav file before the slowing
    """
    # Load MIDI file into PrettyMIDI object
    midi_data = pretty_midi.PrettyMIDI(str(midi_fn))

    if id_instr == "ask":
        print("The instruments are the following")
        for n, instr in enumerate(midi_data.instr):
            print(f"{n} - {instr}")
        ans = input("What instrument do you want to choose?\n")
        id_instr = int(ans)
        voice_instr = midi_data.instruments[id_instr]
    elif id_instr == "all":
        voice_instr = midi_data.instruments[0]
        for instr in midi_data.instruments[1:]:
            voice_instr.notes.extend(instr.notes)
    else:
        voice_instr = midi_data.instruments[id_instr]
    # Starting from the beginning
    start_ = np.min([note.start for note in voice_instr.notes])
    for note in voice_instr.notes:
        note.start = (note.start - start_)
        note.end = (note.end - start_)
        assert note.duration == note.end - note.start
    voice_instr.pitch_bends = []

    # uncomment if you want to hear the normal version
    if mid_out_fn != "":
        data_normal, sr = synthesize_samples(voice_instr.notes)
        sf.write(mid_out_fn, to_int16(data_normal, 0.707), sr)

    # %% Slow everything down   
    voice_instr.notes = slowdown(voice_instr.notes, slowdown_rate=slowdown_rate)

    # data_slow=voice_instr.synthesize(SR)
    data_slow, SR = synthesize_samples(voice_instr.notes)
    # up to 64 notes because of reasons
    sf.write(out_fn, to_int16(data_slow, 0.707), SR)
    return data_slow, voice_instr, SR


# %%
if __name__ == "__main__":
    open_and_slow_down(MIDI_FN, OUT_FN, ID_INSTR)

if False:
    # %%
    sample_directory = RES_DIR / "24Samples"
    midi_data = pretty_midi.PrettyMIDI(str(MIDI_FN))
    notes = midi_data.instruments[2].notes[:64]
    sample_format = "samples{0:02d}.wav"
    # %%
    pitches_unique = np.unique([note.pitch for note in notes])
    assert np.max(pitches_unique) - np.min(pitches_unique) < 24
    # def synthesize(notes, sample_directory, sample_format)

    notes_rescaled = []
    min_pitch = np.min(pitches_unique)
    start_ = notes[0].start
    max_end = 0
    for note in slowdown(notes):
        notes_rescaled.append(
            pretty_midi.Note(note.velocity, note.pitch - min_pitch + 1, note.start - start_ + 1, note.end - start_ + 1))
        max_end = max(max_end, notes_rescaled[-1].end)
    pitches_unique = pitches_unique - min_pitch + 1
    # %%

    samples = {}
    max_peak = {}
    for pitch in pitches_unique:
        samples[pitch], sr = sf.read(sample_directory / sample_format.format(pitch))
        samples[pitch] = samples[pitch][:, 0]  # left channel
        max_peak[pitch] = np.max(np.abs(samples[pitch]))

    # %%

    y = np.zeros([int(sr * (max_end + 1)), ])

    for note in notes_rescaled:
        i_l = int(sr * (note.start))
        i_r = i_l + samples[note.pitch].size
        y[i_l:i_r] = y[i_l:i_r] + samples[note.pitch]

    # %%
    sf.write(RES_DIR / "toms_musicbox.wav", to_int16(y, 0.707), sr)

    # %%
