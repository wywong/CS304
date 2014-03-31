#!/usr/bin/python

import MySQLdb
import dbConn
def insertTuple(table, row):
    """
    Pre:    conn     - database connection
            table    - table to be inserted into
            row      - tuple to be inserted

    Post:   Inserts row into table
    """
    conn = dbConn.dbConn()
    sql = "INSERT INTO %s VALUE %s" % (table, str(row))
    print sql + ';'
    cur = conn.cursor()
    try:
        cur.execute(sql)
        conn.commit()
    except:
        conn.rollback()
        print("Query Failed: " + sql)
    cur.close()
    conn.close()

def deleteTuple(table, conds):
    """
    Pre:    conn     - database connection
            table    - table to be inserted into
            conds    - conditions for rows to be deleted

    Post:   Deletes row(s) from table
    """
    conn = dbConn.dbConn()
    sql = "DELETE FROM %s WHERE %s" % (table, str(conds))
    print sql + ';'
    cur = conn.cursor()
    try:
        cur.execute(sql)
        conn.commit()
    except:
        conn.rollback()
        print("Query Failed: " + sql)
    cur.close()
    conn.close()

def usw(table, settings, conds):
    """
    Pre:    conn     - database connection
            table    - table to be inserted into
            settings - values to be set
            conds    - conditions for rows to be updated

    Post:   Deletes row(s) from table
    """
    conn = dbConn.dbConn()
    sql = "UPDATE %s SET %s WHERE %s" % (table, settings, conds)
    print sql + ';'
    cur = conn.cursor()
    try:
        cur.execute(sql)
        conn.commit()
    except:
        conn.rollback()
        print("Query Failed: " + sql)
    cur.close()
    conn.close()

def sfw(table, cols, conds):
    """
    Pre:    conn     - database connection
            table    - table to be inserted into
            cols     - list of columns to be selected
            conds    - conditions for rows to be selected

    Post:   Returns the tables rows as a list of tuples
    """
    conn = dbConn.dbConn()
    cur = conn.cursor()
    sql = "SELECT %s FROM %s WHERE %s" % (', '.join(cols), table, conds)
    print sql
    cur.execute(sql)
    t = cur.fetchall()
    cur.close()
    conn.close()
    return [ list(l) for l in t ]

def selectFrom(table, cols):
    """
    Pre:    conn     - database connection
            table    - table to be inserted into
            cols     - list of columns to be selected
            conds    - conditions for rows to be selected

    Post:   Returns the tables rows as a list of tuples
    """
    conn = dbConn.dbConn()
    cur = conn.cursor()
    sql = "SELECT %s FROM %s" % (', '.join(cols), table)
    print sql
    cur.execute(sql)
    t = cur.fetchall()
    cur.close()
    conn.close()
    return [ list(l) for l in t ]

def showTable(table):
    """
    Pre:    conn     - database connection
            table    - table to be inserted into

    Post:   Returns the tables rows as a list of tuples
    """
    conn = dbConn.dbConn()
    cur = conn.cursor()
    sql = "SELECT * FROM %s" % (table)
    print sql + ';'
    cur.execute(sql)
    t = cur.fetchall()
    cur.close()
    conn.close()
    return [list(l) for l in t]

def getFieldNames(table):
    """
    Pre:    conn     - database connection
            table    - the table being queried

    Post:   Returns the field names of table
    """
    conn = dbConn.dbConn()
    cur = conn.cursor()
    cur.execute("DESC %s" %(table))
    rows = cur.fetchall()
    names = [r[0] for r in rows]
    cur.close()
    conn.close()
    return names

def getColumns(table, cols):
    """
    Pre:    conn     - database connection
            table    - the table being queried
            cols     - list of columns to be selected

    Post:   Returns the columns of the fields selected
    """
    conn = dbConn.dbConn()
    cur = conn.cursor()
    cur.execute("SELECT %s FROM %s" %(', '.join(cols), table))
    t = cur.fetchall()
    cur.close()
    conn.close()
    return [list(l) for l in t ]

