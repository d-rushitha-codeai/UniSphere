
from database.db import get_connection


def get_profile(user_id):
    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute(
            "INSERT OR IGNORE INTO profiles (user_id) VALUES (?)",
            (user_id,)
        )

        connection.commit()

        cursor.execute(
            "SELECT * FROM profiles WHERE user_id = ?",
            (user_id,)
        )

        profile = cursor.fetchone()

        return dict(profile) if profile else None

    finally:
        connection.close()


def save_profile(user_id, programme, branch, academic_year,
                 bio, skills, interests):

    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute("""
            INSERT OR IGNORE INTO profiles (user_id)
            VALUES (?)
        """, (user_id,))

        cursor.execute("""
            UPDATE profiles
            SET programme = ?,
                branch = ?,
                academic_year = ?,
                bio = ?,
                skills = ?,
                interests = ?
            WHERE user_id = ?
        """, (
            programme,
            branch,
            academic_year,
            bio,
            skills,
            interests,
            user_id
        ))

        connection.commit()

        return True, "Profile saved successfully!"

    except Exception as error:
        connection.rollback()
        return False, str(error)

    finally:
        connection.close()