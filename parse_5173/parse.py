#encoding=gbk

from settings import *
from common import *
import json
import sys
import urllib
import re

class CGameInfo :
    game_id = None
    game_identity = None
    game_name = None
    is_hot = None
    type = None
    category = None

class CGameOperator :
    game_id = None
    game_identity = None
    game_name = None
    operator_id = None
    operator_identity = None
    operator_name = None

class CGameArea :
    game_id = None
    game_identity = None
    game_name = None
    operator_id = None
    operator_identity = None
    area_id = None
    area_identity = None
    area_name = None

class CGameGroupArea :
    game_id = None
    game_identity = None
    game_name = None
    operator_id = None
    operator_identity = None
    operator_name = None
    area_id = None
    area_identity = None
    area_name = None
    group_id = None
    group_identity = None
    group_name = None

def parasGame() :
    t_ParseGameUrl = 'http://fcd.5173.com/commondata/Category.aspx?type=game'
    #t_ParseGameUrl = 'http://fcd.5173.com/commondata/Category.aspx?type=operator&id=5b4dca7c7fdd4fd280562b843ad36cbe'

    t_Content = urllib.urlopen(t_ParseGameUrl).read()

    #去掉前后的空格
    #t_Content = t_Content[1:t_Len-1]

    t_Content = DealJsonString(t_Content)

    try :
        t_Data = json.read(t_Content)

        t_GameIdBegin = getMaxGameId()
        for k,v in t_Data.items() :
            if k != "Types" and k != "HOT" :
                for t_Game in v :
                    t_GameIdBegin += 1
                    t_GameInfo = CGameInfo();
                    t_GameInfo.game_id =t_GameIdBegin
                    t_GameInfo.game_identity = t_Game["id"]
                    t_GameInfo.game_name = t_Game["name"].decode('gbk').encode('utf-8')
                    t_GameInfo.is_hot = t_Game["hot"]
                    t_GameInfo.type = k
                    t_GameInfo.category = t_Game["type"]
                    InsertGameInfo(t_GameInfo)
    except :
        logger.error( sys.exc_info())

def parasOperator(game_id,identity,game_name) :
    t_ParasOperatorUrl = 'http://fcd.5173.com/commondata/Category.aspx?type=operator&id='+identity
    t_Content = urllib.urlopen(t_ParasOperatorUrl).read()

    t_Content = DealJsonString(t_Content)

    try :
        t_Data = json.read(t_Content)

        if len(t_Data) == 0 :
            return False;
        else :
            UpdateGameOperator(identity)

        t_OperatorIdBegin = getMaxOperatorId(game_id)

        for t_Operator in t_Data :
            t_OperatorIdBegin += 1
            t_OperatorInfo = CGameOperator()

            t_OperatorInfo.game_id = game_id
            t_OperatorInfo.game_identity = identity
            t_OperatorInfo.game_name = game_name
            t_OperatorInfo.operator_id = t_OperatorIdBegin
            t_OperatorInfo.operator_identity = t_Operator["id"]
            t_OperatorInfo.operator_name = t_Operator["name"].decode('gbk').encode('utf-8')
            InsertGameOperatorInfo(t_OperatorInfo)
    except :
        logger.error("json decode error,url:"+t_ParasOperatorUrl)
        logger.error( sys.exc_info())

def parseArea(game_id,identity,game_name) :
    t_ParasAreaUrl = 'http://fcd.5173.com/commondata/Category.aspx?type=area&id='+identity

    t_Content = urllib.urlopen(t_ParasAreaUrl).read()

    t_Content = DealJsonString(t_Content)

    try :
        t_Data = json.read(t_Content)

        t_AreaIdBegin = getMaxAreaId(game_id,-1)
        for t_Operator in t_Data :
            t_AreaIdBegin += 1
            t_AreaInfo = CGameArea()

            t_AreaInfo.game_id = game_id
            t_AreaInfo.game_identity = identity
            t_AreaInfo.game_name = game_name
            t_AreaInfo.operator_id = -1
            t_AreaInfo.operator_identity = ''
            t_AreaInfo.operator_name = ''
            t_AreaInfo.area_id = t_AreaIdBegin
            t_AreaInfo.area_identity = t_Operator["id"]
            t_AreaInfo.area_name = t_Operator["name"].decode('gbk').encode('utf-8')
            InsertGameAreaInfo(t_AreaInfo)
    except :
        logger.error("json decode error,url:"+t_ParasAreaUrl)
        logger.error( sys.exc_info())

