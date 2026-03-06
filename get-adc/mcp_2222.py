import mcp3021_driver as driver
import adc_plot
import time

# Динамический диапазон должен быть измерен мультиметром (пример 5.19 В)
mcp = driver.MCP3021(dynamic_range=5.19)

voltages = []      # список измеренных напряжений
times = []         # список относительных моментов времени
duration = 3.0     # длительность эксперимента, секунд

try:
    start_time = time.time()
    while (time.time() - start_time) < duration:
        times.append(time.time() - start_time)
        voltages.append(mcp.get_voltage())
        # Можно добавить небольшую задержку, если нужна фиксированная частота
        # time.sleep(0.1)

    # Построение графика зависимости напряжения от времени
    adc_plot.plot_voltage_vs_time(times, voltages, mcp.dynamic_range * 1.1)

    # Построение гистограммы периодов дискретизации
    adc_plot.plot_sampling_period_hist(times)

finally:
    mcp.deinit()
