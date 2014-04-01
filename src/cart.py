from flask import Flask, request, session, url_for, redirect, \
     render_template, abort, g, flash, Blueprint
from jinja2 import TemplateNotFound

import MySQLdb
import TableOperation

from datetime import date
import datetime

cart_page = Blueprint('cart_page', __name__)

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
    return render_template('cart.html', user=g.userInfo[0], accType=g.userInfo[8],
            bid=_bid, message=session.pop('message', None))

@cart_page.route('/addtocart', methods=['POST', 'GET'])
def addtocart():
    if not g.userInfo:
        return redirect(url_for('base_page.index', user=None))
    if request.method == 'POST':
        selected = request.form.keys()
        print selected
        selectable = session['bquery']
        print selectable

        rows = [selectable[int(s)] for s in selected]
        for r in rows:
            TableOperation.insertTuple('Cart', (g.userInfo[0], r[0]))

        message = "Added to cart: %s" % (rows)
        session['message'] = message

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
                        session['message'] = ""
                        return redirect("viewcart/%s" %(bid))
                    else:
                        session['message'] = ""
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
                date.today().isoformat(), '0000-00-00')
        TableOperation.insertTuple('Borrowing (bid, callNumber, copyNo, outDate, inDate)',
                borrowing)
        borid = TableOperation.selectFrom('Borrowing', ['MAX(Borid)'])[0]
        bor = borid + list(borrowing)
        borTable.append(bor)
        TableOperation.deleteTuple('Cart',
                "bid = '%s' AND callNumber = '%s'" %(bid, r[0]))

    difference = [x for x in selectable if x not in intersection]
    message = ""
    if intersection:
        message = message + "Checkedout: %s " % (str(intersection))
    if difference:
        message = message + "No available copies for: %s" % (str(difference))
    session['message'] = message
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

    message = "Books removed from cart:: %s" % (str(remove))
    session['message'] = message

    return redirect(url_for('.viewcart', user=g.userInfo[0], accType=g.userInfo[8]))

