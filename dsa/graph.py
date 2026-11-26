
from dsa.queue import Queue


class Graph:
    """Undirected graph using an adjacency list and sets."""

    def __init__(self):
        self.adjacency_list = {}

    def add_vertex(self, vertex):
        """Add a student to the graph."""

        if vertex not in self.adjacency_list:
            self.adjacency_list[vertex] = set()

    def add_edge(self, vertex1, vertex2):
        """Create an undirected connection."""

        if vertex1 == vertex2:
            return

        self.add_vertex(vertex1)
        self.add_vertex(vertex2)

        self.adjacency_list[vertex1].add(vertex2)
        self.adjacency_list[vertex2].add(vertex1)

    def remove_edge(self, vertex1, vertex2):
        """Remove a connection between two students."""

        if vertex1 in self.adjacency_list:
            self.adjacency_list[vertex1].discard(vertex2)

        if vertex2 in self.adjacency_list:
            self.adjacency_list[vertex2].discard(vertex1)

    def get_neighbors(self, vertex):
        """Return all directly connected students."""

        return self.adjacency_list.get(vertex, set()).copy()

    def bfs(self, start_vertex):
        """Perform Breadth-First Search."""

        if start_vertex not in self.adjacency_list:
            return []

        visited = set()
        result = []
        queue = Queue()

        visited.add(start_vertex)
        queue.enqueue(start_vertex)

        while not queue.is_empty():

            current = queue.dequeue()
            result.append(current)

            for neighbor in sorted(self.adjacency_list[current]):

                if neighbor not in visited:

                    visited.add(neighbor)
                    queue.enqueue(neighbor)

        return result

    def display_graph(self):
        """Return the adjacency list."""

        return {
            vertex: sorted(neighbors)
            for vertex, neighbors in self.adjacency_list.items()
        }
