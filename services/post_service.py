
from database.db import get_connection
from services.notification_service import create_notification


def create_post(user_id, content):

    content = content.strip()

    if not content:
        return False, "Post cannot be empty."

    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute("""
            INSERT INTO posts (user_id, content)
            VALUES (?, ?)
        """, (user_id, content))

        connection.commit()

        return True, "Your post was published successfully!"

    except Exception as error:
        connection.rollback()
        return False, str(error)

    finally:
        connection.close()


def get_feed_posts(user_id):

    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute("""
            SELECT
                p.id AS post_id,
                p.user_id,
                p.content,
                p.created_at,
                users.full_name,
                users.username,

                (SELECT COUNT(*)
                 FROM post_likes
                 WHERE post_id = p.id) AS like_count,

                (SELECT COUNT(*)
                 FROM post_comments
                 WHERE post_id = p.id) AS comment_count,

                EXISTS (
                    SELECT 1
                    FROM post_likes
                    WHERE post_id = p.id
                    AND user_id = ?
                ) AS liked_by_user

            FROM posts p

            JOIN users ON users.id = p.user_id

            WHERE p.user_id = ?
               OR p.user_id IN (
                    SELECT CASE
                        WHEN user1_id = ? THEN user2_id
                        ELSE user1_id
                    END
                    FROM connections
                    WHERE user1_id = ? OR user2_id = ?
               )

            ORDER BY p.created_at DESC, p.id DESC

        """, (user_id, user_id, user_id, user_id, user_id))

        return [dict(row) for row in cursor.fetchall()]

    finally:
        connection.close()



def toggle_like(user_id, post_id):

    connection = get_connection()
    notification_recipient = None

    try:
        cursor = connection.cursor()

        cursor.execute("""
            SELECT id FROM post_likes
            WHERE post_id = ? AND user_id = ?
        """, (post_id, user_id))

        existing_like = cursor.fetchone()

        if existing_like:

            cursor.execute("""
                DELETE FROM post_likes WHERE id = ?
            """, (existing_like["id"],))

            message = "Like removed."

        else:

            cursor.execute("""
                INSERT INTO post_likes (post_id, user_id)
                VALUES (?, ?)
            """, (post_id, user_id))

            cursor.execute("""
                SELECT user_id FROM posts WHERE id = ?
            """, (post_id,))

            post = cursor.fetchone()

            if post:
                notification_recipient = post["user_id"]

            message = "Post liked!"

        connection.commit()

        if notification_recipient is not None:
            create_notification(
                notification_recipient,
                user_id,
                "post_like",
                "liked your post.",
                post_id
            )

        return True, message

    except Exception as error:
        connection.rollback()
        return False, str(error)

    finally:
        connection.close()





def add_comment(user_id, post_id, comment):

    comment = comment.strip()

    if not comment:
        return False, "Comment cannot be empty."

    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute("""
            SELECT user_id FROM posts WHERE id = ?
        """, (post_id,))

        post = cursor.fetchone()

        if not post:
            return False, "Post not found."

        cursor.execute("""
            INSERT INTO post_comments (post_id, user_id, comment)
            VALUES (?, ?, ?)
        """, (post_id, user_id, comment))

        connection.commit()

        create_notification(
            post["user_id"],
            user_id,
            "post_comment",
            "commented on your post.",
            post_id
        )

        return True, "Comment added successfully!"

    except Exception as error:
        connection.rollback()
        return False, str(error)

    finally:
        connection.close()


def get_post_comments(post_id):

    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute("""
            SELECT
                post_comments.id,
                post_comments.comment,
                post_comments.created_at,
                users.full_name,
                users.username
            FROM post_comments
            JOIN users
                ON users.id = post_comments.user_id
            WHERE post_comments.post_id = ?
            ORDER BY post_comments.created_at ASC,
                     post_comments.id ASC
        """, (post_id,))

        return [dict(row) for row in cursor.fetchall()]

    finally:
        connection.close()


def delete_post(user_id, post_id):

    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute("""
            DELETE FROM posts
            WHERE id = ? AND user_id = ?
        """, (post_id, user_id))

        if cursor.rowcount == 0:
            return False, "Post not found or you cannot delete this post."

        cursor.execute("""
            DELETE FROM post_likes
            WHERE post_id = ?
        """, (post_id,))

        cursor.execute("""
            DELETE FROM post_comments
            WHERE post_id = ?
        """, (post_id,))

        connection.commit()

        return True, "Post deleted successfully!"

    except Exception as error:
        connection.rollback()
        return False, str(error)

    finally:
        connection.close()


def edit_post(user_id, post_id, new_content):

    new_content = new_content.strip()

    if not new_content:
        return False, "Post cannot be empty."

    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute("""
            UPDATE posts
            SET content = ?,
                updated_at = CURRENT_TIMESTAMP
            WHERE id = ? AND user_id = ?
        """, (new_content, post_id, user_id))

        if cursor.rowcount == 0:
            return False, "Post not found or you cannot edit this post."

        connection.commit()

        return True, "Post updated successfully!"

    except Exception as error:
        connection.rollback()
        return False, str(error)

    finally:
        connection.close()
