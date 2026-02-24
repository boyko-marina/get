import mcp4725_driver as mcpdr
import signal_generator as sg
import time


try:
    amplitude = 2
    signal_frequency = 10
    sampling_frequency = 500
    mcp = mcpdr.MCP4725(5.0, 0x61, True)

    while True:
        try:
            t = time.time()
            voltage = sg.get_triangle_amplitude(signal_frequency, t)
            mcp.set_voltage(voltage*amplitude)
            sg.wait_for_sampling_period(sampling_frequency)
        except ValueError:
            print("Вы ввели не число. Попробуйте ещё раз\n")

finally:
    mcp.deinit()
