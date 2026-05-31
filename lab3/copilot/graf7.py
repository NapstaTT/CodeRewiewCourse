#!/usr/bin/env python3
"""
Поиск городов, достижимых из двух заданных городов (K1 и K2)
не более чем через L промежуточных городов.

Используется матрица смежности, считанная из файла FileName.

Если город достижим из обоих штаб-квартир — он включается в результат.
Если таких городов нет — выводится -1.
"""

from collections import deque
from typing import List, Set


def bfs_limited(start: int, graph: List[List[int]], max_depth: int) -> Set[int]:
    """
    Выполнить поиск в ширину (BFS) с ограничением глубины.

    :param start: Номер стартового города (0-индексация).
    :param graph: Матрица смежности.
    :param max_depth: Максимальная глубина (количество рёбер).
    :return: Множество достижимых городов (0-индексация).
    """
    n = len(graph)
    visited = set()
    queue = deque([(start, 0)])  # (город, глубина)

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
    - читает данные из файла FileName,
    - выполняет BFS от K1 и K2,
    - выводит пересечение достижимых городов.
    """
    filename = "filename.txt"

    with open(filename, "r", encoding="utf-8") as file:
        n = int(file.readline().strip())
        graph = [list(map(int, file.readline().split())) for _ in range(n)]

    # В условии не сказано, где брать K1, K2, L — предположим, что пользователь вводит их.
    K1 = int(input("Введите номер города K1: ")) - 1
    K2 = int(input("Введите номер города K2: ")) - 1
    L = int(input("Введите L (максимум промежуточных городов): "))

    # Максимальная глубина BFS = количество рёбер = L + 1
    max_depth = L + 1

    reachable_from_K1 = bfs_limited(K1, graph, max_depth)
    reachable_from_K2 = bfs_limited(K2, graph, max_depth)

    # Пересечение
    result = sorted(reachable_from_K1 & reachable_from_K2)

    if not result:
        print(-1)
    else:
        # Переводим обратно к нумерации с 1
        print(*[city + 1 for city in result])
        

if __name__ == "__main__":
    main()
