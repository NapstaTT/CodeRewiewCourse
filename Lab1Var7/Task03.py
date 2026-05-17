"""Объединение двух отсортированных бинарных файлов вещественных чисел.

Даны два файла вещественных чисел с именами S1 и S2, элементы которых
упорядочены по возрастанию. Объединить эти файлы в новый файл с именем S3
так, чтобы его элементы также оказались упорядоченными по возрастанию.

Числа хранятся в бинарном формате (4 байта, тип 'f' модуля struct).
"""

import struct
import os
from typing import List, Optional


def write_floats_to_binary_file(filename: str, numbers: List[float]) -> None:
    """Записывает список вещественных чисел в бинарный файл.

    Args:
        filename (str): Имя файла.
        numbers (List[float]): Список чисел для записи.

    Raises:
        OSError: При ошибках ввода-вывода.
    """
    with open(filename, 'wb') as file:
        for number in numbers:
            file.write(struct.pack('f', number))


def read_floats_from_binary_file(filename: str) -> List[float]:
    """Читает вещественные числа из бинарного файла.

    Args:
        filename (str): Имя файла.

    Returns:
        List[float]: Список прочитанных чисел.

    Raises:
        FileNotFoundError: Если файл не существует.
        struct.error: Если размер файла не кратен 4 (неверный формат).
        OSError: При других ошибках ввода-вывода.
    """
    numbers = []
    with open(filename, 'rb') as file:
        while True:
            byte = file.read(4)
            if not byte:
                break
            number = struct.unpack('f', byte)[0]
            numbers.append(number)
    return numbers


def merge_sorted_files(file1: str, file2: str, output_file: str) -> None:
    """Объединяет два отсортированных бинарных файла в один отсортированный.

    Алгоритм: читает оба файла полностью (для простоты), затем сливает списки.
    Для очень больших файлов следовало бы использовать потоковое слияние.

    Args:
        file1 (str): Имя первого отсортированного файла.
        file2 (str): Имя второго отсортированного файла.
        output_file (str): Имя выходного файла.

    Raises:
        FileNotFoundError: Если один из исходных файлов не найден.
        struct.error: При неверном формате любого из файлов.
        OSError: При ошибках ввода-вывода.
    """
    numbers1 = read_floats_from_binary_file(file1)
    numbers2 = read_floats_from_binary_file(file2)

    merged = []
    i = j = 0

    # Слияние двух отсортированных списков
    while i < len(numbers1) and j < len(numbers2):
        if numbers1[i] < numbers2[j]:
            merged.append(numbers1[i])
            i += 1
        else:
            merged.append(numbers2[j])
            j += 1

    # Добавление остатков
    merged.extend(numbers1[i:])
    merged.extend(numbers2[j:])

    write_floats_to_binary_file(output_file, merged)


def display_binary_file(filename: str) -> None:
    """Выводит содержимое бинарного файла на экран в удобочитаемом виде.

    Args:
        filename (str): Имя файла.
    """
    try:
        numbers = read_floats_from_binary_file(filename)
    except FileNotFoundError:
        print(f"Файл '{filename}' не найден.")
        return
    except struct.error:
        print(f"Файл '{filename}' повреждён (неверный формат).")
        return
    except OSError as e:
        print(f"Ошибка при чтении файла '{filename}': {e}")
        return

    # Форматируем числа с одним знаком после запятой для красоты
    formatted = [f"{x:.1f}" for x in numbers]
    print(f"Содержимое {filename}: {formatted}")


def get_valid_filename(prompt: str) -> str:
    """Запрашивает у пользователя имя существующего файла.

    Args:
        prompt (str): Текст приглашения.

    Returns:
        str: Имя существующего файла (повторяет запрос, пока не будет введено корректное).
    """
    while True:
        name = input(prompt).strip()
        if not name:
            print("Имя файла не может быть пустым.")
            continue
        if os.path.exists(name):
            return name
        print(f"Файл '{name}' не найден. Проверьте имя и попробуйте снова.")


def main() -> None:
    """Основная функция: запрос имён файлов, слияние, вывод результата."""
    print("Объединение двух отсортированных бинарных файлов вещественных чисел.")
    print("Файлы должны содержать числа типа float (4 байта), упорядоченные по возрастанию.\n")

    file1 = get_valid_filename("Введите имя первого файла (S1): ")
    if file1 is None:
        return

    file2 = get_valid_filename("Введите имя второго файла (S2): ")
    if file2 is None:
        return

    output = input("Введите имя выходного файла (S3): ").strip()
    if not output:
        print("Имя выходного файла не может быть пустым. Используем 'S3.bin'.")
        output = "S3.bin"

    try:
        merge_sorted_files(file1, file2, output)
    except FileNotFoundError as e:
        print(f"Ошибка: {e}")
        return
    except struct.error as e:
        print(f"Ошибка формата данных: {e}")
        return
    except OSError as e:
        print(f"Ошибка ввода-вывода: {e}")
        return

    print(f"\nФайлы '{file1}' и '{file2}' успешно объединены в '{output}'.")
    display_binary_file(output)


if __name__ == "__main__":
    main()