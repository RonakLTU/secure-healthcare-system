import sqlite3
from app.security.password_utils import hash_password

DATABASE = "database/auth.db"


def create_user_table():

    with sqlite3.connect(DATABASE) as conn:

        cursor = conn.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL
        )
        """)

        conn.commit()


def create_default_admin():

    admin_email = "admin@healthcare.com"
    admin_password = hash_password("Admin@123")

    with sqlite3.connect(DATABASE) as conn:

        cursor = conn.cursor()

        cursor.execute("SELECT * FROM users WHERE email=?", (admin_email,))
        user = cursor.fetchone()

        if not user:

            cursor.execute(
                "INSERT INTO users (name,email,password,role) VALUES (?,?,?,?)",
                ("System Admin", admin_email, admin_password, "admin")
            )

            conn.commit()