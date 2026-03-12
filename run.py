from flask import Flask, render_template, session
from app.models.user_model import create_user_table, create_default_admin
from app.routes.auth_routes import register_user, login_user, logout_user
from app.routes.patient_routes import add_patient, view_patients
from app.security.csrf_protection import csrf

app = Flask(__name__,
            template_folder='app/templates',
            static_folder='app/static')

app.config['SECRET_KEY'] = 'supersecurekey123'

# Secure session settings
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SECURE'] = False
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'

csrf.init_app(app)


@app.route('/')
def home():
    return render_template('dashboard.html', role=session.get("role"))


@app.route('/login', methods=['GET', 'POST'])
def login():
    return login_user()


@app.route('/logout')
def logout():
    return logout_user()


@app.route('/register', methods=['GET', 'POST'])
def register():
    return register_user()


@app.route('/add_patient', methods=['GET', 'POST'])
def add_patient_page():
    return add_patient()


@app.route('/patients')
def patients_page():
    return view_patients()


if __name__ == '__main__':
    create_user_table()
    create_default_admin()
    app.run(debug=True)