from flask import Flask, render_template, request, redirect, url_for, session, flash, json
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a random secret key

# Dummy user data for demonstration purposes
users = {
}

def database_write():
    with open('users.json','w') as f:
        json.dump(users,f)

def database_read():
    f = open('users.json','r')
    global users
    users = json.load(f)

@app.route('/')
def home():
    return render_template('login.html')

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


@app.route('/welcome')
def welcome():
    if 'user' not in session:
        return redirect(url_for('home'))

    return render_template('welcome.html', user=session['user'])


@app.route('/logout')
def logout():
    session.pop('user', None)
    flash('Logged out successfully!', 'info')
    return redirect(url_for('home'))


if __name__ == '__main__':
    database_read()
    print(users)
    app.run(debug=True)