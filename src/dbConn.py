import MySQLdb

def dbConn():
    dbCFG = []
    with open('database.cfg') as f:
        for line in iter(f):
            dbCFG.append(line.strip())
    dbHost, dbUser, dbPasswd, dbName = dbCFG
    try:
        db = MySQLdb.connect(host=dbHost,
                            user=dbUser,
                            passwd=dbPasswd,
                            db=dbName)
    except:
        print "Error %d: %s" % (e.args[0], e.args[1])

    return db
