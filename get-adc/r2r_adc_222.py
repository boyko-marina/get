import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

class R2R_ADC:
    def __init__(self, dynamic_range, compare_time=0.01, verbose=False):
        self.dynamic_range = dynamic_range
        self.verbose = verbose
        self.compare_time = compare_time

        self.bits_gpio = [26, 20, 19, 16, 13, 12, 25, 11]
        self.comp_gpio = 21

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.bits_gpio, GPIO.OUT, initial=0)
        GPIO.setup(self.comp_gpio, GPIO.IN)

    def deinit(self):
        GPIO.output(self.bits_gpio, 0)
        GPIO.cleanup()

    def number_to_dac(self, number):
        bits = [int(element) for element in bin(number)[2:].zfill(8)]
        GPIO.output(self.bits_gpio, bits)

    def sequential_counting_acd(self):
        for value in range(256):
            self.number_to_dac(value)
            time.sleep(self.compare_time)
            if GPIO.input(self.comp_gpio) == 1:
                return value
        return 255

    def get_sc_voltage(self):
        value = self.sequential_counting_acd()
        return (value / 255) * self.dynamic_range

    def successive_approximation_adc(self):
        right = 256
        left = 0
        while right - left > 1:
            value = (right + left) // 2
            self.number_to_dac(value)
            time.sleep(self.compare_time)
            if GPIO.input(self.comp_gpio) == 1:
                right = value
            else:
                left = value
        return right  # возвращаем правую границу – первое значение, вызвавшее срабатывание компаратора

    def get_sar_voltage(self):
        value = self.successive_approximation_adc()
        return (value / 255) * self.dynamic_range


if name == "__main__":
    try:
        adc = R2R_ADC(3.2, 0.1)
        while True:
            voltage = adc.get_sar_voltage()
            print(f"Напряжение: {voltage:.3f} В")
    except KeyboardInterrupt:
        print("\nИзмерение прервано пользователем")
    finally:
        adc.deinit()
