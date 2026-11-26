
from database.db import get_connection
from services.notification_service import create_notification



def send_connection_request(sender_id, receiver_id):

    if sender_id == receiver_id:
        return False, "You cannot connect with yourself."

    connection = get_connection()

    try:
        cursor = connection.cursor()

        user1 = min(sender_id, receiver_id)
        user2 = max(sender_id, receiver_id)

        cursor.execute("""
            SELECT id FROM connections
            WHERE user1_id = ? AND user2_id = ?
        """, (user1, user2))

        if cursor.fetchone():
            return False, "You are already connected."

        cursor.execute("""
            SELECT id, sender_id FROM connection_requests
            WHERE (
                (sender_id = ? AND receiver_id = ?)
                OR (sender_id = ? AND receiver_id = ?)
            )
            AND status = 'pending'
        """, (sender_id, receiver_id, receiver_id, sender_id))

        existing = cursor.fetchone()

        if existing:
            if existing["sender_id"] == sender_id:
                return False, "Connection request already sent."
            return False, "This student has already sent you a request."

        cursor.execute("""
            SELECT id FROM connection_requests
            WHERE sender_id = ? AND receiver_id = ?
        """, (sender_id, receiver_id))

        previous = cursor.fetchone()

        if previous:
            cursor.execute("""
                UPDATE connection_requests
                SET status = 'pending',
                    created_at = CURRENT_TIMESTAMP
                WHERE id = ?
            """, (previous["id"],))
        else:
            cursor.execute("""
                INSERT INTO connection_requests
                (sender_id, receiver_id)
                VALUES (?, ?)
            """, (sender_id, receiver_id))

        connection.commit()

        create_notification(
            receiver_id,
            sender_id,
            "connection_request",
            "sent you a connection request."
        )

        return True, "Connection request sent successfully!"

    except Exception as error:
        connection.rollback()
        return False, str(error)

    finally:
        connection.close()


def get_incoming_requests(user_id):

    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute("""
            SELECT
                cr.id AS request_id,
                users.id AS user_id,
                users.full_name,
                users.username,
                profiles.branch,
                profiles.academic_year,
                profiles.bio
            FROM connection_requests cr
            JOIN users ON cr.sender_id = users.id
            LEFT JOIN profiles ON users.id = profiles.user_id
            WHERE cr.receiver_id = ?
            AND cr.status = 'pending'
            ORDER BY cr.created_at DESC
        """, (user_id,))

        return [dict(row) for row in cursor.fetchall()]

    finally:
        connection.close()


def get_connections(user_id):

    connection = get_connection()

    try:
        cursor = connection.cursor()

        
        cursor.execute("""
            SELECT
                users.id AS user_id,
                users.full_name,
                users.username,
                COALESCE(NULLIF(profiles.branch, 'None'), 'CSE AI') AS branch,
                COALESCE(NULLIF(profiles.academic_year, 'None'), '2nd Year') AS academic_year,
                COALESCE(NULLIF(profiles.bio, 'None'), '') AS bio
            FROM connections c
            JOIN users
                ON users.id = CASE
                    WHEN c.user1_id = ? THEN c.user2_id
                    ELSE c.user1_id
                END
            LEFT JOIN profiles
                ON users.id = profiles.user_id
            WHERE c.user1_id = ? OR c.user2_id = ?
            ORDER BY users.full_name COLLATE NOCASE
        """, (user_id, user_id, user_id))

        return [dict(row) for row in cursor.fetchall()]

    finally:
        connection.close()



def accept_connection_request(request_id, receiver_id):

    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute("""
            SELECT sender_id, receiver_id
            FROM connection_requests
            WHERE id = ? AND receiver_id = ?
            AND status = 'pending'
        """, (request_id, receiver_id))

        request = cursor.fetchone()

        if not request:
            return False, "Connection request not found."

        user1 = min(request["sender_id"], receiver_id)
        user2 = max(request["sender_id"], receiver_id)

        cursor.execute("""
            INSERT OR IGNORE INTO connections
            (user1_id, user2_id)
            VALUES (?, ?)
        """, (user1, user2))

        cursor.execute("""
            UPDATE connection_requests
            SET status = 'accepted'
            WHERE id = ?
        """, (request_id,))

        connection.commit()

        create_notification(
            request["sender_id"],
            receiver_id,
            "connection_accepted",
            "accepted your connection request.",
            request_id
        )

        return True, "Connection accepted successfully!"

    except Exception as error:
        connection.rollback()
        return False, str(error)

    finally:
        connection.close()


def reject_connection_request(request_id, receiver_id):

    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute("""
            UPDATE connection_requests
            SET status = 'rejected'
            WHERE id = ?
            AND receiver_id = ?
            AND status = 'pending'
        """, (request_id, receiver_id))

        if cursor.rowcount == 0:
            return False, "Connection request not found."

        connection.commit()
        return True, "Connection request rejected."

    except Exception as error:
        connection.rollback()
        return False, str(error)

    finally:
        connection.close()


def remove_connection(user_id, other_user_id):

    connection = get_connection()

    try:
        cursor = connection.cursor()

        user1 = min(user_id, other_user_id)
        user2 = max(user_id, other_user_id)

        cursor.execute("""
            DELETE FROM connections
            WHERE user1_id = ? AND user2_id = ?
        """, (user1, user2))

        if cursor.rowcount == 0:
            return False, "Connection not found."

        connection.commit()
        return True, "Connection removed successfully!"

    except Exception as error:
        connection.rollback()
        return False, str(error)

    finally:
        connection.close()

def get_connection_status(user_id, other_user_id):

    if user_id == other_user_id:
        return "self"

    connection = get_connection()

    try:
        cursor = connection.cursor()

        user1 = min(user_id, other_user_id)
        user2 = max(user_id, other_user_id)

        cursor.execute("""
            SELECT id
            FROM connections
            WHERE user1_id = ? AND user2_id = ?
        """, (user1, user2))

        if cursor.fetchone():
            return "connected"

        cursor.execute("""
            SELECT id
            FROM connection_requests
            WHERE status = 'pending'
            AND (
                (sender_id = ? AND receiver_id = ?)
                OR
                (sender_id = ? AND receiver_id = ?)
            )
        """, (user_id, other_user_id, other_user_id, user_id))

        if cursor.fetchone():
            return "pending"

        return "not_connected"

    finally:
        connection.close()


