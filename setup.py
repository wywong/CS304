#!/usr/bin/python
import MySQLdb
from src import TableOperation, dbConn

db = dbConn.dbConn()

cur = db.cursor()

fd = open('Resources/createTables.sql')

sqlFile = fd.read()

sqlCmds = sqlFile.split(';')

sqlCmds = [cmd for cmd in sqlCmds if cmd.strip()]

for cmd in sqlCmds:
    cur.execute(cmd)

TableOperation.insertTuple(db, 'BorrowerType', ('student', 2))
TableOperation.insertTuple(db, 'BorrowerType', ('faculty', 12))
TableOperation.insertTuple(db, 'BorrowerType', ('staff', 6))
