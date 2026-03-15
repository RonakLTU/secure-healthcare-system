from flask import Flask, render_template
from flask_login import login_required, current_user
from app.models.user_model import create_user_table, create_default_admin
from app.routes.auth_routes import register_user, login_user, logout_user
from app.routes.patient_routes import add_patient, view_patients
from app.security.csrf_protection import csrf
from app.security.login_manager import login_manager

app = Flask(__name__,
            template_folder='app/templates',
            static_folder='app/static')

app.config['SECRET_KEY'] = 'supersecurekey123'

app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'

csrf.init_app(app)
login_manager.init_app(app)


@app.route('/')
@login_required
def home():
    return render_template('dashboard.html', role=current_user.role)


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


@app.route('/add_patient', methods=['GET', 'POST'])
@login_required
def add_patient_page():
    return add_patient()


@app.route('/patients')
@login_required
def patients_page():
    return view_patients()


if __name__ == '__main__':
    create_user_table()
    create_default_admin()
    app.run(debug=True)