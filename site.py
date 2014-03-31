#!/usr/bin/python

from flask import Flask, request, session, url_for, redirect, \
     render_template, abort, g, flash

from functools import wraps
import MySQLdb
from src import TableOperation

from src.base import base_page
from src.cart import cart_page
from src.borrow import borrow_page

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
        if TableOperation.sfw('Book', ['callNumber'],
                                    "callNumber = '%s'" %(callNum)):
            # Insert new copy
            bookCopyFields = TableOperation.getFieldNames('BookCopy')

            numCopies = int(TableOperation.sfw('BookCopy', ['callNumber', 'MAX(copyNo)'],
                                "callNumber = '%s'" % (callNum))[0][1]) + 1
            bCopy = (callNum, numCopies, 'in')
            TableOperation.insertTuple('BookCopy', bCopy)

            session['result'] = [[bookCopyFields, bCopy]]
        else:
            # Insert new Book and the first book copy
            bookFields = TableOperation.getFieldNames('Book')
            TableOperation.insertTuple('Book', tuple(row))

            subject = request.form[ 'subject' ].encode('utf-8')
            authors = request.form[ 'authors' ].encode('utf-8')
            subFields = []
            authFields = []

            if subject:
                subs = subject.split(',')
                for s in subs:
                    TableOperation.insertTuple('HasSubject', (callNum, s))

            if authors:
                auths = authors.split(',')
                for a in auths:
                    TableOperation.insertTuple('HasAuthor', (callNum, a))

            bookCopyFields = TableOperation.getFieldNames('BookCopy')
            bCopy = (callNum, 1, 'in')
            TableOperation.insertTuple('BookCopy', bCopy)

            session['result'] = [[bookFields, row], [bookCopyFields, bCopy]]

        return redirect(url_for('base_page.result', user=g.userInfo[0], accType=g.userInfo[8]))

    return render_template('addbook.html', error=error,
                            user=g.userInfo[0], accType=g.userInfo[8])

@app.route('/catalogue')
@app.route('/catalogue/<searchtype>/<keyword>')
def catalogue(searchtype=None,keyword=None):
    if searchtype and keyword:
        _searchtype = searchtype
        _keyword = keyword
    else:
        _searchtype = request.args.get( 'searchtype' )
        _keyword = request.args.get( 'keyword' )
    if _searchtype==None or _keyword==None:
        _searchtype = ""
        _keyword = ""
    else:
        _searchtype = _searchtype.encode('utf-8')
        _keyword = _keyword.encode('utf-8')
    fieldnames = TableOperation.getFieldNames('Book')
    if _searchtype == 'title':
        rows = TableOperation.sfw('Book', ['*'],"title LIKE '%%%s%%'" % _keyword)
    elif _searchtype == 'author':
        if(TableOperation.sfw("Book AS b INNER JOIN HasAuthor AS a ON (b.callNumber = a.callNumber)"
        ,["b.callNumber"],"a.name LIKE '%%%s%%' or b.mainAuthor LIKE '%%%s%%'" % (_keyword,_keyword))):
            rows = TableOperation.sfw("Book AS b INNER JOIN HasAuthor AS a ON (b.callNumber = a.callNumber)",["b.callNumber,b.isbn,b.title,b.mainAuthor,b.publisher,b.year"],"a.name LIKE '%%%s%%' or b.mainAuthor LIKE '%%%s%%'" % (_keyword,_keyword))
        else:
            rows = TableOperation.sfw("Book",["callNumber,isbn,title,mainAuthor,publisher,year"],"mainAuthor LIKE '%%%s%%'" % (_keyword))
    elif _searchtype == 'subject':
        rows = TableOperation.sfw("Book AS b INNER JOIN HasSubject AS a ON (b.callNumber = a.callNumber)",["*"],"a.subject LIKE '%%%s%%'" % (_keyword))
    else:
        rows = TableOperation.getColumns('Book', ['*'])
    session['catalogue'] = [rows]
    session['bquery'] = rows
    return render_template('catalogue.html', user=g.userInfo[0], accType=g.userInfo[8])

@app.route('/show')
def show():
    """ Displays the contents of table for debugging use """
    table = request.args.get('table')
    fieldNames = TableOperation.getFieldNames(table)
    rows = TableOperation.showTable(table)
    rows.insert(0, fieldNames)
    session['result'] = [rows]
    return render_template('result.html')

if __name__ == '__main__':
    app.run(debug=True)
