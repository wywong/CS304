from flask import Flask, request, session, url_for, redirect, \
     render_template, abort, g, flash, Blueprint
from jinja2 import TemplateNotFound

import MySQLdb
import TableOperation

from datetime import date
import datetime

report_checkedout_page = Blueprint('report_checkedout_page', __name__)

@report_checkedout_page.route('/reportcheckedout')
@report_checkedout_page.route('/reportcheckedout/<subject>')
def reportcheckedout(subject=None):
    if subject:
        _subject = subject
    else:
        _subject = request.args.get( 'subject' )
    if _subject==None:
        _subject = ""

        dates = TableOperation.getColumns('Borrowing AS bor INNER JOIN Borrower AS b ON (bor.bid = b.bid) INNER JOIN BorrowerType AS bt ON (b.type = bt.type)',['bookTimeLimit','outDate'])
        duedates = [datetime.timedelta(r[0]*7) for r in dates]
        today = date.today()
        overdue = [today > d for d in duedates]

        rows = TableOperation.sfw('Borrowing AS bor INNER JOIN Borrower AS b ON (bor.bid = b.bid) INNER JOIN Book AS bk ON (bor.callNumber = bk.callNumber) INNER JOIN HasSubject AS h ON (bk.callNumber = h.callNUmber) INNER JOIN BookCopy AS bc ON (bc.callNumber=bk.callNumber)', ['bk.callNumber','bk.isbn','bk.title','bk.mainAuthor','h.subject','bc.copyNo','b.name','bor.outDate'],"bor.inDate = '0000-00-00'")
        rows = [[x if type(x) is not date else str(x) for x in y] for y in rows]
        [x.append(duedates.pop(0).isoformat())for x in y]
    else:
        _subject = _subject.encode('utf-8')
        dates = TableOperation.getColumns('Borrowing AS bor INNER JOIN Borrower AS b ON (bor.bid = b.bid) INNER JOIN BorrowerType AS bt ON (b.type = bt.type)',['bookTimeLimit','outDate'])
        duedates = [datetime.timedelta(r[0]*7) for r in dates]
        today = date.today()
        overdue = [today > d for d in duedates]
        rows = TableOperation.sfw('Borrowing AS bor INNER JOIN Borrower AS b ON (bor.bid = b.bid) INNER JOIN Book AS bk ON (bor.callNumber = bk.callNumber) INNER JOIN HasSubject AS h ON (bk.callNumber = h.callNUmber) INNER JOIN BookCopy AS bc ON (bc.callNumber=bk.callNumber)', ['bk.callNumber','bk.isbn','bk.title','bk.mainAuthor','h.subject','bc.copyNo','b.name','bor.outDate'],
            "h.subject = '%%%s%%' and bor.inDate = '0000-00-00'" % _subject)
        rows = [[x if type(x) is not date else str(x) for x in y] for y in rows]
        [x.append(duedates.pop(0).isoformat())for x in y]


    return render_template('reportcheckedout.html', user=g.userInfo[0], accType=g.userInfo[8])
