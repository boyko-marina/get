import smbus
import time

class MCP3021:
    def __init__(self, dynamic_range, verbose=False):
        """
        Конструктор класса.
        :param dynamic_range: Динамический диапазон АЦП (опорное напряжение), В
        :param verbose: Флаг вывода отладочной информации
        """
        self.bus = smbus.SMBus(1)          # шина I2C-1 на Raspberry Pi
        self.dynamic_range = dynamic_range
        self.address = 0x4D                 # адрес MCP3021 по умолчанию
        self.verbose = verbose

    def deinit(self):
        """Освобождение ресурсов шины I2C"""
        self.bus.close()

    def get_number(self):
        """
        Чтение сырого значения из АЦП (10 бит).
        :return: целое число от 0 до 1023
        """
        try:
            # Читаем слово (2 байта) с устройства
            data = self.bus.read_word_data(self.address, 0)
        except OSError as e:
            print(f"Ошибка чтения I2C: {e}")
            return 0

        # В smbus.read_word_data() первый принятый байт становится младшим,
        # второй – старшим. Меняем местами для получения правильного порядка.
        lower_byte = data >> 8        # байт, пришедший первым (MSB устройства)
        upper_byte = data & 0xFF      # байт, пришедший вторым (LSB устройства)

        # Восстановление 10-битного значения согласно даташиту MCP3021
        number = (upper_byte << 2) | (lower_byte >> 6)

        if self.verbose:
            print(f"data=0x{data:04X}  upper_byte=0x{upper_byte:02X}  lower_byte=0x{lower_byte:02X}  number={number}")
        return number

    def get_voltage(self):
        """
        Перевод сырого значения АЦП в напряжение.
        :return: напряжение в вольтах
        """
        raw = self.get_number()
        # Для 10-битного АЦП максимальное значение 1023 соответствует dynamic_range
        return raw / 1023.0 * self.dynamic_range


if name == "__main__":
    # Динамический диапазон измеряется мультиметром на контакте PWR при замкнутой перемычке 5V.
    # В примере используется значение 5.19 В (рекомендуется уточнить под свою плату).
    adc = MCP3021(dynamic_range=5.19, verbose=False)

    try:
        while True:
            voltage = adc.get_voltage()
            print(f"{voltage:.3f} В")
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nИзмерения прерваны пользователем")
    finally:
        adc.deinit()