def parseOperatorArea(game_id,game_identity,game_name,operator_id,operator_identity,operator_name) :
    t_ParasAreaUrl = 'http://fcd.5173.com/commondata/Category.aspx?type=operatorArea&id=%s&gameid=%s' % (operator_identity,game_identity)

    t_Content = urllib.urlopen(t_ParasAreaUrl).read()

    t_Content = DealJsonString(t_Content)

    try :
        t_Data = json.read(t_Content)

        t_AreaIdBegin = getMaxAreaId(game_id,operator_id)
        for t_Operator in t_Data :
            t_AreaIdBegin += 1
            t_AreaInfo = CGameArea()

            t_AreaInfo.game_id = game_id
            t_AreaInfo.game_identity = game_identity
            t_AreaInfo.game_name = game_name
            t_AreaInfo.operator_id = operator_id
            t_AreaInfo.operator_identity = operator_identity
            t_AreaInfo.operator_name = operator_name
            t_AreaInfo.area_id = t_AreaIdBegin
            t_AreaInfo.area_identity = t_Operator["id"]
            t_AreaInfo.area_name = t_Operator["name"].decode('gbk').encode('utf-8')
            InsertGameAreaInfo(t_AreaInfo)
    except :
        logger.error("json decode error,url:"+t_ParasAreaUrl)
        logger.error( sys.exc_info())

def parseGroup(game_id,game_identity,game_name,operator_id,operator_identity,operator_name,area_id,area_identity,area_name) :
    t_ParasGroupUrl = 'http://fcd.5173.com/commondata/Category.aspx?type=server&id='+area_identity
    t_Content = urllib.urlopen(t_ParasGroupUrl).read()

    t_Content = DealJsonString(t_Content)

    try :
        t_Data = json.read(t_Content)

        t_GroupIdBegin = getMaxGroupId(game_id,area_id)
        for t_Operator in t_Data :
            t_GroupIdBegin += 1
            t_GroupInfo = CGameGroupArea()

            t_GroupInfo.game_id = game_id
            t_GroupInfo.game_identity = game_identity
            t_GroupInfo.game_name = game_name
            t_GroupInfo.operator_id = operator_id
            t_GroupInfo.operator_identity = operator_identity
            t_GroupInfo.operator_name = operator_name
            t_GroupInfo.area_id = area_id
            t_GroupInfo.area_identity = area_identity
            t_GroupInfo.area_name = area_name
            t_GroupInfo.group_id = t_GroupIdBegin
            t_GroupInfo.group_identity = t_Operator["id"]
            t_GroupInfo.group_name = t_Operator["name"].decode('gbk').encode('utf-8')
            InsertGameAreaGroupInfo(t_GroupInfo)
    except :
        logger.error("json decode error,url:"+t_ParasGroupUrl)
        logger.error( sys.exc_info())

def DealJsonString(t_Content) :
    #在{之后加上单引号
    t_Content = re.sub(r"{", r"{'", t_Content)

    #在冒号之前加上单引号
    t_Content = re.sub(r":", r"':", t_Content)

    #在不是以}，{形式出现的逗号后面加上单引号
    t_Content = re.sub(r"([^}]),([^{])", r"\1,'\2", t_Content)

    #把所有单引号变成双引号
    t_Content = re.sub(r"'", r'"', t_Content)

    return t_Content

