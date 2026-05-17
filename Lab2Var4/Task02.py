"""Dynamic26. Очередь с добавлением элементов и выводом ссылок.

Даны ссылки A1 и A2 на начало и конец очереди (если очередь пуста, A1 = A2 = null).
Также дано число N (> 0) и набор из N чисел. Описать класс IntQueue, содержащий:
• закрытые поля head и tail типа Node (начало и конец очереди);
• конструктор с параметрами aHead, aTail — началом и концом существующей очереди;
• процедура Enqueue(D) – добавляет в конец очереди элемент со значением D;
• процедура Put – выводит ссылки на head и tail (используя метод Put класса PT).
С помощью Enqueue добавить в исходную очередь набор чисел и вывести новые ссылки.
"""

from typing import Optional


class Node:
    """Узел очереди (односвязный список)."""

    def __init__(self, data: int) -> None:
        """Инициализирует узел с данными.

        Args:
            data (int): Числовое значение узла.
        """
        self.data = data
        self.next: Optional['Node'] = None

    def __repr__(self) -> str:
        """Строковое представление узла (для читаемого вывода ссылки)."""
        return f"Node({self.data})"


class IntQueue:
    """Очередь на основе односвязного списка (FIFO)."""

    def __init__(self, a_head: Optional[Node] = None, a_tail: Optional[Node] = None) -> None:
        """Конструктор очереди.

        Args:
            a_head (Optional[Node]): Начало существующей очереди (по умолчанию None).
            a_tail (Optional[Node]): Конец существующей очереди (по умолчанию None).
        """
        self.head = a_head
        self.tail = a_tail

    def enqueue(self, d: int) -> None:
        """Добавляет элемент в конец очереди.

        Args:
            d (int): Значение нового элемента.
        """
        new_node = Node(d)
        if self.head is None:
            self.head = new_node
            self.tail = new_node
        else:
            # Безопасно: tail точно не None, так как head не None
            self.tail.next = new_node  # type: ignore
            self.tail = new_node

    def put(self) -> None:
        """Выводит ссылки на начало и конец очереди.

        Примечание: согласно заданию, должен использоваться метод Put класса PT.
        Так как PT не определён, здесь используется стандартный print.
        """
        # Если требуется использовать PT, его нужно реализовать отдельно.
        # Например: PT.Put(self.head, self.tail)
        print(f"Ссылка на начало очереди: {self.head}")
        print(f"Ссылка на конец очереди: {self.tail}")


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

    # Исходная очередь (по условию может быть непустой, но здесь создаём пустую)
    queue = IntQueue()

    print("Введите числа для добавления в очередь:")
    for i in range(1, N + 1):
        value = safe_int_input(f"Число {i}: ")
        queue.enqueue(value)

    # Вывод ссылок
    queue.put()


if __name__ == "__main__":
    main()
    