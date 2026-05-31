#!/usr/bin/env python3
"""
Построение дерева арифметического выражения, заданного в обратной польской записи (ОПЗ).

Операции кодируются числами:
    +  → -1
    -  → -2
    *  → -3
    /  → -4
    %  → -5
    ^  → -6

После построения дерева выполняется преобразование:
все поддеревья, содержащие операции / или %, заменяются
их вычисленным значением (целым числом).

Автор: (ваше имя)
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import Optional, Union


# -----------------------------
#   Структура узла дерева
# -----------------------------

@dataclass
class Node:
    """
    Узел дерева выражения.

    value — либо число (операнд), либо код операции (отрицательное число).
    left, right — дочерние узлы (для операций).
    """
    value: int
    left: Optional["Node"] = None
    right: Optional["Node"] = None

    def is_leaf(self) -> bool:
        """Проверить, является ли узел листом (числом)."""
        return self.left is None and self.right is None


# -----------------------------
#   Построение дерева из ОПЗ
# -----------------------------

OPERATION_CODES = {
    "+": -1,
    "-": -2,
    "*": -3,
    "/": -4,
    "%": -5,
    "^": -6,
}


def build_tree(tokens: list[str]) -> Node:
    """
    Построить дерево выражения по списку токенов в обратной польской записи.

    :param tokens: Список строк — токенов выражения.
    :return: Корень дерева.
    """
    stack: list[Node] = []

    for token in tokens:
        if token.isdigit():
            # Операнд
            stack.append(Node(int(token)))
        else:
            # Операция
            if token not in OPERATION_CODES:
                raise ValueError(f"Неизвестная операция: {token}")

            right = stack.pop()
            left = stack.pop()
            op_code = OPERATION_CODES[token]

            stack.append(Node(op_code, left, right))

    if len(stack) != 1:
        raise ValueError("Некорректное выражение: стек не пуст после обработки.")

    return stack[0]


# -----------------------------
#   Вычисление поддеревьев
# -----------------------------

def evaluate(node: Node) -> int:
    """
    Рекурсивно вычислить значение поддерева.

    :param node: Узел дерева.
    :return: Целое значение поддерева.
    """
    if node.is_leaf():
        return node.value

    left = evaluate(node.left)
    right = evaluate(node.right)

    match node.value:
        case -1:  # +
            return left + right
        case -2:  # -
            return left - right
        case -3:  # *
            return left * right
        case -4:  # /
            return left // right
        case -5:  # %
            return left % right
        case -6:  # ^
            return left ** right
        case _:
            raise ValueError(f"Неизвестный код операции: {node.value}")


# -----------------------------
#   Замена деления на значения
# -----------------------------

def replace_divisions(node: Node) -> Node:
    """
    Преобразовать дерево так, чтобы в нём не было операций / и %.

    Если узел — операция / или %, то вычисляем поддерево и
    заменяем узел листом с числом.

    :param node: Корень поддерева.
    :return: Преобразованный узел.
    """
    if node.is_leaf():
        return node

    # Сначала преобразуем детей
    node.left = replace_divisions(node.left)
    node.right = replace_divisions(node.right)

    # Если операция — деление или остаток
    if node.value in (-4, -5):
        result = evaluate(node)
        return Node(result)

    return node


# -----------------------------
#   Основная функция
# -----------------------------

def main() -> None:
    """
    Прочитать выражение из файла, построить дерево,
    преобразовать его и вывести корень.
    """
    filename = "filename.txt"

    with open(filename, "r", encoding="utf-8") as file:
        tokens = file.read().split()

    root = build_tree(tokens)
    root = replace_divisions(root)

    print("Корень дерева:", root)


if __name__ == "__main__":
    main()
