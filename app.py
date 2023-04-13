from flask import Flask, url_for
from flask.templating import render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/add_new_emp')
def add_new_emp():
    return render_template('addNewEmp.html')

@app.route('/update_emp')
def update_emp():
    return render_template('updateEmp.html')

if __name__ == '__main__':
    app.run(debug=True)