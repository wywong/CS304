from flask import Flask, request, session, url_for, redirect, \
     render_template, abort, g, flash, Blueprint
from jinja2 import TemplateNotFound

import MySQLdb
import TableOperation

from datetime import date
import datetime

report_overdue_page = Blueprint('report_overdue_page', __name__)

@report_overdue_page.route('/reportoverdue')
def reportoverdue():
    dates = TableOperation.sfw('Borrowing AS bor INNER JOIN Borrower AS b ON (bor.bid = b.bid) INNER JOIN BorrowerType AS bt ON (b.type = bt.type) INNER JOIN Book as bk ON (bk.callNumber=bor.callNumber)',['outDate','bookTimeLimit','b.emailAddress','bk.title'],"bor.inDate= '0000-00-00'")
    duedates = [r[0]+datetime.timedelta(r[1]*7) for r in dates]
    emails = [r[2] for r in dates]
    book = [r[3] for r in dates]
    today = date.today()
    overdue = [today > d for d in duedates]
    rows = TableOperation.sfw('Borrowing AS bor INNER JOIN Borrower AS b ON (b.bid = bor.bid) INNER JOIN Book AS bk ON (bor.callNumber = bk.callNumber) INNER JOIN HasSubject AS h ON (bk.callNumber = h.callNUmber) INNER JOIN BookCopy AS bc ON (bc.callNumber=bk.callNumber)', ['bk.callNumber','bk.isbn','bk.title','bk.mainAuthor','h.subject','bc.copyNo','b.name','bor.outDate'],"bor.inDate = '0000-00-00' and bor.copyNo=bc.copyNo")
    rows = [[x if type(x) is not date else str(x) for x in y] for y in rows]
    [x.append(duedates.pop(0).isoformat())for x in rows]
    session['report'] = [rows]
    return render_template('report.html',reporttype=2,overdue=overdue,emails=emails,book=book, user=g.userInfo[0], accType=g.userInfo[8])
