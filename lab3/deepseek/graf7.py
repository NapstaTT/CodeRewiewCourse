#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Модуль для определения городов, достижимых из двух заданных штаб-квартир
с ограничением на число промежуточных городов.

Граф задаётся матрицей смежности в текстовом файле. Пользователь вводит номера
штаб-квартир K1, K2 и максимальное количество промежуточных городов L.
Программа находит все города, достижимые из обеих штаб-квартир при движении
не более чем через L промежуточных городов (то есть длина пути в рёбрах ≤ L+1).
Результат выводится в порядке возрастания номеров.
"""

import sys
from collections import deque


def read_graph(filename: str):
    """
    Читает граф из файла с матрицей смежности.

    Формат файла:
    - первая строка: целое число n (количество городов, n ≤ 25)
    - следующие n строк: по n целых чисел (0 или 1) — матрица смежности
    (числа могут быть разделены пробелами)

    Args:
        filename (str): Имя файла.

    Returns:
        tuple: (n, матрица_смежности)
               матрица_смежности — список списков целых чисел 0/1,
               индексация с 0 (соответствует городам 1..n).

    Raises:
        FileNotFoundError: если файл не найден.
        ValueError: если данные в файле некорректны.
    """
    with open(filename, 'r', encoding='utf-8') as f:
        lines = [line.strip() for line in f if line.strip()]

    if not lines:
        raise ValueError("Файл пуст.")

    try:
        n = int(lines[0])
    except ValueError:
        raise ValueError("Первая строка должна содержать целое число (количество городов).")

    if n > 25:
        raise ValueError("Количество городов не должно превышать 25.")

    adj = []
    for i in range(1, n + 1):
        if i >= len(lines):
            raise ValueError(f"Недостаточно строк для матрицы: ожидается {n}, получено {len(lines)-1}.")
        row = list(map(int, lines[i].split()))
        if len(row) != n:
            raise ValueError(f"Строка {i+1} матрицы содержит {len(row)} элементов, ожидается {n}.")
        adj.append(row)

    return n, adj


def reachable_with_limit(start: int, max_edges: int, adj):
    """
    Возвращает множество городов, достижимых из start за не более чем max_edges рёбер.

    Используется поиск в ширину (BFS) с ограничением глубины.
    Начальный город включается в множество (путь длины 0).

    Args:
        start (int): Номер стартового города (1-индексация).
        max_edges (int): Максимальное количество рёбер в пути.
        adj (list): Матрица смежности (0-индексация).

    Returns:
        set: Множество номеров городов (1-индексация), достижимых из start.
    """
    n = len(adj)
    start0 = start - 1
    # dist[i] = -1 означает, что вершина не посещена
    dist = [-1] * n
    dist[start0] = 0
    q = deque([start0])

    while q:
        v = q.popleft()
        if dist[v] >= max_edges:
            continue
        for to in range(n):
            if adj[v][to] == 1 and dist[to] == -1:
                dist[to] = dist[v] + 1
                q.append(to)

    # Преобразуем индексы обратно в номера городов (1-индексация)
    return {i + 1 for i, d in enumerate(dist) if d != -1}


def main():
    """Основная функция программы."""
    # Имя файла с графом (по условию — "FileName", можно изменить при необходимости)
    filename = "filename.txt"

    try:
        n, adj = read_graph(filename)
    except FileNotFoundError:
        print(f"Ошибка: файл '{filename}' не найден.", file=sys.stderr)
        sys.exit(1)
    except ValueError as e:
        print(f"Ошибка в файле: {e}", file=sys.stderr)
        sys.exit(1)

    print(f"Граф успешно загружен. Количество городов: {n}")

    # Ввод параметров задачи
    try:
        k1 = int(input("Введите номер первой штаб-квартиры (K1): "))
        k2 = int(input("Введите номер второй штаб-квартиры (K2): "))
        L = int(input("Введите максимальное количество промежуточных городов (L): "))
    except ValueError:
        print("Ошибка: все значения должны быть целыми числами.", file=sys.stderr)
        sys.exit(1)

    # Проверка корректности номеров городов
    if not (1 <= k1 <= n and 1 <= k2 <= n):
        print(f"Ошибка: номера городов должны быть в диапазоне от 1 до {n}.", file=sys.stderr)
        sys.exit(1)

    # Максимальное количество рёбер в пути.
    # Если разрешено не более L промежуточных городов,
    # то длина пути в рёбрах не превышает L+1.
    max_edges = L + 1

    # Множества достижимых городов
    reachable1 = reachable_with_limit(k1, max_edges, adj)
    reachable2 = reachable_with_limit(k2, max_edges, adj)

    # Пересечение множеств
    common = reachable1 & reachable2

    if not common:
        print(-1)
    else:
        print(' '.join(str(city) for city in sorted(common)))


if __name__ == "__main__":
    main()