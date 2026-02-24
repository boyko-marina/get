import r2r_dac as r2r
import signal_generator as sg
import time

try:
    amplitude = 3.2
    signal_frequency = 10
    sampling_frequency = 100
    dac = r2r.R2R_DAC([16, 20, 21, 25, 26, 17, 27, 22], 3.183, True)

    while True:
        try:
            t = time.time()
            voltage = sg.get_sin_wave_amplitude(signal_frequency, t)
            dac.set_voltage(voltage*amplitude)
            sg.wait_for_sampling_period(sampling_frequency)
        except ValueError:
            print("Вы ввели не число. Попробуйте ещё раз\n")

finally:
    dac.deinit()
