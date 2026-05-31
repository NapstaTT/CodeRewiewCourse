from collections import deque


def read_graph(filename):
    """
    Считывает граф из файла.

    Формат файла:
    n
    строка матрицы 1
    строка матрицы 2
    ...
    строка матрицы n

    Returns:
        tuple[int, list[list[int]]]:
            количество вершин и матрица смежности.
    """
    with open(filename, "r", encoding="utf-8") as file:
        n = int(file.readline())

        matrix = [
            list(map(int, file.readline().split()))
            for _ in range(n)
        ]

    return n, matrix


def reachable_cities(matrix, start, max_edges):
    """
    Находит все города, достижимые из start
    не более чем за max_edges дорог.

    Args:
        matrix: матрица смежности.
        start: начальный город (индекс с 0).
        max_edges: максимальная длина пути.

    Returns:
        set[int]: множество достижимых городов.
    """
    n = len(matrix)

    distance = [-1] * n
    distance[start] = 0

    queue = deque([start])

    while queue:
        current = queue.popleft()

        if distance[current] >= max_edges:
            continue

        for neighbor in range(n):
            if matrix[current][neighbor] == 1:
                if distance[neighbor] == -1:
                    distance[neighbor] = distance[current] + 1
                    queue.append(neighbor)

    result = set()

    for city in range(n):
        if distance[city] != -1 and distance[city] <= max_edges:
            result.add(city + 1)

    return result


def common_cities(filename, k1, k2, l):
    """
    Находит города, достижимые из обеих штаб-квартир.

    Args:
        filename: имя файла с матрицей смежности.
        k1: номер первой штаб-квартиры.
        k2: номер второй штаб-квартиры.
        l: максимальное количество промежуточных городов.
    """
    _, matrix = read_graph(filename)

    max_edges = l + 1

    cities_1 = reachable_cities(
        matrix,
        k1 - 1,
        max_edges
    )

    cities_2 = reachable_cities(
        matrix,
        k2 - 1,
        max_edges
    )

    common = sorted(cities_1 & cities_2)

    if common:
        print(*common)
    else:
        print(-1)


def main():
    filename = "FileName.txt"

    k1 = int(input("Введите K1: "))
    k2 = int(input("Введите K2: "))
    l = int(input("Введите L: "))

    common_cities(filename, k1, k2, l)


if __name__ == "__main__":
    main()