import time
from r2r_adc_22 import R2R_ADC
import adc_plot

DYNAMIC_RANGE = 3.3
DURATION = 3.0
COMPARE_TIME = 0.0001

adc = R2R_ADC(dynamic_range=DYNAMIC_RANGE, compare_time=COMPARE_TIME)

voltage_values = []
time_values = []

try:
    start_time = time.time()
    while (time.time() - start_time) < DURATION:
        voltage = adc.get_sc_voltage()
        current_time = time.time() - start_time
        voltage_values.append(voltage)
        time_values.append(current_time)

    adc_plot.plot_voltage_vs_time(time_values, voltage_values, DYNAMIC_RANGE)

    adc_plot.plot_sampling_period_hist(time_values)

except Exception as e:
    print(f"Ошибка во время измерений: {e}")

finally:
    adc.deinit()
