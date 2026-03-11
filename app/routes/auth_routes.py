from flask import request, render_template
import sqlite3
from app.security.password_utils import hash_password

DATABASE = "database/auth.db"


def register_user():

    if request.method == "POST":

        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]
        role = "patient"

        hashed_password = hash_password(password)

        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO users (name,email,password,role) VALUES (?,?,?,?)",
            (name, email, hashed_password, role)
        )

        conn.commit()
        conn.close()

        return "User Registered Successfully"

    return render_template("register.html")