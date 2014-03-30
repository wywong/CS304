from flask import Flask, request, session, url_for, redirect, \
     render_template, abort, g, flash, Blueprint
from jinja2 import TemplateNotFound

import MySQLdb
import TableOperation, dbConn

base_page = Blueprint('base_page', __name__)

# hard coded clerk and librarian accounts
accs = {
        'clerk1':['clerk1', '1234', 'evan', None, None, None, None, None, 'clerk'],
        'clerk2':['clerk2', '1234', 'shibo', None, None, None, None, None, 'clerk'],
        'lib1':['lib1', '1234', 'wilson', None, None, None, None, None, 'librarian']
        }

db = dbConn.dbConn()

@base_page.route("/")
def index():
    if not g.userInfo:
        return render_template('index.html', user=None, accType=None)
    else:
        return render_template('index.html', user=g.userInfo[0], accType=g.userInfo[8])

@base_page.route('/login', methods=['POST', 'GET'])
def login():
    """Logs the user in."""
    if g.userInfo:
        return redirect(url_for('index', user=g.userInfo))
    error = None
    if request.method == 'POST':
        u = request.form['username'].encode('utf-8')
        p = request.form['password'].encode('utf-8')
        cur = db.cursor()
        queryData = TableOperation.sfw(db, 'Borrower', ['*'], "bid = '%s'" % (u))
        cur.close()
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
            return redirect(url_for('.index', user=user))
    return render_template('login.html', error=error)

@base_page.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('user_id', None)
    g.userInfo = None
    return redirect(url_for('.index'))

@base_page.route('/result')
def result():
    """ Return the result of an insert """
    return render_template('result.html',
            user=g.userInfo[0], accType=g.userInfo[8])

@base_page.route('/addborrower', methods=['POST', 'GET'])
def addborrower():
    error = None
    if not g.userInfo:
        return redirect(url_for('.index', user=None, accType=None))
    elif g.userInfo[8] != 'clerk':
        return redirect(url_for('.index', user=g.userInfo[0], accType=g.userInfo[8]))

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
        return redirect(url_for('base_page.result', user=g.userInfo[0], accType=g.userInfo[8]))

    return render_template('addborrower.html', error=error,
                            user=g.userInfo[0], accType=g.userInfo[8])

