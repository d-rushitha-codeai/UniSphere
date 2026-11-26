
from database.db import get_connection
from dsa.trie import Trie

def get_all_students(current_user_id, search="", branch="All",
                     academic_year="All"):

    connection = get_connection()

    try:
        cursor = connection.cursor()

        query = """
            SELECT
                users.id,
                users.full_name,
                users.username,
                COALESCE(NULLIF(profiles.programme, 'None'), 'BTech') AS programme,
                COALESCE(NULLIF(profiles.branch, 'None'), 'CSE AI') AS branch,
                COALESCE(NULLIF(profiles.academic_year, 'None'), '2nd Year') AS academic_year,
                COALESCE(NULLIF(profiles.bio, 'None'), '') AS bio,
                COALESCE(NULLIF(profiles.skills, 'None'), '') AS skills,
                COALESCE(NULLIF(profiles.interests, 'None'), '') AS interests
            FROM users
            LEFT JOIN profiles ON users.id = profiles.user_id
            WHERE users.id != ?
            AND users.is_active = 1
        """

        parameters = [current_user_id]

        if search.strip():

            cursor.execute("""
                SELECT id, full_name, username
                FROM users
                WHERE id != ? AND is_active = 1
            """, (current_user_id,))

            all_students = cursor.fetchall()
            student_trie = Trie()

            for student in all_students:
                for text in [student["full_name"], student["username"]]:
                    text = text.lower()

                    for index in range(len(text)):
                        student_trie.insert(text[index:], student["id"])

            matching_ids = sorted(
                student_trie.search_prefix(search.strip().lower())
            )

            if matching_ids:
                placeholders = ",".join("?" for _ in matching_ids)
                query += f" AND users.id IN ({placeholders})"
                parameters.extend(matching_ids)
            else:
                query += " AND 1 = 0"

        if branch != "All":
            query += """
                AND COALESCE(NULLIF(profiles.branch, 'None'), 'CSE AI') = ?
            """
            parameters.append(branch)

        if academic_year != "All":
            query += """
                AND COALESCE(NULLIF(profiles.academic_year, 'None'), '2nd Year') = ?
            """
            parameters.append(academic_year)

        query += " ORDER BY users.full_name COLLATE NOCASE"

        cursor.execute(query, parameters)

        students = cursor.fetchall()

        return [dict(student) for student in students]

    finally:
        connection.close()



def get_branches():

    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute("""
            SELECT DISTINCT branch
            FROM profiles
            WHERE branch IS NOT NULL
            AND branch != ''
            ORDER BY branch
        """)

        branches = cursor.fetchall()

        return [row["branch"] for row in branches]

    finally:
        connection.close()
