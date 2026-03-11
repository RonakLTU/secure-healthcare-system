from flask import Flask, render_template

app = Flask(__name__,
            template_folder='app/templates',
            static_folder='app/static')

# Secret key for sessions
app.config['SECRET_KEY'] = 'supersecurekey123'


@app.route('/')
def home():
    return render_template('dashboard.html')


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/register')
def register():
    return render_template('register.html')


if __name__ == '__main__':
    app.run(debug=True)