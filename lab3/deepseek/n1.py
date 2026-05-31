3

"""
Модуль генерации случайных паролей с тремя уровнями сложности.

Пользователь выбирает уровень, программа создаёт надёжный пароль,
соответствующий требованиям: для лёгкого уровня — строчные буквы и цифры,
для среднего — строчные, прописные буквы и цифры,
для сложного — дополнительно спецсимволы.

Для уровней выше лёгкого гарантируется наличие хотя бы одного символа
из каждой требуемой категории. Генерация использует криптостойкий модуль secrets.
"""

import secrets
import string

# Наборы символов
LOWERS = string.ascii_lowercase        # строчные буквы a-z
UPPERS = string.ascii_uppercase        # прописные буквы A-Z
DIGITS = string.digits                 # цифры 0-9
# Расширенный набор спецсимволов (без проблемных вроде пробела или кавычек)
SYMBOLS = "!@#$%^&*()_+-=[]{}|;:,.<>?/~`"

# Конфигурация уровней сложности
LEVELS = {
    1: {
        "name": "Лёгкий",
        "length": 6,
        "charsets": [LOWERS, DIGITS],        # только буквы и цифры
        "require_all": False                 # не требуем все категории
    },
    2: {
        "name": "Средний",
        "length": 10,
        "charsets": [LOWERS, UPPERS, DIGITS],
        "require_all": True                  # нужны все три категории
    },
    3: {
        "name": "Сложный",
        "length": 14,
        "charsets": [LOWERS, UPPERS, DIGITS, SYMBOLS],
        "require_all": True                  # нужны все четыре категории
    }
}


def shuffle_list(lst):
    """
    Перемешивает список in-place с использованием криптостойкого генератора.

    Алгоритм Фишера-Йетса на основе secrets.randbelow обеспечивает
    равномерное и безопасное перемешивание для паролей.

    Args:
        lst (list): Список, который нужно перемешать.
    """
    for i in range(len(lst) - 1, 0, -1):
        j = secrets.randbelow(i + 1)
        lst[i], lst[j] = lst[j], lst[i]


def generate_password(level: int) -> str:
    """
    Генерирует случайный пароль согласно заданному уровню сложности.

    Для уровней с require_all=True гарантирует наличие минимум одного символа
    из каждого набора charsets. Для простого уровня символы выбираются
    случайно из объединённого набора.

    Args:
        level (int): Номер уровня сложности (1, 2 или 3).

    Returns:
        str: Сгенерированный пароль.

    Raises:
        ValueError: Если передан неизвестный уровень.
    """
    if level not in LEVELS:
        raise ValueError(f"Неизвестный уровень сложности: {level}. "
                         f"Допустимые значения: {list(LEVELS.keys())}")

    cfg = LEVELS[level]
    length = cfg["length"]
    charsets = cfg["charsets"]
    require_all = cfg["require_all"]

    # Объединяем все доступные символы для данного уровня
    all_chars = "".join(charsets)

    if not require_all:
        # Лёгкий уровень: просто случайные символы из общего набора
        password_chars = [secrets.choice(all_chars) for _ in range(length)]
    else:
        # Для среднего и сложного уровней обеспечиваем наличие каждой категории
        # Шаг 1: добавить по одному обязательному символу из каждого набора
        mandatory_chars = [secrets.choice(charset) for charset in charsets]
        password_chars = mandatory_chars[:]

        # Шаг 2: заполнить оставшиеся позиции случайными символами
        remaining = length - len(mandatory_chars)
        password_chars.extend(secrets.choice(all_chars) for _ in range(remaining))

        # Шаг 3: перемешать, чтобы обязательные символы не стояли в начале
        shuffle_list(password_chars)

    return "".join(password_chars)


def get_user_choice() -> int:
    """
    Запрашивает у пользователя выбор уровня сложности.

    Выводит меню и проверяет корректность ввода. При ошибке повторяет запрос.

    Returns:
        int: Выбранный уровень (1, 2 или 3).
    """
    while True:
        print("\n=== Генератор паролей ===")
        print("Выберите уровень сложности:")
        for lvl, cfg in LEVELS.items():
            print(f"  {lvl}. {cfg['name']} (длина {cfg['length']})")
        try:
            choice = int(input("Ваш выбор (1/2/3): ").strip())
            if choice in LEVELS:
                return choice
            else:
                print(f"Ошибка: введите число от 1 до {len(LEVELS)}.")
        except ValueError:
            print("Ошибка: пожалуйста, введите целое число.")


def main():
    """Основная функция программы: запрос уровня и вывод пароля."""
    level = get_user_choice()
    password = generate_password(level)
    cfg = LEVELS[level]
    print(f"\nСгенерированный пароль ({cfg['name']} уровень):")
    print(password)


if __name__ == "__main__":
    main()