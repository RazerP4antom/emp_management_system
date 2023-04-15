import os
import sqlite3
from flask import Flask, g, redirect, request, session, url_for
from flask.templating import render_template
from werkzeug.security import generate_password_hash, check_password_hash
from database import get_database

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)

def get_current_user():
    user = None
    if 'user' in session:
        user = session['user']
        db = get_database()
        user_cur = db.execute('select * from users where name = ?', [user])
        user = user_cur.fetchone()
    return user

@app.teardown_appcontext
def close_database(error):
    if hasattr(g, 'crudapp_db'):
        g.crudapp_db.close()


@app.route('/')
def index():
    user = get_current_user()
    return render_template('home.html', user = user)

@app.route('/login', methods=['POST','GET'])
def login():
    user = get_current_user()
    error = None
    db = get_database()
    if request.method == 'POST':
        name = request.form['name']
        password = request.form['password']
        user_cursor = db.execute('select * from users where name = ?', [name])
        user = user_cursor.fetchone()
        if user:
            if check_password_hash(user['password'], password):
                session['user'] = user['name']
                return redirect(url_for('dashboard'))
            else:
                error = "Username or Password did not match"     
        else:
            error = "Username not found"
    return render_template('login.html', login_error = error, user = user)

@app.route('/register', methods=['POST','GET'])
def register():
    user = get_current_user()
    db = get_database()
    if request.method == 'POST':
        name = request.form['name']
        password = request.form['password']
        hashed_password = generate_password_hash(password)
        db_user_cursor = db.execute('select * from users where name = ?',[name])
        existing_user = db_user_cursor.fetchone()
        if existing_user:
            return render_template('register.html', register_error = 'Username already taken')
        db.execute('insert into users (name, password) values (?, ?)',[name, hashed_password])
        db.commit()
        return redirect(url_for('index'))
    return render_template('register.html', user = user)

@app.route('/dashboard')
def dashboard():
    user = get_current_user()
    return render_template('dashboard.html',user = user)

@app.route('/add_new_emp')
def add_new_emp():
    user = get_current_user()
    return render_template('addNewEmp.html', user = user)

@app.route('/update_emp')
def update_emp():
    user = get_current_user()
    return render_template('updateEmp.html', user = user)

@app.route('/single_emp_profile')
def single_emp_profile():
    user = get_current_user()
    return render_template('singleEmpProfile.html', user = user)

@app.route('/logout')
def logout():
    session.pop('user',None)
    return render_template('home.html')

if __name__ == '__main__':
    app.run(debug=True)