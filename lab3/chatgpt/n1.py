"""
Генератор паролей.

Программа предлагает пользователю выбрать уровень сложности
и генерирует случайный пароль соответствующей длины.

Уровни сложности:
1 — лёгкий (8 символов)
2 — средний (12 символов)
3 — сложный (16 символов)

Для повышения надёжности пароли содержат:
- строчные буквы;
- прописные буквы;
- цифры;
- специальные символы.

Каждый новый пароль генерируется случайным образом.
"""

import random
import string


EASY_LENGTH = 8
MEDIUM_LENGTH = 12
HARD_LENGTH = 16

SPECIAL_SYMBOLS = "!@#$%^&*()-_=+[]{};:,.<>?"


def generate_password(length):
    """
    Генерирует пароль заданной длины.

    Гарантирует наличие:
    - одной строчной буквы;
    - одной прописной буквы;
    - одной цифры;
    - одного специального символа.

    Args:
        length (int): длина пароля.

    Returns:
        str: сгенерированный пароль.
    """
    lowercase = random.choice(string.ascii_lowercase)
    uppercase = random.choice(string.ascii_uppercase)
    digit = random.choice(string.digits)
    symbol = random.choice(SPECIAL_SYMBOLS)

    all_characters = (
        string.ascii_lowercase
        + string.ascii_uppercase
        + string.digits
        + SPECIAL_SYMBOLS
    )

    password = [lowercase, uppercase, digit, symbol]

    password.extend(
        random.choice(all_characters)
        for _ in range(length - len(password))
    )

    random.shuffle(password)

    return "".join(password)


def choose_difficulty():
    """
    Запрашивает у пользователя уровень сложности.

    Returns:
        int: длина пароля.
    """
    print("Выберите уровень сложности:")
    print("1 — Лёгкий (8 символов)")
    print("2 — Средний (12 символов)")
    print("3 — Сложный (16 символов)")

    while True:
        choice = input("Ваш выбор: ")

        if choice == "1":
            return EASY_LENGTH
        if choice == "2":
            return MEDIUM_LENGTH
        if choice == "3":
            return HARD_LENGTH

        print("Ошибка: введите 1, 2 или 3.")


def main():
    """
    Основная функция программы.
    """
    print("=== Генератор паролей ===")

    while True:
        password_length = choose_difficulty()
        password = generate_password(password_length)

        print(f"\nВаш пароль: {password}")

        answer = input(
            "\nСгенерировать ещё один пароль? (да/нет): "
        ).strip().lower()

        if answer not in ("да", "д", "yes", "y"):
            print("Работа программы завершена.")
            break


if __name__ == "__main__":
    main()