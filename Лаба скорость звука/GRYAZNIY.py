import matplotlib.pyplot as plt

file_path1 = 'data1NOGAS.txt'
file_path2 = 'data2NOGAS.txt'

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

max_value1, max_index1 = find_max(data1)
max_value2, max_index2 = find_max(data2)

offset = abs(max_index1 - max_index2)

print(f"Максимум в файле 1: {max_value1} (Индекс: {max_index1})")
print(f"Максимум в файле 2: {max_value2} (Индекс: {max_index2})")
print(f"Смещение между максимумами: {offset}")

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