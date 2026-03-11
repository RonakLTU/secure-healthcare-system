from flask import request, render_template, redirect, session
import sqlite3
import re
from app.security.password_utils import hash_password, check_password

DATABASE = "database/auth.db"


def register_user():

    if request.method == "POST":

        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")
        role = request.form.get("role")

        # Email validation
        email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if not re.match(email_pattern, email):
            return render_template("register.html", error="Invalid email format")

        # Password validation
        if len(password) < 8:
            return render_template("register.html", error="Password must be at least 8 characters")

        if not re.search(r'[A-Z]', password):
            return render_template("register.html", error="Password must contain uppercase letter")

        if not re.search(r'[a-z]', password):
            return render_template("register.html", error="Password must contain lowercase letter")

        if not re.search(r'[0-9]', password):
            return render_template("register.html", error="Password must contain number")

        if not re.search(r'[!@#$%^&*(),.?\":{}|<>]', password):
            return render_template("register.html", error="Password must contain special character")

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
            return render_template("register.html", error="Email already exists")

        return redirect("/login")

    return render_template("register.html")


def login_user():

    if request.method == "POST":

        email = request.form.get("email")
        password = request.form.get("password")

        with sqlite3.connect(DATABASE) as conn:

            cursor = conn.cursor()

            cursor.execute(
                "SELECT id,name,password,role FROM users WHERE email=?",
                (email,)
            )

            user = cursor.fetchone()

        if user:

            user_id = user[0]
            name = user[1]
            hashed_password = user[2]
            role = user[3]

            if check_password(password, hashed_password):

                session["user_id"] = user_id
                session["name"] = name
                session["role"] = role

                return redirect("/")

        return render_template("login.html", error="Invalid email or password")

    return render_template("login.html")