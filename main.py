import os

from flask import Flask, render_template, request, redirect, url_for, session, flash, json
from werkzeug.security import generate_password_hash, check_password_hash
import atexit

from backend.search import create_query

app = Flask(__name__)

# Dummy user data for demonstration purposes
users = {
}
app.secret_key = "dfjsklajfks;flafj"

def database_write():
    with open('users.json','w') as f:
        json.dump(users,f)

def database_read():
    if not os.path.exists('users.json'):
        with open('users.json', 'w') as f:
            json.dump({}, f)
    f = open('users.json','r')
    global users
    users = json.load(f)

@app.route('/')
def home():
    return render_template('index.html')
@app.route('/index', methods=['GET','POST'])
def index():
    if request.method == 'POST':
        if 'Login' in request.form:
            return redirect(url_for('login'))
        if 'Cut' in request.form:
            pass
        if 'Burn' in request.form:
            pass
        if 'Scrape' in request.form:
            pass
    return render_template('index.html')
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        if email in users and check_password_hash(users[email], password):
            session['user'] = email
            flash('Login successful!', 'success')
            return redirect(url_for('welcome'))
        else:
            flash('Invalid email or password.', 'danger')

    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        if email in users and check_password_hash(users[email], password):
            flash('User already exists!', 'danger')
        else:
            users['email'] = generate_password_hash(password)
            session['user'] = email
            flash('Account creation successful!', 'success')
            return redirect(url_for('welcome'))


    return render_template('signup.html')

@app.route('/welcome')
def welcome():
    if 'user' not in session:
        return redirect(url_for('home'))

    return render_template('welcome.html', user=session['user'])


@app.route('/chat', methods=['GET','POST'])
def chat():
    if request.method == 'POST':
        msg = request.form["msg"]
        response = create_query(msg)
        return render_template("chat.html", response=response)
    return render_template("chat.html", response="Sorry, an error occurred! Can you try again?")

@app.route('/logout')
def logout():
    session.pop('user', None)
    flash('Logged out successfully!', 'info')
    return redirect(url_for('home'))


def exit_handler():
    database_write()


if __name__ == '__main__':
    database_read()
    print(users)
    app.run(debug=True)
    atexit.register(exit_handler)
