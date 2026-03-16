from flask import Flask, render_template
from flask_login import login_required, current_user

from app.models.user_model import create_user_table, create_default_admin
from app.routes.auth_routes import register_user, login_user, logout_user
from app.routes.patient_routes import add_patient, view_patients
from app.security.csrf_protection import csrf
from app.security.login_manager import login_manager
from app.models.patient_model import patients_collection

app = Flask(__name__,
            template_folder='app/templates',
            static_folder='app/static')

app.config['SECRET_KEY'] = 'supersecurekey123'

app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'

csrf.init_app(app)
login_manager.init_app(app)


# LANDING PAGE

@app.route('/')
def home():
    return render_template('landing.html')


# AUTH ROUTES

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


# PATIENT MANAGEMENT (Clinician)

@app.route('/add_patient', methods=['GET', 'POST'])
@login_required
def add_patient_page():
    return add_patient()


@app.route('/patients')
@login_required
def patients_page():
    return view_patients()


# PATIENT DASHBOARD

@app.route('/patient_dashboard')
@login_required
def patient_dashboard():
    return render_template('patient/patient_dashboard.html')


# PATIENT RECORD VIEW

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

@app.route('/clinician_dashboard')
@login_required
def clinician_dashboard():

    if current_user.role != "clinician":
        return redirect("/")

    return render_template("clinician/clinician_dashboard.html")


if __name__ == '__main__':
    create_user_table()
    create_default_admin()
    app.run(debug=True)
