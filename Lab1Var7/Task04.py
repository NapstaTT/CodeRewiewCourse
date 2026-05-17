"""Набор геометрических фигур.

Программа позволяет ввести с клавиатуры данные о N фигурах (круги, квадраты, отрезки),
сохранить их в бинарный файл и вывести содержимое файла в виде таблицы.

Для каждой фигуры известен цвет. Для круга – радиус (int), для квадрата – сторона (int),
для отрезка – длина (float). Используются классы с конструкторами, метод __str__ переопределён.
"""

import struct
from typing import List, Union, BinaryIO


class Shape:
    """Базовый класс для всех фигур."""

    def __init__(self, color: str) -> None:
        """Инициализирует фигуру с заданным цветом.

        Args:
            color (str): Цвет фигуры.
        """
        self.color = color

    def __str__(self) -> str:
        """Возвращает строковое представление фигуры.

        Returns:
            str: Цвет фигуры.
        """
        return f"Цвет: {self.color}"


class Circle(Shape):
    """Класс, представляющий круг."""

    def __init__(self, color: str, radius: int) -> None:
        """Инициализирует круг.

        Args:
            color (str): Цвет круга.
            radius (int): Радиус круга.
        """
        super().__init__(color)
        self.radius = radius

    def __str__(self) -> str:
        """Возвращает строковое описание круга.

        Returns:
            str: Информация о круге.
        """
        return f"Круг: {super().__str__()}, Радиус: {self.radius}"


class Square(Shape):
    """Класс, представляющий квадрат."""

    def __init__(self, color: str, side: int) -> None:
        """Инициализирует квадрат.

        Args:
            color (str): Цвет квадрата.
            side (int): Длина стороны квадрата.
        """
        super().__init__(color)
        self.side = side

    def __str__(self) -> str:
        """Возвращает строковое описание квадрата.

        Returns:
            str: Информация о квадрате.
        """
        return f"Квадрат: {super().__str__()}, Сторона: {self.side}"


class Line(Shape):
    """Класс, представляющий отрезок."""

    def __init__(self, color: str, length: float) -> None:
        """Инициализирует отрезок.

        Args:
            color (str): Цвет отрезка.
            length (float): Длина отрезка.
        """
        super().__init__(color)
        self.length = length

    def __str__(self) -> str:
        """Возвращает строковое описание отрезка.

        Returns:
            str: Информация об отрезке.
        """
        return f"Отрезок: {super().__str__()}, Длина: {self.length:.2f}"


# Тип фигуры: любая из трёх
ShapeType = Union[Circle, Square, Line]


def input_shape() -> ShapeType:
    """Интерактивный ввод данных одной фигуры с клавиатуры.

    Returns:
        ShapeType: Объект фигуры (Circle, Square или Line).

    Raises:
        ValueError: Если тип фигуры не распознан (но цикл обработки предотвращает выход).
    """
    print("\n--- Новая фигура ---")
    while True:
        shape_type = input("Тип фигуры (круг, квадрат, отрезок): ").strip().lower()
        if shape_type in ("круг", "квадрат", "отрезок"):
            break
        print("Ошибка: допустимые типы: 'круг', 'квадрат', 'отрезок'")

    while True:
        color = input("Цвет: ").strip()
        if color:
            break
        print("Цвет не может быть пустым. Повторите ввод.")

    if shape_type == "круг":
        while True:
            try:
                radius = int(input("Радиус (целое число): "))
                return Circle(color, radius)
            except ValueError:
                print("Ошибка: радиус должен быть целым числом.")

    if shape_type == "квадрат":
        while True:
            try:
                side = int(input("Сторона (целое число): "))
                return Square(color, side)
            except ValueError:
                print("Ошибка: сторона должна быть целым числом.")

    # shape_type == "отрезок"
    while True:
        try:
            length = float(input("Длина (вещественное число): "))
            return Line(color, length)
        except ValueError:
            print("Ошибка: длина должна быть числом.")


def _write_string(file: BinaryIO, s: str) -> None:
    """Записывает строку в бинарный файл с предшествующей длиной (2 байта).

    Args:
        file: Файловый объект, открытый для записи в бинарном режиме.
        s (str): Строка для записи.

    Returns:
        None

    Note:
        Используется формат 'H' (unsigned short) для длины, чтобы избежать
        проблем с нулевыми байтами внутри строки.
    """
    encoded = s.encode('utf-8')
    file.write(struct.pack('H', len(encoded)))   # длина строки (2 байта)
    file.write(encoded)                          # сама строка


def _read_string(file: BinaryIO) -> str:
    """Читает строку из бинарного файла, записанную функцией _write_string.

    Args:
        file: Файловый объект, открытый для чтения в бинарном режиме.

    Returns:
        str: Прочитанная строка.

    Raises:
        struct.error: Если не удаётся прочитать длину или данные,
                      или файл имеет неожиданный конец.
    """
    try:
        length_data = file.read(2)
        if not length_data:
            raise EOFError("Неожиданный конец файла при чтении строки")
        length = struct.unpack('H', length_data)[0]
        data = file.read(length)
        if len(data) != length:
            raise EOFError("Неожиданный конец файла: строка обрезана")
        return data.decode('utf-8')
    except EOFError as e:
        raise struct.error(str(e))


