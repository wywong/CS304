from flask import Flask, render_template
from flask import request, Response, session, flash, redirect, url_for

from functools import wraps

logins = {'clerk1':'word',
          'clerk2':'1234',
          'bor1':'1234',
          'bor2':'1234',
          'fac1':'bob',
          'lib1':'asdf'}

app = Flask(__name__)
app.secret_key = 'totally not safe'

@app.route("/")
def welcome():
    return render_template('welcome.html')

@app.route("/index")
def index(name=None):
    return render_template('index.html', name=name)

@app.route('/login', methods=['POST', 'GET'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        passwd = request.form['password']
        if username not in logins:
            error = 'Invalid username'
        elif passwd != logins[username]:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('index'))
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
