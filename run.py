from flask import Flask, render_template, redirect, request
from flask_login import login_required, current_user
import sqlite3

from app.models.user_model import create_user_table, create_default_admin
from app.routes.auth_routes import register_user, login_user, logout_user
from app.routes.patient_routes import add_patient, view_patients
from app.security.csrf_protection import csrf
from app.security.login_manager import login_manager
from app.models.patient_model import patients_collection
from app.security.password_utils import hash_password

DATABASE = "database/auth.db"

app = Flask(__name__,
            template_folder='app/templates',
            static_folder='app/static')

app.config['SECRET_KEY'] = 'supersecurekey123'

app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'

csrf.init_app(app)
login_manager.init_app(app)


# ======================
# LANDING PAGE
# ======================

@app.route('/')
def home():
    return render_template('landing.html')


# ======================
# AUTH ROUTES
# ======================

@app.route('/login', methods=['GET', 'POST'])
def login():
    return login_user()


@app.route('/logout')
@login_required
def logout():
    return logout_user()


@app.route('/register', methods=['GET', 'POST'])
def register():
    return register_user()


# ======================
# PATIENT DASHBOARD
# ======================

@app.route('/patient_dashboard')
@login_required
def patient_dashboard():
    return render_template('patient/patient_dashboard.html')


@app.route('/my_record')
@login_required
def my_record():

    record = patients_collection.find_one({
        "patient_email": current_user.email
    })

    return render_template(
        "patient/my_record.html",
        record=record
    )


# ======================
# CLINICIAN ROUTES
# ======================

@app.route('/clinician_dashboard')
@login_required
def clinician_dashboard():

    if current_user.role != "clinician":
        return redirect("/")

    return render_template("clinician/clinician_dashboard.html")


@app.route('/add_patient', methods=['GET', 'POST'])
@login_required
def add_patient_page():
    return add_patient()


@app.route('/patients')
@login_required
def patients_page():
    return view_patients()


# ======================
# ADMIN DASHBOARD
# ======================

@app.route('/admin_dashboard')
@login_required
def admin_dashboard():

    if current_user.role != "admin":
        return redirect("/")
    
    msg = request.args.get("msg")

    return render_template("admin/admin_dashboard.html", msg=msg)


# ======================
# CREATE CLINICIAN
# ======================

@app.route('/create_clinician', methods=['GET', 'POST'])
@login_required
def create_clinician():

    if current_user.role != "admin":
        return redirect("/")

    error = None
    success = None

    if request.method == "POST":

        clinician_id = request.form.get("clinician_id")
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")

        import re

        email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        password_pattern = r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@$!%*?&]).{8,16}$'

        if not re.match(email_pattern, email):
            error = "Invalid email format"
            return render_template("admin/create_clinician.html", error=error)

        if not re.match(password_pattern, password):
            error = "Password must be 8–16 chars with uppercase, lowercase, number & symbol"
            return render_template("admin/create_clinician.html", error=error)

        if not clinician_id.isdigit():
            error = "Clinician ID must be numeric"
            return render_template("admin/create_clinician.html", error=error)

        hashed_password = hash_password(password)

        try:

            with sqlite3.connect(DATABASE) as conn:

                cursor = conn.cursor()

                cursor.execute(
                    """
                    INSERT INTO users (clinician_id,name,email,password,role)
                    VALUES (?,?,?,?,?)
                    """,
                    (clinician_id, name, email, hashed_password, "clinician")
                )

                conn.commit()

                return redirect("/admin_dashboard?msg=created")
            

                

        except sqlite3.IntegrityError:

            error = "Email or Clinician ID already exists"

    return render_template(
        "admin/create_clinician.html",
        error=error,
        success=success
    )

# ======================
# MANAGE USERS
# ======================

@app.route('/manage_users')
@login_required
def manage_users():

    if current_user.role != "admin":
        return redirect("/")

    with sqlite3.connect(DATABASE) as conn:

        cursor = conn.cursor()

        cursor.execute("""
        SELECT id, clinician_id, name, email, role
        FROM users WHERE role='clinician'
        """)

        users = cursor.fetchall()

    user_list = []

    for u in users:

        user_list.append({
            "id": u[0],
            "clinician_id": u[1],
            "name": u[2],
            "email": u[3],
            "role": u[4]
        })

    return render_template(
        "admin/manage_users.html",
        users=user_list
    )

#Patient_Users
@app.route('/patient_users')
@login_required
def patient_users():

    if current_user.role != "admin":
        return redirect("/")

    with sqlite3.connect(DATABASE) as conn:

        cursor = conn.cursor()

        cursor.execute("""
        SELECT id,name,email FROM users WHERE role='patient'
        """)

        users = cursor.fetchall()

    user_list = []

    for u in users:
        user_list.append({
            "id": u[0],
            "name": u[1],
            "email": u[2]
        })

    return render_template("admin/patient_users.html", users=user_list)

# ======================
# DELETE USER
# ======================

@app.route('/delete_user/<int:user_id>')
@login_required
def delete_user(user_id):

    if current_user.role != "admin":
        return redirect("/")

    with sqlite3.connect(DATABASE) as conn:

        cursor = conn.cursor()

        cursor.execute(
            "DELETE FROM users WHERE id=?",
            (user_id,)
        )

        conn.commit()

    return redirect("/manage_users")


# ======================
# START APP
# ======================

if __name__ == '__main__':

    create_user_table()
    create_default_admin()

    app.run(debug=True)
