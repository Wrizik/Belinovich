import RPi.GPIO as gpio
import sys
from time import sleep
gpio.setmode(gpio.BCM)
gpio.setup(2, gpio.OUT)
dac=[26, 19, 13, 6, 5, 11, 9, 10]
gpio.setup(dac, gpio.OUT, initial=gpio.HIGH)
pwm=gpio.PWM(2, 1000)
pwm.start(0)

try:
        while True:
                DutyCicle=int(input())
                pwm.ChangeDutyCycle(DutyCicle)
                print("{:.2f}".format(DutyCicle*3.3/100))
finally:
    gpio.output(2, 0)
    gpio.output(dac, 0)
    gpio.cleanup()   