def InsertGameInfo(info) :
    select_sql = "select * from TradeAdmin.cAllGame where game_identity='%s'" % (info.game_identity)
    result = ExecuteSqlQuery(select_sql,GetAdminDbConn())
    if len(result) > 0 :
        update_sql = "update TradeAdmin.cAllGame set update_time=NOW() where game_identity='%s'" % (info.game_identity)
        logger.info(update_sql)
        affected  = ExecuteSql(update_sql,GetAdminDbConn())
        logger.info("affected: " + str(affected))
    else :
        insert_sql = "REPLACE INTO TradeAdmin.cAllGame (game_id,game_identity,game_name,is_hot,type,category,image,,create_time,update_time) VALUES (%d,'%s','%s',%d,'%s','%s','%s',NOW(),NOW())"  % (int(info.game_id),info.game_identity,info.game_name,int(info.is_hot),info.type,info.category,'http://static.sdg-china.com/openg/souzhuangbei/game_image/szb.png')
        logger.info(insert_sql)
        affected  = ExecuteSql(insert_sql,GetAdminDbConn())
        logger.info("affected: " + str(affected))

def UpdateGameOperator(game_identity) :
    update_sql = "UPDATE TradeAdmin.cAllGame SET has_operator=1 WHERE game_identity='%s'"  % (game_identity)
    logger.info(update_sql)
    affected  = ExecuteSql(update_sql,GetAdminDbConn())
    logger.info("affected: " + str(affected))

def InsertGameOperatorInfo(info) :
    select_sql = "select * from TradeAdmin.cAllGameOperator where game_identity='%s' and operator_identity='%s'" % (info.game_identity,info.operator_identity)
    result = ExecuteSqlQuery(select_sql,GetAdminDbConn())
    if len(result) > 0 :
        update_sql = "update TradeAdmin.cAllGameOperator set update_time=NOW(),del_flag=0 where game_identity='%s' and operator_identity='%s'" % (info.game_identity,info.operator_identity)
        logger.info(update_sql)
        affected  = ExecuteSql(update_sql,GetAdminDbConn())
        logger.info("affected: " + str(affected))
    else :
        insert_sql = "REPLACE INTO TradeAdmin.cAllGameOperator (game_id,game_identity,game_name,operator_id,operator_identity,operator_name,create_time,update_time) VALUES (%d,'%s','%s',%d,'%s','%s',NOW(),NOW())"  % (int(info.game_id),info.game_identity,info.game_name,int(info.operator_id),info.operator_identity,info.operator_name)
        logger.info(insert_sql)
        affected  = ExecuteSql(insert_sql,GetAdminDbConn())
        logger.info("affected: " + str(affected))

def InsertGameAreaInfo(info) :
    select_sql = "select * from TradeAdmin.cAllGameArea where game_identity='%s' and area_identity='%s'" % (info.game_identity,info.area_identity)
    result = ExecuteSqlQuery(select_sql,GetAdminDbConn())
    if len(result) > 0 :
        update_sql = "update TradeAdmin.cAllGameArea set update_time=NOW(),del_flag=0 where game_identity='%s' and area_identity='%s'" % (info.game_identity,info.area_identity)
        logger.info(update_sql)
        affected  = ExecuteSql(update_sql,GetAdminDbConn())
        logger.info("affected: " + str(affected))
    else :
        insert_sql = "REPLACE INTO TradeAdmin.cAllGameArea (game_id,game_identity,game_name,operator_id,operator_identity,operator_name,area_id,area_identity,area_name,create_time,update_time) VALUES (%d,'%s','%s',%d,'%s','%s',%d,'%s','%s',NOW(),NOW())"  % (int(info.game_id),info.game_identity,info.game_name,int(info.operator_id),info.operator_identity,info.operator_name,int(info.area_id),info.area_identity,info.area_name)
        logger.info(insert_sql)
        affected  = ExecuteSql(insert_sql,GetAdminDbConn())
        logger.info("affected: " + str(affected))

