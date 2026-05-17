"""Вставка значения M перед каждым вторым элементом односвязного списка.

Дан односвязный линейный список и указатель на голову списка P1.
Необходимо вставить значение M перед каждым вторым элементом списка
и вывести ссылку на последний элемент полученного списка P2.
При нечётном числе элементов исходного списка в конец списка вставлять не надо.
"""

from typing import Optional, Any


class Node:
    """Узел односвязного списка.

    Attributes:
        data (Any): Данные, хранящиеся в узле.
        next (Optional[Node]): Ссылка на следующий узел.
    """

    def __init__(self, data: Any) -> None:
        """Инициализирует узел с данными.

        Args:
            data (Any): Значение узла.
        """
        self.data = data
        self.next: Optional['Node'] = None

    def __repr__(self) -> str:
        """Строковое представление узла (для отладки)."""
        return f"Node({self.data})"


class LinkedList:
    """Односвязный список с операциями добавления, вставки и получения последнего узла."""

    def __init__(self) -> None:
        """Инициализирует пустой список."""
        self.head: Optional[Node] = None

    def append(self, data: Any) -> None:
        """Добавляет элемент в конец списка.

        Args:
            data (Any): Значение нового элемента.
        """
        new_node = Node(data)
        if self.head is None:
            self.head = new_node
            return

        current = self.head
        while current.next is not None:
            current = current.next
        current.next = new_node

    def insert_before_even_positions(self, value: Any) -> None:
        """Вставляет значение перед каждым вторым элементом (позиции 2, 4, 6...).

        Args:
            value (Any): Значение для вставки.
        """
        if self.head is None or self.head.next is None:
            # Список пуст или имеет только один элемент – вставлять некуда
            return

        # Используем виртуальную голову для упрощения вставок в начало
        dummy = Node(None)
        dummy.next = self.head
        prev = dummy
        current = self.head
        position = 1  # позиция текущего узла в исходном списке (до вставок)

        while current is not None:
            if position % 2 == 0:  # каждый второй исходный элемент
                # Вставляем новый узел перед current
                new_node = Node(value)
                new_node.next = current
                prev.next = new_node
                # После вставки prev остаётся на месте (перед current), current не меняется
                # Но теперь текущий узел стал на позицию (position+1) из-за вставленного
                # Однако нам не нужно пересчитывать позицию для следующего исходного элемента,
                # так как мы должны вставлять перед исходными элементами с чётными номерами,
                # а current всё ещё указывает на исходный элемент.
                # Сдвигаем prev на вставленный узел, чтобы при следующем шаге перейти к current.next
                prev = new_node
            # Переход к следующему исходному узлу
            prev = current
            current = current.next
            position += 1

        # Обновляем голову (если вставка была перед первым элементом? позиция 2, так что не перед головой)
        self.head = dummy.next

    def get_last(self) -> Optional[Node]:
        """Возвращает последний узел списка или None, если список пуст."""
        if self.head is None:
            return None
        current = self.head
        while current.next is not None:
            current = current.next
        return current

    def __str__(self) -> str:
        """Строковое представление списка (элементы через пробел)."""
        elements = []
        current = self.head
        while current is not None:
            elements.append(str(current.data))
            current = current.next
        return " ".join(elements)


def safe_int_input(prompt: str) -> int:
    """Безопасно запрашивает целое число.

    Args:
        prompt (str): Текст приглашения.

    Returns:
        int: Введённое целое число.
    """
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Ошибка: введите целое число.")


def safe_any_input(prompt: str) -> str:
    """Запрашивает строковое значение (без преобразования)."""
    return input(prompt)


def main() -> None:
    """Основная функция программы."""
    # Ввод количества элементов
    while True:
        num = safe_int_input("Введите количество элементов в списке (>0): ")
        if num > 0:
            break
        print("Количество элементов должно быть положительным.")

    lst = LinkedList()
    print("Введите элементы списка:")
    for i in range(1, num + 1):
        elem = safe_any_input(f"Элемент {i}: ")
        lst.append(elem)

    m = safe_any_input("Введите значение M для вставки: ")

    # Выполняем вставку перед каждым вторым элементом
    lst.insert_before_even_positions(m)

    print("\nИзменённый список:")
    print(lst)

    last = lst.get_last()
    if last is not None:
        print(f"Последний элемент: {last.data}, ссылка: {last}")
    else:
        print("Список пуст.")


if __name__ == "__main__":
    main()