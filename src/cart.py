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
            "callNumber IN (SELECT callNumber FROM Cart WHERE bid = '%s' and isHold=0)" % (_bid))
    session['cart'] = [rows]
    session['bquery'] = rows
    
    rows = TableOperation.sfw('Book', ['*'],"callNumber IN (SELECT callNumber FROM Cart WHERE bid = '%s' and isHold = 1)" % (_bid))
    session['readyforpickup'] = [rows]
    session['readyquery'] = rows
    
    rows = TableOperation.sfw('HoldRequest', ['*'],
            "bid = '%s'" % (_bid))
    session['holds'] = [rows]
    session['hquery'] = rows
    hname = TableOperation.getFieldNames('HoldRequest')

    return render_template('cart.html', user=g.userInfo[0], accType=g.userInfo[8],
            bid=_bid, message=session.pop('message', None), hname=hname)

@cart_page.route('/addtocart', methods=['POST', 'GET'])
def addtocart():
    if not g.userInfo:
        return redirect(url_for('base_page.index', user=None))
    if request.method == 'POST':
        selected = request.form.keys()
        print selected
        selectable = session['bquery']
        print selectable

        out = TableOperation.sfw('Borrowing', ['callNumber'],
                "bid = '%s' AND inDate='0000-00-00'" % (g.userInfo[0]))
        print out
        rows = [selectable[int(s)] for s in selected]
        print rows
        tocart = [x for x in rows if not [x[0]] in out]
        print tocart
        for r in tocart:
            TableOperation.insertTuple('Cart', (g.userInfo[0], r[0], 0))
        difference = [x for x in rows if x not in tocart]
        message = ""
        if tocart:
            message = message + "Added to cart: %s" % (tocart)
        if difference:
            message = message + "Already Checked out: %s" % (difference)
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
                unpaid = TableOperation.sfw("""Fine F INNER JOIN Borrowing B
                        INNER JOIN Borrower R ON F.borid=B.borid AND R.bid=B.bid""",
                        ['fid', 'amount', 'issuedDate', 'paidDate', 'F.borid'],
                        "F.paidDate='0000-00-00' AND B.bid = '%s'" % (bid))
                if expDate < today:
                    error = "Error borrower account is expired"
                    return render_template('bidcheck.html', error=error,
                                     user=g.userInfo[0], accType=g.userInfo[8])
                elif unpaid:
                    error = "Error borrower account has unpaid fines"
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
        print session['selected']
        if cartOp == 'checkout' and g.userInfo[8] in ['clerk']:
            return redirect(url_for('.checkoutcart', user=g.userInfo[0],
                accType=g.userInfo[8], bid=bid))
        elif cartOp == 'checkouthold'and g.userInfo[8] in ['clerk']:
            return redirect(url_for('.checkoutholdcart', user=g.userInfo[0],
                accType=g.userInfo[8], bid=bid))
        elif cartOp == 'holdrequest':
            return redirect(url_for('holds_page.addtoholds', user=g.userInfo[0],
                accType=g.userInfo[8], bid=bid))
        elif cartOp == 'remove':
            return redirect(url_for('.removefromcart', user=g.userInfo[0],
                accType=g.userInfo[8], bid=bid))
        elif cartOp == 'removehold':
             return redirect(url_for('.removeholdfromcart', user=g.userInfo[0],
                accType=g.userInfo[8], bid=bid))
    return render_template('base_page.result', user=g.userInfo[0], accType=g.userInfo[8])

@cart_page.route('/checkoutholdcart/<bid>', methods=['GET'])
def checkoutholdcart(bid):
    if not g.userInfo or bid == None:
        return redirect(url_for('base_page.index', user=None))
    selected = session['selected']
    selectable = [session['readyquery'][int(s)] for s in selected]

    borrowable = [s for s in selectable if TableOperation.sfw('BookCopy', ['*'],
                "status = 'on-hold' AND callNumber = '%s'" %(s[0]))]
    intersection = [x for x in borrowable if x in selectable]
    copyTable = [TableOperation.getFieldNames('BookCopy')]
    borTable = [TableOperation.getFieldNames('Borrowing')]
    for r in intersection:
        copy = TableOperation.sfw('BookCopy', ['callNumber', 'MIN(CopyNo)'],
                "callNumber = '%s' AND status = 'on-hold'" % (r[0]))
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
                "bid = '%s' AND callNumber = '%s' and isHold = 0" %(bid, r[0]))

    message = "Books removed from cart:: %s" % (str(remove))
    session['message'] = message

    return redirect(url_for('.viewcart', user=g.userInfo[0], accType=g.userInfo[8]))
    
@cart_page.route('/removeholdfromcart/<bid>', methods=['POST','GET'])
def removeholdfromcart(bid):
    if not g.userInfo or bid == None:
        return redirect(url_for('base_page.index', user=None))
    selected = session['selected']
    removable = session['readyquery']

    remove = [removable[int(s)] for s in selected]
    for r in remove:
        TableOperation.deleteTuple('Cart',
                "bid = '%s' AND callNumber = '%s' and isHold = 1" %(bid, r[0]))

    message = "Books removed from cart:: %s" % (str(remove))
    session['message'] = message

    return redirect(url_for('.viewcart', user=g.userInfo[0], accType=g.userInfo[8]))

