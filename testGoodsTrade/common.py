from settings import *
def CloseAllDb():
    pass
def GetAdminDbConn(reconnect=False):
    global dbConnTrade
    if dbConnAdmin == None:
       logger.info("connect to admin db..")
       try:
          dbConnTrade = MySQLdb.connect(dbHostAdmin,dbUserAdmin,dbPassAdmin,charset="utf8",port=dbPortAdmin)
          logger.info("connect db ok")
       except Exception,e:
           logger.warning(e)
           sys.exit(-1)
    
    try:
       dbConnTrade.ping()
    except Exception,e:
       logger.warning("connection lost,reconnect to admin db..")
       try:
          dbConnTrade = MySQLdb.connect(dbHostAdmin,dbUserAdmin,dbPassAdmin,charset="utf8",port=dbPortAdmin)
          logger.info("reconnect ok")
       except Exception,e:
          logger.warning(e)
          sys.exit(-1)

    return dbConnTrade

def ExecuteSqlQuery(sql,conn):
    dbconn = conn
    try:
        cursor = dbconn.cursor()
        cursor.execute(sql)
        return cursor.fetchall()
    except MySQLdb.Error, e:
        logger.error("error:" + str(e))
        
    return None


def ExecuteSql(sql,conn):
    dbconn = conn
    try:
        cursor = dbconn.cursor()
        affected = cursor.execute(sql)
        dbconn.commit()
        return affected
    except MySQLdb.Error,e:
        logger.error("error:" + str(e))

    return None
