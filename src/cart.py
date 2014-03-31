from flask import Flask, request, session, url_for, redirect, \
     render_template, abort, g, flash, Blueprint
from jinja2 import TemplateNotFound

import MySQLdb
import TableOperation

from datetime import date
import datetime

cart_page = Blueprint('cart_page', __name__)

# hard coded clerk and librarian accounts
accs = {
        'clerk1':['clerk1', '1234', 'evan', None, None, None, None, None, 'clerk'],
        'clerk2':['clerk2', '1234', 'shibo', None, None, None, None, None, 'clerk'],
        'lib1':['lib1', '1234', 'wilson', None, None, None, None, None, 'librarian']
        }

@cart_page.route('/viewcart')
@cart_page.route('/viewcart/<bid>')
def viewcart(bid=None):
    """ Displays logged in borrowers cart or specified borrowers cart"""
    if bid:
        _bid = bid
    else:
        _bid = g.userInfo[0]
    rows = TableOperation.sfw('Book', ['*'],
            "callNumber IN (SELECT callNumber FROM Cart WHERE bid = '%s')" % (_bid))
    session['cart'] = [rows]
    session['bquery'] = rows
    return render_template('cart.html', user=g.userInfo[0], accType=g.userInfo[8], bid=_bid)

@cart_page.route('/addtocart', methods=['POST', 'GET'])
def addtocart():
    if not g.userInfo:
        return redirect(url_for('base_page.index', user=None))
    if request.method == 'POST':
        selected = request.form.keys()
        selectable = session['bquery']

        rows = [selectable[int(s)] for s in selected]
        for r in rows:
            TableOperation.insertTuple('Cart', (g.userInfo[0], r[0]))

    return redirect(url_for('.viewcart', user=g.userInfo[0], accType=g.userInfo[8]))

@cart_page.route('/bidcheck', methods=['POST', 'GET'])
def bidcheck():
    """ Get bid to determine which cart to display """
    if not g.userInfo:
        return redirect(url_for('base_page.index', user=None))
    error = None
    if request.method == 'POST':
        if g.userInfo[8] in ['clerk']:
            bid = request.form['bid'].encode('utf-8')
            bAction = request.form['bAction'].encode('utf-8')
            match = TableOperation.sfw('Borrower', ['*'], "bid = '%s'" % (bid))
            today = date.today()
            if match:
                expDate = match[0][7]
                print expDate
                if expDate < today:
                    error = "Error borrower account is expired"
                    return render_template('bidcheck.html', error=error,
                                     user=g.userInfo[0], accType=g.userInfo[8])
                else:
                    if bAction == 'cart':
                        return redirect("viewcart/%s" %(bid))
                    else:
                        return redirect("borrowed/%s" %(bid))
            else:
                error = "Invalid bid"
                return render_template('bidcheck.html', error=error,
                                 user=g.userInfo[0], accType=g.userInfo[8])
        else:
            return redirect(url_for('.viewcart', user=g.userInfo[0],
                accType=g.userInfo[8], bid=g.userInfo[0]))

    return render_template('bidcheck.html', error=error,
                     user=g.userInfo[0], accType=g.userInfo[8])

@cart_page.route('/cartaction/<bid>', methods=['POST', 'GET'])
def cartaction(bid):
    if not g.userInfo or bid == None:
        return redirect(url_for('base_page.index', user=None))
    if request.method == 'POST':
        cartOp = request.form['cartOperation'].encode('utf-8')
        session['selected'] = [x for x in request.form.keys() if x != 'cartOperation']
        if cartOp == 'checkout' and g.userInfo[8] in ['clerk']:
            return redirect(url_for('.checkoutcart', user=g.userInfo[0],
                accType=g.userInfo[8], bid=bid))
        elif cartOp == 'holdrequest':
            return redirect(url_for('.viewcart', user=g.userInfo[0], accType=g.userInfo[8]))
        elif cartOp == 'remove':
            return redirect(url_for('.removefromcart', user=g.userInfo[0],
                accType=g.userInfo[8], bid=bid))
    return render_template('base_page.result', user=g.userInfo[0], accType=g.userInfo[8])

@cart_page.route('/checkoutcart/<bid>', methods=['GET'])
def checkoutcart(bid):
    if not g.userInfo or bid == None:
        return redirect(url_for('base_page.index', user=None))
    selected = session['selected']
    selectable = [session['bquery'][int(s)] for s in selected]

    borrowable = [s for s in selectable if TableOperation.sfw('BookCopy', ['*'],
                "status = 'in' AND callNumber = '%s'" %(s[0]))]
    intersection = [x for x in borrowable if x in selectable]
    copyTable = [TableOperation.getFieldNames('BookCopy')]
    borTable = [TableOperation.getFieldNames('Borrowing')]
    for r in intersection:
        copy = TableOperation.sfw('BookCopy', ['callNumber', 'MIN(CopyNo)'],
                "callNumber = '%s' AND status = 'in'" % (r[0]))
        copyTable.append(TableOperation.sfw('BookCopy', ['*'],
            "callNumber = '%s' AND copyNo = '%s'" %tuple(copy[0]))[0])
        conds = "callNumber='%s' AND copyNo='%s'" % tuple(copy[0])
        TableOperation.usw('BookCopy', "status='out'", conds)
        borrowing = (bid.encode('utf-8'), copy[0][0], int(copy[0][1]),
                date.today().isoformat(), 'NULL')
        TableOperation.insertTuple(db,
                'Borrowing (bid, callNumber, copyNo, outDate, inDate)',
                borrowing)
        borid = TableOperation.selectFrom('Borrowing', ['MAX(Borid)'])[0]
        bor = borid + list(borrowing)
        borTable.append(bor)
        TableOperation.deleteTuple('Cart',
                "bid = '%s' AND callNumber = '%s'" %(bid, r[0]))

    session['result'] = [copyTable, borTable]
    return redirect(url_for('base_page.result',
        user=g.userInfo[0], accType=g.userInfo[8]))

@cart_page.route('/removefromcart/<bid>', methods=['POST', 'GET'])
def removefromcart(bid):
    if not g.userInfo or bid == None:
        return redirect(url_for('base_page.index', user=None))
    selected = session['selected']
    removable = session['bquery']

    remove = [removable[int(s)] for s in selected]
    for r in remove:
        TableOperation.deleteTuple('Cart',
                "bid = '%s' AND callNumber = '%s'" %(bid, r[0]))

    return redirect(url_for('.viewcart', user=g.userInfo[0], accType=g.userInfo[8]))

