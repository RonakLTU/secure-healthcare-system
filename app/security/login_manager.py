import sqlite3
from flask_login import LoginManager
from app.models.auth_user import User

DATABASE = "database/auth.db"

login_manager = LoginManager()


@login_manager.user_loader
def load_user(user_id):

    with sqlite3.connect(DATABASE) as conn:

        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT id, name, email, role
            FROM users
            WHERE id=?
            """,
            (user_id,)
        )

        user = cursor.fetchone()

    if user:

        # user = (id, name, email, role)
        return User(user[0], user[1], user[2], user[3])

    return None
