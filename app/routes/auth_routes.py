from flask import request, render_template, redirect
import sqlite3
import re

from app.security.password_utils import hash_password, check_password
from flask_login import login_user as flask_login_user
from flask_login import logout_user as flask_logout

from app.models.auth_user import User

DATABASE = "database/auth.db"


# ==============================
# REGISTER PATIENT
# ==============================

def register_user():

    if request.method == "POST":

        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")

        role = "patient"

        email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'

        if not re.match(email_pattern, email):
            return render_template(
                "register.html",
                error="Invalid email format"
            )

        if len(password) < 8:
            return render_template(
                "register.html",
                error="Password must be at least 8 characters"
            )

        hashed_password = hash_password(password)

        try:

            with sqlite3.connect(DATABASE) as conn:

                cursor = conn.cursor()

                cursor.execute(
                    """
                    INSERT INTO users (name,email,password,role)
                    VALUES (?,?,?,?)
                    """,
                    (name, email, hashed_password, role)
                )

                conn.commit()

        except sqlite3.IntegrityError:

            return render_template(
                "register.html",
                error="Email already exists"
            )

        return redirect("/login")

    return render_template("register.html")


# ==============================
# LOGIN USER
# ==============================

def login_user():

    if request.method == "POST":

        email = request.form.get("email")
        password = request.form.get("password")

        with sqlite3.connect(DATABASE) as conn:

            cursor = conn.cursor()

            cursor.execute(
                """
                SELECT id,name,email,password,role
                FROM users
                WHERE email=?
                """,
                (email,)
            )

            user = cursor.fetchone()

        if user:

            user_id, name, email, hashed_password, role = user

            if check_password(password, hashed_password):

                user_obj = User(user_id, name, email, role)

                flask_login_user(user_obj)

                # ROLE BASED REDIRECT

                if role == "patient":
                    return redirect("/patient_dashboard")

                elif role == "clinician":
                    return redirect("/clinician_dashboard")

                elif role == "admin":
                    return redirect("/admin_dashboard")

        return render_template(
            "login.html",
            error="Invalid email or password"
        )

    return render_template("login.html")


# ==============================
# LOGOUT
# ==============================

def logout_user():

    flask_logout()

    return redirect("/login")
