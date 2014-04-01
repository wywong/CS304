from flask import Flask, request, session, url_for, redirect, \
     render_template, abort, g, flash, Blueprint
from jinja2 import TemplateNotFound

import MySQLdb
import TableOperation

from datetime import date
import datetime

borrow_page = Blueprint('borrow_page', __name__)

@borrow_page.route('/addborrower', methods=['POST', 'GET'])
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

        bid = TableOperation.selectFrom('Borrower', ['MAX(bid)'])[0][0]
        bid = '%08d' % (int(bid) + 1)
        row = [ bid, passwd, bName, addr, phone, email, sNum, expiryDate, bType ]

        borrowerFields = TableOperation.getFieldNames('Borrower')
        session['result'] = [[borrowerFields, row]]
        TableOperation.insertTuple('Borrower', tuple(row))
        return redirect(url_for('base_page.result', user=g.userInfo[0], accType=g.userInfo[8],
                message='Added Borrower'))

    return render_template('addborrower.html', error=error,
                            user=g.userInfo[0], accType=g.userInfo[8])

@borrow_page.route('/renewborrower', methods=['POST', 'GET'])
def renewborrower():
    """ Get bid to determine which cart to display """
    if not g.userInfo:
        return redirect(url_for('base_page.index', user=None))
    error = None
    if request.method == 'POST':
        if g.userInfo[8] in ['clerk']:
            bid = request.form['bid'].encode('utf-8')
            match = TableOperation.sfw('Borrower', ['*'], "bid = '%s'" % (bid))
            if match:
                newDate = date.today() + datetime.timedelta(365)
                s = "expiryDate = '%s'" % (newDate.isoformat())
                conds = "bid = '%s'" % (bid)
                TableOperation.usw('Borrower', s, conds)
                rows = TableOperation.sfw('Borrower', ['*'], "bid = '%s'" % (bid))
                borrowerFields = TableOperation.getFieldNames('Borrower')
                rows.insert(0, borrowerFields)
                session['result'] = [rows]
                return render_template('result.html', error=error, message="Renewed",
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

@borrow_page.route('/borrowed')
@borrow_page.route('/borrowed/<bid>')
def borrowed(bid=None):
    if not g.userInfo:
        return redirect(url_for('base_page.index', user=None, accType=None))
    if g.userInfo[8] not in ['student', 'faculty', 'staff', 'clerk']:
        return redirect(url_for('base_page.index', user=g.userInfo[0], accType=g.userInfo[8]))
    if not bid:
        bid = g.userInfo[0]
    fieldNames = TableOperation.getFieldNames('Borrowing')
    rows = TableOperation.sfw('Borrowing', ['*'],
            "bid = '%s' AND inDate = '%s'" % (bid, '0000-00-00'))
    rows = [[x if type(x) is not date else str(x) for x in y] for y in rows]
    print rows
    if g.userInfo[8] in ['clerk']:
        session['borrowed'] = [rows]
        session['bquery'] = rows
        session['bid'] = bid
        return render_template('returnbook.html', user=g.userInfo[0], accType=g.userInfo[8],
                message=session.pop('message', None))
    else:
        rows.insert(0, fieldNames)
        session['result'] = [rows]
        return redirect(url_for('base_page.result', user=g.userInfo[0], accType=g.userInfo[8]))

@borrow_page.route('/returnbook', methods=['POST', 'GET'])
def returnbook():
    if not g.userInfo:
        return redirect(url_for('base_page.index', user=None))
    if request.method == 'POST':
        selected = [session['bquery'][int(s)] for s in request.form.keys()]
        intersection = [x for x in session['bquery'] if x in selected]
        copies = TableOperation.sfw("""Borrowing B INNER JOIN BookCopy C
            ON B.callNumber=C.callNumber AND B.copyNo=C.copyNo""",
            ['B.callNumber', 'B.copyNo'],
            "bid='%s' AND inDate='0000-00-00'" % (session['bid']))
        callNums = [x[2] for x in intersection]
        copyUpdate = [x for x in copies if x[0] in callNums]
        copyRows = copyUpdate[:]
        if intersection:
            bid = intersection[0][1]
            timeLimit = TableOperation.sfw("""Borrower INNER JOIN BorrowerType
                                    ON Borrower.type=BorrowerType.type""",
                                    ['bookTimeLimit'], "bid = '%s'" % (bid))[0][0] * 7
        fines = []
        mails = []
        for r in intersection:
            settings = "inDate = '%s'" % (date.today().isoformat())
            _borid = r[0]
            conds = "borid = '%s'" % _borid
            TableOperation.usw('Borrowing', settings, conds)
            ymd = r[4].split('-')
            ymd = [int(x) for x in ymd]
            dueDate = datetime.date(ymd[0], ymd[1], ymd[2]) + datetime.timedelta(timeLimit)
            if  dueDate < date.today():
                amount = (date.today() - dueDate).days
                fine = (amount, date.today().isoformat(), '0000-00-00', r[0])
                fines.append(fine)
                TableOperation.insertTuple('Fine (amount, issuedDate, paidDate, borid)',
                        fine)
            checkHolds = TableOperation.sfw('HoldRequest AS h INNER JOIN Borrowing AS bor ON (h.callNumber=bor.callNumber) ORDER BY h.hid ASC', ['h.hid'],"bor.borid='%s'" % _borid)
            print checkHolds
            if checkHolds:
                _hid = checkHolds[0][0]
                result = TableOperation.sfw("Borrower AS b INNER JOIN HoldRequest as h ON (h.bid=b.bid)",['b.bid','b.emailAddress'],'h.hid=%s' % _hid)
                _bid = result[0][0]
                _email = result[0][1]
                _callNumber = checkHolds[0][1]
                row = [_hid,_callNumber,1]
                TableOperation.insertTuple('Cart',str(row))
                TableOperation.deleteTuple('HoldRequest','hid=%s' %_hid)
                settings = "status ='on-hold'"
                mails.append(_email)
            else:
                settings = "status ='in'"
            conds = "callNumber = '%s' AND copyNo = '%s'" % tuple(copyUpdate.pop())
            TableOperation.usw('BookCopy', settings, conds)
        print mails
        message=""
        if copyRows:
            message = message + "Returned copies: %s" % (str(copies))
        if fines:
            message = message + "Fines Assessed: %s" % (str(fines))
        session['message'] = message
        return redirect(url_for('.borrowed', user=g.userInfo[0],
            accType=g.userInfo[8], bid=session.pop('bid', None)))
    return render_template('.borrow_page', user=g.userInfo[0], accType=g.userInfo[8])
