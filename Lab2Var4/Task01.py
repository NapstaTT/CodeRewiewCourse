"""Создание стека из N чисел.

Дано число N (> 0) и набор из N чисел. Создать стек, содержащий исходные числа
(последнее число будет вершиной стека), и вывести ссылку на его вершину.
"""

from typing import Optional


class Node:
    """Узел стека (односвязный список)."""

    def __init__(self, data: int, next_node: Optional['Node'] = None) -> None:
        """Инициализирует узел с данными и ссылкой на следующий узел.

        Args:
            data (int): Числовое значение узла.
            next_node (Optional[Node]): Ссылка на следующий узел (по умолчанию None).
        """
        self.data = data
        self.next = next_node

    def __repr__(self) -> str:
        """Возвращает строковое представление узла (только значение)."""
        return f"Node({self.data})"


class Stack:
    """Стек на основе односвязного списка (вершина — head)."""

    def __init__(self) -> None:
        """Инициализирует пустой стек."""
        self.head: Optional[Node] = None

    def push(self, data: int) -> None:
        """Добавляет элемент на вершину стека.

        Args:
            data (int): Число для добавления.
        """
        new_node = Node(data, self.head)
        self.head = new_node

    def peek(self) -> Optional[Node]:
        """Возвращает ссылку на вершину стека (узел) без удаления.

        Returns:
            Optional[Node]: Узел на вершине стека или None, если стек пуст.
        """
        return self.head

    def __str__(self) -> str:
        """Возвращает строковое представление стека от вершины к основанию."""
        elements = []
        current = self.head
        while current is not None:
            elements.append(str(current.data))
            current = current.next
        return " -> ".join(elements)


def safe_int_input(prompt: str) -> int:
    """Безопасно запрашивает целое число у пользователя.

    Args:
        prompt (str): Текст приглашения.

    Returns:
        int: Введённое целое число.
    """
    while True:
        try:
            value = int(input(prompt))
            return value
        except ValueError:
            print("Ошибка: необходимо ввести целое число.")


def main() -> None:
    """Основная функция программы."""
    # Ввод N с проверкой > 0
    while True:
        N = safe_int_input("Введите число N (> 0): ")
        if N > 0:
            break
        print("Ошибка: N должно быть больше 0.")

    stack = Stack()

    print(f"Введите {N} чисел (последнее будет вершиной стека):")
    for i in range(1, N + 1):
        num = safe_int_input(f"Число {i}: ")
        stack.push(num)

    # Вывод результатов
    top_node = stack.peek()
    if top_node is not None:
        print(f"Ссылка на вершину стека: {top_node} (значение = {top_node.data})")
    else:
        print("Стек пуст.")

    print("Содержимое стека (вершина -> основание):", stack)


if __name__ == "__main__":
    main()