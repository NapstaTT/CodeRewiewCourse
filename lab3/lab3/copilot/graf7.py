#!/usr/bin/env python3
# FIXME:
# 1. Добавлена обработка ошибок при чтении файла (FileNotFoundError, ValueError).
# 2. Реализована защита от некорректного ввода пользователя (функция safe_int_input).
# 3. Добавлены проверки диапазона для K1, K2 (1..n) и L (>=0).
# 4. Исправлены docstrings (полное условие задачи, Google-формат).
# 5. Учтён принцип DRY: вынесен безопасный ввод в отдельную функцию.
"""
Поиск городов, достижимых из двух заданных городов (K1 и K2)
не более чем через L промежуточных городов.

Условие задачи:
Используется матрица смежности, считанная из файла filename.txt.
Города нумеруются с 1 до n.
Если город достижим из обоих штаб-квартир (K1 и K2) не более чем через L
промежуточных городов (т.е. длина пути ≤ L+1 ребро) – он включается в результат.
Если таких городов нет – выводится -1.
"""

from collections import deque
from typing import List, Set
import sys


def safe_int_input(prompt: str, min_val: int = None, max_val: int = None) -> int:
    """
    Запросить у пользователя целое число с проверкой диапазона.

    Args:
        prompt (str): Текст приглашения.
        min_val (int, optional): Минимально допустимое значение.
        max_val (int, optional): Максимально допустимое значение.

    Returns:
        int: Корректно введённое целое число.
    """
    while True:
        try:
            val = int(input(prompt))
            if min_val is not None and val < min_val:
                print(f"Ошибка: число должно быть не меньше {min_val}.")
                continue
            if max_val is not None and val > max_val:
                print(f"Ошибка: число должно быть не больше {max_val}.")
                continue
            return val
        except ValueError:
            print("Ошибка: введите целое число.")


def bfs_limited(start: int, graph: List[List[int]], max_depth: int) -> Set[int]:
    """
    Выполнить поиск в ширину (BFS) с ограничением глубины.

    Args:
        start (int): Номер стартового города (0-индексация).
        graph (List[List[int]]): Матрица смежности.
        max_depth (int): Максимальная глубина (количество рёбер).

    Returns:
        Set[int]: Множество достижимых городов (0-индексация).
    """
    n = len(graph)
    visited = set()
    queue = deque([(start, 0)])
    visited.add(start)

    while queue:
        city, depth = queue.popleft()
        if depth == max_depth:
            continue
        for next_city in range(n):
            if graph[city][next_city] == 1 and next_city not in visited:
                visited.add(next_city)
                queue.append((next_city, depth + 1))
    return visited


def main() -> None:
    """
    Основная функция:
    - читает данные из файла filename.txt,
    - выполняет BFS от K1 и K2,
    - выводит пересечение достижимых городов.
    """
    filename = "filename.txt"

    # ---- Чтение файла с обработкой ошибок ----
    try:
        with open(filename, "r", encoding="utf-8") as file:
            line = file.readline().strip()
            if not line:
                print(f"Ошибка: файл '{filename}' пуст.")
                return
            n = int(line)
            graph = []
            for i in range(n):
                row_line = file.readline()
                if not row_line:
                    print(f"Ошибка: недостаточно строк в файле (ожидается {n}).")
                    return
                graph.append(list(map(int, row_line.split())))
    except FileNotFoundError:
        print(f"Ошибка: файл '{filename}' не найден.")
        return
    except ValueError:
        print(f"Ошибка: некорректный формат данных в файле '{filename}'.")
        return
    except Exception as e:
        print(f"Непредвиденная ошибка при чтении файла: {e}")
        return

    # ---- Ввод K1, K2, L с проверками ----
    n_cities = n
    K1 = safe_int_input(f"Введите номер города K1 (1..{n_cities}): ",
                        min_val=1, max_val=n_cities) - 1
    K2 = safe_int_input(f"Введите номер города K2 (1..{n_cities}): ",
                        min_val=1, max_val=n_cities) - 1
    L = safe_int_input("Введите L (максимум промежуточных городов, >=0): ",
                       min_val=0)

    max_depth = L + 1

    reachable_from_K1 = bfs_limited(K1, graph, max_depth)
    reachable_from_K2 = bfs_limited(K2, graph, max_depth)

    # Пересечение и вывод
    result = sorted(reachable_from_K1 & reachable_from_K2)
    if not result:
        print(-1)
    else:
        print(*[city + 1 for city in result])


if __name__ == "__main__":
    main()