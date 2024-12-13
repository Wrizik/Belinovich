import RPi.GPIO as GPIO
import time
import matplotlib.pyplot as plt
GPIO.setwarnings(False)

def decimal2binary(value):
    return [int(element) for element in bin(value)[2:].zfill(8)]

dac = [8,11,7,1,0,5,12,6]
leds = [2, 3, 4, 17, 27, 22, 10, 9]
comp = 14
troyka = 13 

GPIO.setmode(GPIO.BCM)
GPIO.setup(dac, GPIO.OUT)
GPIO.setup(comp,GPIO.IN)
volts = []


try:
    flag = 0
    t_begin = time.time()
    GPIO.setup(troyka, GPIO.OUT, initial = GPIO.HIGH)
    while True:
        N = 0
        for i in range(7, -1, -1):
            N+=2**i
            dec_i = [int(bit) for bit in bin(N)[2:].zfill(8)]
            GPIO.output(dac, dec_i)
            time.sleep(0.006)
            compVal = GPIO.input(comp)
            if (compVal == 1):
                N-=2**i
        digitalVal = N
        voltage = digitalVal / 256 * 3.3
        if voltage > 2.6 and flag == 0:
            flag = 1
            GPIO.output(troyka, 0)
        volts.append(voltage)
        if flag and voltage < 2.27:
            break
        print(digitalVal, voltage)
    t_end = time.time()
    time_of_experiment = t_end - t_begin
    freq = time_of_experiment / len(volts)
    with open('/home/b03-404/py/freq.txt', 'w') as f_freq:
        f_freq.write(f'Frequency is {freq}')
    with open('/home/b03-404/py/data.txt', 'w') as f_data:
        for i in range(len(volts)):
            f_data.write(str(volts[i]) + '\n')  
    num_of_exp = [i for i in range(0, len(volts))]
    plt.plot(num_of_exp, volts)
    plt.show()          
finally:
    GPIO.output(dac, GPIO.LOW)
    GPIO.cleanup()