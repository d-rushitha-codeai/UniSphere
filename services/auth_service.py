
import hashlib
import secrets

from database.db import get_connection


def hash_password(password, salt=None):
    """Securely hash a password using PBKDF2-HMAC-SHA256."""

    if salt is None:
        salt = secrets.token_hex(16)

    password_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        bytes.fromhex(salt),
        600000
    ).hex()

    return password_hash, salt


def register_user(full_name, username, email, password):
    """Validate and register a new student."""

    full_name = full_name.strip()
    username = username.strip()
    email = email.strip().lower()

    if not all([full_name, username, email, password]):
        return False, "Please fill in all required fields."

    if len(password) < 8:
        return False, "Password must contain at least 8 characters."

    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute(
            "SELECT id FROM users WHERE username = ? OR email = ?",
            (username, email)
        )

        if cursor.fetchone():
            return False, "Username or email already exists."

        password_hash, password_salt = hash_password(password)

        cursor.execute("""
            INSERT INTO users (
                full_name,
                username,
                email,
                password_hash,
                password_salt
            )
            VALUES (?, ?, ?, ?, ?)
        """, (
            full_name,
            username,
            email,
            password_hash,
            password_salt
        ))

        connection.commit()

        return True, "Your UniSphere account has been created successfully!"

    except Exception:
        connection.rollback()
        return False, "Registration failed. Please try again."

    finally:
        connection.close()

def verify_password(password, stored_hash, salt):
    """Verify a password against its stored hash."""

    calculated_hash, _ = hash_password(password, salt)

    return secrets.compare_digest(
        calculated_hash,
        stored_hash
    )


def login_user(username, password):
    """Authenticate a registered student."""

    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT id, full_name, username, email,
                   password_hash, password_salt
            FROM users
            WHERE username = ? AND is_active = 1
            """,
            (username.strip(),)
        )

        user = cursor.fetchone()

        if user is None:
            return False, "Invalid username or password.", None

        if not verify_password(
            password,
            user["password_hash"],
            user["password_salt"]
        ):
            return False, "Invalid username or password.", None

        user_data = {
            "id": user["id"],
            "full_name": user["full_name"],
            "username": user["username"],
            "email": user["email"]
        }

        return True, "Login successful!", user_data

    finally:
        connection.close()
