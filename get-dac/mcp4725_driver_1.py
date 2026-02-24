import smbus

class MCP4725:
    def __init__(self, dynamic_range, address=0x61, verbose=True):
        self.bus = smbus.SMBus(1)          # шина I2C №1 (стандартная для Raspberry Pi)
        self.address = address
        self.wm = 0x00                      # режим записи без EEPROM
        self.pds = 0x00                      # нормальный режим (не power-down)
        self.verbose = verbose
        self.dynamic_range = dynamic_range   # опорное напряжение (макс. выход)

    def deinit(self):
        """Закрытие I2C-шины"""
        self.bus.close()

    def set_number(self, number):
        """Прямая запись 12-битного кода (0..4095) в ЦАП"""
        if not isinstance(number, int):
            print("Ошибка: значение должно быть целым числом")
            return
        if not (0 <= number <= 4095):
            print("Ошибка: число выходит за пределы 12 бит (0–4095)")
            return
        # Упаковка: первый байт = управляющие биты + старшие 4 бита данных
        first_byte = self.wm | self.pds | ((number >> 8) & 0x0F)
        second_byte = number & 0xFF          # младшие 8 бит
        self.bus.write_byte_data(self.address, first_byte, second_byte)
        if self.verbose:
            print(f"Установлен код {number:4d} -> напряжение {number/4095*self.dynamic_range:.3f} В")

    def set_voltage(self, voltage):
        """Установка выходного напряжения (0 .. dynamic_range)"""
        if not (0.0 <= voltage <= self.dynamic_range):
            print(f"Напряжение {voltage:.2f} В вне диапазона (0–{self.dynamic_range:.2f} В). Устанавливаю 0 В.")
            voltage = 0.0
        code = int(voltage / self.dynamic_range * 4095)   # 4095 соответствует Vref
        self.set_number(code)

# Простой тест при запуске модуля отдельно
if name == "__main__":
    try:
        dac = MCP4725(5.0, 0x61, True)
        while True:
            try:
                v = float(input("Введите напряжение (В): "))
                dac.set_voltage(v)
            except ValueError:
                print("Ошибка ввода, повторите")
            except KeyboardInterrupt:
                print("\nЗавершение")
                break
    finally:
        dac.deinit()
