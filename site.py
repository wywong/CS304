from flask import Flask, render_template
from flask import request, Response, session, flash, redirect, url_for

from functools import wraps

class Account:
    def __init__(self, passwd, accType):
        self.passwd = passwd
        self.accType = accType


accs = {'clerk1':Account('word', 'clerk'),
        'clerk2':Account('1234', 'clerk'),
        'bor1':Account('1234', 'borrower'),
        'bor2':Account('1234', 'borrower'),
        'fac1':Account('1234', 'borrower'),
        'lib1':Account('1234', 'librarian')
        }

app = Flask(__name__)
app.secret_key = 'totally not safe'

@app.route("/")
def welcome():
    return render_template('welcome.html')

@app.route("/index")
@app.route("/index/<user>")
def index(user=None):
    if user in session:
        return render_template('index.html', user=user, accType=accs[user].accType)
    else:
        return render_template('index.html', user=user, accType=None)

@app.route('/login', methods=['POST', 'GET'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        passwd = request.form['password']
        if username not in accs:
            error = 'Invalid username'
        elif passwd != accs[username].passwd:
            error = 'Invalid password'
        else:
            session[ username ] = username
            flash('You were logged in')
            return redirect(url_for('index', user=username))
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
