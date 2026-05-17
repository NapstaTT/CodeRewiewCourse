# Во всех заданиях данной подгруппы предполагается, что исходные строки, определяющие
# # выражения, не содержат пробелов. При выполнении заданий не следует использовать оператор
# # цикла.Вывести значение логического выражения, заданного в виде строки S. Выражениеопределяется следующим образом («T» — True, «F» — False):
# <выражение> ::= T | F | And(<выражение> , <выражение>) |
# Or(<выражение> , <выражение>)
def evaluate_expression(expression):
    expression = expression.replace(" ", "")  # Удаляем пробелы

    def parse_expression(expr):  # Разбор выражения и вычисление его значения
        if expr == "T" or expr == "t":
            return True
        elif expr == "F" or expr == "f":
            return False
        elif expr[:4] == "And(" and expr[-1] == ")":
            inner_expr = expr[4:-1]  # Выделяем внутреннее выражение
            left_expr, right_expr = split_expression(inner_expr)  # Разбиваем выражение на две части
            return parse_expression(left_expr) and parse_expression(right_expr)
        elif expr[:3] == "Or(" and expr[-1] == ")":
            inner_expr = expr[3:-1]
            left_expr, right_expr = split_expression(inner_expr)
            return parse_expression(left_expr) or parse_expression(right_expr)
        else:
            raise ValueError("Некорректное выражение")

    def split_expression(expr):  # Разбивает выражение на две части
        balance = 0
        for i in range(len(expr)):  # Проверка скобок и запятых
            if expr[i] == '(':
                balance += 1
            elif expr[i] == ')':
                balance -= 1
            elif expr[i] == ',' and balance == 0:
                return expr[:i], expr[i + 1:]
        raise ValueError("Некорректное выражение")

    return parse_expression(expression)


expression = str(input("Введите выражение: "))
result = evaluate_expression(expression)
print(f"Результат выражения '{expression}': {result}")


