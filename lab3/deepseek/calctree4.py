#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Модуль для обработки арифметического выражения в обратной польской записи.

Программа читает выражение из файла 'filename', строит дерево, заменяет
поддеревья с операциями деления (/) и остатка (%) на их числовые значения,
после чего выводит полученное дерево в префиксной форме.
"""

import sys

# Коды операций (отрицательные числа)
OPCODES = {
    '+': -1,
    '-': -2,
    '*': -3,
    '/': -4,
    '%': -5,
    '^': -6
}


class Node:
    """Узел дерева выражения: для операнда (value >= 0) или операции (value < 0)."""
    __slots__ = ('value', 'left', 'right')

    def __init__(self, value, left=None, right=None):
        """
        Args:
            value (int): число (0-9) для операнда, код операции (<0) для оператора.
            left (Node, optional): левое поддерево.
            right (Node, optional): правое поддерево.
        """
        self.value = value
        self.left = left
        self.right = right

    def __repr__(self):
        """Возвращает строковое представление узла в префиксной форме."""
        if self.value >= 0:   # лист (операнд)
            return str(self.value)
        # узел-операция
        return f"({self.value} {repr(self.left)} {repr(self.right)})"


def build_tree(tokens):
    """
    Строит дерево выражения из списка токенов в обратной польской записи.

    Args:
        tokens (list of str): токены (числа или операторы).

    Returns:
        Node: корень построенного дерева.

    Raises:
        ValueError: при некорректном выражении.
    """
    stack = []
    for tok in tokens:
        if tok in OPCODES:          # оператор
            if len(stack) < 2:
                raise ValueError("Недостаточно операндов для операции " + tok)
            right = stack.pop()
            left = stack.pop()
            op_code = OPCODES[tok]
            stack.append(Node(op_code, left, right))
        else:                       # операнд (целое число 0-9)
            try:
                val = int(tok)
                if not 0 <= val <= 9:
                    raise ValueError(f"Число должно быть от 0 до 9: {tok}")
            except ValueError:
                raise ValueError(f"Некорректный токен: {tok}")
            stack.append(Node(val))

    if len(stack) != 1:
        raise ValueError("Некорректное выражение: остались лишние операнды")
    return stack[0]


def simplify_tree(node):
    """
    Упрощает дерево, заменяя поддеревья с операциями / и % на их значения.

    Args:
        node (Node): корень дерева.

    Returns:
        Node: упрощённое дерево (без операций -4 и -5).
    """
    # Если лист, возвращаем его без изменений
    if node.value >= 0:
        return node

    # Рекурсивно упрощаем поддеревья
    left_simp = simplify_tree(node.left)
    right_simp = simplify_tree(node.right)

    # Если операция — деление или остаток, вычисляем результат и возвращаем лист
    if node.value == -4 or node.value == -5:
        # К этому моменту оба поддерева уже должны быть листьями (числами),
        # так как все вложенные / и % были заменены рекурсивно.
        # Но для надёжности проверим и вычислим через их значения.
        if left_simp.value < 0 or right_simp.value < 0:
            # Если вдруг осталась операция, вычисляем рекурсивно (не должно случиться)
            raise RuntimeError("В поддереве осталась невычисленная операция")
        left_val = left_simp.value
        right_val = right_simp.value
        if node.value == -4:   # деление нацело
            res = left_val // right_val
        else:                  # остаток от деления
            res = left_val % right_val
        return Node(res)
    else:
        # Для остальных операций возвращаем узел с упрощёнными детьми
        return Node(node.value, left_simp, right_simp)


def main():
    """Основная функция программы."""
    filename = "filename"
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"Ошибка: файл '{filename}' не найден.", file=sys.stderr)
        sys.exit(1)
    except IOError as e:
        print(f"Ошибка при чтении файла: {e}", file=sys.stderr)
        sys.exit(1)

    # Разбиваем на токены (пробелы, переводы строк и т.д.)
    tokens = content.split()
    if not tokens:
        print("Ошибка: файл пуст.", file=sys.stderr)
        sys.exit(1)

    try:
        root = build_tree(tokens)
    except ValueError as e:
        print(f"Ошибка построения дерева: {e}", file=sys.stderr)
        sys.exit(1)

    # Упрощаем дерево (убираем деление и остаток)
    simplified_root = simplify_tree(root)

    # Выводим корень полученного дерева (используется __repr__)
    print(simplified_root)


if __name__ == "__main__":
    main()