#coding=utf-8
import sys
import logging
import logging.handlers
from datetime import datetime,timedelta
import md5
from datetime import *
import time

reload(sys)
sys.setdefaultencoding('utf-8')

#logger settings 
logger = logging.getLogger('newnotify_CM')
logger.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

rotatingFileHandler = logging.handlers.RotatingFileHandler("newnotify_cm.log",maxBytes=500000000,backupCount=1)
rotatingFileHandler.setFormatter(formatter)
rotatingFileHandler.setLevel(logging.INFO)
logger.addHandler(rotatingFileHandler)

consolehandler = logging.StreamHandler(sys.stdout)
consolehandler.setFormatter(formatter)
consolehandler.setLevel(logging.INFO)
logger.addHandler(consolehandler)

#database settings
import MySQLdb
dbHostAdmin = "116.211.4.170"
dbUserAdmin = "DnSnsUser"
dbPassAdmin = "DnSnsUser_P10y1m25dSnsFeed"
dbPortAdmin= 3306
dbConnAdmin = None



