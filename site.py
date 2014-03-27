#!/usr/bin/python

from flask import Flask, render_template
from flask import request, Response, session, flash, redirect, url_for

from functools import wraps

import MySQLdb
from src import TableOperation

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

try:
    db = MySQLdb.connect(host="localhost",
                        user="testuser",
                        passwd="01189998819991197253",
                        db="cs304")
except:
    print "Error %d: %s" % (e.args[0], e.args[1])

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

@app.route('/addborrower', methods=['POST', 'GET'])
def addborrower():
    error = None
    if request.method == 'POST':
        bid = request.form[ 'bid' ]
        passwd = request.form[ 'passwd' ]
        bName = request.form[ 'name' ]
        addr = request.form[ 'addr' ]
        phone = request.form[ 'phone' ]
        email = request.form[ 'email' ]
        sNum = request.form[ 'sNum' ]
        expiryDate = request.form[ 'expiryDate' ]
        bType = request.form[ 'bType' ]

        row = (bid, passwd, bName, addr, phone, email, sNum, expiryDate, bType)

        row = [element.encode('utf-8') for element in row]

        TableOperation.insertTuple(db, 'Borrower', tuple(row))
        return redirect(url_for('index', user=None))

    return render_template('addborrower.html', error=error)

if __name__ == '__main__':
    app.run(debug=True)
