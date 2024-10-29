import RPi.GPIO as GPIO
import time
from matplotlib import plt

GPIO.setmode(GPIO.BCM)

LEDS=[&&, &&, &&, &&, &&, &&, &&, &&]
GPIO.setup(LEDS, GPIO.OUT)

dac=[&&, &&, &&, &&, &&, &&, &&, &&]
GPIO.setup(dac, GPIO.OUT, initial=GPIO.HIGH)

comp=&&
troyka=&&
GPIO.setup(troyka,GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(comp, GPIO.IN)

def to_binary(a):
    return [int (elem) for elem in bin(a)[2:].zfill(8)]

def adc():
    o=0
    for i in range(7, -1, -1):
        o+=2**i
        GPIO.output(dac, to_binary(o))
        time.sleep(0.05)
        if GPIO.input(comp)==0:
            o-=2**i
    return o

try:
    schet_2=0
    results=[]
    time_begin=time.time()
    schet=0

    print('ЗАРЯДКА КОНДЕНСАТОРА')
    while schet_2<256*0.25:
        schet_2=adc()
        results.append(schet_2)
        time.sleep(0)
        schet+=1
        GPIO.output(LEDS, to_binary(schet_2))

    GPIO.setup(troyka,GPIO.OUT, initial=GPIO.LOW)

    print('РАЗРЯДКА КОНДЕНСАТОРА')
    while schet_2>256*0.02:
        schet_2=adc()
        results.append(schet_2)
        time.sleep(0)
        schet+=1
        GPIO.output(LEDS, to_binary(schet_2))

    exp_time=time.time()-time_begin

    print('ЗАПИСЬ В .TXT ФАЙЛ')
    with open('data.txt', 'w') as f:
        for i in results:
            f.write(str(i) + '\n')
    with open('settings.txt', 'w') as f:
        f.write(str(1/exp_time/schet) + '\n')
        f.write('0.01289')
    
    print('общая продолжительность эксперимента {}, период одного измерения {}, средняя частота дискретизации {}, шаг квантования АЦП {}'.format(exp_time, exp_time/schet, 1/exp_time/schet, 0.013))

    #графики
    print('ГРАФИКИ')
    y=[i/256*3.3 for i in results]
    x=[i*exp_time/schet for i in range(len(results))]
    plt.plot(x, y)
    plt.xlabel('ВРЕМЯ')
    plt.ylabel('ВОЛЬТЫ')
    plt.minorticks_on()
    plt.grid(visible=True, which='minor', linewidth=2, color='r')
    plt.show()

finally:
    GPIO.output(LEDS, 0)
    GPIO.output(dac, 0)
    GPIO.cleanup()