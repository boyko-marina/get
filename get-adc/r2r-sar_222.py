import r2r_adc as adc
import adc_plot as plot
import time

# Создаём объект АЦП с динамическим диапазоном 3.2 В
adc_device = adc.R2R_ADC(3.2)

voltages = []      # список измеренных напряжений
times = []         # список моментов времени
duration = 3.0     # продолжительность эксперимента (секунд)

try:
    start_time = time.time()
    while time.time() - start_time < duration:
        current_time = time.time() - start_time
        times.append(current_time)
        voltages.append(adc_device.get_sar_voltage())

    # Построение графика зависимости напряжения от времени
    plot.plot_voltage_vs_time(times, voltages, adc_device.dynamic_range * 1.1)

    # Построение гистограммы периодов дискретизации
    plot.plot_sampling_period_hist(times)

except KeyboardInterrupt:
    print("\nИзмерение прервано досрочно")
finally:
    adc_device.deinit()
