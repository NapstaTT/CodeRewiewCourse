# Dynamic26. Даны ссылки A1 и A2 на начало и конец очереди (если очередь является пустой,
# то A1 = A2 = null). Также дано число N (> 0) и набор из N чисел. Описать класс IntQueue,
# содержащий следующие члены:
# • закрытые поля head и tail типа Node (начало и конец очереди);
# • конструктор с параметрами aHead, aTail — началом и концом существующей очереди;
# • процедура Enqueue(D), которая добавляет в конец очереди новый элемент со значением D (D
# — входной параметр целого типа);
# • процедура Put (без параметров), которая выводит ссылки на поля head и tail, используя метод
# Put класса PT.
# С помощью метода Enqueue добавить в исходную очередь данный набор чисел и вывести
# новые ссылки на ее начало и конец, используя для этого метод Put класса IntQueue.

class Node:

    def __init__(self, data):
        self.data = data
        self.next = None

    def __str__(self):
        return str(self.data)

class IntQueue:

    def __init__(self, aHead = None, aTail = None):
        self.head = aHead
        self.tail = aTail

    def Enqueue(self, D):
        new_node = Node(D)
        if self.head is None:
            self.head = new_node
            self.tail = new_node
        else:
            self.tail.next = new_node
            self.tail = new_node

    def Put(self):

        print(f"Ссылка на начало очереди {self.head}")
        print(f"Ссылка на конец очереди {self.tail}")

if __name__ == "__main__":

    queue = IntQueue()
    N = int(input("Введите число N (>0): "))
    if N < 0:
        print("N должно быть больше 0!!!")
    else:
        for i in range(N):
            data = int(input("Введите число: "))
            queue.Enqueue(data)
    queue.Put()



