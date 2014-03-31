from flask import Flask, request, session, url_for, redirect, \
     render_template, abort, g, flash, Blueprint
from jinja2 import TemplateNotFound

import MySQLdb
import TableOperation

from datetime import date
import datetime

fine_page = Blueprint('fine_page', __name__)

@fine_page.route('/viewfine')
@fine_page.route('/viewfine/<bid>')
def viewfine(bid=None):
    """ Displays logged in borrowers fine or specified borrowers fine"""
    if bid:
        _bid = bid
    else:
        _bid = g.userInfo[0]
    fieldNames = TableOperation.getFieldNames('Fine')
    rows = TableOperation.sfw("""Fine F INNER JOIN Borrowing B INNER JOIN Borrower R
            ON F.borid=B.borid AND R.bid=B.bid""",
            ['fid', 'amount', 'issuedDate', 'paidDate', 'F.borid'],
            "F.paidDate='0000-00-00' AND B.bid = '%s'" % (_bid))
    rows = [[x if type(x) is not date else str(x) for x in y] for y in rows]
    session['bquery'] = rows
    session['fine'] = [rows]
    return render_template('fine.html', user=g.userInfo[0], accType=g.userInfo[8],
            bid=_bid, message=session['message'], fname=fieldNames)