def InsertGameAreaGroupInfo(info):
    select_sql = "select * from TradeAdmin.cAllGameAreaGroup where game_identity='%s' and area_identity='%s' and group_identity='%s'" % (info.game_identity,info.area_identity,info.group_identity)
    result = ExecuteSqlQuery(select_sql,GetAdminDbConn())
    if len(result) > 0 :
        update_sql = "update TradeAdmin.cAllGameAreaGroup set update_time=NOW(),del_flag=0 where game_identity='%s' and area_identity='%s' and group_identity='%s'" % (info.game_identity,info.area_identity,info.group_identity)
        logger.info(update_sql)
        affected  = ExecuteSql(update_sql,GetAdminDbConn())
        logger.info("affected: " + str(affected))
    else :
        insert_sql = "REPLACE INTO TradeAdmin.cAllGameAreaGroup (game_id,game_identity,game_name,operator_id,operator_identity,operator_name,area_id,area_identity,area_name,group_id,group_identity,group_name,create_time,update_time) VALUES (%d,'%s','%s',%d,'%s','%s',%d,'%s','%s',%d,'%s','%s',NOW(),NOW())"  % (int(info.game_id),info.game_identity,info.game_name,int(info.operator_id),info.operator_identity,info.operator_name,int(info.area_id),info.area_identity,info.area_name,int(info.group_id),info.group_identity,info.group_name)
        logger.info(insert_sql)
        affected  = ExecuteSql(insert_sql,GetAdminDbConn())
        logger.info("affected: " + str(affected))

def getMaxGameId() :
    select_sql = 'SELECT game_id FROM TradeAdmin.`cAllGame` where is_snda_game=0 ORDER BY game_id desc LIMIT 1'
    result = ExecuteSqlQuery(select_sql,GetAdminDbConn())
    max_game_id = 10000
    if len(result) != 0 :
        max_game_id = result[0][0]
    return max_game_id

def getMaxOperatorId(game_id) :
    select_sql = 'SELECT operator_id FROM TradeAdmin.`cAllGameOperator` where game_id=%d ORDER BY operator_id desc LIMIT 1' % game_id
    result = ExecuteSqlQuery(select_sql,GetAdminDbConn())
    max_operator_id = 10000
    if len(result) != 0 :
        max_operator_id = result[0][0]
    return max_operator_id

def getMaxAreaId(game_id,operator_id) :
    select_sql = 'SELECT area_id FROM TradeAdmin.`cAllGameArea` where game_id=%d and operator_id=%d ORDER BY area_id desc LIMIT 1' % (game_id,operator_id)
    result = ExecuteSqlQuery(select_sql,GetAdminDbConn())
    max_area_id = 10000
    if len(result) != 0 :
        max_area_id = result[0][0]
    return max_area_id

def getMaxGroupId(game_id,area_id) :
    select_sql = 'SELECT group_id FROM TradeAdmin.`cAllGameAreaGroup` where game_id=%d and area_id=%d ORDER BY group_id desc LIMIT 1' % (game_id,area_id)
    result = ExecuteSqlQuery(select_sql,GetAdminDbConn())
    max_group_id = 10000
    if len(result) != 0 :
        max_group_id = result[0][0]
    return max_group_id


def DealOperator() :
    t_SelectGameSql = "select * from TradeAdmin.cAllGame where open_flag = 1";
    logger.info(t_SelectGameSql)
    result = ExecuteSqlQuery(t_SelectGameSql,GetAdminDbConn())
    for record in result:
        parasOperator(record[1],record[2],record[3])

def DealOperatorArea(game_identity) :
    t_SelectOperatorSql = "select * from TradeAdmin.cAllGameOperator where game_identity='%s' and del_flag=0" % (game_identity)
    logger.info(t_SelectOperatorSql)
    result = ExecuteSqlQuery(t_SelectOperatorSql,GetAdminDbConn())
    for record in result:
        parseOperatorArea(record[1],record[2],record[3],record[4],record[5],record[6])

