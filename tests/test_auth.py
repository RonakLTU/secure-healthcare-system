import sqlite3

DATABASE = "database/auth.db"


def test_user_table_exists():

    conn = sqlite3.connect(DATABASE)

    cursor = conn.cursor()

    cursor.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name='users'"
    )

    table = cursor.fetchone()

    conn.close()

    assert table is not None


def test_admin_account_exists():

    conn = sqlite3.connect(DATABASE)

    cursor = conn.cursor()

    cursor.execute(
        "SELECT email FROM users WHERE role='admin'"
    )

    admin = cursor.fetchone()

    conn.close()

    assert admin is not None