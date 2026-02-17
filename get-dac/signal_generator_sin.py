import numpy as np
import time

def get_sin_wave_amplitude(freq, time):
    raw = np.sin(2.0 * np.pi * freq * time)
    shifted = raw + 1
    normalised = shifted / 2.0

    return normalised

def wait_for_sampling_period(sampling_frequency):
    period = 1.0 / sampling_frequency
    time.sleep(period)
