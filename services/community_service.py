
from database.db import get_connection


def create_community(user_id, name, description):

    name = name.strip()
    description = description.strip()

    if not name:
        return False, "Community name cannot be empty."

    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute("""
            INSERT INTO communities (name, description, created_by)
            VALUES (?, ?, ?)
        """, (name, description, user_id))

        community_id = cursor.lastrowid

        cursor.execute("""
            INSERT INTO community_members (community_id, user_id)
            VALUES (?, ?)
        """, (community_id, user_id))

        connection.commit()

        return True, "Community created successfully!"

    except Exception as error:
        connection.rollback()

        if "UNIQUE constraint failed" in str(error):
            return False, "A community with this name already exists."

        return False, str(error)

    finally:
        connection.close()


def get_communities(user_id):

    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute("""
            SELECT
                c.id,
                c.name,
                c.description,
                c.created_by,
                c.created_at,
                users.full_name AS creator_name,
                COUNT(DISTINCT cm.user_id) AS member_count,
                EXISTS (
                    SELECT 1
                    FROM community_members
                    WHERE community_id = c.id
                    AND user_id = ?
                ) AS is_member
            FROM communities c
            JOIN users ON users.id = c.created_by
            LEFT JOIN community_members cm
                ON cm.community_id = c.id
            WHERE c.is_active = 1
            GROUP BY c.id
            ORDER BY c.created_at DESC, c.id DESC
        """, (user_id,))

        return [dict(row) for row in cursor.fetchall()]

    finally:
        connection.close()


def join_community(user_id, community_id):

    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute("""
            SELECT id FROM communities
            WHERE id = ? AND is_active = 1
        """, (community_id,))

        if not cursor.fetchone():
            return False, "Community not found."

        cursor.execute("""
            INSERT OR IGNORE INTO community_members
            (community_id, user_id)
            VALUES (?, ?)
        """, (community_id, user_id))

        if cursor.rowcount == 0:
            return False, "You are already a member."

        connection.commit()

        return True, "You joined the community!"

    except Exception as error:
        connection.rollback()
        return False, str(error)

    finally:
        connection.close()


def leave_community(user_id, community_id):

    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute("""
            SELECT created_by
            FROM communities
            WHERE id = ? AND is_active = 1
        """, (community_id,))

        community = cursor.fetchone()

        if not community:
            return False, "Community not found."

        if community["created_by"] == user_id:
            return False, "The creator cannot leave their own community."

        cursor.execute("""
            DELETE FROM community_members
            WHERE community_id = ? AND user_id = ?
        """, (community_id, user_id))

        if cursor.rowcount == 0:
            return False, "You are not a member."

        connection.commit()

        return True, "You left the community."

    except Exception as error:
        connection.rollback()
        return False, str(error)

    finally:
        connection.close()


def create_community_post(user_id, community_id, content):

    content = content.strip()

    if not content:
        return False, "Discussion cannot be empty."

    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute("""
            SELECT id FROM community_members
            WHERE community_id = ? AND user_id = ?
        """, (community_id, user_id))

        if not cursor.fetchone():
            return False, "Join the community before posting."

        cursor.execute("""
            INSERT INTO community_posts
            (community_id, user_id, content)
            VALUES (?, ?, ?)
        """, (community_id, user_id, content))

        connection.commit()

        return True, "Discussion posted successfully!"

    except Exception as error:
        connection.rollback()
        return False, str(error)

    finally:
        connection.close()


def get_community_posts(community_id):

    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute("""
            SELECT
                cp.id,
                cp.content,
                cp.created_at,
                users.full_name,
                users.username
            FROM community_posts cp
            JOIN users ON users.id = cp.user_id
            WHERE cp.community_id = ?
            ORDER BY cp.created_at DESC, cp.id DESC
        """, (community_id,))

        return [dict(row) for row in cursor.fetchall()]

    finally:
        connection.close()
