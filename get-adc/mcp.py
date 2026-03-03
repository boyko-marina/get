import mcp3021_driver as driver
import adc_plot
import time

mcp = driver.MCP3021(5.19)
voltages = []
times = []
duration = 3.0
try:
    start_time = time.time()
    while (time.time() - start_time < duration):
        times.append(time.time() - start_time)
        voltages.append(mcp.get_voltage())
    adc_plot.plot_voltage_vs_time(times, voltages, mcp.dynamic_range*1.1)
    adc_plot.plot_sampling_period_hist(times)
finally:
    mcp.deinit()
