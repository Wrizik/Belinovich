import numpy as np
import matplotlib.pyplot as plt
x=[]
y=[]
s=[]
sec = -1
with open('data.txt', 'r') as f:    
    for line in  f:   
        d=line.split(' ')   
        y.append(float(d[0]))
        sec+=1
with open('settings.txt', 'r') as f:    
    for line in  f:   
        h=line.split(' ') 
        s.append(float(h[0]))
descritization = float(s[0])
stepq = float(s[1])
h=sec/descritization
tmax=descritization*np.argmax(y)
x=np.array(x)
x=np.linspace(0, sec*descritization, sec+1)
y=np.array(y)
y= stepq*y
plt.plot(x,y, color='g')
plt.scatter(x, y, marker='v', s=5)
plt.title(" Процесс заряда и разряда конденсатора в RC-цепочке")
plt.ticklabel_format(style='sci', axis='both', scilimits=(0, 0), useMathText=True)
plt.minorticks_on()
plt.grid(   visible=True,  which='major',   linestyle='-',         linewidth=1.5, color='0.7')
plt.grid(   visible=True,  which='minor',   linestyle='--',        linewidth=1,   color='0.8')
plt.xlim([0, np.max(x) * 1.05])
plt.ylim([0, np.max(y) * 1.05])
plt.xlabel(" Время, с ")
plt.ylabel(" Напряжение, В")
plt.legend()
plt.show()
