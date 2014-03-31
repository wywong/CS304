#!/usr/bin/python

from flask import Flask, request, session, url_for, redirect, \
     render_template, abort, g, flash

from functools import wraps

import MySQLdb
from src import TableOperation, dbConn

from src.base import base_page
from src.cart import cart_page
from src.borrow import borrow_page

db = dbConn.dbConn()

app = Flask(__name__)
app.secret_key = 'totally not safe'
app.register_blueprint(base_page)
app.register_blueprint(cart_page)
app.register_blueprint(borrow_page)

@app.before_request
def before_request():
    g.userInfo = None
    if 'user_id' in session:
        g.userInfo = session['user_id']

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

        return redirect(url_for('base_page.result', user=g.userInfo[0], accType=g.userInfo[8]))

    return render_template('addbook.html', error=error,
                            user=g.userInfo[0], accType=g.userInfo[8])

@app.route('/catalogue')
def catalogue():
    """ Displays search results, and allows users to check out books """
    fieldnames = TableOperation.getFieldNames(db,'Book')
    rows = TableOperation.getColumns(db, 'Book', ['*'])
    session['catalogue'] = [rows]
    session['bquery'] = rows
    return render_template('catalogue.html', user=g.userInfo[0], accType=g.userInfo[8])

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
