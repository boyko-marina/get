import time
from r2r_adc import R2R_ADC   # предполагается, что исправленный класс лежит в этом файле
import adc_plot               # наш модуль для построения графика

# === Настраиваемые параметры ===
DYNAMIC_RANGE = 3.3      # В, максимальное напряжение (диапазон ЦАП)
DURATION = 3.0            # с, время измерения
COMPARE_TIME = 0.0001     # с, время сравнения (согласно заданию)
# ===============================

# Создаём объект АЦП
adc = R2R_ADC(dynamic_range=DYNAMIC_RANGE, compare_time=COMPARE_TIME)

# Списки для накопления данных
voltage_values = []
time_values = []

try:
    start_time = time.time()
    while (time.time() - start_time) < DURATION:
        # Измеряем напряжение методом последовательного счёта (можно заменить на get_sar_voltage)
        voltage = adc.get_sc_voltage()
        current_time = time.time() - start_time
        voltage_values.append(voltage)
        time_values.append(current_time)

    # Построение графика
    adc_plot.plot_voltage_vs_time(time_values, voltage_values, DYNAMIC_RANGE)

except Exception as e:
    print(f"Ошибка во время измерений: {e}")

finally:
    # Обязательно освобождаем GPIO
    adc.deinit()
