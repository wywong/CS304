from flask import Flask, request, session, url_for, redirect, \
     render_template, abort, g, flash, Blueprint
from jinja2 import TemplateNotFound

import MySQLdb
import TableOperation

from datetime import date
import datetime

base_page = Blueprint('base_page', __name__)

# hard coded clerk and librarian accounts
accs = {
        'clerk1':['clerk1', '1234', 'evan', None, None, None, None, None, 'clerk'],
        'clerk2':['clerk2', '1234', 'shibo', None, None, None, None, None, 'clerk'],
        'lib1':['lib1', '1234', 'wilson', None, None, None, None, None, 'librarian']
        }


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
    session['message'] = ""
    if request.method == 'POST':
        u = request.form['username'].encode('utf-8')
        p = request.form['password'].encode('utf-8')
        queryData = TableOperation.sfw('Borrower', ['*'], "bid = '%s'" % (u))
        queryData = [[x if type(x) is not date else str(x) for x in y] for y in queryData]
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
            user=g.userInfo[0], accType=g.userInfo[8], message=session['message'])
