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

def deleteTuple(conn, table, conds):
    """
    Pre:    conn     - database connection
            table    - table to be inserted into
            conds    - conditions for rows to be deleted

    Post:   Deletes row(s) from table
    """
    sql = "DELETE FROM %s WHERE %s" % (table, str(row))
    print sql + ';'
    cur = conn.cursor()
    try:
        cur.execute(sql)
        conn.commit()
    except:
        conn.rollback()

def selectFrom(conn, table, cols, conds):
    """
    Pre:    conn     - database connection
            table    - table to be inserted into
            cols     - list of columns to be selected
            conds    - conditions for rows to be selected

    Post:   Returns the tables rows as a list of tuples
    """
    cur = conn.cursor()
    sql = "SELECT %s FROM %s WHERE %s" % (', '.join(cols), table, conds)
    print sql
    cur.execute(sql)
    return cur.fetchall()

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
    t = cur.fetchall()
    return [list(l) for l in t]

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

def getColumns(conn, table, cols):
    """
    Pre:    conn     - database connection
            table    - the table being queried
            cols     - the columns to be selected

    Post:   Returns the columns of the fields selected
    """
    cur = conn.cursor()
    cur.execute("SELECT %s FROM %s" %(cols, table))
    return cur.fetchall()