def DealArea() :
    t_SelectGameSql = "select * from TradeAdmin.cAllGame where open_flag = 1";
    logger.info(t_SelectGameSql)
    result = ExecuteSqlQuery(t_SelectGameSql,GetAdminDbConn())
    for record in result:
        if record[8] == 0 :
            parseArea(record[1],record[2],record[3])
        else :
            DealOperatorArea(record[2])

def DealGroup() :
    t_SelectGameSql = "select * from TradeAdmin.cAllGameArea where del_flag=0";
    logger.info(t_SelectGameSql)
    result = ExecuteSqlQuery(t_SelectGameSql,GetAdminDbConn())
    for record in result:
        parseGroup(record[1],record[2],record[3],record[4],record[5],record[6],record[7],record[8],record[9])
        #print record[3],record[4]

def DeleteOldGame() :
    t_UpdateSql = "update TradeAdmin.cAllGame set del_flag=1 where update_time < DATE_SUB(CURDATE(), INTERVAL 3 DAY)"
    logger.info(t_UpdateSql)
    affected  = ExecuteSql(t_UpdateSql,GetAdminDbConn())
    logger.info("affected: " + str(affected))

def DeleteOldOperator() :
    t_UpdateSql = "update TradeAdmin.cAllGameOperator set del_flag=1 where update_time < DATE_SUB(CURDATE(), INTERVAL 3 DAY)"
    logger.info(t_UpdateSql)
    affected  = ExecuteSql(t_UpdateSql,GetAdminDbConn())
    logger.info("affected: " + str(affected))

def DeleteOldArea() :
    t_UpdateSql = "update TradeAdmin.cAllGameArea set del_flag=1 where update_time < DATE_SUB(CURDATE(), INTERVAL 3 DAY)"
    logger.info(t_UpdateSql)
    affected  = ExecuteSql(t_UpdateSql,GetAdminDbConn())
    logger.info("affected: " + str(affected))

def DeleteOldGroup() :
    t_UpdateSql = "update TradeAdmin.cAllGameAreaGroup set del_flag=1 where update_time < DATE_SUB(CURDATE(), INTERVAL 3 DAY)"
    logger.info(t_UpdateSql)
    affected  = ExecuteSql(t_UpdateSql,GetAdminDbConn())
    logger.info("affected: " + str(affected))

def OperatorSndaGame() :
    t_ParseSndaGameUrl = 'http://api.shandagames.com/?method=sdg.game.catalog.getGameList&oauth_token=7af476412a23ee11c5eca76a58c4857b%7C1382681023&page=1&count=5000&oauth_consumer_key=20ce99c02d6bf0de48d7d57271040de2&oauth_nonce=6d65ea88a86a55a1472fabfc685d9628&oauth_timestamp=1382682491&oauth_version=2.0&oauth_signature_method=HMAC-SHA1&oauth_signature=3102c4045cfe13a82e202c4289cfe2068469b1e7'
    t_Content = urllib.urlopen(t_ParseSndaGameUrl).read()

    try :
        t_Data = json.read(t_Content)

        if t_Data.has_key("return_code") and t_Data["return_code"] == 0 :
            for t_GameInfo in t_Data["data"] :
                #print t_GameInfo
                UpdateSndaGame(t_GameInfo["game_id"],t_GameInfo["game_name"])


    except :
        logger.error( sys.exc_info())

def UpdateSndaGame(game_id,game_name) :
    t_UpdateSql = "update TradeAdmin.cAllGame set game_id=%s,is_snda_game=1 where game_name='%s' and is_snda_game=0" % (game_id,game_name)
    logger.info(t_UpdateSql)
    affected  = ExecuteSql(t_UpdateSql,GetAdminDbConn())
    logger.info("affected: " + str(affected))

if __name__ == "__main__" :
    parasGame()
    #OperatorSndaGame()
    DeleteOldGame()
    DealOperator()
    DealArea()
    DealGroup()
    DeleteOldOperator()
    DeleteOldArea()
    DeleteOldGroup()





