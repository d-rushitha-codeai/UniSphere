
from database.db import get_connection
from dsa.graph import Graph


def build_connection_graph():
    """Build the student connection graph using SQLite data."""

    connection = get_connection()

    try:
        cursor = connection.cursor()

        graph = Graph()

        # Add all active students as graph vertices
        cursor.execute("""
            SELECT id
            FROM users
            WHERE is_active = 1
        """)

        students = cursor.fetchall()

        for student in students:
            graph.add_vertex(student["id"])

        # Add accepted connections as undirected edges
        cursor.execute("""
            SELECT user1_id, user2_id
            FROM connections
        """)

        connections = cursor.fetchall()

        for item in connections:
            graph.add_edge(
                item["user1_id"],
                item["user2_id"]
            )

        return graph

    finally:
        connection.close()


def get_student_network(user_id):
    """Get all students reachable through BFS."""

    graph = build_connection_graph()

    return graph.bfs(user_id)


def get_direct_connections(user_id):
    """Get students directly connected to a user."""

    graph = build_connection_graph()

    return sorted(graph.get_neighbors(user_id))


def get_mutual_connections(user_id, other_user_id):
    """Find students connected to both users."""

    graph = build_connection_graph()

    user_neighbors = graph.get_neighbors(user_id)
    other_neighbors = graph.get_neighbors(other_user_id)

    return sorted(user_neighbors.intersection(other_neighbors))
