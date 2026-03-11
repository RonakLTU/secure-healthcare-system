from flask import request, render_template, redirect
import sqlite3
import re
from app.security.password_utils import hash_password

DATABASE = "database/auth.db"


def register_user():

    if request.method == "POST":

        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]
        role = request.form["role"]

        # EMAIL VALIDATION
        email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'

        if not re.match(email_pattern, email):
            return "Invalid email format"

        # PASSWORD VALIDATION
        if len(password) < 8:
            return "Password must be at least 8 characters"

        if not re.search(r'[A-Z]', password):
            return "Password must contain uppercase letter"

        if not re.search(r'[a-z]', password):
            return "Password must contain lowercase letter"

        if not re.search(r'[0-9]', password):
            return "Password must contain number"

        if not re.search(r'[!@#$%^&*(),.?\":{}|<>]', password):
            return "Password must contain special character"

        hashed_password = hash_password(password)

        try:
            with sqlite3.connect(DATABASE) as conn:

                cursor = conn.cursor()

                cursor.execute(
                    "INSERT INTO users (name,email,password,role) VALUES (?,?,?,?)",
                    (name, email, hashed_password, role)
                )

                conn.commit()

        except sqlite3.IntegrityError:
            return "Email already exists"

        return redirect("/login")

    return render_template("register.html")