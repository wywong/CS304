#!/usr/bin/python

from flask import Flask, request, session, url_for, redirect, \
     render_template, abort, g, flash
from flask_mail import Mail
from flask.ext.mail import Message

from functools import wraps
import MySQLdb
from src import TableOperation

from src.base import base_page
from src.borrow import borrow_page
from src.cart import cart_page
from src.catalogue import catalogue_page
from src.fine import fine_page
from src.holds import holds_page
from src.reportcheckedout import report_checkedout_page
from src.reportoverdue import report_overdue_page
from src.reporttop import report_top_page

app = Flask(__name__)

mail = Mail(app)
app.config.update(
        DEBUG=True,
        #EMAIL SETTINGS
        MAIL_SERVER='smtp.gmail.com',
        MAIL_PORT=465,
        MAIL_USE_SSL=True,
        MAIL_USERNAME = 'cs304p3@gmail.com',
        MAIL_PASSWORD = '01189998819991197253'
        )
mail=Mail(app)

app.secret_key = 'totally not safe'
app.register_blueprint(base_page)
app.register_blueprint(borrow_page)
app.register_blueprint(cart_page)
app.register_blueprint(catalogue_page)
app.register_blueprint(fine_page)
app.register_blueprint(holds_page)
app.register_blueprint(report_checkedout_page)
app.register_blueprint(report_overdue_page)
app.register_blueprint(report_top_page)

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

            if subject:
                    TableOperation.insertTuple('HasSubject', (callNum, subject))
            else:
                    TableOperation.insertTuple('HasSubject', (callNum, ""))
            if authors:
                    TableOperation.insertTuple('HasAuthor', (callNum, authors))
            else:
                    TableOperation.insertTuple('HasAuthor', (callNum, ""))

            bookCopyFields = TableOperation.getFieldNames('BookCopy')
            bCopy = (callNum, 0, 'in')
            TableOperation.insertTuple('BookCopy', bCopy)

            session['result'] = [[bookFields, row], [bookCopyFields, bCopy]]

        return redirect(url_for('base_page.result', user=g.userInfo[0], accType=g.userInfo[8]))

    return render_template('addbook.html', error=error,
                            user=g.userInfo[0], accType=g.userInfo[8])
@app.route("/checkouthold")
def checkouthold():
    
    bookresult = TableOperation.sfw("Borrower as b INNER JOIN HoldRequest as h ON (h.bid = b.bid) INNER JOIN BookCopy AS bc ON (h.callNumber = bc.callNumber)",'h.hid','b.callNumber','bc.copyNum','b.bid'],"bc.status='on-hold'")
    _hid = bookresult[0][0]
    _callnum = bookresult[0][1]
    _copynum = bookresult[0][2]
    _bid = bookresult[0][3]
    
    TableOperation.insertTuple('Borrowing (bid,callNumber,copyNum,outDate,inDate),  VALUES (_bid,_callnum,_copynum,date.today().isoformat(),'0000-00-00')
    TableOperation.deleteTuple('HoldRequest','hid=%s' %_hid)
    
    return render_tempate('checkoutholds.html')
    
@app.route("/mailer")
def mailer():
    """ A simple mailer """
    # [ string subject, [strings of recipients] ]
    mailData = session.pop( 'email', None )
    if mailData:
        try:
            msg = Message(mailData[0],
                          sender="cs304p3@gmail.com",
                          recipients=mailData[1])
            mail.send(msg)
            message = "Message sent"
        except:
            message = "Invalid message data"
    else:
        message = "No mail data passed"
    session['result'] = []
    return redirect(url_for('base_page.result', user=g.userInfo[0], accType=g.userInfo[8],
        message=message))

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
