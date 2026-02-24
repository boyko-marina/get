import mcp4725_driver_1 as mcpdr
import signal_generator as sg
import time

# Параметры генерируемого сигнала
amplitude = 3.2          # амплитуда (В) – не должна превышать dynamic_range ЦАП
signal_frequency = 10    # частота синуса (Гц)
sampling_frequency = 500 # частота дискретизации (Гц)

try:
    # Инициализация ЦАП MCP4725
    # dynamic_range = 5.0 В, адрес 0x61, вывод отладочной информации включён
    dac = mcpdr.MCP4725(dynamic_range=5.0, address=0x61, verbose=True)

    print("Генерация синусоидального сигнала. Для остановки нажмите Ctrl+C")
    while True:
        try:
            # Текущее время
            t = time.time()
            # Нормализованное значение синуса от 0 до 1
            norm_voltage = sg.get_sin_wave_amplitude(signal_frequency, t)
            # Масштабирование к заданной амплитуде
            voltage = norm_voltage * amplitude
            # Установка напряжения на ЦАП
            dac.set_voltage(voltage)
            # Выдержка периода дискретизации
            sg.wait_for_sampling_period(sampling_frequency)
        except KeyboardInterrupt:
            print("\nОстановка по запросу пользователя")
            break
        except Exception as e:
            print(f"Ошибка в цикле: {e}")
            break

finally:
    # Корректное закрытие I2C-шины
    dac.deinit()
    print("ЦАП деинициализирован")
