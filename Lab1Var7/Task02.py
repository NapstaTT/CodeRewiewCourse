"""Удвоение бинарного файла целых чисел.

Дан файл целых чисел. Необходимо удвоить его размер, записав в конец файла
все его исходные элементы в обратном порядке.

Числа хранятся в бинарном формате (4 байта на число, порядок little-endian,
тип 'i' модуля struct).
"""

import struct
from typing import List, Optional


def read_numbers_from_file(filename: str) -> List[int]:
    """Считывает все целые числа из бинарного файла.

    Args:
        filename (str): Путь к бинарному файлу.

    Returns:
        List[int]: Список прочитанных чисел.

    Raises:
        FileNotFoundError: Если файл не существует.
        struct.error: Если файл имеет некорректный размер (не кратен 4).
    """
    numbers = []
    with open(filename, "rb") as f:
        while True:
            data = f.read(4)          # читаем 4 байта (одно число)
            if not data:
                break
            number = struct.unpack("i", data)[0]
            numbers.append(number)
    return numbers


def write_numbers_to_file(filename: str, numbers: List[int], append: bool = False) -> None:
    """Записывает список целых чисел в бинарный файл.

    Args:
        filename (str): Путь к файлу.
        numbers (List[int]): Список чисел для записи.
        append (bool): Если True, числа дописываются в конец файла.
                       Если False, файл перезаписывается.

    Raises:
        OSError: При ошибках ввода-вывода.
    """
    mode = "ab" if append else "wb"
    with open(filename, mode) as f:
        for number in numbers:
            f.write(struct.pack("i", number))


def double_file_size(filename: str) -> None:
    """Удваивает размер бинарного файла, дописывая исходные элементы в обратном порядке.

    Args:
        filename (str): Путь к файлу.

    Raises:
        FileNotFoundError: Если исходный файл не существует.
        struct.error: При неверном формате файла.
    """
    original_numbers = read_numbers_from_file(filename)
    reversed_numbers = list(reversed(original_numbers))   # обратный порядок
    write_numbers_to_file(filename, reversed_numbers, append=True)


def get_user_numbers(prompt: str) -> Optional[List[int]]:
    """Запрашивает у пользователя целые числа и возвращает их список.

    Args:
        prompt (str): Текст приглашения.

    Returns:
        Optional[List[int]]: Список введённых чисел или None, если ввод пуст.

    Raises:
        ValueError: Если введены не целые числа.
    """
    user_input = input(prompt).strip()
    if not user_input:
        return None
    parts = user_input.split()
    numbers = []
    for part in parts:
        try:
            numbers.append(int(part))
        except ValueError:
            raise ValueError(f"'{part}' не является целым числом")
    return numbers


def print_file_content(filename: str) -> None:
    """Выводит содержимое бинарного файла на экран.

    Args:
        filename (str): Путь к файлу.
    """
    numbers = read_numbers_from_file(filename)
    print(" ".join(str(n) for n in numbers))


def main() -> None:
    """Основная функция программы."""
    filename = "numbers.bin"

    # Ввод исходных данных
    print("Создание бинарного файла целых чисел.")
    numbers = None
    while numbers is None:
        try:
            numbers = get_user_numbers("Введите целые числа через пробел: ")
            if numbers is None:
                print("Пустая строка. Повторите ввод.")
        except ValueError as e:
            print(f"Ошибка ввода: {e}. Попробуйте снова.")

    # Запись в файл (перезапись)
    try:
        write_numbers_to_file(filename, numbers, append=False)
    except OSError as e:
        print(f"Не удалось записать файл: {e}")
        return

    print(f"Исходный файл '{filename}' создан. Содержимое:")
    print_file_content(filename)

    # Удвоение файла
    try:
        double_file_size(filename)
    except FileNotFoundError:
        print(f"Ошибка: файл '{filename}' не найден.")
        return
    except struct.error:
        print(f"Ошибка: файл '{filename}' имеет неверный формат (размер не кратен 4).")
        return
    except OSError as e:
        print(f"Ошибка ввода-вывода: {e}")
        return

    print("Файл успешно удвоен. Содержимое после удвоения:")
    print_file_content(filename)


if __name__ == "__main__":
    main()