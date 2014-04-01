from flask import Flask, request, session, url_for, redirect, \
     render_template, abort, g, flash, Blueprint
from jinja2 import TemplateNotFound

import MySQLdb
import TableOperation

from datetime import date
import datetime

holds_page = Blueprint('holds_page', __name__)

@holds_page.route('/addtoholds', methods=['POST', 'GET'])
def addtoholds():
    if not g.userInfo:
        return redirect(url_for('base_page.index', user=None))
    if request.method == 'POST':
        selected = request.form.keys()
        print selected
        selectable = session['hquery']
        print selectable

        rows = [selectable[int(s)] for s in selected]
        for r in rows:
            TableOperation.insertTuple('Holds', (g.userInfo[0], r[0]))

        message = "Added to holds: %s" % (rows)
        session['message'] = message

    return redirect(url_for('cart_page.viewcart', user=g.userInfo[0], accType=g.userInfo[8]))

@holds_page.route('/holdsaction/<bid>', methods=['POST', 'GET'])
def holdsaction(bid):
    if not g.userInfo or bid == None:
        return redirect(url_for('base_page.index', user=None))
    if request.method == 'POST':
        holdsOp = request.form['holdsOperation'].encode('utf-8')
        session['selected'] = [x for x in request.form.keys() if x != 'holdsOperation']
        if holdsOp == 'checkout' and g.userInfo[8] in ['clerk']:
            return redirect(url_for('cart_page.viewcart', user=g.userInfo[0],
                accType=g.userInfo[8], bid=bid))
        elif holdsOp == 'remove':
            return redirect(url_for('.removefromholds', user=g.userInfo[0],
                accType=g.userInfo[8], bid=bid))
    return render_template('base_page.result', user=g.userInfo[0], accType=g.userInfo[8])

@holds_page.route('/removefromholds/<bid>', methods=['POST', 'GET'])
def removefromholds(bid):
    if not g.userInfo or bid == None:
        return redirect(url_for('base_page.index', user=None))
    selected = session['selected']
    removable = session['hquery']

    remove = [removable[int(s)] for s in selected]
    for r in remove:
        TableOperation.deleteTuple('Holds',
                "hid = '%s' AND issuedDate = '0000-00-00'" %(hid))

    message = "Books removed from holds: %s" % (str(remove))
    session['message'] = message

    return redirect(url_for('.viewholds', user=g.userInfo[0], accType=g.userInfo[8]))

