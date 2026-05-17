"""Поиск второго элемента, кратного 6, в односвязном списке.

Дан односвязный линейный список и указатель на голову списка P1. Необходимо
найти второй элемент, кратный 6, и вывести указатель на этот элемент списка Px.
Если такого элемента в списке нет, то результат должен быть равен nil.
"""

from typing import Optional


class Node:
    """Узел односвязного списка.

    Attributes:
        data (int): Значение, хранящееся в узле.
        next (Optional[Node]): Ссылка на следующий узел (или None).
    """

    def __init__(self, data: int, next_node: Optional['Node'] = None) -> None:
        """Инициализирует узел списка.

        Args:
            data (int): Числовое значение узла.
            next_node (Optional[Node]): Ссылка на следующий узел (по умолчанию None).
        """
        self.data = data
        self.next = next_node

    def __str__(self) -> str:
        """Возвращает строковое представление узла (его значение)."""
        return str(self.data)


def find_second_multiple_of_six(head: Optional[Node]) -> Optional[Node]:
    """Находит второй узел, значение которого кратно 6.

    Args:
        head (Optional[Node]): Указатель на голову списка (может быть None).

    Returns:
        Optional[Node]: Указатель на второй узел, кратный 6, или None, если такого узла нет.
    """
    count = 0
    current = head
    while current is not None:
        if current.data % 6 == 0:
            count += 1
            if count == 2:
                return current
        current = current.next
    return None


def main() -> None:
    """Демонстрация работы функции поиска."""
    # Создаём список: 6 -> 7 -> 12 -> 5 -> 18
    node5 = Node(18)
    node4 = Node(5, node5)
    node3 = Node(12, node4)
    node2 = Node(7, node3)
    node1 = Node(6, node2)   # Голова списка

    result = find_second_multiple_of_six(node1)
    if result is None:
        print("В списке нет второго элемента, кратного 6.")
    else:
        print(f"Узел, являющийся вторым элементом, кратным 6, имеет значение: {result.data}")


if __name__ == "__main__":
    main()