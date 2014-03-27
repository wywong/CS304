#!/usr/bin/python
import MySQLdb
try:
    db = MySQLdb.connect(host="localhost",
                        user="testuser",
                        passwd="01189998819991197253",
                        db="cs304")
except:
    print "Error %d: %s" % (e.args[0], e.args[1])

cur = db.cursor()

fd = open('Resources/drop.sql')

sqlFile = fd.read()

sqlCmds = sqlFile.split(';')

sqlCmds = [cmd for cmd in sqlCmds if cmd.strip()]

for cmd in sqlCmds:
    cur.execute(cmd)

