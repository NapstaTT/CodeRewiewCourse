"""Dynamic59: Добавление N чисел в конец двусвязного списка.

Даны ссылки A1, A2 и A3 на первый, последний и текущий элементы двусвязного списка
(если список пуст, A1 = A2 = A3 = null), число N (> 0) и набор из N чисел. Программа:
- Определяет класс IntList с полями first, last, current и методами insert_last, put.
- Добавляет N чисел в конец списка с помощью insert_last.
- Выводит ссылки на первый, последний и текущий элементы, а также весь список.

Пользователь задаёт начальный список, N и набор чисел (могут быть строки, например, '00').
"""

from typing import Optional


class Node:
    """Узел двусвязного списка.

    Attributes:
        value (str): Значение, хранящееся в узле.
        prev (Optional[Node]): Ссылка на предыдущий узел.
        next (Optional[Node]): Ссылка на следующий узел.
    """

    def __init__(self, value: str) -> None:
        """Инициализирует узел с заданным значением.

        Args:
            value (str): Строковое значение узла.
        """
        self.value = value
        self.prev: Optional['Node'] = None
        self.next: Optional['Node'] = None

    def __repr__(self) -> str:
        """Возвращает строковое представление узла (его адрес в памяти).

        Returns:
            str: Идентификатор узла (имитация ссылки).
        """
        return f"Node({id(self)})"

    def get_value(self) -> str:
        """Возвращает значение узла.

        Returns:
            str: Значение узла.
        """
        return self.value


class IntList:
    """Управляет двусвязным списком строковых значений.

    Attributes:
        first (Optional[Node]): Первый узел списка.
        last (Optional[Node]): Последний узел списка.
        current (Optional[Node]): Текущий узел списка.
    """

    def __init__(self, a_first: Optional[Node], a_last: Optional[Node], a_current: Optional[Node]) -> None:
        """Инициализирует список с заданными первым, последним и текущим узлами.

        Args:
            a_first (Optional[Node]): Первый узел списка.
            a_last (Optional[Node]): Последний узел списка.
            a_current (Optional[Node]): Текущий узел списка.
        """
        self.first = a_first
        self.last = a_last
        self.current = a_current

    def insert_last(self, d: str) -> None:
        """Добавляет новый узел с заданным значением в конец списка.

        Args:
            d (str): Значение для нового узла (строка).
        """
        new_node = Node(d)
        if self.first is None:   # список пуст
            self.first = new_node
            self.last = new_node
            self.current = new_node
        else:
            self.last.next = new_node
            new_node.prev = self.last
            self.last = new_node
            self.current = new_node   # новый элемент становится текущим

    def put(self) -> None:
        """Выводит ссылки на первый, последний и текущий элементы."""
        # Выводим ссылки (представление узла через __repr__)
        first_repr = repr(self.first) if self.first is not None else "null"
        last_repr = repr(self.last) if self.last is not None else "null"
        current_repr = repr(self.current) if self.current is not None else "null"
        print(f"Первый элемент (first): {first_repr}")
        print(f"Последний элемент (last): {last_repr}")
        print(f"Текущий элемент (current): {current_repr}")

    def display_list(self) -> None:
        """Выводит весь список в читаемом формате (значения узлов)."""
        if self.first is None:
            print("Список пуст.")
            return

        current = self.first
        elements = []
        while current is not None:
            elements.append(str(current.value))
            current = current.next
        print("Список: " + " <-> ".join(elements))


def safe_int_input(prompt: str, min_val: Optional[int] = None, max_val: Optional[int] = None) -> int:
    """Безопасно запрашивает целое число с проверкой границ.

    Args:
        prompt (str): Текст приглашения.
        min_val (Optional[int]): Минимальное допустимое значение (включительно).
        max_val (Optional[int]): Максимальное допустимое значение (включительно).

    Returns:
        int: Корректно введённое целое число.
    """
    while True:
        try:
            val = int(input(prompt).strip())
            if min_val is not None and val < min_val:
                print(f"Ошибка: число должно быть не меньше {min_val}.")
                continue
            if max_val is not None and val > max_val:
                print(f"Ошибка: число должно быть не больше {max_val}.")
                continue
            return val
        except ValueError:
            print("Ошибка: введите целое число.")


def get_user_input(prompt: str, required: bool = True) -> str:
    """Получает ввод от пользователя с заданным приглашением.

    Args:
        prompt (str): Текст приглашения для ввода.
        required (bool): Если True, пустая строка не допускается.

    Returns:
        str: Введённое пользователем значение (не пустое, если required=True).
    """
    while True:
        value = input(prompt).strip()
        if required and value == "":
            print("Ошибка: значение не может быть пустым. Повторите ввод.")
            continue
        return value


def create_initial_list() -> IntList:
    """Создаёт начальный двусвязный список на основе ввода пользователя.

    Returns:
        IntList: Созданный список с выбранным текущим элементом.
    """
    count = safe_int_input(
        "Введите количество элементов в начальном списке (0 для пустого): ",
        min_val=0
    )

    if count == 0:
        return IntList(None, None, None)

    nodes = []
    print("Введите значения элементов (строки):")
    for i in range(count):
        value = get_user_input(f"  Элемент {i+1}: ", required=True)
        nodes.append(Node(value))

    # Связываем узлы
    for i in range(len(nodes) - 1):
        nodes[i].next = nodes[i+1]
        nodes[i+1].prev = nodes[i]

    int_list = IntList(nodes[0], nodes[-1], nodes[0])

    print("\nВаш начальный список:")
    int_list.display_list()

    # Выбор текущего элемента
    if count == 1:
        int_list.current = nodes[0]
    else:
        current_index = safe_int_input(
            f"Выберите номер текущего элемента (1-{count}): ",
            min_val=1, max_val=count
        ) - 1
        int_list.current = nodes[current_index]

    return int_list


def add_numbers_to_list(int_list: IntList) -> None:
    """Добавляет N чисел (строк) в конец списка.

    Args:
        int_list (IntList): Список, в который добавляются элементы.
    """
    n = safe_int_input("Введите количество чисел для добавления (N > 0): ", min_val=1)

    print("Введите значения для добавления (каждое — строка):")
    for i in range(n):
        value = get_user_input(f"  Число {i+1}: ", required=True)
        int_list.insert_last(value)


def main() -> None:
    """Основная функция программы."""
    print("Добро пожаловать в программу добавления чисел в двусвязный список!")

    int_list = create_initial_list()
    add_numbers_to_list(int_list)

    print("\nРезультат после добавления чисел:")
    int_list.put()
    int_list.display_list()


if __name__ == "__main__":
    main()