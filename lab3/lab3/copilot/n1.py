#!/usr/bin/env python3
# FIXME:
# 1. Приведены docstrings к формату Google (Args:, Returns:) для всех функций.
# 2. Добавлено полное условие задачи в модульный docstring.
# 3. Улучшена читаемость: аннотации типов и переменные вынесены в отдельные строки.
# 4. Сохранены принципы DRY, KISS, SoC.
"""
Генератор паролей с тремя уровнями сложности.

Условие задачи:
Программа генерирует случайные пароли трёх уровней сложности.
Пользователь выбирает уровень (1 – простой, 2 – средний, 3 – сложный).
Программа выводит пароль и предлагает сгенерировать ещё один.
Пароли генерируются с использованием криптостойкого модуля secrets.

Уровни сложности:
1 — простой (только буквы, длина 8)
2 — средний (буквы + цифры, длина 12)
3 — сложный (буквы + цифры + символы, длина 16)
"""

import string
import secrets


def get_password_config(level: int) -> tuple[int, str]:
    """
    Вернуть длину пароля и набор символов для указанного уровня сложности.

    Args:
        level (int): Уровень сложности (1, 2 или 3).

    Returns:
        tuple[int, str]: Кортеж (длина_пароля, строка_символов).

    Raises:
        ValueError: Если уровень сложности некорректен.
    """
    if level == 1:
        length = 8
        alphabet = string.ascii_letters
    elif level == 2:
        length = 12
        alphabet = string.ascii_letters + string.digits
    elif level == 3:
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

    Args:
        length (int): Длина пароля.
        alphabet (str): Строка с допустимыми символами.

    Returns:
        str: Случайно сгенерированный пароль.
    """
    return "".join(secrets.choice(alphabet) for _ in range(length))


def ask_level() -> int:
    """
    Запросить у пользователя уровень сложности пароля.

    Returns:
        int: Выбранный уровень сложности (1, 2 или 3).
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