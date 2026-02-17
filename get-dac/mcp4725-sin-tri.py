import mcp4725_driver as mcp4725
import signal_generator_tri as sg
import time

amplitude = 3.0
signal_frequency = 10
sampling_frequency = 1000

if __name__ == "__main__":
    try:
        dac = mcp4725.MCP4725(5.21, 0x61 ,False)
        start_time = time.time()

        while True:
            t = time.time() - start_time

            norm_amp = sg.get_sin_wave_amplitude(signal_frequency, t)

            voltage = amplitude * norm_amp

            dac.set_voltage(voltage)

            sg.wait_for_sampling_period(sampling_frequency)

    finally:
        dac.deinit()
