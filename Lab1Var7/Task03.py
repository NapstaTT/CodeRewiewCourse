"""
Даны два файла вещественных чисел с именами S1 и S2, элементы которых
упорядочены по возрастанию. Объединить эти файлы в новый файл с
именем S3 так, чтобы его элементы также оказались упорядоченными
по возрастанию.
"""
import struct


def write_floats_to_binary_file(filename, numbers):
    """Записывает вещественные числа в бинарный файл."""
    with open(filename, 'wb') as file:
        for number in numbers:
            file.write(struct.pack('f', number))  # 'f' - формат для float


def read_floats_from_binary_file(filename):
    """Читает вещественные числа из бинарного файла и возвращает их в виде списка."""
    numbers = []
    with open(filename, 'rb') as file:
        while True:
            byte = file.read(4)  # Читаем 4 байта (размер float)
            if not byte:
                break  # Если не осталось байтов, выходим из цикла
            number = struct.unpack('f', byte)[0]
            numbers.append(number)
    return numbers


def merge_sorted_files(file1, file2, output_file):
    """Объединяет два отсортированных бинарных файла в один отсортированный файл."""
    numbers1 = read_floats_from_binary_file(file1)
    numbers2 = read_floats_from_binary_file(file2)

    merged_numbers = []
    i = j = 0

    # Сливаем два отсортированных списка
    while i < len(numbers1) and j < len(numbers2):
        if numbers1[i] < numbers2[j]:
            merged_numbers.append(numbers1[i])
            i += 1
        else:
            merged_numbers.append(numbers2[j])
            j += 1

    # Добавляем оставшиеся элементы из первого файла, если такие есть
    while i < len(numbers1):
        merged_numbers.append(numbers1[i])
        i += 1

    # Добавляем оставшиеся элементы из второго файла, если такие есть
    while j < len(numbers2):
        merged_numbers.append(numbers2[j])
        j += 1

    # Записываем объединенные числа в выходной файл
    write_floats_to_binary_file(output_file, merged_numbers)

    return merged_numbers


def display_binary_file_contents(filename):
    """Отображает содержимое бинарного файла в виде списка вещественных чисел."""
    numbers = read_floats_from_binary_file(filename)
    print("Содержимое файла:", numbers)


# Пример использования:
# Записываем числа в файлы S1 и S2
write_floats_to_binary_file("S1.bin", [1.0, 2.5, 3.0, 4.6, 5.9])
write_floats_to_binary_file("S2.bin", [0.5, 2.0, 3.5, 4.0, 6.1])

# Объединяем файлы S1 и S2 в S3
merged_numbers = merge_sorted_files("S1.bin", "S2.bin", "S3.bin")

print("Содержимое файла S3:", [f"{num:.1f}" for num in merged_numbers])