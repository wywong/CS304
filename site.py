#!/usr/bin/python

from flask import Flask, request, session, url_for, redirect, \
     render_template, abort, g, flash

from functools import wraps

import MySQLdb
from src import TableOperation, dbConn

# hard coded clerk and librarian accounts
accs = {
        'clerk1':['clerk1', '1234', 'evan', None, None, None, None, None, 'clerk'],
        'clerk2':['clerk2', '1234', 'shibo', None, None, None, None, None, 'clerk'],
        'lib1':['lib1', '1234', 'wilson', None, None, None, None, None, 'librarian']
        }

db = dbConn.dbConn()

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
        queryData = TableOperation.sfw(db, 'Borrower', ['*'], "bid = '%s'" % (u))
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
    g.userInfo = None
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
        bid = request.form[ 'bid' ].encode('utf-8')
        passwd = request.form[ 'passwd' ].encode('utf-8')
        bName = request.form[ 'name' ].encode('utf-8')
        addr = request.form[ 'addr' ].encode('utf-8')
        phone = request.form[ 'phone' ].encode('utf-8')
        email = request.form[ 'email' ].encode('utf-8')
        sNum = request.form[ 'sNum' ].encode('utf-8')
        expiryDate = request.form[ 'expiryDate' ].encode('utf-8')
        bType = request.form[ 'bType' ].encode('utf-8')

        row = (bid, passwd, bName, addr, phone, email, sNum, expiryDate, bType)

        borrowerFields = TableOperation.getFieldNames(db, 'Borrower')
        session['result'] = [[borrowerFields, row]]
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
        return redirect(url_for('index', user=g.userInfo[8], accType=g.userInfo[8]))

    if request.method == 'POST':
        callNum = request.form[ 'callNum' ].encode('utf-8')
        isbn = request.form[ 'isbn' ].encode('utf-8')
        title = request.form[ 'title' ].encode('utf-8')
        mainAuthor = request.form[ 'mainAuthor' ].encode('utf-8')
        publisher = request.form[ 'publisher' ].encode('utf-8')
        year = request.form[ 'year' ].encode('utf-8')

        row = (callNum, isbn, title, mainAuthor, publisher, year)

        # Check if book already exists
        if TableOperation.sfw(db, 'Book', ['callNumber'],
                                    "callNumber = '%s'" %(callNum)):
            # Insert new copy
            bookCopyFields = TableOperation.getFieldNames(db, 'BookCopy')

            numCopies = int(TableOperation.sfw(db, 'BookCopy', ['callNumber', 'MAX(copyNo)'],
                                "callNumber = '%s'" % (callNum))[0][1]) + 1
            bCopy = (callNum, numCopies, 'in')
            TableOperation.insertTuple(db, 'BookCopy', bCopy)

            session['result'] = [[bookCopyFields, bCopy]]
        else:
            # Insert new Book and the first book copy
            bookFields = TableOperation.getFieldNames(db, 'Book')
            TableOperation.insertTuple(db, 'Book', tuple(row))

            bookCopyFields = TableOperation.getFieldNames(db, 'BookCopy')
            bCopy = (callNum, 1, 'in')
            TableOperation.insertTuple(db, 'BookCopy', bCopy)

            session['result'] = [[bookFields, row], [bookCopyFields, bCopy]]


        return redirect(url_for('result', user=g.userInfo[0], accType=g.userInfo[8]))

    return render_template('addbook.html', error=error,
                            user=g.userInfo[0], accType=g.userInfo[8])

@app.route('/myborrowed')
def myborrowed():
    return redirect(url_for('result', user=g.userInfo[0], accType=g.userInfo[8]))

@app.route('/catalogue')
def catalogue():
    """ Displays search results, and allows users to check out books """
    fieldnames = TableOperation.getFieldNames(db,'Book')
    rows = TableOperation.getColumns(db, 'Book', ['*'])
    session['catalogue'] = [rows]
    session['catquery'] = rows
    return render_template('catalogue.html', user=g.userInfo[0], accType=g.userInfo[8])

@app.route('/viewcart')
@app.route('/viewcart/<bid>')
def viewcart(bid=None):
    """ Displays logged in borrowers cart or specified borrowers cart"""
    if bid:
        _bid = bid
    else:
        _bid = g.userInfo[0]
    fieldNames = TableOperation.getFieldNames(db,'Book')
    rows = TableOperation.sfw(db, 'Book', ['*'],
            "callNumber IN (SELECT callNumber FROM Cart WHERE bid = '%s')" % (_bid))
    session['cart'] = [rows]
    return render_template('cart.html', user=g.userInfo[0], accType=g.userInfo[8])

@app.route('/addtocart', methods=['POST', 'GET'])
def addtocart():
    if not g.userInfo:
        return redirect(url_for('index', user=None))
    if request.method == 'POST':
        selected = request.form.keys()
        selectable = session['catquery']

        rows = [selectable[int(s)] for s in selected]
        for r in rows:
            TableOperation.insertTuple(db, 'Cart', (g.userInfo[0], r[0]))

    return redirect(url_for('viewcart', user=g.userInfo[0], accType=g.userInfo[8]))

@app.route('/cartaction', methods=['POST', 'GET'])
def cartaction():
    """ Perform cartaction"""
    if not g.userInfo:
        return redirect(url_for('index', user=None))
    error = None
    if request.method == 'POST':
        if g.userInfo[8] in ['clerk']:
            bid = request.form['bid'].encode('utf-8')
            if TableOperation.sfw(db, 'Borrower', ['*'], "bid = '%s'" % (bid)):
                return redirect("viewcart/%s" %(bid))
            else:
                error = "Invalid bid"

    return render_template('cartaction.html', error=error,
                     user=g.userInfo[0], accType=g.userInfo[8])

@app.route('/removefromcart', methods=['POST', 'GET'])
def removefromcart():
    if not g.userInfo:
        return redirect(url_for('index', user=None))
    if request.method == 'POST':
        if bid:
            _bid = bid
        else:
            _bid = g.userInfo[0]
        selected = request.form.keys()
        selectable = session['catquery']

        remove = [selectable[int(s)] for s in selected]
        for r in rows:
            TableOperation.deleteTuple(db, 'Cart',
                    "bid = '%s' AND callNumber = '%s'" %(bid, r[0]))

    return redirect(url_for('viewcart', user=g.userInfo[0], accType=g.userInfo[8]))

@app.route('/show')
def show():
    """ Displays the contents of table for debugging use """
    table = request.args.get('table')
    fieldNames = TableOperation.getFieldNames(db, table)
    rows = TableOperation.showTable(db, table)
    rows.insert(0, fieldNames)
    session['result'] = [rows]
    return render_template('result.html')

if __name__ == '__main__':
    app.run(debug=True)
