import RPi.GPIO as GPIO
import time

class R2R_ADC:
    def __init__(self, dynamic_range, compare_time = 0.01):
        self.dynamic_range = dynamic_range
        self.compare_time = compare_time
        self.cur_res = 0

        self.bits_gpio = [26,20,19,16,13,12,25,11]
        self.comp_gpio = 21

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.bits_gpio, GPIO.OUT, initial = 0)
        GPIO.setup(self.comp_gpio, GPIO.IN)

    def deinit(self):
        GPIO.output(self.bits_gpio,0)
        GPIO.cleanup()

    def dec_to_bin(self, val):
        return [int(el) for el in bin(val)[2:].zfill(8)]

    def number_to_dac(self, num):
        GPIO.output(self.bits_gpio, self.dec_to_bin(num))

    def seq_get_vlt(self):
        self.cur_res = 0
        self.number_to_dac(0)
        while (True):
            cmp = GPIO.input(self.comp_gpio)
            if cmp > 0:
                break
            self.cur_res += 1
            if self.cur_res >= 256:
                self.cur_res = 255
                break
            self.number_to_dac(self.cur_res)
            time.sleep(self.compare_time)
        return self.cur_res*self.dynamic_range/255.0

    def sar_approx_vlt(self):
        self.cur_res = 0
        cb = 7
        time.sleep(self.compare_time)
        while (cb>=0):
            cmp = GPIO.input(self.comp_gpio)
            if cmp > 0:
                self.cur_res -= 1 << cb
            else:
                self.cur_res += 1 << cb
            if self.cur_res >= 256:
                self.cur_res = 255

            if self.cur_res < 0:
                self.cur_res = 0

            cb -= 1
            self.number_to_dac(self.cur_res)
            time.sleep(self.compare_time)
        return self.cur_res*self.dynamic_range/255.0



if __name__ == "__main__":
    try:
        mode = int(input())
    except ValueError:
        mode = 0

    try:
        adc = R2R_ADC(3.3, 0.01)
        while True:
            try:
                if mode == 0:
                    print(adc.seq_get_vlt())
                else:
                    print(adc.sar_approx_vlt())
            except ValueError:
                print("error")
    finally:
        adc.deinit()
