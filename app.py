from flask import Flask, redirect, request, url_for
from flask.templating import render_template
from werkzeug.security import generate_password_hash, check_password_hash
from database import get_database

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/login', methods=['POST','GET'])
def login():
    error = None
    if request.method == 'POST':
        name = request.form['name']
        password = request.form['password']
        db = get_database()
        user_cursor = db.execute('select * from users where name = ?', [name])
        user = user_cursor.fetchone()

        if user:
            if check_password_hash(user['password'], password):
                return redirect(url_for('dashboard'))
            else:
                error = "Password did not match"                
    return render_template('login.html', login_error = error)

@app.route('/register', methods=['POST','GET'])
def register():
    if request.method == 'POST':
        db = get_database()
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

@app.route('/single_emp_profile')
def single_emp_profile():
    return render_template('singleEmpProfile.html')

def logout():
    return render_template('home.html')

if __name__ == '__main__':
    app.run(debug=True)