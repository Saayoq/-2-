import matplotlib.pyplot as plt


class Node:
    def __init__(self, value):
        self.value = value
        self.next = None


class LinkedList:
    def __init__(self):
        self.head = None

    def add_end(self, value):
        new_node = Node(value)

        if self.head is None:
            self.head = new_node
            return

        current = self.head

        while current.next is not None:
            current = current.next

        current.next = new_node

    def add_beginning(self, value):
        new_node = Node(value)
        new_node.next = self.head
        self.head = new_node

    def print_list(self):
        current = self.head

        if current is None:
            print("Список пуст.")
            return

        print("Элементы связного списка:")

        while current is not None:
            print(current.value, end=" -> ")
            current = current.next

        print("None")

    def length(self):
        count = 0
        current = self.head

        while current is not None:
            count += 1
            current = current.next

        return count

    def search(self, value):
        current = self.head
        position = 0

        while current is not None:
            if current.value == value:
                return position

            current = current.next
            position += 1

        return -1

    def draw_list(self):
        values = []
        current = self.head

        while current is not None:
            values.append(current.value)
            current = current.next

        plt.figure(figsize=(12, 4))
        plt.title("Визуализация связного списка")

        x = 0
        y = 0

        for i, value in enumerate(values):
            plt.text(
                x, y, str(value),
                ha="center",
                va="center",
                fontsize=12,
                bbox=dict(boxstyle="round", edgecolor="black", facecolor="white")
            )

            if i < len(values) - 1:
                plt.annotate(
                    "",
                    xy=(x + 1.45, y),
                    xytext=(x + 0.55, y),
                    arrowprops=dict(arrowstyle="->", color="black", lw=1.5)
                )

            x += 2

        plt.text(
            x, y, "None",
            ha="center",
            va="center",
            fontsize=12,
            bbox=dict(boxstyle="round", edgecolor="black", facecolor="lightgray")
        )

        plt.axis("off")
        plt.savefig("linked_list.png", dpi=300, bbox_inches="tight")
        plt.show()


linked_list = LinkedList()

linked_list.add_end(10)
linked_list.add_end(20)
linked_list.add_end(30)
linked_list.add_end(40)
linked_list.add_beginning(5)

linked_list.print_list()

print("Длина списка:", linked_list.length())

number = 30
position = linked_list.search(number)

if position != -1:
    print("Элемент", number, "найден на позиции", position)
else:
    print("Элемент", number, "не найден")

linked_list.draw_list()
