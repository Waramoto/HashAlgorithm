import binascii

# Реализации логических операций


def XOR(a, b):
    c = ""
    for i in range(0, len(a)):
        if a[i] == b[i]:
            c += "0"
        else:
            c += "1"
    return c


def OR(a, b):
    c = ""
    for i in range(0, len(a)):
        if a[i] == b[i] == "0":
            c += "0"
        else:
            c += "1"
    return c


def AND(a, b):
    c = ""
    for i in range(0, len(a)):
        if a[i] == b[i] == "1":
            c += "1"
        else:
            c += "0"
    return c


def NOT(a):
    c = ""
    for i in range(0, len(a)):
        if a[i] == "1":
            c += "0"
        else:
            c += "1"
    return c


# Вектор инициализации в виде словаря (ключ: значение)
init_v0 = {"A": "0010111011000000", "B": "1110001110111100", "C": "1111110100010111", "D": "1010000100111111"}

# Копия словаря вектора инициализации
init_v1 = init_v0.copy()

print("Введите полный путь к файлу (вместе с названием файла):")
filepath = input()

# Открываем файл в режиме чтения
file = open(filepath, "rb")

# Считываем файл в байтовом представлении
with file: byte = file.read()

# Закрываем файл
file.close()

# Шестнадцатеричное представление
hexadecimal = binascii.hexlify(byte)

# Десятичное представление
decimal = int(hexadecimal, 16)

# Двоичное представление
binary = bin(decimal)[2:].zfill(8)

# Пока длина строки не кратна 16, добавляем в конец строки нули
while len(binary) % 16 != 0:
    binary += "0"

# Разбиваем строку на массив по 16 символов
M = [binary[i:i+16] for i in range(0, len(binary), 16)]

# Цикл, реализующий алгоритм хеширования
for i in range(0, len(M)):
    if i % 2 == 0:
        init_v1["A"] = XOR(init_v0["D"], XOR((AND(init_v0["B"], init_v0["C"])), (AND(NOT(init_v0["B"]), init_v0["C"]))))
        init_v1["B"] = init_v0["D"]
        init_v1["C"] = XOR(M[i], XOR(init_v0["A"], init_v0["B"]))
        init_v1["D"] = init_v0["C"]
    else:
        init_v0["A"] = XOR(init_v1["D"], AND((OR(init_v1["B"], init_v1["C"])), (XOR(init_v1["B"], init_v1["C"]))))
        init_v0["B"] = init_v1["D"]
        init_v0["C"] = XOR(M[i], XOR(init_v0["A"], init_v1["B"]))
        init_v0["D"] = init_v1["C"]

if (len(M) - 1) % 2 == 0:
    result = init_v1["A"] + init_v1["B"] + init_v1["C"] + init_v1["D"]
else:
    result = init_v0["A"] + init_v0["B"] + init_v0["C"] + init_v0["D"]

# Вывод результата
print("Хеш в шестнадцатеричном формате: " + hex(int(result, 2))[2:])
