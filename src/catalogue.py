from flask import Flask, request, session, url_for, redirect, \
     render_template, abort, g, flash, Blueprint
from jinja2 import TemplateNotFound

import MySQLdb
import TableOperation

catalogue_page = Blueprint('catalogue_page', __name__)

@catalogue_page.route('/catalogue')
@catalogue_page.route('/catalogue/<searchtype>/<keyword>')
def catalogue(searchtype=None,keyword=None):
    if searchtype and keyword:
        _searchtype = searchtype
        _keyword = keyword
    else:
        _searchtype = request.args.get( 'searchtype' )
        _keyword = request.args.get( 'keyword' )
    if _searchtype==None or _keyword==None:
        _searchtype = ""
        _keyword = ""
    else:
        _searchtype = _searchtype.encode('utf-8')
        _keyword = _keyword.encode('utf-8')
    fieldnames = TableOperation.getFieldNames('Book')
    if _searchtype == 'title':
        rows = TableOperation.sfw("Book AS b INNER JOIN HasAuthor AS a ON (b.callNumber = a.callNumber) INNER JOIN HasSubject AS s ON (b.callNumber = s.callNumber)",["b.callNumber,b.isbn,b.title,b.mainAuthor,a.name,s.subject,b.publisher,b.year"],"b.title LIKE '%%%s%%'" % _keyword)
    elif _searchtype == 'author':
        rows = TableOperation.sfw("Book AS b INNER JOIN HasAuthor AS a ON (b.callNumber = a.callNumber) INNER JOIN HasSubject AS s ON (b.callNumber = s.callNumber)",["b.callNumber,b.isbn,b.title,b.mainAuthor,a.name,s.subject,b.publisher,b.year"],"a.name LIKE '%%%s%%' or b.mainAuthor LIKE '%%%s%%'" % (_keyword,_keyword))
    elif _searchtype == 'subject':
        rows = TableOperation.sfw("Book AS b INNER JOIN HasAuthor AS a ON (b.callNumber = a.callNumber) INNER JOIN HasSubject AS s ON (b.callNumber = s.callNumber)",["b.callNumber,b.isbn,b.title,b.mainAuthor,a.name,s.subject,b.publisher,b.year"],"s.subject LIKE '%%%s%%'" % (_keyword))
    else:
        rows = TableOperation.getColumns("Book AS b INNER JOIN HasAuthor AS a ON (b.callNumber = a.callNumber) INNER JOIN HasSubject AS s ON (b.callNumber = s.callNumber)",["b.callNumber,b.isbn,b.title,b.mainAuthor,a.name,s.subject,b.publisher,b.year"])
    session['catalogue'] = [rows]
    session['bquery'] = rows
    return render_template('catalogue.html', user=g.userInfo[0], accType=g.userInfo[8])