def save_shapes_to_file(shapes: List[ShapeType], filename: str) -> None:
    """Сохраняет список фигур в бинарный файл.

    Формат записи для каждой фигуры:
        - тип (1 байт, для выравнивания используем 'B')
        - параметр (int для круга/квадрата, float для отрезка)
        - цвет (строкой с предшествующей длиной)

    Args:
        shapes (List[ShapeType]): Список фигур.
        filename (str): Имя выходного файла.

    Raises:
        OSError: При ошибках ввода-вывода.
    """
    with open(filename, 'wb') as f:
        for shape in shapes:
            if isinstance(shape, Circle):
                f.write(struct.pack('B', 1))          # тип 1 – круг
                f.write(struct.pack('i', shape.radius))
                _write_string(f, shape.color)
            elif isinstance(shape, Square):
                f.write(struct.pack('B', 2))          # тип 2 – квадрат
                f.write(struct.pack('i', shape.side))
                _write_string(f, shape.color)
            elif isinstance(shape, Line):
                f.write(struct.pack('B', 3))          # тип 3 – отрезок
                f.write(struct.pack('f', shape.length))
                _write_string(f, shape.color)
            else:
                raise TypeError(f"Неизвестный тип фигуры: {type(shape)}")


def load_shapes_from_file(filename: str) -> List[ShapeType]:
    """Загружает фигуры из бинарного файла, созданного save_shapes_to_file.

    Args:
        filename (str): Имя файла.

    Returns:
        List[ShapeType]: Список загруженных фигур.

    Raises:
        FileNotFoundError: Если файл не существует.
        struct.error: Если файл повреждён или имеет неверный формат.
        OSError: При других ошибках ввода-вывода.
    """
    shapes = []
    with open(filename, 'rb') as f:
        while True:
            # Пытаемся прочитать тип фигуры (1 байт)
            type_byte = f.read(1)
            if not type_byte:                # достигнут конец файла
                break
            shape_type = struct.unpack('B', type_byte)[0]

            if shape_type == 1:              # круг
                radius = struct.unpack('i', f.read(4))[0]
                color = _read_string(f)
                shapes.append(Circle(color, radius))
            elif shape_type == 2:            # квадрат
                side = struct.unpack('i', f.read(4))[0]
                color = _read_string(f)
                shapes.append(Square(color, side))
            elif shape_type == 3:            # отрезок
                length = struct.unpack('f', f.read(4))[0]
                color = _read_string(f)
                shapes.append(Line(color, length))
            else:
                raise struct.error(f"Неизвестный тип фигуры {shape_type} в файле")
    return shapes


def print_shapes_table(shapes: List[ShapeType]) -> None:
    """Выводит список фигур в виде таблицы.

    Args:
        shapes (List[ShapeType]): Список фигур.

    Returns:
        None
    """
    # Заголовок таблицы
    print("\n{:<12} {:<12} {:<20}".format("Тип", "Цвет", "Параметр"))
    print("-" * 44)

    for shape in shapes:
        if isinstance(shape, Circle):
            print("{:<12} {:<12} {:<20}".format("Круг", shape.color, f"Радиус: {shape.radius}"))
        elif isinstance(shape, Square):
            print("{:<12} {:<12} {:<20}".format("Квадрат", shape.color, f"Сторона: {shape.side}"))
        elif isinstance(shape, Line):
            print("{:<12} {:<12} {:<20}".format("Отрезок", shape.color, f"Длина: {shape.length:.2f}"))


def main() -> None:
    """Основная функция: запрос N, ввод фигур, сохранение, загрузка и вывод."""
    print("Программа для работы с геометрическими фигурами")
    print("Доступные типы: круг, квадрат, отрезок")

    # Ввод количества фигур с защитой
    while True:
        try:
            n = int(input("\nВведите количество фигур: "))
            if n > 0:
                break
            print("Количество должно быть положительным целым числом.")
        except ValueError:
            print("Ошибка: введите целое число.")

    shapes = []
    for i in range(1, n + 1):
        print(f"\nФигура №{i}")
        shapes.append(input_shape())

    filename = "shapes.bin"
    try:
        save_shapes_to_file(shapes, filename)
        print(f"\nФигуры сохранены в файл '{filename}'.")
    except OSError as e:
        print(f"Ошибка при записи файла: {e}")
        return

    try:
        loaded_shapes = load_shapes_from_file(filename)
    except FileNotFoundError:
        print(f"Файл '{filename}' не найден после записи – странная ошибка.")
        return
    except struct.error as e:
        print(f"Файл повреждён: {e}")
        return
    except OSError as e:
        print(f"Ошибка при чтении файла: {e}")
        return

    print("\nСодержимое файла (таблица):")
    print_shapes_table(loaded_shapes)


if __name__ == "__main__":
    main()