import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
dac = [8, 11, 7, 1, 0, 5, 12, 6]
GPIO.setup(dac + [13], GPIO.OUT)
GPIO.setup(24, GPIO.IN)
GPIO.output(13, 1)

def voltage(x):
    schet = 0
    for i in str(x):
        if (i in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']):
            t = 1
        else:
            GPIO.output(dac, 0)     
            schet += 1
    if(schet != 0):
        schet = 0
        print("Incorrect")
        return 0
    if ( float(x) < 0 or float(x) > 255):
        GPIO.output(dac, 0)
        print("Over the range")
        return 0
    x = int(x)
    a = bin(x)[2::]
    lst = [0] * 8
    for i in range(len(a)):
        lst[8 - len(a) + i] = int(a[i])
    GPIO.output(dac, lst)
    return (x / 255 * 3.3)
voltage(0)
voltage(128)
st = 128
cc = 64
while cc != 0:
    voltage (st)
    time.sleep(0.1)
    if (GPIO.input(24) == 0):
        st += cc
    else:
        st -= cc
    cc //= 2
    print(st, cc)
    
