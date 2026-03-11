from flask import Flask, render_template
from app.models.user_model import create_user_table
from app.routes.auth_routes import register_user, login_user

app = Flask(__name__,
            template_folder='app/templates',
            static_folder='app/static')

app.config['SECRET_KEY'] = 'supersecurekey123'


@app.route('/')
def home():
    return render_template('dashboard.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    return login_user()


@app.route('/register', methods=['GET', 'POST'])
def register():
    return register_user()


if __name__ == '__main__':
    create_user_table()
    app.run(debug=True)
