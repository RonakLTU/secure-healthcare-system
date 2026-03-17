import sqlite3
from app.security.password_utils import hash_password

DATABASE = "database/auth.db"


# =========================
# CREATE USERS TABLE
# =========================

def create_user_table():

    with sqlite3.connect(DATABASE) as conn:

        cursor = conn.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            clinician_id INTEGER UNIQUE,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL
        )
        """)

        conn.commit()

# =========================
# CREATE DEFAULT ADMIN
# =========================

def create_default_admin():

    admin_email = "admin@healthcare.com"
    admin_password = hash_password("Admin@123")

    with sqlite3.connect(DATABASE) as conn:

        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM users WHERE email=?",
            (admin_email,)
        )

        admin = cursor.fetchone()

        if not admin:

            cursor.execute(
                """
                INSERT INTO users (name,email,password,role)
                VALUES (?,?,?,?)
                """,
                ("System Admin", admin_email, admin_password, "admin")
            )

            conn.commit()


# =========================
# GET USER BY EMAIL
# =========================

def get_user_by_email(email):

    with sqlite3.connect(DATABASE) as conn:

        cursor = conn.cursor()

        cursor.execute(
            "SELECT id,name,email,password,role FROM users WHERE email=?",
            (email,)
        )

        return cursor.fetchone()