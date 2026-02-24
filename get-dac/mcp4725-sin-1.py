import mcp4725_driver_1 as mcpdr
import signal_generator as sg
import time
import sys

# Параметры сигнала
amplitude = 3.2
signal_frequency = 10
sampling_frequency = 500

def main():
    dac = None
    try:
        # Инициализация с проверкой
        try:
            dac = mcpdr.MCP4725(dynamic_range=5.0, address=0x61, verbose=True)
            # Небольшая задержка для стабилизации
            time.sleep(0.1)
        except Exception as e:
            print(f"Не удалось инициализировать MCP4725: {e}")
            print("Проверьте подключение и включите I2C (sudo raspi-config)")
            sys.exit(1)

        print("Генерация синусоидального сигнала. Для остановки нажмите Ctrl+C")
        while True:
            try:
                t = time.time()
                norm_voltage = sg.get_sin_wave_amplitude(signal_frequency, t)
                voltage = norm_voltage * amplitude
                dac.set_voltage(voltage)
                sg.wait_for_sampling_period(sampling_frequency)
            except KeyboardInterrupt:
                print("\nОстановка по запросу пользователя")
                break
            except OSError as e:
                print(f"Ошибка ввода-вывода I2C: {e}")
                print("Попытка восстановления...")
                time.sleep(0.5)
                # Можно попробовать переинициализировать устройство
                try:
                    dac.deinit()
                    dac = mcpdr.MCP4725(dynamic_range=5.0, address=0x61, verbose=True)
                except:
                    print("Не удалось восстановить соединение. Выход.")
                    break
            except Exception as e:
                print(f"Неожиданная ошибка: {e}")
                break

    finally:
        if dac:
            dac.deinit()
            print("ЦАП деинициализирован")

if name == "__main__":
    main()
