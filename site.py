#!/usr/bin/python

from flask import Flask, request, session, url_for, redirect, \
     render_template, abort, g, flash

from functools import wraps

import MySQLdb
from src import TableOperation

# hard coded clerk and librarian accounts
accs = {
        'clerk1':['clerk1', 'word', 'stan', None, None, None, None, None, 'clerk'],
        'clerk2':['clerk2', '1234', 'steve', None, None, None, None, None, 'clerk'],
        'lib1':['lib1', '1234', 'mel', None, None, None, None, None, 'librarian']
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

@app.before_request
def before_request():
    g.userInfo = None
    if 'user_id' in session:
        g.userInfo = session['user_id']

@app.route("/")
def index():
    if not g.userInfo:
        return render_template('index.html', user=None, accType=None)
    else:
        return render_template('index.html', user=g.userInfo[0], accType=g.userInfo[8])

@app.route('/login', methods=['POST', 'GET'])
def login():
    """Logs the user in."""
    if g.userInfo:
        return redirect(url_for('index', user=g.userInfo))
    error = None
    cur = db.cursor()
    if request.method == 'POST':
        u = request.form['username'].encode('utf-8')
        p = request.form['password'].encode('utf-8')
        sql = "SELECT * FROM Borrower WHERE bid = '%s'" % (u)
        cur.execute(sql)
        queryData = cur.fetchall()
        if queryData:
            row = queryData[0]
            user = row[0]
            pw = row[1]
        else:
            if u in accs:
                user = u
                pw = accs[user][1]
            else:
                user = None
                pw = None
        if user is None:
            error = 'Invalid username'
        elif not pw == p:
            error = 'Invalid password'
        else:
            flash('You were logged in')
            session['user_id'] = row if queryData else accs[u]
            print session['user_id']
            return redirect(url_for('index', user=user))
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('user_id', None)
    if g.userInfo:
        return redirect(url_for('index'))

@app.route('/result')
def result():
    """ Return the result of an insert """
    return render_template('result.html',
            user=g.userInfo[0], accType=g.userInfo[8])


@app.route('/addborrower', methods=['POST', 'GET'])
def addborrower():
    error = None
    if not g.userInfo:
        return redirect(url_for('index', user=None, accType=None))
    elif g.userInfo[8] != 'clerk':
        return redirect(url_for('index', user=g.userInfo[0], accType=g.userInfo[8]))

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
        print row

        fieldNames = TableOperation.getFieldNames(db, 'Borrower')
        session['result'] = [fieldNames, row]
        TableOperation.insertTuple(db, 'Borrower', tuple(row))
        return redirect(url_for('result', user=g.userInfo[0], accType=g.userInfo[8]))

    return render_template('addborrower.html', error=error,
                            user=g.userInfo[0], accType=g.userInfo[8])

@app.route('/addbook', methods=['POST', 'GET'])
def addbook():
    error = None
    if not g.userInfo:
        return redirect(url_for('index', user=None))
    elif g.userInfo[8] != 'librarian':
        return redirect(url_for('index', user=g.userInfo[8]))

    if request.method == 'POST':
        callNum = request.form[ 'callNum' ]
        isbn = request.form[ 'isbn' ]
        title = request.form[ 'title' ]
        mainAuthor = request.form[ 'mainAuthor' ]
        publisher = request.form[ 'publisher' ]
        year = request.form[ 'year' ]

        row = (callNum, isbn, title, mainAuthor, publisher, year)

        row = [element.encode('utf-8') for element in row]

        TableOperation.insertTuple(db, 'Book', tuple(row))
        TableOperation.insertTuple(db, 'BookCopy (callNumber, status)',
                (callNum.encode('utf-8'), 'in'))
        return redirect(url_for('index', user=None))

    return render_template('addbook.html', error=error,
                            user=g.userInfo[0], accType=g.userInfo[8])

if __name__ == '__main__':
    app.run(debug=True)
