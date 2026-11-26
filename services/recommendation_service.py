
from services.graph_service import build_connection_graph
from database.db import get_connection
from dsa.max_heap import MaxHeap


def get_connection_recommendations(user_id):

    graph = build_connection_graph()

    direct_connections = graph.get_neighbors(user_id)

    recommendations = []

    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute("""
            SELECT id, full_name, username
            FROM users
            WHERE id != ?
            AND is_active = 1
        """, (user_id,))

        students = cursor.fetchall()

        for student in students:

            student_id = student["id"]

            # Skip already connected students
            if student_id in direct_connections:
                continue

            # Skip students with pending requests
            cursor.execute("""
                SELECT id
                FROM connection_requests
                WHERE status = 'pending'
                AND (
                    (sender_id = ? AND receiver_id = ?)
                    OR
                    (sender_id = ? AND receiver_id = ?)
                )
            """, (user_id, student_id, student_id, user_id))

            if cursor.fetchone():
                continue

            # Find mutual connections
            mutual_connections = (
                direct_connections.intersection(
                    graph.get_neighbors(student_id)
                )
            )

            if mutual_connections:
                recommendations.append({
                    "id": student_id,
                    "full_name": student["full_name"],
                    "username": student["username"],
                    "mutual_count": len(mutual_connections)
                })

        recommendation_heap = MaxHeap()

        for recommendation in recommendations:
            recommendation_heap.insert(
                recommendation["mutual_count"],
                recommendation
            )

        sorted_recommendations = []

        while not recommendation_heap.is_empty():
            priority, recommendation = recommendation_heap.extract_max()
            sorted_recommendations.append(recommendation)

        return sorted_recommendations

    finally:
        connection.close()
