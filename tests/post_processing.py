from pathlib import Path

import numpy as np

from open_isolate_slowdown_midi import to_int16, synthesize_samples, slowdown
import os
import soundfile as sf
from scipy.signal import lfilter
from paths import RES_DIR

# RES_DIR = Path(os.environ["TSOAI_HACK_LULLABY_RESOURCES"])


def lp(x, rate):
    b = [rate]
    a = [1, rate - 1]
    return lfilter(b, a, x)


def rand_N(range_x, N):
    return np.random.randint(range_x[0] * N, range_x[1] * N) / N


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
    noise_pars = {
        "SNR_range": [-30, -18],
        "dur_range": [3, 10],
        "overlap_secs": [0.2, 1],
        "lp_factor_range": [0.01, 0.2],
    }

    lullaby_lp_reverb, sr = sf.read(fn_out_rev)

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
