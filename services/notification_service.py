
from database.db import get_connection


def create_notification(recipient_id, actor_id, notification_type,
                        message, related_id=None):

    if recipient_id == actor_id:
        return False

    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute("""
            INSERT INTO notifications (
                recipient_id,
                actor_id,
                notification_type,
                message,
                related_id
            )
            VALUES (?, ?, ?, ?, ?)
        """, (
            recipient_id,
            actor_id,
            notification_type,
            message,
            related_id
        ))

        connection.commit()
        return True

    except Exception:
        connection.rollback()
        return False

    finally:
        connection.close()


def get_notifications(user_id, status="All"):

    connection = get_connection()

    try:
        cursor = connection.cursor()

        query = """
            SELECT
                n.id,
                n.actor_id,
                n.notification_type,
                n.message,
                n.related_id,
                n.is_read,
                n.created_at,
                COALESCE(users.full_name, 'UniSphere') AS actor_name
            FROM notifications n
            LEFT JOIN users
                ON users.id = n.actor_id
            WHERE n.recipient_id = ?
        """

        parameters = [user_id]

        if status == "Unread":
            query += " AND n.is_read = 0"

        elif status == "Read":
            query += " AND n.is_read = 1"

        query += " ORDER BY n.created_at DESC, n.id DESC"

        cursor.execute(query, parameters)

        return [dict(row) for row in cursor.fetchall()]

    finally:
        connection.close()


def mark_notification_read(notification_id, user_id):

    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute("""
            UPDATE notifications
            SET is_read = 1
            WHERE id = ? AND recipient_id = ?
        """, (notification_id, user_id))

        connection.commit()

        return cursor.rowcount > 0

    finally:
        connection.close()


def mark_all_notifications_read(user_id):

    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute("""
            UPDATE notifications
            SET is_read = 1
            WHERE recipient_id = ? AND is_read = 0
        """, (user_id,))

        connection.commit()

        return True

    finally:
        connection.close()


def delete_notification(notification_id, user_id):

    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute("""
            DELETE FROM notifications
            WHERE id = ? AND recipient_id = ?
        """, (notification_id, user_id))

        connection.commit()

        return cursor.rowcount > 0

    finally:
        connection.close()


def get_unread_notification_count(user_id):

    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute("""
            SELECT COUNT(*) AS total
            FROM notifications
            WHERE recipient_id = ? AND is_read = 0
        """, (user_id,))

        result = cursor.fetchone()

        return result["total"]

    finally:
        connection.close()
