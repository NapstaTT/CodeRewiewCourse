"""Dynamic59: Добавление N чисел в конец двусвязного списка.

Даны ссылки A1, A2 и A3 на первый, последний и текущий элементы двусвязного списка
(если список пуст, A1 = A2 = A3 = null), число N (> 0) и набор из N чисел. Программа:
- Определяет класс IntList с полями first, last, current и методами InsertLast, Put.
- Добавляет N чисел в конец списка с помощью InsertLast.
- Выводит ссылки на первый, последний и текущий элементы, а также весь список.

Пользователь задает начальный список, N и набор чисел (могут быть строки, например, '00').
"""

from typing import Optional


class Node:
    """Представляет узел двусвязного списка.

    Args:
        value (str): Значение, хранимое в узле (строка).
    """
    def __init__(self, value: str) -> None:
        self.value = value
        self.prev: Optional[Node] = None  # Ссылка на предыдущий узел
        self.next: Optional[Node] = None  # Ссылка на следующий узел

    def put(self) -> str:
        """Возвращает строковое представление значения узла.

        Returns:
            str: Значение узла как строка.
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
        if not self.first:  # Если список пуст
            self.first = new_node
            self.last = new_node
            self.current = new_node
        else:
            self.last.next = new_node
            new_node.prev = self.last
            self.last = new_node
            self.current = new_node  # Новый элемент становится текущим

    def put(self) -> None:
        """Выводит ссылки на первый, последний и текущий элементы."""
        first_val = self.first.put() if self.first else "null"
        last_val = self.last.put() if self.last else "null"
        current_val = self.current.put() if self.current else "null"
        print(f"Первый элемент (first): {first_val}")
        print(f"Последний элемент (last): {last_val}")
        print(f"Текущий элемент (current): {current_val}")

    def display_list(self) -> None:
        """Выводит весь список в читаемом формате."""
        if not self.first:
            print("Список пуст.")
            return

        current = self.first
        elements = []
        while current:
            elements.append(str(current.value))
            current = current.next
        print("Список: " + " <-> ".join(elements))


def get_user_input(prompt: str) -> str:
    """Получает ввод от пользователя с заданным приглашением.

    Args:
        prompt (str): Текст приглашения для ввода.

    Returns:
        str: Введенное пользователем значение.
    """
    return input(prompt).strip()


def create_initial_list() -> IntList:
    """Создает начальный двусвязный список на основе ввода пользователя.

    Returns:
        IntList: Созданный список с выбором текущего элемента.
    """
    nodes = []

    # Запрашиваем количество элементов начального списка
    while True:
        try:
            count = int(get_user_input("Введите количество элементов в начальном списке (0 для пустого): "))
            if count < 0:
                print("Ошибка: Количество не может быть отрицательным.")
                continue
            break
        except ValueError:  # Обрабатываем некорректный ввод
            print("Ошибка: Введите целое число.")

    # Если список пустой
    if count == 0:
        return IntList(None, None, None)

    # Запрашиваем значения элементов (строки)
    for i in range(count):
        value = get_user_input(f"Введите значение элемента {i + 1} (например, '00' или '123'): ")
        nodes.append(Node(value))

    # Связываем узлы
    for i in range(len(nodes) - 1):
        nodes[i].next = nodes[i + 1]
        nodes[i + 1].prev = nodes[i]

    # Выводим список для выбора текущего элемента
    int_list = IntList(nodes[0], nodes[-1], nodes[0])  # Временно ставим current на первый
    print("\nВаш начальный список:")
    int_list.display_list()

    # Запрашиваем индекс текущего элемента
    while True:
        try:
            current_index = int(get_user_input("Выберите номер текущего элемента (1-{}): ".format(count))) - 1
            if 0 <= current_index < count:
                int_list.current = nodes[current_index]
                break
            print("Ошибка: Номер должен быть от 1 до", count)
        except ValueError:  # Обрабатываем некорректный ввод
            print("Ошибка: Введите целое число.")

    return int_list


def add_numbers_to_list(int_list: IntList) -> None:
    """Добавляет N чисел в конец списка.

    Args:
        int_list (IntList): Список для добавления чисел.
    """
    # Запрашиваем N
    while True:
        try:
            n = int(get_user_input("Введите количество чисел для добавления (N > 0): "))
            if n <= 0:
                print("Ошибка: N должно быть положительным числом.")
                continue
            break
        except ValueError:  # Обрабатываем некорректный ввод
            print("Ошибка: Введите целое число.")

    # Запрашиваем N чисел (строки)
    for i in range(n):
        value = get_user_input(f"Введите число {i + 1} для добавления (например, '00' или '123'): ")
        int_list.insert_last(value)


def main() -> None:
    """Основная функция для работы с двусвязным списком."""
    print("Добро пожаловать в программу добавления чисел в двусвязный список!")

    # Создаем начальный список
    int_list = create_initial_list()

    # Добавляем N чисел
    add_numbers_to_list(int_list)

    # Выводим результаты
    print("\nРезультат после добавления чисел:")
    int_list.put()
    int_list.display_list()


if __name__ == "__main__":
    main()