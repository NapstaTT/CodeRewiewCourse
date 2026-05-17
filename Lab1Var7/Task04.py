#1. Имеется набор геометрических фигур разного цвета. Среди фигур могут встречаться круги, квадраты и отрезки.
# Для каждой фигуры известно, какого она цвета. Кроме того, для круга известен его радиус (тип int), для квадрата
# – размер стороны (тип int), для отрезка–длина (тип float). Написать функцию, позволяющую ввести с клавиатуры
# данные для одной фигуры. Используя эту функцию, ввести сведения об N фигурах и сохранить их в бинарном файле.
# Распечатать на экране содержимое данного файла в виде таблицы.
# Для решения использовать классы, обязательно наличие конструктора(ов),для вывода информации переопределить метод __str__()

import struct  # Импортируем модуль для работы с бинарными данными

# Базовый класс для всех фигур
class Shape:
    def __init__(self, color):
        self.color = color  # Цвет фигуры

    def __str__(self):
        return f"Цвет: {self.color}"  # Возвращает строку с цветом фигуры

# Класс для круга
class Circle(Shape):
    def __init__(self, color, radius):
        super().__init__(color)  # Вызов конструктора базового класса для установки цвета
        self.radius = radius  # Радиус круга

    def __str__(self):
        # Возвращает строку с информацией о круге
        return f"Круг: {super().__str__()}, Радиус: {self.radius}"

# Класс для квадрата
class Square(Shape):
    def __init__(self, color, side):
        super().__init__(color)  # Вызов конструктора базового класса для установки цвета
        self.side = side  # Длина стороны квадрата

    def __str__(self):
        # Возвращает строку с информацией о квадрате
        return f"Квадрат: {super().__str__()}, Сторона: {self.side}"

# Класс для отрезка
class Line(Shape):
    def __init__(self, color, length):
        super().__init__(color)  # Вызов конструктора базового класса для установки цвета
        self.length = length  # Длина отрезка

    def __str__(self):
        # Возвращает строку с информацией об отрезке
        return f"Отрезок: {super().__str__()}, Длина: {self.length:.2f}"

# Функция для ввода данных о фигуре
def input_shape():
    # Запрашиваем у пользователя тип фигуры
    shape_type = input("Введите тип фигуры (круг, квадрат, отрезок): ").strip().lower()
    # Запрашиваем цвет фигуры
    color = input("Введите цвет фигуры: ").strip()

    # В зависимости от типа фигуры запрашиваем дополнительные параметры
    if shape_type == "круг":
        radius = int(input("Введите радиус круга: "))
        return Circle(color, radius)  # Создаем объект круга
    elif shape_type == "квадрат":
        side = int(input("Введите размер стороны квадрата: "))
        return Square(color, side)  # Создаем объект квадрата
    elif shape_type == "отрезок":
        length = float(input("Введите длину отрезка: "))
        return Line(color, length)  # Создаем объект отрезка
    else:
        raise ValueError("Неизвестный тип фигуры")  # Ошибка, если тип фигуры неизвестен

# Функция для сохранения фигур в бинарный файл
def save_shapes_to_file(shapes, filename):
    with open(filename, 'wb') as f:  # Открываем файл для записи в бинарном режиме
        for shape in shapes:
            if isinstance(shape, Circle):
                f.write(struct.pack('i', 1))  # Записываем тип фигуры: круг (1)
                f.write(struct.pack('i', shape.radius))  # Записываем радиус
            elif isinstance(shape, Square):
                f.write(struct.pack('i', 2))  # Записываем тип фигуры: квадрат (2)
                f.write(struct.pack('i', shape.side))  # Записываем длину стороны
            elif isinstance(shape, Line):
                f.write(struct.pack('i', 3))  # Записываем тип фигуры: отрезок (3)
                f.write(struct.pack('f', shape.length))  # Записываем длину отрезка
            # Записываем цвет фигуры как строку, заканчивающуюся нулевым байтом
            f.write(shape.color.encode('utf-8') + b'\x00')

# Функция для загрузки фигур из бинарного файла
def load_shapes_from_file(filename):
    shapes = []  # Список для хранения загруженных фигур
    with open(filename, 'rb') as f:  # Открываем файл для чтения в бинарном режиме
        while True:
            type_bytes = f.read(4)  # Читаем 4 байта (тип фигуры)
            if not type_bytes:  # Если файл закончился, выходим из цикла
                break
            shape_type = struct.unpack('i', type_bytes)[0]  # Преобразуем байты в число

            # В зависимости от типа фигуры читаем параметр
            if shape_type == 1:  # Круг
                radius = struct.unpack('i', f.read(4))[0]  # Читаем радиус
                color = b''
                while True:
                    byte = f.read(1)  # Читаем цвет посимвольно
                    if byte == b'\x00':  # Нулевой байт означает конец строки
                        break
                    color += byte
                color = color.decode('utf-8')  # Преобразуем байты в строку
                shapes.append(Circle(color, radius))  # Создаем объект круга
            elif shape_type == 2:  # Квадрат
                side = struct.unpack('i', f.read(4))[0]  # Читаем длину стороны
                color = b''
                while True:
                    byte = f.read(1)
                    if byte == b'\x00':
                        break
                    color += byte
                color = color.decode('utf-8')
                shapes.append(Square(color, side))  # Создаем объект квадрата
            elif shape_type == 3:  # Отрезок
                length = struct.unpack('f', f.read(4))[0]  # Читаем длину отрезка
                color = b''
                while True:
                    byte = f.read(1)
                    if byte == b'\x00':
                        break
                    color += byte
                color = color.decode('utf-8')
                shapes.append(Line(color, length))  # Создаем объект отрезка
    return shapes  # Возвращаем список фигур

# Функция для вывода фигур в виде таблицы
def print_shapes_table(shapes):
    # Выводим заголовок таблицы
    print("{:<10} {:<10} {:<10}".format("Тип", "Цвет", "Параметр"))
    print("-" * 30)  # Разделитель
    for shape in shapes:
        # В зависимости от типа фигуры выводим информацию
        if isinstance(shape, Circle):
            print("{:<10} {:<10} {:<10}".format("Круг", shape.color, f"Радиус: {shape.radius}"))
        elif isinstance(shape, Square):
            print("{:<10} {:<10} {:<10}".format("Квадрат", shape.color, f"Сторона: {shape.side}"))
        elif isinstance(shape, Line):
            print("{:<10} {:<10} {:<10}".format("Отрезок", shape.color, f"Длина: {shape.length:.2f}"))

# Основная часть программы
if __name__ == "__main__":
    # Запрашиваем количество фигур
    N = int(input("Введите количество фигур: "))
    shapes = []  # Список для хранения фигур
    for _ in range(N):
        shapes.append(input_shape())  # Вводим данные о каждой фигуре

    filename = "shapes.bin"  # Имя файла для сохранения данных
    save_shapes_to_file(shapes, filename)  # Сохраняем фигуры в файл

    loaded_shapes = load_shapes_from_file(filename)  # Загружаем фигуры из файла
    print_shapes_table(loaded_shapes)  # Выводим данные в виде таблицы