import smbus
import time

class MCP4725:
    def __init__(self, dynamic_range, address=0x61, verbose=True):
        try:
            self.bus = smbus.SMBus(1)
            # Проверяем, отвечает ли устройство (читаем что-нибудь или просто пишем)
            # Для MCP4725 можно попробовать записать 0 и сразу прочитать (но это сложно)
            # Просто проверим, что шина открылась
        except FileNotFoundError:
            raise Exception("I2C шина не доступна. Включите I2C в raspi-config.")
        except Exception as e:
            raise Exception(f"Не удалось открыть I2C шину: {e}")

        self.address = address
        self.wm = 0x00
        self.pds = 0x00
        self.verbose = verbose
        self.dynamic_range = dynamic_range

        # Проверим, отвечает ли устройство, записав служебную команду (например, чтение)
        # Это необязательно, но поможет сразу выявить проблему.
        try:
            # Попробуем прочитать что-нибудь (любые данные). Для MCP4725 нет стандартного регистра,
            # но можно попытаться прочитать байт с адреса устройства – это вызовет ошибку, если устройство не отвечает.
            self.bus.read_byte(self.address)
        except OSError as e:
            self.bus.close()
            raise Exception(f"Устройство с адресом 0x{address:02X} не отвечает по I2C. Проверьте подключение.")

    def deinit(self):
        self.bus.close()

    def set_number(self, number):
        if not isinstance(number, int):
            print("Ошибка: значение должно быть целым числом")
            return
        if not (0 <= number <= 4095):
            print("Ошибка: число выходит за пределы 12 бит (0–4095)")
            return
        first_byte = self.wm | self.pds | ((number >> 8) & 0x0F)
        second_byte = number & 0xFF
        try:
            self.bus.write_byte_data(self.address, first_byte, second_byte)
        except OSError as e:
            print(f"Ошибка I2C при записи: {e}")
            raise  # Пробрасываем дальше для обработки в основном цикле
        if self.verbose:
            print(f"Установлен код {number:4d} -> напряжение {number/4095*self.dynamic_range:.3f} В")

    def set_voltage(self, voltage):
        if not (0.0 <= voltage <= self.dynamic_range):
            print(f"Напряжение {voltage:.2f} В вне диапазона (0–{self.dynamic_range:.2f} В). Устанавливаю 0 В.")
            voltage = 0.0
        code = int(voltage / self.dynamic_range * 4095)
        self.set_number(code)
