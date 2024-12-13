import matplotlib.pyplot as plt
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

dac = [8, 11, 7, 1, 0, 5, 12, 6]

led = [2, 3, 4, 17, 27, 22, 10, 9]

comp = 14

troyka = 13

measured_data = [0] * 100000

number_of_measuring = 0

flag = 0

GPIO.setup(dac, GPIO.OUT)

GPIO.setup(led, GPIO.OUT)

GPIO.setup(troyka, GPIO.OUT)

GPIO.setup(comp, GPIO.IN)

GPIO.output(troyka, 0)

def decimal2binary(value):            #перевод десятичного числа в двоичное
    return [int(element) for element in bin(value)[2:].zfill(8)]

t = 0.0
Time = 0.0
def adc(T):                     #измерение напряжения
    global Time
    current_code = 128
    for i in range(0, 8):
        GPIO.output(dac, decimal2binary(int(current_code)))
        time.sleep(0.01)
        T +=0.01
        if (GPIO.input(comp) == 0):
            current_code += 128/2**(i+1)
        else:
            current_code -= 128/2**(i+1)
    Time += T
    output_current = 3.3/256*current_code
    return output_current, T, int(current_code)

try:
    if (input() == "s"):
        GPIO.output(troyka, 1)
        Time_1 = 0
        while(1):    #зарядка конденсатора
            #print('напряжение на входе S: ', adc(t)[0],' В,   затрачено времени: ', adc(t)[1], ' с')
            measured_data[number_of_measuring] = adc(t)[2]
            print(measured_data[number_of_measuring])
            if(measured_data[number_of_measuring] >= 230):
                Time_1 = Time
                #print("время зарядки:  ",Time_1)
                break
            number_of_measuring += 1
        GPIO.output(troyka, 0)
        #Time = 0
        while(1):   #разрядка конденсатора
            measured_data[number_of_measuring] = adc(t)[2]
            print(measured_data[number_of_measuring])
            if(measured_data[number_of_measuring] <= 25):
                print("время зарядки:  ",Time_1, "c   время разрядки:", Time - Time_1, "c")
                break
            number_of_measuring += 1
        plt.plot(measured_data[:number_of_measuring])
        measured_data_str = [str(item) for item in measured_data[:number_of_measuring]]
        
        with open("data.txt", "w") as outfile:         #файл с данными
            outfile.write("\n".join(measured_data_str))
            
        with open("data_time.txt", "w") as outfile_2:   #файл с характеристиками
            outfile_2.write('средняя частота дискретизации: ')
            outfile_2.write(str(number_of_measuring/Time))
            outfile_2.write(' измерений в секунду')
            outfile_2.write("\n")
            outfile_2.write('шаг квантованя АЦП: ')
            outfile_2.write(str(3.3/255))
            outfile_2.write(' В')
        
        plt.show()   #график
    

finally:
    GPIO.output(dac, decimal2binary(0))