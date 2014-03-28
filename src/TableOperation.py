#!/usr/bin/python

import MySQLdb

def insertTuple(conn, table, row):
    """
    Pre:    conn     - database connection
            table    - table to be inserted into
            row      - tuple to be inserted

    Post:   Inserts row into table
    """
    sql = "INSERT INTO %s VALUE %s" % (table, str(row))
    print sql + ';'
    cur = conn.cursor()
    try:
        cur.execute(sql)
        conn.commit()
    except:
        conn.rollback()

def showTable(conn, table):
    """
    Pre:    conn     - database connection
            table    - table to be inserted into

    Post:   Returns the tables rows as a list of tuples
    """
    cur = conn.cursor()
    sql = "SELECT * FROM %s" % (table)
    print sql + ';'
    cur.execute(sql)
    return list(cur.fetchall())

def getFieldNames(conn, table):
    """
    Pre:    conn     - database connection
            table    - the table being queried

    Post:   Returns the field names of table
    """
    cur = conn.cursor()
    cur.execute("DESC %s" %(table))
    rows = cur.fetchall()
    names = [r[0] for r in rows]
    return names

