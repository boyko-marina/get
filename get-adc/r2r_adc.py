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
        #print(f"Число на вход АЦП: {number}, биты: {bits}")
        GPIO.output(self.bits_gpio, bits)

    def sequential_counting_acd(self):
        for value in range(256):
            R2R_ADC.number_to_dac(self, value)
            time.sleep(self.compare_time)
            if (GPIO.input(self.comp_gpio)==1):
                #print(f"Число на вход АЦП: {value}, напряжение - {voltage}В")
                return value
        #print("Число на выходе АЦП: 256, напряжение - 3.2В")
        return 255

    def get_sc_voltage(self):
        value = R2R_ADC.sequential_counting_acd(self)
        return (value/255)*self.dynamic_range

    def successive_approximation_adc(self):
        right = 256
        left = 0
        value = 0
        while (right-left>1):
            value = (right+left)//2
            R2R_ADC.number_to_dac(self, value)
            time.sleep(self.compare_time)
            if (GPIO.input(self.comp_gpio)==1):
                right=value
            else:
                left=value
        return value

    def get_sar_voltage(self):
        value = R2R_ADC.successive_approximation_adc(self)
        return (value/255)*self.dynamic_range


if __name__ == "__main__":
    try:
        adc = R2R_ADC(3.2, 0.1)
        while True:
            voltage = adc.get_sar_voltage()
            print(f"Напряжение: {voltage}")
    finally:
        adc.deinit()
