#!/usr/bin/env python3
"""
Генератор паролей с тремя уровнями сложности.

Уровни сложности:
1 — простой
2 — средний
3 — сложный

Пароли генерируются случайным образом при каждом запросе.
"""

import string
import secrets


def get_password_config(level: int) -> tuple[int, str]:
    """
    Вернуть длину пароля и набор символов для указанного уровня сложности.

    :param level: Уровень сложности (1, 2 или 3).
    :return: Кортеж (длина_пароля, строка_символов).
    :raises ValueError: Если уровень сложности некорректен.
    """
    if level == 1:
        # Простой: только буквы (строчные + прописные), длина 8
        length = 8
        alphabet = string.ascii_letters
    elif level == 2:
        # Средний: буквы + цифры, длина 12
        length = 12
        alphabet = string.ascii_letters + string.digits
    elif level == 3:
        # Сложный: буквы + цифры + символы, длина 16
        length = 16
        alphabet = (
            string.ascii_letters +
            string.digits +
            string.punctuation
        )
    else:
        raise ValueError("Уровень сложности должен быть 1, 2 или 3.")

    return length, alphabet


def generate_password(length: int, alphabet: str) -> str:
    """
    Сгенерировать пароль заданной длины из указанного набора символов.

    Для генерации используется модуль secrets, подходящий для
    криптографически стойких случайных значений.

    :param length: Длина пароля.
    :param alphabet: Строка с допустимыми символами.
    :return: Случайно сгенерированный пароль.
    """
    return "".join(secrets.choice(alphabet) for _ in range(length))


def ask_level() -> int:
    """
    Запросить у пользователя уровень сложности пароля.

    :return: Целое число — выбранный уровень сложности.
    """
    print("Выберите уровень сложности пароля:")
    print("1 — простой (только буквы, длина 8)")
    print("2 — средний (буквы и цифры, длина 12)")
    print("3 — сложный (буквы, цифры и символы, длина 16)")

    while True:
        user_input = input("Введите 1, 2 или 3: ").strip()
        if user_input in {"1", "2", "3"}:
            return int(user_input)
        print("Некорректный ввод. Пожалуйста, введите 1, 2 или 3.")


def main() -> None:
    """
    Точка входа в программу.

    Запрашивает у пользователя уровень сложности и выводит
    сгенерированный пароль. Позволяет запрашивать новые пароли,
    пока пользователь не решит завершить работу.
    """
    print("=== Генератор паролей ===")

    while True:
        level = ask_level()
        length, alphabet = get_password_config(level)
        password = generate_password(length, alphabet)

        print(f"\nВаш сгенерированный пароль: {password}\n")

        again = input(
            "Сгенерировать ещё один пароль? (y/n): "
        ).strip().lower()
        if again not in {"y", "д", "yes", "да"}:
            print("Работа завершена. Берегите свои пароли!")
            break


if __name__ == "__main__":
    main()
