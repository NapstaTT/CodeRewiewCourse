"""Логические выражения.

Программа вычисляет значение логического выражения, заданного строкой S.
Выражение определяется грамматикой:
    <выражение> ::= T | F | And(<выражение> , <выражение>) | Or(<выражение> , <выражение>)
Символы 'T' и 'F' соответствуют True и False.
Исходные строки не содержат пробелов.
"""


def evaluate_expression(expression: str) -> bool:
    """Вычисляет логическое выражение, заданное строкой.

    Args:
        expression (str): Строка с выражением (без пробелов).

    Returns:
        bool: Результат вычисления (True или False).

    Raises:
        ValueError: Если строка не соответствует грамматике.
    """
    # Удаляем возможные пробелы (на всякий случай, хотя по условию их нет)
    expr_clean = expression.replace(" ", "")

    def parse_expression(expr: str) -> bool:
        """Рекурсивно разбирает и вычисляет выражение без пробелов."""
        # Базовые случаи
        if expr.upper() == "T":
            return True
        if expr.upper() == "F":
            return False

        # Оператор And
        if expr.startswith("And(") and expr.endswith(")"):
            inner = expr[4:-1]               # содержимое между And( и )
            left, right = _split_expression(inner)
            return parse_expression(left) and parse_expression(right)

        # Оператор Or
        if expr.startswith("Or(") and expr.endswith(")"):
            inner = expr[3:-1]               # содержимое между Or( и )
            left, right = _split_expression(inner)
            return parse_expression(left) or parse_expression(right)

        raise ValueError(f"Некорректное выражение: {expr}")

    def _split_expression(expr: str) -> tuple[str, str]:
        """Разделяет два подвыражения, разделённые запятой на нулевом уровне вложенности.

        Args:
            expr (str): Строка вида "<левое>,<правое>".

        Returns:
            tuple[str, str]: Пара (левое_выражение, правое_выражение).

        Raises:
            ValueError: Если разделитель не найден или вложенность нарушена.
        """
        balance = 0
        for i, ch in enumerate(expr):
            if ch == '(':
                balance += 1
            elif ch == ')':
                balance -= 1
            elif ch == ',' and balance == 0:
                return expr[:i], expr[i + 1:]
        raise ValueError(f"Не удалось разделить выражение: {expr}")

    return parse_expression(expr_clean)


def main() -> None:
    """Основная функция: ввод, вычисление, вывод результата с защитой от ошибок."""
    print("Калькулятор логических выражений")
    print("Допустимые формы: T, F, And(..., ...), Or(..., ...)")
    while True:
        user_input = input("Введите выражение (или 'q' для выхода): ").strip()
        if user_input.lower() == 'q':
            print("Выход.")
            break
        if not user_input:
            print("Пустая строка. Попробуйте снова.")
            continue

        try:
            result = evaluate_expression(user_input)
            print(f"Результат: {result}\n")
        except ValueError as e:
            print(f"Ошибка в выражении: {e}")
            print("Пожалуйста, используйте формат: "
                  "T, F, And(T,F), Or(And(T,F),T) и т.п.\n")


if __name__ == "__main__":
    main()