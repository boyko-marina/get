import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

led = 26
GPIO.setup(led, GPIO.OUT)

foto_trans = 6
GPIO.setup(foto_trans, GPIO.IN)

state = 0

while True:
    state = not state
    GPIO.output(foto_trans, state)

