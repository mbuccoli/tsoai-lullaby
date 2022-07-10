import numpy as np


def delay(audio,fs,Echo_duration_sec = 0.1,
          Delay_amp = 0.5,
          ):


    delay_len_samples = round(Echo_duration_sec*fs)
    IR = np.zeros(delay_len_samples)
    IR[0] = 1
    IR[-1] = Delay_amp
    output_sig = np.convolve(audio,IR)

    return output_sig