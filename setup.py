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
    print(cmd)

filept = open('Resources/insertTestData.sql')
insertFile = filept.read()
insert = insertFile.split(';')
insert = [cmd2 for cmd2 in insert if cmd2.strip()]
for cmd2 in insert:
    try:
        cur.execute(cmd2)
        db.commit()
    except:
        db.rollback()
    print(cmd2)

db.close()
