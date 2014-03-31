from flask import Flask, request, session, url_for, redirect, \
     render_template, abort, g, flash, Blueprint
from jinja2 import TemplateNotFound

import MySQLdb
import TableOperation, dbConn

from datetime import date
import datetime

borrower_page = Blueprint('borrower_page', __name__)

db = dbConn.dbConn()

@borrower_page.route('/addborrower', methods=['POST', 'GET'])
def addborrower():
    error = None
    if not g.userInfo:
        return redirect(url_for('.index', user=None, accType=None))
    elif g.userInfo[8] != 'clerk':
        return redirect(url_for('.index', user=g.userInfo[0], accType=g.userInfo[8]))

    if request.method == 'POST':
        passwd = request.form[ 'passwd' ].encode('utf-8')
        bName = request.form[ 'name' ].encode('utf-8')
        addr = request.form[ 'addr' ].encode('utf-8')
        phone = request.form[ 'phone' ].encode('utf-8')
        email = request.form[ 'email' ].encode('utf-8')
        sNum = request.form[ 'sNum' ].encode('utf-8')
        expiryDate = request.form[ 'expiryDate' ].encode('utf-8')
        bType = request.form[ 'bType' ].encode('utf-8')

        bid = TableOperation.selectFrom(db, 'Borrower', ['MAX(bid)'])[0][0]
        bid = '%08d' % (int(bid) + 1)
        row = [ bid, passwd, bName, addr, phone, email, sNum, expiryDate, bType ]

        borrowerFields = TableOperation.getFieldNames(db, 'Borrower')
        session['result'] = [[borrowerFields, row]]
        TableOperation.insertTuple(db, 'Borrower', tuple(row))
        return redirect(url_for('base_page.result', user=g.userInfo[0], accType=g.userInfo[8]))

    return render_template('addborrower.html', error=error,
                            user=g.userInfo[0], accType=g.userInfo[8])

@borrower_page.route('/renewborrower', methods=['POST', 'GET'])
def renewborrower():
    """ Get bid to determine which cart to display """
    if not g.userInfo:
        return redirect(url_for('base_page.index', user=None))
    error = None
    if request.method == 'POST':
        if g.userInfo[8] in ['clerk']:
            bid = request.form['bid'].encode('utf-8')
            match = TableOperation.sfw(db, 'Borrower', ['*'], "bid = '%s'" % (bid))
            if match:
                newDate = date.today() + datetime.timedelta(365)
                s = "expiryDate = '%s'" % (newDate.isoformat())
                conds = "bid = '%s'" % (bid)
                TableOperation.usw(db, 'Borrower', s, conds)
                rows = TableOperation.sfw(db, 'Borrower', ['*'], "bid = '%s'" % (bid))
                borrowerFields = TableOperation.getFieldNames(db, 'Borrower')
                rows.insert(0, borrowerFields)
                session['result'] = [rows]
                return render_template('result.html', error=error,
                                 user=g.userInfo[0], accType=g.userInfo[8])
            else:
                error = "Invalid bid"
                return render_template('renewborrower.html', error=error,
                                 user=g.userInfo[0], accType=g.userInfo[8])
        else:
            return redirect(url_for('base_page.index', user=g.userInfo[0],
                accType=g.userInfo[8], bid=g.userInfo[0]))

    return render_template('renewborrower.html', error=error,
                     user=g.userInfo[0], accType=g.userInfo[8])

@borrower_page.route('/myborrowed/')
def myborrowed():
    if not g.userInfo:
        return redirect(url_for('base_page.index', user=None, accType=None))
    if g.userInfo[8] not in ['student', 'faculty', 'staff']:
        return redirect(url_for('base_page.index', user=g.userInfo[0], accType=g.userInfo[8]))
    bid = g.userInfo[0]
    fieldNames = TableOperation.getFieldNames(db, 'Borrowing')
    rows = TableOperation.sfw(db, 'Borrowing', ['*'],
            "bid = '%s' AND inDate = '%s'" % (bid, '0000-00-00'))
    rows = [[x if type(x) is not date else str(x) for x in y] for y in rows]
    rows.insert(0, fieldNames)
    print rows
    session['result'] = [rows]
    return redirect(url_for('base_page.result', user=g.userInfo[0], accType=g.userInfo[8]))
