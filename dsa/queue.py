
class Node:
    """A node in the linked-list queue."""

    def __init__(self, data):
        self.data = data
        self.next = None


class Queue:
    """Custom FIFO queue using a linked list."""

    def __init__(self):
        self.front = None
        self.rear = None
        self.size = 0

    def enqueue(self, data):
        new_node = Node(data)

        if self.rear is None:
            self.front = new_node
            self.rear = new_node
        else:
            self.rear.next = new_node
            self.rear = new_node

        self.size += 1

    def dequeue(self):
        if self.is_empty():
            return None

        data = self.front.data
        self.front = self.front.next

        if self.front is None:
            self.rear = None

        self.size -= 1
        return data

    def is_empty(self):
        return self.front is None

    def get_size(self):
        return self.size
