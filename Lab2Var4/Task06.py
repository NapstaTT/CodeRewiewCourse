"""Dynamic70. Преобразование двусвязного списка в циклический с барьерным элементом.

Даны ссылки A1 и A2 на первый и последний элементы двусвязного списка, 
реализованного в виде цепочки узлов, которая ограничена по краям константами null. 
Если список пуст, то A1 = A2 = null. Преобразовать исходный список в циклический 
список, снабженный барьерным элементом. Барьерный элемент должен иметь значение 0 
и быть связан своими свойствами Next и Prev с первым и последним элементом 
исходного списка (в случае пустого исходного списка свойства Next и Prev 
барьерного элемента должны указывать на сам барьерный элемент). 
Вывести ссылку на барьерный элемент полученного списка. 
Не создавать новые объекты типа Node, за исключением барьерного элемента.
"""

from typing import Optional


class Node:
    """Узел двусвязного списка.

    Attributes:
        key (int): Значение узла.
        next (Optional[Node]): Ссылка на следующий узел.
        prev (Optional[Node]): Ссылка на предыдущий узел.
    """

    def __init__(self, key: int) -> None:
        """Инициализирует узел.

        Args:
            key (int): Значение узла.
        """
        self.key = key
        self.next: Optional['Node'] = None
        self.prev: Optional['Node'] = None


class DoubleLinkedList:
    """Двусвязный список с операциями добавления в начало и печати."""

    def __init__(self) -> None:
        """Инициализирует пустой список."""
        self.head: Optional[Node] = None
        self.tail: Optional[Node] = None

    def push_front(self, key: int) -> None:
        """Добавляет элемент в начало списка.

        Args:
            key (int): Значение нового узла.

        Raises:
            TypeError: Если key не является целым числом.
        """
        if not isinstance(key, int):
            raise TypeError("Ключ должен быть целым числом")

        new_node = Node(key)
        if self.head is None:
            self.head = self.tail = new_node
        else:
            new_node.next = self.head
            self.head.prev = new_node
            self.head = new_node

    def __str__(self) -> str:
        """Возвращает строковое представление списка (от головы к хвосту).

        Returns:
            str: Элементы списка, разделённые запятыми.
        """
        if self.head is None:
            return "Список пуст"
        elements = []
        current = self.head
        while current is not None:
            elements.append(str(current.key))
            current = current.next
        return ", ".join(elements)


def make_circular_with_barrier(
    head: Optional[Node], tail: Optional[Node]
) -> Node:
    """Преобразует двусвязный список в циклический с барьерным элементом.

    Args:
        head (Optional[Node]): Первый элемент исходного списка.
        tail (Optional[Node]): Последний элемент исходного списка.

    Returns:
        Node: Барьерный элемент (значение 0), связанный с исходным списком.

    Raises:
        ValueError: Если head и tail не согласованы (один None, другой нет).
    """
    # Проверка согласованности
    if (head is None) != (tail is None):
        raise ValueError("head и tail должны быть одновременно None или оба не None")

    barrier = Node(0)

    # Пустой список
    if head is None and tail is None:
        barrier.next = barrier
        barrier.prev = barrier
        return barrier

    # Непустой список
    barrier.next = head
    barrier.prev = tail
    head.prev = barrier      # type: ignore
    tail.next = barrier      # type: ignore
    return barrier


def main() -> None:
    """Демонстрация работы программы."""
    # Формируем исходный список
    lst = DoubleLinkedList()
    for value in [1, 2, 3, 4, 5, 6]:
        lst.push_front(value)
    print("Исходный список (в обратном порядке из-за push_front):", lst)

    # Получаем ссылки на первый и последний элементы
    a1 = lst.head
    a2 = lst.tail

    # Преобразуем в циклический с барьером
    barrier_node = make_circular_with_barrier(a1, a2)
    print(f"Барьерный элемент: {barrier_node.key}")

    # Дополнительная проверка: выведем несколько элементов циклического списка
    print("Проверка: первые 5 элементов цикла (через next от барьера):")
    current = barrier_node.next
    count = 0
    while current is not None and count < 10:
        print(f"  {current.key}", end=" -> ")
        current = current.next
        count += 1
        if current is barrier_node:
            break
    print("(возврат к барьеру)")


if __name__ == "__main__":
    main()