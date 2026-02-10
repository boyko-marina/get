import RPi.GPIO as GPIO


GPIO.setmode(GPIO.BCM)

led = 26
GPIO.setup(led, GPIO.OUT)

foto_trans = 6
GPIO.setup(foro_trans, GPIO.IN)

while True:
    state = not GPIO.input(foto_trans)
    GPIO.output(led, state)
