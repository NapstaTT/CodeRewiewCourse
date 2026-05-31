"""
Построение дерева выражения по обратной польской записи.

Коды операций:
+ -> -1
- -> -2
* -> -3
/ -> -4
% -> -5
^ -> -6

Поддеревья с операциями / и % заменяются вычисленным значением.
"""

from __future__ import annotations


OP_CODES = {
    "+": -1,
    "-": -2,
    "*": -3,
    "/": -4,
    "%": -5,
    "^": -6,
}


class Node:
    """
    Узел бинарного дерева.
    """

    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right

    def __repr__(self):
        return f"Node({self.value})"


def build_tree(postfix_expr):
    """
    Строит дерево по выражению в ОПЗ.
    """
    stack = []

    for token in postfix_expr.split():
        if token.isdigit():
            stack.append(Node(int(token)))
        else:
            right = stack.pop()
            left = stack.pop()

            stack.append(
                Node(
                    OP_CODES[token],
                    left,
                    right
                )
            )

    return stack.pop()


def calculate(node):
    """
    Вычисляет значение поддерева.
    """
    if node.left is None and node.right is None:
        return node.value

    left = calculate(node.left)
    right = calculate(node.right)

    if node.value == -1:
        return left + right
    if node.value == -2:
        return left - right
    if node.value == -3:
        return left * right
    if node.value == -4:
        return left // right
    if node.value == -5:
        return left % right
    if node.value == -6:
        return left ** right

    raise ValueError("Неизвестная операция")


def contains_division(node):
    """
    Проверяет наличие операций / или % в поддереве.
    """
    if node is None:
        return False

    if node.value in (-4, -5):
        return True

    return (
        contains_division(node.left)
        or contains_division(node.right)
    )


def transform_tree(node):
    """
    Заменяет поддеревья с / и % их значением.
    """
    if node is None:
        return None

    if contains_division(node):
        return Node(calculate(node))

    node.left = transform_tree(node.left)
    node.right = transform_tree(node.right)

    return node


def print_tree(node, level=0):
    """
    Красивый вывод дерева.
    """
    if node is None:
        return

    print_tree(node.right, level + 1)
    print("    " * level + str(node.value))
    print_tree(node.left, level + 1)


def main():
    filename = "filename.txt"

    with open(filename, "r", encoding="utf-8") as file:
        expression = file.read().strip()

    root = build_tree(expression)

    print("Исходное дерево:")
    print_tree(root)

    root = transform_tree(root)

    print("\nПреобразованное дерево:")
    print_tree(root)

    print("\nУказатель на корень:")
    print(root)


if __name__ == "__main__":
    main()