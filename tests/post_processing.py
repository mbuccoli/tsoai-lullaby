from pathlib import Path

import numpy as np

from open_isolate_slowdown_midi import to_int16, synthesize_samples, slowdown
import os
import soundfile as sf
from scipy.signal import lfilter

RES_DIR = Path(os.environ["TSOAI_HACK_LULLABY_RESOURCES"])


def lp(x, rate):
    b = [rate]
    a = [1, rate - 1]
    return lfilter(b, a, x)


def rand_N(range_x, N):
    return np.random.randint(range_x[0] * N, range_x[1] * N) / N


def add_noise(signal, sr):
    noise_pars = {
        "SNR_range": [10, 30],  # what's the SNR w.r.t. the lullaby?
        "dur_range": [3, 10],  # duration of each noise wave
        "overlap_secs": [0.2, 1],  # second of overlap between two waves
        "lp_factor_range": [0.01, 0.2],  # rates for low-pass filters
    }

    white_noise_array = np.zeros(signal.size)  # zeroes with the array
    k = 0  # starting with the first sample

    while k < white_noise_array.size:
        # computing random parameter
        dur_noise = rand_N(noise_pars["dur_range"], 1000)
        lp_rate = rand_N(noise_pars["lp_factor_range"], 10000)
        target_SNR_dB = rand_N(noise_pars["SNR_range"], 10)
        overlap_sec = rand_N(noise_pars["overlap_secs"], 10)
        overlap_sample = int(overlap_sec * sr)

        # generate the noise with 1 second more of length 
        # I am directly applying lowpass, so removing the first 1second will
        # avoid smooth transition
        noise_i = lp(np.random.normal(0, 1, int((1 + dur_noise) * sr)), lp_rate)
        noise_i = noise_i[sr:]

        N = noise_i.size
        ampl = np.sin(np.linspace(0, np.pi, N))  # sine between 0 to 1 and back to 0 in N samples
        noise_i = noise_i * ampl

        # samples will be betweek k and k+max_N
        max_N = min(white_noise_array.size - k, noise_i.size)

        # computing gain to scale noise to a given snr
        energy_noise = np.std(noise_i[:max_N])
        energy_sig = np.std(signal[k:k + max_N])
        cur_SNR_dB = 20 * np.log10(energy_sig / energy_noise)
        diff_SNR = np.power(10, (target_SNR_dB - cur_SNR_dB) / 20)

        # assert diff_SNR<1, "Problem"
        noise_i = noise_i * (1 / diff_SNR)

        # summing the noise_i component in the white_noise array
        white_noise_array[k:k + max_N] = white_noise_array[k:k + max_N] + noise_i[:max_N]

        # updating k takes into account the overlap
        k += noise_i.size - overlap_sample

    return white_noise_array + signal


def post_process(
        re_synth_slow,
        sr,
        fn_in,
        fn_out,
        lowpass_rate=0.1,
):
    """

    Returns:

    """
    # TODO do this with temporary files
    re_synth_slow_lp = lp(re_synth_slow, lowpass_rate)
    sf.write(fn_in, to_int16(re_synth_slow_lp, 0.5), sr)

    fn_out_rev = fn_in.replace('.wav', '_rev.wav')
    os.system(f"sox {fn_in} {fn_out_rev} reverb 75 70 75 100 25 3")

    # %%

    lullaby_lp_reverb, sr = sf.read(fn_out_rev)

    # replace all below with:
    lullaby_lp_reverb_sea= add_noise(lullaby_lp_reverb, sr)
    sf.write(fn_out, to_int16(lullaby_lp_reverb_sea, 0.7), sr)
    return

    noise_pars = {
        "SNR_range": [-30, -18],
        "dur_range": [3, 10],
        "overlap_secs": [0.2, 1],
        "lp_factor_range": [0.01, 0.2],
    }

    energy = np.std(lullaby_lp_reverb)
    white_noise_array = np.zeros(lullaby_lp_reverb.size)
    k = 0

    while k < white_noise_array.size:
        dur_noise = rand_N(noise_pars["dur_range"], 1000)
        lp_rate = rand_N(noise_pars["lp_factor_range"], 10000)
        target_SNR_dB = rand_N(noise_pars["SNR_range"], 10)
        overlap_sec = rand_N(noise_pars["overlap_secs"], 10)
        overlap_sample = int(overlap_sec * sr)
        # print(dur_noise, target_SNR_dB, overlap_sec)

        noise_i = lp(np.random.normal(0, 1, int((1 + dur_noise) * sr)), lp_rate)
        noise_i = noise_i[sr:]  # add one second to avoid smoothing entrance
        N = noise_i.size
        ampl = np.sin(np.linspace(0, np.pi, N))
        noise_i = noise_i * ampl
        energy_noise = np.std(noise_i)
        cur_SNR_dB = 20 * np.log10(energy / energy_noise)
        diff_SNR = np.power(10, (target_SNR_dB - cur_SNR_dB) / 20)
        # assert diff_SNR<1, "Problem"
        noise_i = noise_i * diff_SNR
        max_N = min(white_noise_array.size - k, noise_i.size)
        white_noise_array[k:k + max_N] = white_noise_array[k:k + max_N] + noise_i[:max_N]
        k += noise_i.size - overlap_sample

    sf.write(fn_out,
             to_int16(lullaby_lp_reverb + white_noise_array, 0.7), sr)

# %%
