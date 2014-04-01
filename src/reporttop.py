from flask import Flask, request, session, url_for, redirect, \
     render_template, abort, g, flash, Blueprint
from jinja2 import TemplateNotFound

import MySQLdb
import TableOperation

report_top_page = Blueprint('report_top_page', __name__)

@report_top_page.route('/reporttop')
@report_top_page.route('/reporttop/<number>')
def reporttop(number=None):
    if number:
        _number = number
    else:
        _number = request.args.get( 'number' )
    if _number==None:
        _number = "25"
    rows = TableOperation.getColumns("Borrowing AS bor INNER JOIN Book as bk ON (bor.callNumber=bk.callNumber) GROUP BY bor.callNumber ORDER BY count(bor.callNumber) DESC LIMIT %s " % _number,['count(bor.callNumber)','bk.callNumber','bk.title'])
    session['report'] = [rows]
    return render_template('report.html',reporttype=1, user=g.userInfo[0], accType=g.userInfo[8])
