'''Dynamic70. Даны ссылки A1 и A2 на первый и последний элементы двусвязного списка, реализованного в виде цепочки узлов, которая ограничена по краям константами null (если
список пуст, то A1 = A2 = null). Преобразовать исходный список в циклический список (см. задание Dynamic55), снабженный барьерным элементом. Барьерный элемент должен иметь значение 0 
и быть связан своими свойствами Next и Prev с первым и последним элементом исходного списка (в случае пустого исходного списка свойства Next и Prev барьерного элемента должны 
указывать на сам барьерный элемент). Вывести ссылку на барьерный элемент полученного списка. Не создавать новые объекты типа Node, за исключением барьерного элемента.'''

class Node:
	def __init__(self, key):
		self.key = key
		self.next = None
		self.prev = None

class List_:
	def __init__(self):
		self.head = None
		self.tail = None
		self.current = None

	def append(self, key):
		new_node = Node(key)
		if self.tail == None:
			self.head = new_node
			self.tail = new_node
		else:
			self.head.prev = new_node
			new_node.next = self.head
			self.head = new_node
		return self.head

	def cycle(self, A1, A2):
		barrier = Node(0)
		if A1 == None and A2 == None:
			barrier.next = barrier
			barrier.prev = barrier
			return barrier

		barrier.next = A1
		barrier.prev = A2
		A1.prev = barrier
		A2.next = barrier
		return barrier

	def print_list(self):
		current = self.head
		output = []
		while current:
			output.append(str(current.key))
			current = current.next
		print(', '.join(output))

list_ = List_()
list_.append(1)
list_.append(2)
list_.append(3)
list_.append(4)
list_.append(5)
list_.append(6)

A1 = list_.head
A2 = list_.tail

barrier = list_.cycle(A1, A2)

print(barrier.key)
