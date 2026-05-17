"""
Дан односвязный линейный список и указатель на голову списка P1. Необходимо
найти второй элемент, кратный 6, и вывести указатель на этот элемент списка Px. Если такого
элемента в списке нет, то результат должен быть равен nil.
"""

class Node:
    def __init__(self, data, next=None):
        self.data = data
        self.next = next

    def __str__(self):
        return str(self.data)

def find_second_multiple_of_six(P1):
    count = 0
    current = P1
    while current is not None:
        if current.data % 6 == 0:
            count += 1
            if count == 2:
                return current
        current = current.next
    return None

if __name__ == "__main__":
    node5 = Node(18)
    node4 = Node(5, node5)
    node3 = Node(12, node4)
    node2 = Node(7, node3)
    node1 = Node(6, node2)  # Голова списка P1

    result = find_second_multiple_of_six(node1)
    if result is None:
        print("В списке нет второго элемента, кратного 6.")
    else:
        print("Узел, являющийся вторым элементом, кратным 6, имеет значение:", result.data)
