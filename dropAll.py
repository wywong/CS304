#!/usr/bin/python
import MySQLdb
from src import dbConn

db = dbConn.dbConn()

cur = db.cursor()

fd = open('Resources/drop.sql')

sqlFile = fd.read()

sqlCmds = sqlFile.split(';')

sqlCmds = [cmd for cmd in sqlCmds if cmd.strip()]

for cmd in sqlCmds:
    cur.execute(cmd)

