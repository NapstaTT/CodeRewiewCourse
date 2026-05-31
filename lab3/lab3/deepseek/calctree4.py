#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# FIXME:
# 1. Исправлена логическая ошибка упрощения: добавлена функция eval_node для вычисления
#    любого поддерева (включая вложенные операции) перед заменой / и % на число.
# 2. Добавлена проверка деления на ноль и остатка от деления на ноль.
# 3. Улучшен __repr__: теперь выводятся символы операций вместо числовых кодов.
# 4. Добавлена обработка ошибки ZeroDivisionError в main.
# 5. Константа filename вынесена с расширением .txt для ясности.
# 6. Сохранены принципы DRY, KISS, SoC.
"""
Модуль для обработки арифметического выражения в обратной польской записи.

Условие задачи:
Программа читает выражение в обратной польской записи из файла 'filename.txt',
строит дерево, заменяет поддеревья с операциями деления (/) и остатка (%)
на их числовые значения, после чего выводит полученное дерево в префиксной форме.
Поддерживаются операции +, -, *, /, %, ^.
Числа – целые от 0 до 9.
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
# Обратное отображение для вывода
REV_OPCODES = {v: k for k, v in OPCODES.items()}


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
        """Возвращает строковое представление узла в префиксной форме с символами операций."""
        if self.value >= 0:
            return str(self.value)
        # узел-операция: выводим символ операции вместо кода
        op_sym = REV_OPCODES.get(self.value, str(self.value))
        return f"({op_sym} {repr(self.left)} {repr(self.right)})"


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
        if tok in OPCODES:
            if len(stack) < 2:
                raise ValueError(f"Недостаточно операндов для операции {tok}")
            right = stack.pop()
            left = stack.pop()
            op_code = OPCODES[tok]
            stack.append(Node(op_code, left, right))
        else:
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


def eval_node(node):
    """
    Вычисляет числовое значение узла (рекурсивно).

    Args:
        node (Node): корень поддерева.

    Returns:
        int: результат вычисления.

    Raises:
        ZeroDivisionError: при делении или остатке на ноль.
        ValueError: при неизвестной операции.
    """
    if node.value >= 0:
        return node.value
    left_val = eval_node(node.left)
    right_val = eval_node(node.right)
    if node.value == -1:      # '+'
        return left_val + right_val
    if node.value == -2:      # '-'
        return left_val - right_val
    if node.value == -3:      # '*'
        return left_val * right_val
    if node.value == -4:      # '/'
        if right_val == 0:
            raise ZeroDivisionError("деление на ноль")
        return left_val // right_val
    if node.value == -5:      # '%'
        if right_val == 0:
            raise ZeroDivisionError("остаток от деления на ноль")
        return left_val % right_val
    if node.value == -6:      # '^'
        return left_val ** right_val
    raise ValueError(f"Неизвестный код операции {node.value}")


def simplify_tree(node):
    """
    Упрощает дерево, заменяя поддеревья с операциями / и % на их значения.

    Args:
        node (Node): корень дерева.

    Returns:
        Node: упрощённое дерево (без операций -4 и -5).
    """
    if node.value >= 0:
        return node

    # Рекурсивно упрощаем поддеревья
    left_simp = simplify_tree(node.left)
    right_simp = simplify_tree(node.right)

    # Если операция — деление или остаток, вычисляем результат и возвращаем лист
    if node.value in (-4, -5):
        try:
            # Вычисляем текущий узел (включая любые вложенные операции)
            result = eval_node(Node(node.value, left_simp, right_simp))
        except ZeroDivisionError as e:
            raise RuntimeError(f"Ошибка вычисления: {e}")
        return Node(result)
    else:
        # Для остальных операций возвращаем узел с упрощёнными детьми
        return Node(node.value, left_simp, right_simp)


def main():
    """Основная функция программы."""
    filename = "filename.txt"
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"Ошибка: файл '{filename}' не найден.", file=sys.stderr)
        sys.exit(1)
    except IOError as e:
        print(f"Ошибка при чтении файла: {e}", file=sys.stderr)
        sys.exit(1)

    tokens = content.split()
    if not tokens:
        print("Ошибка: файл пуст.", file=sys.stderr)
        sys.exit(1)

    try:
        root = build_tree(tokens)
    except ValueError as e:
        print(f"Ошибка построения дерева: {e}", file=sys.stderr)
        sys.exit(1)

    try:
        simplified_root = simplify_tree(root)
    except RuntimeError as e:
        print(f"Ошибка упрощения: {e}", file=sys.stderr)
        sys.exit(1)

    print(simplified_root)


if __name__ == "__main__":
    main()