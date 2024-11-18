import matplotlib.pyplot as plt

L = 1.158
nu = 500000

# константы
R = 8.31446
T = 298.15

c_O2_сух = 0.20946  # мольная доля кислорода в чистом сухом воздухе
c_N2 = 0.78084  # мольная доля азота в сухом воздухе
c_Ar = 0.00934  # мольная доля аргона в сузом воздухе

M_O2 = 0.032
M_N2 = 0.028
M_Ar = 0.03995
M_H2O = 0.01802
M_CO2 = 0.04401

Cp_O2 = 29.4
Cp_N2 = 29.125
Cp_Ar = 20.79
Cp_H2O = 33.26
Cp_CO2 = 33.26

Cv_O2 = 20.79
Cv_N2 = 20.79
Cv_Ar = 12.47
Cv_H2O = 24.94
Cv_CO2 = 24.94

file_path1 = 'data1GAS.txt'
file_path2 = 'data2GAS.txt'

file_path3 = 'data1NOGAS.txt'
file_path4 = 'data2NOGAS.txt'

def read_data(file_path):
    with open(file_path, 'r') as file:
        data = [int(line.strip()) for line in file if line.strip().isdigit()]
    return data

def find_max(data):
    max_value = max(data)
    max_index = data.index(max_value)
    return max_value, max_index

data1 = read_data(file_path1)
data2 = read_data(file_path2)

data3 = read_data(file_path3)
data4 = read_data(file_path4)

max_value1, max_index1 = find_max(data1)
max_value2, max_index2 = find_max(data2)

max_value3, max_index3 = find_max(data3)
max_value4, max_index4 = find_max(data4)

offset1 = abs(max_index1 - max_index2)
offset2 = abs(max_index3 - max_index4)


print(f"Максимум в файле 1: {max_value1} (Индекс: {max_index1})")
print(f"Максимум в файле 2: {max_value2} (Индекс: {max_index2})")
print(f"Смещение между максимумами: {offset1}")
print(f"скорость звука в чистом воздухе {L*nu/offset1}")

print(' ')

print(f"Максимум в файле 3: {max_value3} (Индекс: {max_index3})")
print(f"Максимум в файле 4: {max_value4} (Индекс: {max_index4})")
print(f"Смещение между максимумами: {offset2}")
print(f"скорость звука в грязном воздухе {L*nu/offset2}")

V1 = L*nu/offset1
V2 = L*nu/offset2
def fun_chis(v2): # функция нахождения концентрации
    # от скорости в атмосферном воздухе
    phi_чист = 0.379

    c_H2O_чист=phi_чист*3170/101375

    k_1 = (1 - c_H2O_чист) * M_CO2 * Cp_CO2
    k_2 = (1 - c_H2O_чист) * M_CO2 * Cv_CO2
    k_3 = (1 - c_H2O_чист) * M_CO2

    a=(1 - c_H2O_чист) * (Cp_N2*M_N2*c_N2 + Cp_O2*M_O2*c_O2_сух + Cp_Ar*M_Ar*c_Ar) + c_H2O_чист*M_H2O*Cp_H2O
    b=(1 - c_H2O_чист) * (Cv_N2*M_N2*c_N2 + Cv_O2*M_O2*c_O2_сух + Cv_Ar*M_Ar*c_Ar) + c_H2O_чист*M_H2O*Cv_H2O
    c=(1 - c_H2O_чист) * (M_N2*c_N2 + M_O2*c_O2_сух + M_Ar*c_Ar) + c_H2O_чист*M_H2O

    #коэффициенты квадратного уранения
    e1=v2*k_2*k_3
    e2=v2*(k_2*c+k_3*b)-k_1*R*T
    e3=v2*b*c-a*R*T

    # решение квадратного уравнения
    d = e2 ** 2 - 4 * e1 * e3
    x = (-e2 + d ** 0.5) / (2 * e1)
    #print(x)
    #print(v2**0.5)
    return x


def fun_graz(v2): # для выдыхаемого воздуха, все аналогично
    # от скорости в атмосферном воздухе
    phi_грязн = 1

    c_H2O_грязн = phi_грязн * 3170 / 101375

    k_1 = (1 - c_H2O_грязн) * (M_CO2 * Cp_CO2 - M_O2 * Cp_O2)
    k_2 = (1 - c_H2O_грязн) * (M_CO2 * Cv_CO2 - M_O2 * Cv_O2)
    k_3 = (1 - c_H2O_грязн) * (M_CO2-M_O2)

    a = (1 - c_H2O_грязн) * (Cp_N2 * M_N2 * c_N2 + Cp_O2 * M_O2 * c_O2_сух + Cp_Ar * M_Ar * c_Ar) + c_H2O_грязн * M_H2O * Cp_H2O
    b = (1 - c_H2O_грязн) * (Cv_N2 * M_N2 * c_N2 + Cv_O2 * M_O2 * c_O2_сух + Cv_Ar * M_Ar * c_Ar) + c_H2O_грязн * M_H2O * Cv_H2O
    c = (1 - c_H2O_грязн) * (M_N2 * c_N2 + M_O2 * c_O2_сух + M_Ar * c_Ar) + c_H2O_грязн * M_H2O

    # коэффициенты квадратного уранения
    e1 = v2 * k_2 * k_3
    e2 = v2 * (k_2 * c + k_3 * b) - k_1 * R * T
    e3 = v2 * b * c - a * R * T

    # решение квадратного уравнения
    d = e2 ** 2 - 4 * e1 * e3
    x = (-e2 + d ** 0.5) / (2 * e1)
    #print(x)
    #print(v2 ** 0.5)
    return x

#график чистого воздуха
mas_x_chis=[i/10 for i in range(3350, 3469)]
mas_y_chis=[fun_chis(i**2) for i in mas_x_chis]
c_CO2_чист = fun_chis(V1**2)


#график грязного воздуха
mas_x_graz=[i/10 for i in range(3430, 3481)]
mas_y_graz=[fun_graz(i**2) for i in mas_x_graz]
c_CO2_грязн = fun_graz(V2**2)

print(' ')
print(f"процент углекислого газа в чистом воздухе {c_CO2_чист*100}")
print(f"процент углекислого газа в выдохе {c_CO2_грязн*100}")

'''
plt.figure(figsize=(10, 6))
plt.plot(data1, label='Данные 1 файла', linestyle='-', color='b')  # Первая линия синего цвета
plt.plot(data2, label='Данные 2 файла', linestyle='--', color='r')  # Вторая линия красного цвета с пунктиром
plt.axvline(x=max_index1, color='blue', linestyle=':', label='Максимум 1 файла')  # Линия на максимуме первого файла
plt.axvline(x=max_index2, color='red', linestyle=':', label='Максимум 2 файла')   # Линия на максимуме второго файла

plt.xlabel('Индекс')
plt.ylabel('Значение')
plt.title('График')
plt.legend()
plt.grid(True)
plt.show()
'''
fig, ax=plt.subplots()
ax.grid(which='major', color = 'k')
ax.minorticks_on()
ax.grid(which='minor', color = 'gray', linestyle = ':')

ax.plot([i*100 for i in mas_y_chis], mas_x_chis, label = 'атмосферный', color='blue')
ax.plot([i*100 for i in mas_y_graz], mas_x_graz, label = 'выдыхаемый', color='red')
ax.scatter(c_CO2_чист*100, V1, c='blue')
ax.scatter(c_CO2_грязн*100, V2, c='red')

ax.legend(shadow = False, loc = 'right', fontsize = 10)
ax.set_xlabel("содержание углекислого газа, %")
ax.set_ylabel("скорость звука, м/с")
plt.show()



