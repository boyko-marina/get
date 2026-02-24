import pwm_dac_1 as pwd
import signal_generator as sg
import time

if __name__ == "__main__":
    try:
        amplitude = 2
        signal_frequency = 10
        sampling_frequency = 1000
        dac = pwd.PWM_DAC(12, 500, 3.290, True)

        while True:
            try:
                t = time.time()
                voltage = sg.get_triangle_amplitude(signal_frequency, t)
                dac.set_voltage(voltage*amplitude)
                sg.wait_for_sampling_period(sampling_frequency)
            except ValueError:
                print("Вы ввели не число. Попробуйте ещё раз\n")

    finally:
        dac.deinit()
