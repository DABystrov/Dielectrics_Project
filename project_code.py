import numpy as np

def select_elements (matrix, matrix_name):
    print(f"Выберите элемент из матрицы {matrix_name}:")
    print(f"Размер матрицы {matrix.shape}")
    row = int(input("Введите номер строки элемента: "))
    col = int(input("Введите номер столбца элемента: "))

    # Проверка валидности номеров строки и столбца
    if row <= 0 or row > matrix.shape[0]:
        print("Ошибка: Некорректный номер строки!")
        return
    if col <= 0 or col > matrix.shape[1]:
        print("Ошибка: Некорректный номер столбца!")
        return

    # Вывод выбранного элемента
    element = matrix[row - 1, col - 1]
    print(f"Выбранный элемент из матрицы {matrix_name}:")
    print(f"{matrix_name}[{row}, {col}]: {element}")


# Ввод углов поворота
angles = []
axes = ['1', '2', '3']

for i in range(3):
    angle = float(input(f"Угол поворота на оси {axes[i]} (в градусах): "))
    angles.append(angle)

# Ввод осей поворота
rotation_sequence = []
for i in range(3):
    axis = input(f"Ось поворота для угла {angles[i]}° (X, Y или Z): ")
    rotation_sequence.append(axis)

# Матрицы поворота
rot_matrices = []
for i in range(3):
    angle_rad = np.deg2rad(angles[i])
    axis = rotation_sequence[i]

    if axis == 'X':
        rot_matrix = np.array([[1, 0, 0, 0, 0, 0],
                               [0, np.cos(angle_rad), -np.sin(angle_rad), 0, 0, 0],
                               [0, np.sin(angle_rad), np.cos(angle_rad), 0, 0, 0],
                               [0, 0, 0, 1, 0, 0],
                               [0, 0, 0, 0, 1, 0],
                               [0, 0, 0, 0, 0, 1]])
    elif axis == 'Y':
        rot_matrix = np.array([[np.cos(angle_rad), 0, np.sin(angle_rad), 0, 0, 0],
                               [0, 1, 0, 0, 0, 0],
                               [-np.sin(angle_rad), 0, np.cos(angle_rad), 0, 0, 0],
                               [0, 0, 0, 1, 0, 0],
                               [0, 0, 0, 0, 1, 0],
                               [0, 0, 0, 0, 0, 1]])
    elif axis == 'Z':
        rot_matrix = np.array([[np.cos(angle_rad), -np.sin(angle_rad), 0, 0, 0, 0],
                               [np.sin(angle_rad), np.cos(angle_rad), 0, 0, 0, 0],
                               [0, 0, 1, 0, 0, 0],
                               [0, 0, 0, 1, 0, 0],
                               [0, 0, 0, 0, 1, 0],
                               [0, 0, 0, 0, 0, 1]])
    else:
        print("Ошибка: Неправильно указана ось поворота!")
        exit()

    rot_matrices.append(rot_matrix)

# Общая матрица поворота
rot_matrix = np.eye(6)
for i in range(3):
    rot_matrix = np.matmul(rot_matrix, rot_matrices[i])

# Функция для парсинга ввода
def parse_input(input_string, delimiter):
    values = input_string.split(delimiter)
    values = [val.strip() for val in values]
    return values

# Ввод значений матриц пьезомодулей, упругих податливостей и диэлектрических проницаемостей с клавиатуры
print("Введите значения матрицы пьезомодулей (3x6):")
d_input = []
for i in range(3):
    row_input = input(f"Введите значения {i+1}-й строки, разделенные пробелом: ")
    row_values = parse_input(row_input, ' ')
    d_input.append(row_values)
d_matrix = np.array(d_input, dtype=np.float64)

print("Введите значения матрицы упругих податливостей (6x6):")
s_E_input = []
for i in range(6):
    row_input = input(f"Введите значения {i+1}-й строки, разделенные пробелом: ")
    row_values = parse_input(row_input, ' ')
    s_E_input.append(row_values)
s_E_matrix = np.array(s_E_input, dtype=np.float64)

print("Введите значения матрицы диэлектрических проницаемостей (3x3):")
epsilon_input = []
for i in range(3):
    row_input = input(f"Введите значения {i+1}-й строки, разделенные пробелом: ")
    row_values = parse_input(row_input, ' ')
    epsilon_input.append(row_values)
e_matrix = np.array(epsilon_input, dtype=np.float64)

# Поворот матрицы пьезоэлектрических коэффициентов d
d_matrix_new = np.zeros((3, 6))
for i in range(3):
    for j in range(6):
        for k in range(3):
            for l in range(6):
                d_matrix_new[i, j] += d_matrix[k, l] * rot_matrix[i, k] * rot_matrix[j, l]

# Масштабирование матрицы d_matrix_new
d_matrix_new *= 1e-11

# Поворот матрицы упругих податливостей s_E
s_E_matrix_new = np.zeros((6, 6))
for i in range(6):
    for j in range(6):
        for k in range(3):
            for l in range(6):
                s_E_matrix_new[i, j] += s_E_matrix[k, l] * rot_matrix[k, i] * rot_matrix[l, j]

# Масштабирование матрицы s_E_matrix_new
s_E_matrix_new *= 1e-12

# Расчет пьезоэлектрического модуля d32
d32_new = d_matrix_new[2, 1]

# Расчет диэлектрической проницаемости e33
e33_new = e_matrix[2, 2]
for i in range(3):
    for j in range(3):
        for k in range(3):
            for l in range(3):
                e33_new += e_matrix[i, j] * rot_matrix[k, i] * rot_matrix[l, j]

# Расчет упругой податливости s22E
s22E_new = s_E_matrix_new[1, 1]

# Пример использования функции select_elements
select_elements(d_matrix_new, "d_matrix_new")
select_elements(s_E_matrix_new, "s_E_matrix_new")
select_elements(e_matrix, "e_matrix")
