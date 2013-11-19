#encoding=utf8
__author__ = 'weizijun.mike'

import sys
import Ice
import random
import unittest
from settings import *
from common import *
import json
import types
import time

Ice.loadSlice('base.ice')
Ice.loadSlice('CashTrade.ice')

import Trade
reload(sys)
key = "MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCx+cLzqmMhKatIxAZHo3UHe57IM6G7AWsNhz4LhsqjV0B9Dpugh8KzWCd7OGrK9yZzEOP3yVNwefPXJdqLgmDr0erwYFpZlWNQEsvnvNMFf1TDZGoEu2eN1xWUl2JyeyJEsY7+f4H6jyyTeuKssoI2+zlVT9GXgy0QX1vHL3GyQQIDAQAB"
ice_string = "GoodsTrade:tcp -h 127.0.0.1 -p 10122"
#ice_string = "GoodsTrade:tcp -h 116.211.2.131 -p 10122"

def _GetIdentity() :
    Id = Trade.Identity()
    Id.strName = "C2C"
    Id.strAccessToken = md5.new("name="+Id.strName+"&key="+key).hexdigest()
    Id.matrixid = "-1--1--1"
    Id.ptaccount = "w195438178"
    Id.ptsdid = "976030482"
    Id.charactername = ""
    return Id

def SearchGoodsList(param) :
    communicator = Ice.initialize(sys.argv)
    cashTrade = Trade.GoodsTradePrx.checkedCast(communicator.stringToProxy(ice_string))
    Id = _GetIdentity()
    t_Method = 'SearchGoodsList'
    t_JsonParam = json.write(param)
    ret = cashTrade.GoodsAPI(Id,t_Method,t_JsonParam)
    return ret

def GoodsAPI(method,param) :
    communicator = Ice.initialize(sys.argv)
    cashTrade = Trade.GoodsTradePrx.checkedCast(communicator.stringToProxy(ice_string))
    Id = _GetIdentity()
    t_JsonParam = json.write(param)
    ret = cashTrade.GoodsAPI(Id,method,t_JsonParam)
    return ret

def TradeAPI(method,param) :
    communicator = Ice.initialize(sys.argv)
    cashTrade = Trade.GoodsTradePrx.checkedCast(communicator.stringToProxy(ice_string))
    Id = _GetIdentity()
    t_JsonParam = json.write(param)
    ret = cashTrade.TradeAPI(Id,method,t_JsonParam)
    return ret

def HpsAPI(method,param) :
    communicator = Ice.initialize(sys.argv)
    cashTrade = Trade.GoodsTradePrx.checkedCast(communicator.stringToProxy(ice_string))
    Id = _GetIdentity()
    t_JsonParam = json.write(param)
    ret = cashTrade.HpsAPI(Id,method,t_JsonParam)
    return ret

def SimulatePayConfrim(orderId):
    sql = "update globalTradeCenter.tOrder set state=5 where order_id = '%s' and state = 2"%(orderId)
    affected  = ExecuteSql(sql,GetAdminDbConn())
    logger.info("SimulatePayConfrim affected: " + str(affected))
    return affected

class TestAPI(unittest.TestCase) :
    def setUp(self):
        self._TestFlag = {
            'test_SoldAccountVerify' : False,
            'test_SendVerifySms' : False,
            'test_SendVerifySms2' : False,
            'test_RealInfoPhone' : True,
            'test_QueryAllGameAccount' : False,
            'test_FreezeAccount' : False,
            'test_UnfreezeAccount' : False,
            'test_TradeAccount' : False,
            }

    def test_RealInfoPhone(self):
        if self._TestFlag['test_RealInfoPhone'] == False :
            return
        t_Method = "RealInfoPhone"
        t_Param = {
            "sdid" : "3238781305",
            "client_ip" : "127.0.0.1",
            }
        ret = HpsAPI(t_Method,t_Param)
        print ret
        self.assertEqual(ret[0],0)

    def test_QueryAllGameAccount(self):
        if self._TestFlag['test_QueryAllGameAccount'] == False :
            return
        t_Method = "QueryAllGameAccount"
        t_Param = {
            "sdid" : "3238781305",
            "client_ip" : "127.0.0.1",
            }
        ret = HpsAPI(t_Method,t_Param)
        print ret
        self.assertEqual(ret[0],0)

    def test_FreezeAccount(self):
        if self._TestFlag['test_FreezeAccount'] == False :
            return
        t_Method = "FreezeAccount"
        t_Param = {
            "sdid" : "976030482",
            "client_ip" : "127.0.0.1",
            }
        ret = HpsAPI(t_Method,t_Param)
        print ret
        self.assertEqual(ret[0],0)

        t_Method = "UnfreezeAccount"
        t_Param = {
            "sdid" : "3238781305",
            "client_ip" : "127.0.0.1",
            }
        ret = HpsAPI(t_Method,t_Param)
        print ret
        self.assertEqual(ret[0],0)

    def test_UnfreezeAccount(self):
        if self._TestFlag['test_UnfreezeAccount'] == False :
            return

    def test_TradeAccount(self):
        if self._TestFlag['test_TradeAccount'] == False :
            return
        t_Method = "FreezeAccount"
        t_Param = {
            "sdid" : "3238781305",
            "client_ip" : "127.0.0.1",
            }
        ret = HpsAPI(t_Method,t_Param)
        print ret
        self.assertEqual(ret[0],0)

        t_Method = "TradeAccount"
        t_Param = {
            "sdid" : "3238781305",
            "client_ip" : "127.0.0.1",
            "phone" : "18501735725",
            "pass_word" : "abc123456789",
            "customer_acc" : "weizijuntestc2c",
            }
        ret = HpsAPI(t_Method,t_Param)
        print ret
        self.assertEqual(ret[0],0)


    def test_SoldAccountVerify(self):
        if self._TestFlag['test_SoldAccountVerify'] == False :
            return
        t_Method = "SoldAccountVerify"
        t_Param = {
            "sdid" : "3238781305",
            "client_ip" : "127.0.0.1",
            }
        ret = HpsAPI(t_Method,t_Param)
        print ret
        self.assertEqual(ret[0],0)

        t_Result = json.read(ret[1])
        print t_Result["reason"]

    def test_SendVerifySms(self):
        if self._TestFlag['test_SendVerifySms'] == False :
            return
        t_Method = "SendVerifySms"
        t_Param = {
            "validContext" : "1111111111111",
            "validValue" : "775158907",
            "validType" : 3,
            "client_ip" : "127.0.0.1",
            }
        ret = HpsAPI(t_Method,t_Param)
        print ret
        logger.info("test_SendVerifySms:")
        self.assertEqual(ret[0],0)

    def test_SendVerifySms2(self):
        if self._TestFlag['test_SendVerifySms2'] == False :
             return
        t_Method = "SendVerifySms"
        t_Param = {
            "validContext" : "11111111121",
            "validValue" : "18501735725",
            "validType" : 2,
            "client_ip" : "127.0.0.1",
            }
        ret = HpsAPI(t_Method,t_Param)
        print ret

    def test_QuerySndaId(self):
        t_Method = "QuerySndaId"
        t_Param = {
            "type" :"2",
            "value" : "weizijuntestc2c"
            }
        ret = HpsAPI(t_Method,t_Param)
        print ret

    def test_QueryUserInfo(self):
        t_Method = "QueryUserInfo"
        t_Param = {
            "sdid" : "3238781305",
            "type" : "1,2,3",
            }
        ret = HpsAPI(t_Method,t_Param)
        print ret

    def test_QueryInsertMid(self):
        t_Method = "QueryInsertMid"
        t_Param = {
            "phone" : "18501735725"
            }
        ret = HpsAPI(t_Method,t_Param)
        print ret

    def test_QueryRealUserInfo(self):
        t_Method = "RealUserInfo"
        t_Param = {
            "phone" : "18507735725"
        }
        ret = HpsAPI(t_Method,t_Param)
        print ret

class TestGoodsTrade(unittest.TestCase):

    def setUp(self):
        self._TestFlag = {
            'test_GetGoodsStatus' : True,
            'test_GoodsOnShelf' : True,
            'test_ProcessGoods' : True,
            'test_ProcessBuy' : True,
            'test_ProcessTotallyTrade' : True,
            'test_Favorite' : True,
        }

    def test_SearchGoodsList(self):
        t_Param = {
            "state" : 2
        }
        ret = SearchGoodsList(t_Param)
        logger.info("test_SearchGoodsList 1:")
        logger.info("result:%s",ret )
        self.assertEqual(ret[0],0)
        t_Result = json.read(ret[1])
        self.assertTrue(type(t_Result["sum"]) is types.IntType)

        t_Param = {
            "state" : 2,
            "game_id" : 89,
        }
        ret = SearchGoodsList(t_Param)
        logger.info("test_SearchGoodsList 2:")
        logger.info("result:%s",ret )
        self.assertEqual(ret[0],0)
        t_Result = json.read(ret[1])
        self.assertTrue(type(t_Result["sum"]) is types.IntType)

        t_Param = {
            "state" : 2,
            "game_id" : 89,
            "area_id" : 1,
            "group_id" : 1,
        }
        ret = SearchGoodsList(t_Param)
        logger.info("test_SearchGoodsList 3:")
        logger.info("result:%s",ret )
        self.assertEqual(ret[0],0)
        t_Result = json.read(ret[1])
        self.assertTrue(type(t_Result["sum"]) is types.IntType)

        t_Param = {
            "state" : 2,
            "game_id" : 89,
            "area_id" : 1,
            "group_id" : 1,
            "page" : 1,
            "count" : 100
        }
        ret = SearchGoodsList(t_Param)
        logger.info("test_SearchGoodsList 4:")
        logger.info("result:%s",ret )
        self.assertEqual(ret[0],0)
        t_Result = json.read(ret[1])
        self.assertTrue(type(t_Result["sum"]) is types.IntType)

        t_Param = {
            "state" : 2,
            "game_id" : 89,
            "area_id" : 1,
            "group_id" : 1,
            "page" : 1,
            "count" : 100,
            "keyword" : "龙之谷"
        }
        ret = SearchGoodsList(t_Param)
        logger.info("test_SearchGoodsList 5:")
        logger.info("result:%s",ret )
        self.assertEqual(ret[0],0)
        t_Result = json.read(ret[1])
        self.assertTrue(type(t_Result["sum"]) is types.IntType)

        t_Param = {
            "state" : 2,
            "game_id" : 89,
            "area_id" : 1,
            "group_id" : 1,
            "page" : 1,
            "count" : 100,
            "keyword" : "龙之谷",
            "order" : "d",
            "order_type" : "create_time",
        }
        ret = SearchGoodsList(t_Param)
        logger.info("test_SearchGoodsList 6:")
        logger.info("result:%s",ret )
        self.assertEqual(ret[0],0)
        t_Result = json.read(ret[1])
        self.assertTrue(type(t_Result["sum"]) is types.IntType)

        t_Param = {
            "state" : 2,
            "game_id" : 89,
            "area_id" : 1,
            "group_id" : 1,
            "page" : 1,
            "count" : 100,
            "keyword" : "龙之谷",
            "order" : "d",
            "order_type" : "create_time",
            "product_type" : 10,
        }
        ret = SearchGoodsList(t_Param)
        logger.info("test_SearchGoodsList 7:")
        logger.info("result:%s",ret )
        self.assertEqual(ret[0],0)
        t_Result = json.read(ret[1])
        self.assertTrue(type(t_Result["sum"]) is types.IntType)

        t_Param = {
            "state" : 2,
            "game_id" : 89,
            "area_id" : 1,
            "group_id" : 1,
            "page" : 1,
            "count" : 100,
            "keyword" : "龙之谷",
            "order" : "d",
            "order_type" : "create_time",
            "product_type" : 10,
            "price_low" : 1,
            "price_high" : 100
        }
        ret = SearchGoodsList(t_Param)
        logger.info("test_SearchGoodsList 8:")
        logger.info("result:%s",ret )
        self.assertEqual(ret[0],0)
        t_Result = json.read(ret[1])
        self.assertTrue(type(t_Result["sum"]) is types.IntType)

    def test_GetGoodsStatus(self):
        method = "GetGoodsStatus"
        t_Param = {
            "book_id" : "EF51EDAC-8FB2-4C5C-AA2F-C88935FBE15D"
        }
        ret = GoodsAPI(method,t_Param)
        logger.info("test_GetGoodsStatus 1:")
        logger.info("result:%s",ret )
        self.assertTrue(type(ret[0]) is types.IntType)
        if ret[1] != '' :
            t_Result = json.read(ret[1])
            self.assertTrue(type(t_Result["book_id"]) is types.StringType)
            self.assertTrue(type(t_Result["favorite_flag"]) is types.IntType)

        method = "GetAccountDetail"
        t_Param = {
            "sdid" : "1974048456",
            "book_id" : "EF51EDAC-8FB2-4C5C-AA2F-C88935FBE15D"
            }
        ret = GoodsAPI(method,t_Param)
        logger.info("test_GetAccountDetail 2:")
        logger.info("result:%s",ret )
        self.assertTrue(type(ret[0]) is types.IntType)
        if ret[1] != '' :
            t_Result = json.read(ret[1])
            self.assertTrue(type(t_Result["book_id"]) is types.StringType)
            self.assertTrue(type(t_Result["favorite_flag"]) is types.IntType)

    def test_GoodsOnShelf(self):
        method = "GoodsOnShelf"

    def test_ProcessGoods(self):
        if self._TestFlag['test_ProcessGoods'] == False :
            return
        #填写信息
        t_RegisterInfoMethod = "RegisterInfo"
        t_Param = {
            "game_id" : 89,
            "area_id" : 10005,
            "group_id" : 10001,
            "game_name" : "龙之谷",
            "area_name" : "5区",
            "group_name" : "5组",
            "sdpt" : "w195438178",
            "sdid" : "976030482",
            "sdpr" : "w195438178",
            "product_type" : 10,
            "content" : "unit test content",
            "sell_account" : "wzjtestc2c1",
            "sell_password" : "wzjtestc2c1",
            "client_ip" : "127.0.0.1",
            "src_code" : 1
        }
        ret = GoodsAPI(t_RegisterInfoMethod,t_Param)
        logger.info("test_RegisterInfo:")
        logger.info("result:%s",ret )

        self.assertEqual(ret[0],0)
        t_Result = json.read(ret[1])
        self.assertTrue(type(t_Result["book_id"]) is types.StringType)

        t_Bookid = t_Result["book_id"]

        #上传图片
        t_UploadImageMethod = "UploadImage"
        t_Param = {
            "game_id" : 89,
            "area_id" : 10005,
            "group_id" : 10001,
            "sdpt" : "w195438178",
            "sdid" : "976030482",
            "local_path" : "unit test local_path 1",
            "url" : "http://www2.souzhuangbei.com/upload/197404845689-999-11270.jpg",
            "book_id" : t_Bookid,
        }
        ret = GoodsAPI(t_UploadImageMethod,t_Param)
        logger.info("test_UploadImage 1:")
        logger.info("result:%s",ret )
        self.assertEqual(ret[0],0)

        t_Param = {
            "game_id" : 89,
            "area_id" : 10005,
            "group_id" : 10001,
            "sdpt" : "w195438178",
            "sdid" : "976030482",
            "local_path" : "unit test local_path 2",
            "url" : "http://www2.souzhuangbei.com/upload/197404845689-999-11270.jpg",
            "book_id" : t_Bookid,
            }
        ret = GoodsAPI(t_UploadImageMethod,t_Param)
        logger.info("test_UploadImage 2:")
        logger.info("result:%s",ret )
        self.assertEqual(ret[0],0)

        t_Param = {
            "game_id" : 89,
            "area_id" : 10005,
            "group_id" : 10001,
            "sdpt" : "w195438178",
            "sdid" : "976030482",
            "local_path" : "unit test local_path 3",
            "url" : "http://www2.souzhuangbei.com/upload/197404845689-999-11270.jpg",
            "book_id" : t_Bookid,
            }
        ret = GoodsAPI(t_UploadImageMethod,t_Param)
        logger.info("test_UploadImage 3:")
        logger.info("result:%s",ret )
        self.assertEqual(ret[0],0)

        t_Param = {
            "game_id" : 89,
            "area_id" : 10005,
            "group_id" : 10001,
            "sdpt" : "w195438178",
            "sdid" : "976030482",
            "local_path" : "unit test local_path 4",
            "url" : "http://www2.souzhuangbei.com/upload/197404845689-999-11270.jpg",
            "book_id" : t_Bookid,
            }
        ret = GoodsAPI(t_UploadImageMethod,t_Param)
        logger.info("test_UploadImage 4:")
        logger.info("result:%s",ret )
        self.assertEqual(ret[0],0)

        t_Param = {
            "game_id" : 89,
            "area_id" : 10005,
            "group_id" : 10001,
            "sdpt" : "w195438178",
            "sdid" : "976030482",
            "local_path" : "unit test local_path 5",
            "url" : "http://www2.souzhuangbei.com/upload/197404845689-999-11270.jpg",
            "book_id" : t_Bookid,
            }
        ret = GoodsAPI(t_UploadImageMethod,t_Param)
        logger.info("test_UploadImage 5:")
        logger.info("result:%s",ret )
        self.assertEqual(ret[0],0)

        t_Param = {
            "game_id" : 89,
            "area_id" : 10005,
            "group_id" : 10001,
            "sdpt" : "w195438178",
            "sdid" : "976030482",
            "local_path" : "unit test local_path 6",
            "url" : "http://www2.souzhuangbei.com/upload/197404845689-999-11270.jpg",
            "book_id" : t_Bookid,
            }
        ret = GoodsAPI(t_UploadImageMethod,t_Param)
        logger.info("test_UploadImage 6:")
        logger.info("result:%s",ret )
        self.assertEqual(ret[0],0)

        #上架商品
        t_OnShelfMethod = "GoodsOnShelf"
        t_Param = {
            "game_id" : 89,
            "area_id" : 10005,
            "group_id" : 10001,
            "sdpt" : "w195438178",
            "sdid" : "976030482",
            "title" : "unit test title",
            "price" : 100.00,
            "client_ip" : "127.0.0.1",
            "src_code" : 1
        }
        ret = GoodsAPI(t_OnShelfMethod,t_Param)
        logger.info("test_GoodsOnShelf:")
        logger.info("result:%s",ret )
        self.assertEqual(ret[0],0)

        #判定已经可以上架
        t_JudgeGoodsOnShelfMethod = "JudgeGoodsOnShelf"
        t_Param = {
            "judge_result" : 1,
            "user_name" : "weizijun",
            "book_id" : t_Bookid,
            }
        ret = GoodsAPI(t_JudgeGoodsOnShelfMethod,t_Param)
        logger.info("test_JudgeGoodsOnShelf:")
        logger.info("result:%s",ret )
        self.assertEqual(ret[0],0)

        #通过列表查看商品
        t_SearchGoodsListMethod = "SearchGoodsList"
        t_Param = {
            "game_id" : 89,
            "area_id" : 10005,
            "group_id" : 10001,
            "product_type" : 10,
            "state" : 2,
            "page" : 1,
            "count" : 100,
            "keyword" : "test",
            "order" : "d",
            "order_type" : "create_time",
            "price_low" : 99,
            "price_high" : 101
        }
        ret = GoodsAPI(t_SearchGoodsListMethod,t_Param)
        logger.info("test_SearchGoodsList:")
        logger.info("result:%s",ret )
        self.assertEqual(ret[0],0)

        t_Result = json.read(ret[1])
        t_BookIdFlag = False
        data = t_Result["list"]
        for value in data :
            if value["book_id"] == t_Bookid :
                t_BookIdFlag = True
                self.assertEqual(value["game_id"],89)
                self.assertEqual(value["area_id"],10005)
                self.assertEqual(value["group_id"],10001)
                self.assertEqual(value["sdpt"],"w195438178")
                self.assertEqual(value["sdid"],"976030482")
                self.assertEqual(value["product_type"],10)
                self.assertEqual(value["trade_mode"],4)
                self.assertEqual(value["p_name"], "unit test title")
                self.assertEqual(value["total_amount"],100)
                self.assertEqual(value["total_amount"],100)
                self.assertEqual(value["count"],1)
                self.assertEqual(value["price"],100)
                self.assertEqual(value["total_amount"],100)
                self.assertEqual(value["state"],2)
                self.assertTrue(type(value["create_time"]) is types.StringType)

        self.assertTrue(t_BookIdFlag)

        #查看商品
        t_GetGoodsStatusMethod = "GetGoodsStatus"
        t_Param = {
            "book_id" : t_Bookid,
            }
        ret = GoodsAPI(t_GetGoodsStatusMethod,t_Param)
        logger.info("test_GetGoodsStatus:")
        logger.info("result:%s",ret )
        self.assertEqual(ret[0],0)

        t_Result = json.read(ret[1])
        self.assertEqual(t_Result["book_id"],t_Bookid)

        value = t_Result
        self.assertEqual(value["game_id"],89)
        self.assertEqual(value["area_id"],10005)
        self.assertEqual(value["group_id"],10001)
        self.assertEqual(value["sdpt"],"w195438178")
        self.assertEqual(value["sdid"],"976030482")
        self.assertEqual(value["product_type"],10)
        self.assertEqual(value["trade_mode"],4)
        self.assertEqual(value["p_name"], "unit test title")
        self.assertEqual(value["p_tips"], "unit test content")
        self.assertEqual(value["total_amount"],100)
        self.assertEqual(value["total_amount"],100)
        self.assertEqual(value["count"],1)
        self.assertEqual(value["price"],100)
        self.assertEqual(value["total_amount"],100)
        self.assertEqual(value["state"],2)
        self.assertTrue(type(value["create_time"]) is types.StringType)
        self.assertEqual(len(t_Result["image_list"]),5)

        #查看商品详情（带账号密码）
        t_GetAccountDetailMethod = "GetAccountDetail"
        t_Param = {
            "book_id" : t_Bookid,
            "sdid" : "976030482"
            }
        ret = GoodsAPI(t_GetAccountDetailMethod,t_Param)
        logger.info("test_GetAccountDetail:")
        logger.info("result:%s",ret )
        self.assertEqual(ret[0],0)

        t_Result = json.read(ret[1])
        self.assertEqual(t_Result["book_id"],t_Bookid)

        value = t_Result
        self.assertEqual(value["game_id"],89)
        self.assertEqual(value["area_id"],10005)
        self.assertEqual(value["group_id"],10001)
        self.assertEqual(value["sdpt"],"w195438178")
        self.assertEqual(value["sdid"],"976030482")
        self.assertEqual(value["product_type"],10)
        self.assertEqual(value["trade_mode"],4)
        self.assertEqual(value["p_name"], "unit test title")
        self.assertEqual(value["p_tips"], "unit test content")
        self.assertEqual(value["p_account"], "wzjtestc2c1")
        self.assertEqual(value["p_pw"], "wzjtestc2c1")
        self.assertEqual(value["total_amount"],100)
        self.assertEqual(value["total_amount"],100)
        self.assertEqual(value["count"],1)
        self.assertEqual(value["price"],100)
        self.assertEqual(value["total_amount"],100)
        self.assertEqual(value["state"],2)
        self.assertTrue(type(value["create_time"]) is types.StringType)
        self.assertEqual(len(t_Result["image_list"]),5)

        #锁定订单
        t_LockGoodsMethod = "LockGoods"
        t_Param = {
            "sdid" : "1974048456",
            "order_id" : "123456789",
            "book_id" : t_Bookid,
        }
        ret = GoodsAPI(t_LockGoodsMethod,t_Param)
        logger.info("test_LockGoods:")
        logger.info("result:%s",ret )
        self.assertEqual(ret[0],0)

        #解锁订单
        t_UnLockGoodsMethod = "UnLockGoods"
        t_Param = {
            "sdid" : "1974048456",
            "order_id" : "123456789",
            "book_id" : t_Bookid,
            }
        ret = GoodsAPI(t_UnLockGoodsMethod,t_Param)
        logger.info("test_UnLockGoods:")
        logger.info("result:%s",ret )
        self.assertEqual(ret[0],0)

        #下架商品
        t_GoodsOffShelfMethod = "GoodsOffShelf"
        t_Param = {
            "sdid" : "976030482",
            "book_id" : t_Bookid,
            }
        ret = GoodsAPI(t_GoodsOffShelfMethod,t_Param)
        logger.info("test_GoodsOffShelf:")
        logger.info("result:%s",ret )
        self.assertEqual(ret[0],0)

    def test_ProcessBuy(self):
        if self._TestFlag['test_ProcessBuy'] == False :
            return
        #填写信息
        t_RegisterInfoMethod = "RegisterInfo"
        t_Param = {
            "game_id" : 89,
            "area_id" : 10005,
            "group_id" : 10001,
            "game_name" : "龙之谷",
            "area_name" : "5区",
            "group_name" : "5组",
            "sdpt" : "w195438178",
            "sdid" : "976030482",
            "sdpr" : "w195438178",
            "product_type" : 10,
            "content" : "unit test content",
            "sell_account" : "wzjtestc2c1",
            "sell_password" : "wzjtestc2c1",
            "mid_account" : "mid_account",
            "client_ip" : "127.0.0.1",
            "src_code" : 1
        }
        ret = GoodsAPI(t_RegisterInfoMethod,t_Param)
        logger.info("test_RegisterInfo:")
        logger.info("result:%s",ret )

        self.assertEqual(ret[0],0)
        t_Result = json.read(ret[1])
        self.assertTrue(type(t_Result["book_id"]) is types.StringType)

        t_Bookid = t_Result["book_id"]

        #上传图片
        t_UploadImageMethod = "UploadImage"
        t_Param = {
            "game_id" : 89,
            "area_id" : 10005,
            "group_id" : 10001,
            "sdpt" : "w195438178",
            "sdid" : "976030482",
            "local_path" : "unit test local_path 1",
            "url" : "http://www2.souzhuangbei.com/upload/197404845689-999-11270.jpg",
            "book_id" : t_Bookid,
            }
        ret = GoodsAPI(t_UploadImageMethod,t_Param)
        logger.info("test_UploadImage 1:")
        logger.info("result:%s",ret )
        self.assertEqual(ret[0],0)

        t_Param = {
            "game_id" : 89,
            "area_id" : 10005,
            "group_id" : 10001,
            "sdpt" : "w195438178",
            "sdid" : "976030482",
            "local_path" : "unit test local_path 2",
            "url" : "http://www2.souzhuangbei.com/upload/197404845689-999-11270.jpg",
            "book_id" : t_Bookid,
            }
        ret = GoodsAPI(t_UploadImageMethod,t_Param)
        logger.info("test_UploadImage 2:")
        logger.info("result:%s",ret )
        self.assertEqual(ret[0],0)

        t_Param = {
            "game_id" : 89,
            "area_id" : 10005,
            "group_id" : 10001,
            "sdpt" : "w195438178",
            "sdid" : "976030482",
            "local_path" : "unit test local_path 3",
            "url" : "http://www2.souzhuangbei.com/upload/197404845689-999-11270.jpg",
            "book_id" : t_Bookid,
            }
        ret = GoodsAPI(t_UploadImageMethod,t_Param)
        logger.info("test_UploadImage 3:")
        logger.info("result:%s",ret )
        self.assertEqual(ret[0],0)

        t_Param = {
            "game_id" : 89,
            "area_id" : 10005,
            "group_id" : 10001,
            "sdpt" : "w195438178",
            "sdid" : "976030482",
            "local_path" : "unit test local_path 4",
            "url" : "http://www2.souzhuangbei.com/upload/197404845689-999-11270.jpg",
            "book_id" : t_Bookid,
            }
        ret = GoodsAPI(t_UploadImageMethod,t_Param)
        logger.info("test_UploadImage 4:")
        logger.info("result:%s",ret )
        self.assertEqual(ret[0],0)

        t_Param = {
            "game_id" : 89,
            "area_id" : 10005,
            "group_id" : 10001,
            "sdpt" : "w195438178",
            "sdid" : "976030482",
            "local_path" : "unit test local_path 5",
            "url" : "http://www2.souzhuangbei.com/upload/197404845689-999-11270.jpg",
            "book_id" : t_Bookid,
            }
        ret = GoodsAPI(t_UploadImageMethod,t_Param)
        logger.info("test_UploadImage 5:")
        logger.info("result:%s",ret )
        self.assertEqual(ret[0],0)

        t_Param = {
            "game_id" : 89,
            "area_id" : 10005,
            "group_id" : 10001,
            "sdpt" : "w195438178",
            "sdid" : "976030482",
            "local_path" : "unit test local_path 6",
            "url" : "http://www2.souzhuangbei.com/upload/197404845689-999-11270.jpg",
            "book_id" : t_Bookid,
            }
        ret = GoodsAPI(t_UploadImageMethod,t_Param)
        logger.info("test_UploadImage 6:")
        logger.info("result:%s",ret )
        self.assertEqual(ret[0],0)

        #上架商品
        t_OnShelfMethod = "GoodsOnShelf"
        t_Param = {
            "game_id" : 89,
            "area_id" : 10005,
            "group_id" : 10001,
            "sdpt" : "w195438178",
            "sdid" : "976030482",
            "title" : "unit test title",
            "price" : 100.00,
            "client_ip" : "127.0.0.1",
            "src_code" : 1
        }
        ret = GoodsAPI(t_OnShelfMethod,t_Param)
        logger.info("test_GoodsOnShelf:")
        logger.info("result:%s",ret )
        self.assertEqual(ret[0],0)

        #判定已经可以上架
        t_JudgeGoodsOnShelfMethod = "JudgeGoodsOnShelf"
        t_Param = {
            "judge_result" : 1,
            "user_name" : "weizijun",
            "book_id" : t_Bookid,
            }
        ret = GoodsAPI(t_JudgeGoodsOnShelfMethod,t_Param)
        logger.info("test_JudgeGoodsOnShelf:")
        logger.info("result:%s",ret )
        self.assertEqual(ret[0],0)

        #通过列表查看商品
        t_SearchGoodsListMethod = "SearchGoodsList"
        t_Param = {
            "game_id" : 89,
            "area_id" : 10005,
            "group_id" : 10001,
            "product_type" : 10,
            "state" : 2,
            "page" : 1,
            "count" : 100,
            "keyword" : "test",
            "order" : "d",
            "order_type" : "create_time",
            "price_low" : 99,
            "price_high" : 101
        }
        ret = GoodsAPI(t_SearchGoodsListMethod,t_Param)
        logger.info("test_SearchGoodsList:")
        logger.info("result:%s",ret )
        self.assertEqual(ret[0],0)

        t_Result = json.read(ret[1])
        t_BookIdFlag = False
        data = t_Result["list"]
        for value in data :
            if value["book_id"] == t_Bookid :
                t_BookIdFlag = True
                self.assertEqual(value["game_id"],89)
                self.assertEqual(value["area_id"],10005)
                self.assertEqual(value["group_id"],10001)
                self.assertEqual(value["sdpt"],"w195438178")
                self.assertEqual(value["sdid"],"976030482")
                self.assertEqual(value["product_type"],10)
                self.assertEqual(value["trade_mode"],4)
                self.assertEqual(value["p_name"], "unit test title")
                self.assertEqual(value["total_amount"],100)
                self.assertEqual(value["total_amount"],100)
                self.assertEqual(value["count"],1)
                self.assertEqual(value["price"],100)
                self.assertEqual(value["total_amount"],100)
                self.assertEqual(value["state"],2)
                self.assertTrue(type(value["create_time"]) is types.StringType)

        self.assertTrue(t_BookIdFlag)

        #查看商品
        t_GetGoodsStatusMethod = "GetGoodsStatus"
        t_Param = {
            "book_id" : t_Bookid,
            }
        ret = GoodsAPI(t_GetGoodsStatusMethod,t_Param)
        logger.info("test_GetGoodsStatus:")
        logger.info("result:%s",ret )
        self.assertEqual(ret[0],0)

        t_Result = json.read(ret[1])
        self.assertEqual(t_Result["book_id"],t_Bookid)

        value = t_Result
        self.assertEqual(value["game_id"],89)
        self.assertEqual(value["area_id"],10005)
        self.assertEqual(value["group_id"],10001)
        self.assertEqual(value["sdpt"],"w195438178")
        self.assertEqual(value["sdid"],"976030482")
        self.assertEqual(value["product_type"],10)
        self.assertEqual(value["trade_mode"],4)
        self.assertEqual(value["p_name"], "unit test title")
        self.assertEqual(value["p_tips"], "unit test content")
        self.assertEqual(value["total_amount"],100)
        self.assertEqual(value["total_amount"],100)
        self.assertEqual(value["count"],1)
        self.assertEqual(value["price"],100)
        self.assertEqual(value["total_amount"],100)
        self.assertEqual(value["state"],2)
        self.assertTrue(type(value["create_time"]) is types.StringType)
        self.assertEqual(len(t_Result["image_list"]),5)

        #查看商品详情（带账号密码）
        t_GetAccountDetailMethod = "GetAccountDetail"
        t_Param = {
            "book_id" : t_Bookid,
            "sdid" : "976030482"
        }
        ret = GoodsAPI(t_GetAccountDetailMethod,t_Param)
        logger.info("test_GetAccountDetail:")
        logger.info("result:%s",ret )
        self.assertEqual(ret[0],0)

        t_Result = json.read(ret[1])
        self.assertEqual(t_Result["book_id"],t_Bookid)

        value = t_Result
        self.assertEqual(value["game_id"],89)
        self.assertEqual(value["area_id"],10005)
        self.assertEqual(value["group_id"],10001)
        self.assertEqual(value["sdpt"],"w195438178")
        self.assertEqual(value["sdid"],"976030482")
        self.assertEqual(value["product_type"],10)
        self.assertEqual(value["trade_mode"],4)
        self.assertEqual(value["p_name"], "unit test title")
        self.assertEqual(value["p_tips"], "unit test content")
        self.assertEqual(value["p_account"], "wzjtestc2c1")
        self.assertEqual(value["p_pw"], "wzjtestc2c1")
        self.assertEqual(value["total_amount"],100)
        self.assertEqual(value["total_amount"],100)
        self.assertEqual(value["count"],1)
        self.assertEqual(value["price"],100)
        self.assertEqual(value["total_amount"],100)
        self.assertEqual(value["state"],2)
        self.assertTrue(type(value["create_time"]) is types.StringType)
        self.assertEqual(len(t_Result["image_list"]),5)

        #购买商品
        t_BuyGoodsMethod = "BuyGoods"
        t_Param = {
            "book_id" : t_Bookid,
            "sdpt" : "gz00098991526.pt",
            "sdid" : "1974048456",
            "game_id" : 89,
            "area_id" : 10005,
            "group_id" : 10001,
            "game_name" : "龙之谷",
            "area_name" : "5区",
            "group_name" : "5组",
            "mid_account" : "",
            "client_ip" : "127.0.0.1",
            "src_code" : 2,
        }
        ret = TradeAPI(t_BuyGoodsMethod,t_Param)
        logger.info("test_BuyGoods:")
        logger.info("result:%s",ret )
        self.assertEqual(ret[0],0)

        t_Result = json.read(ret[1])
        t_OrderId = t_Result["order_id"]

        value = t_Result
        self.assertEqual(value["order_type"],5)
        self.assertEqual(t_Result["book_id"],t_Bookid)
        self.assertEqual(value["total_price"],"100.00")
        self.assertEqual(value["price"],"100.00")
        self.assertEqual(value["num"],"1")
        self.assertEqual(value["b_matrix_id"],"89-10005-10001")
        self.assertEqual(value["s_matrix_id"],"89-10005-10001")
        self.assertEqual(value["buyer_ptaccount"],"gz00098991526.pt")
        self.assertEqual(value["seller_ptaccount"],"w195438178")
        self.assertEqual(value["product_name"], "unit test title")
        self.assertEqual(value["goods_type"],10)
        self.assertEqual(value["product_tips"], "unit test content")
        self.assertTrue(type(value["create_time"]) is types.StringType)
        self.assertEqual(value["status"],"1")

        #关闭订单
        t_CloseOrderMethod = "CloseOrder"
        t_Param = {
            "order_id" : t_OrderId,
            "sdid" : "1974048456",
        }
        ret = TradeAPI(t_CloseOrderMethod,t_Param)
        logger.info("test_CloseOrder:")
        logger.info("result:%s",ret )
        self.assertEqual(ret[0],0)

        time.sleep(15)

        #下架商品
        t_GoodsOffShelfMethod = "GoodsOffShelf"
        t_Param = {
            "sdid" : "976030482",
            "book_id" : t_Bookid,
            }
        ret = GoodsAPI(t_GoodsOffShelfMethod,t_Param)
        logger.info("test_GoodsOffShelf:")
        logger.info("result:%s",ret )
        self.assertEqual(ret[0],0)

    def test_ProcessTotallyTrade(self):
        if self._TestFlag['test_ProcessTotallyTrade'] == False :
            return
        #填写信息
        t_RegisterInfoMethod = "RegisterInfo"
        t_Param = {
            "game_id" : 89,
            "area_id" : 10005,
            "group_id" : 10001,
            "game_name" : "龙之谷",
            "area_name" : "5区",
            "group_name" : "5组",
            "sdpt" : "w195438178",
            "sdid" : "976030482",
            "sdpr" : "w195438178",
            "product_type" : 10,
            "content" : "unit test content",
            "sell_account" : "wzjtestc2c1",
            "sell_password" : "wzjtestc2c1",
            "client_ip" : "127.0.0.1",
            "src_code" : 1
        }
        ret = GoodsAPI(t_RegisterInfoMethod,t_Param)
        logger.info("test_RegisterInfo:")
        logger.info("result:%s",ret )

        self.assertEqual(ret[0],0)
        t_Result = json.read(ret[1])
        self.assertTrue(type(t_Result["book_id"]) is types.StringType)

        t_Bookid = t_Result["book_id"]

        #上传图片
        t_UploadImageMethod = "UploadImage"
        t_Param = {
            "game_id" : 89,
            "area_id" : 10005,
            "group_id" : 10001,
            "sdpt" : "w195438178",
            "sdid" : "976030482",
            "local_path" : "unit test local_path 1",
            "url" : "http://www2.souzhuangbei.com/upload/197404845689-999-11270.jpg",
            "book_id" : t_Bookid,
            }
        ret = GoodsAPI(t_UploadImageMethod,t_Param)
        logger.info("test_UploadImage 1:")
        logger.info("result:%s",ret )
        self.assertEqual(ret[0],0)

        #上架商品
        t_OnShelfMethod = "GoodsOnShelf"
        t_Param = {
            "game_id" : 89,
            "area_id" : 10005,
            "group_id" : 10001,
            "sdpt" : "w195438178",
            "sdid" : "976030482",
            "title" : "unit test title",
            "price" : 100.00,
            "client_ip" : "127.0.0.1",
            "src_code" : 1
        }
        ret = GoodsAPI(t_OnShelfMethod,t_Param)
        logger.info("test_GoodsOnShelf:")
        logger.info("result:%s",ret )
        self.assertEqual(ret[0],0)

        #判定已经可以上架
        t_JudgeGoodsOnShelfMethod = "JudgeGoodsOnShelf"
        t_Param = {
            "judge_result" : 1,
            "user_name" : "weizijun",
            "book_id" : t_Bookid,
            }
        ret = GoodsAPI(t_JudgeGoodsOnShelfMethod,t_Param)
        logger.info("test_JudgeGoodsOnShelf:")
        logger.info("result:%s",ret )
        self.assertEqual(ret[0],0)

        #通过列表查看商品
        t_SearchGoodsListMethod = "SearchGoodsList"
        t_Param = {
            "game_id" : 89,
            "area_id" : 10005,
            "group_id" : 10001,
            "product_type" : 10,
            "state" : 2,
            "page" : 1,
            "count" : 100,
            "keyword" : "test",
            "order" : "d",
            "order_type" : "create_time",
            "price_low" : 99,
            "price_high" : 101
        }
        ret = GoodsAPI(t_SearchGoodsListMethod,t_Param)
        logger.info("test_SearchGoodsList:")
        logger.info("result:%s",ret )
        self.assertEqual(ret[0],0)

        t_Result = json.read(ret[1])
        t_BookIdFlag = False
        data = t_Result["list"]
        for value in data :
            if value["book_id"] == t_Bookid :
                t_BookIdFlag = True
                self.assertEqual(value["game_id"],89)
                self.assertEqual(value["area_id"],10005)
                self.assertEqual(value["group_id"],10001)
                self.assertEqual(value["sdpt"],"w195438178")
                self.assertEqual(value["sdid"],"976030482")
                self.assertEqual(value["product_type"],10)
                self.assertEqual(value["trade_mode"],4)
                self.assertEqual(value["p_name"], "unit test title")
                self.assertEqual(value["total_amount"],100)
                self.assertEqual(value["total_amount"],100)
                self.assertEqual(value["count"],1)
                self.assertEqual(value["price"],100)
                self.assertEqual(value["total_amount"],100)
                self.assertEqual(value["state"],2)
                self.assertTrue(type(value["create_time"]) is types.StringType)

        self.assertTrue(t_BookIdFlag)

        #查看商品
        t_GetGoodsStatusMethod = "GetGoodsStatus"
        t_Param = {
            "book_id" : t_Bookid,
            }
        ret = GoodsAPI(t_GetGoodsStatusMethod,t_Param)
        logger.info("test_GetGoodsStatus:")
        logger.info("result:%s",ret )
        self.assertEqual(ret[0],0)

        t_Result = json.read(ret[1])
        self.assertEqual(t_Result["book_id"],t_Bookid)

        value = t_Result
        self.assertEqual(value["game_id"],89)
        self.assertEqual(value["area_id"],10005)
        self.assertEqual(value["group_id"],10001)
        self.assertEqual(value["sdpt"],"w195438178")
        self.assertEqual(value["sdid"],"976030482")
        self.assertEqual(value["product_type"],10)
        self.assertEqual(value["trade_mode"],4)
        self.assertEqual(value["p_name"], "unit test title")
        self.assertEqual(value["p_tips"], "unit test content")
        self.assertEqual(value["total_amount"],100)
        self.assertEqual(value["total_amount"],100)
        self.assertEqual(value["count"],1)
        self.assertEqual(value["price"],100)
        self.assertEqual(value["total_amount"],100)
        self.assertEqual(value["state"],2)
        self.assertTrue(type(value["create_time"]) is types.StringType)

        #查看商品详情（带账号密码）
        t_GetAccountDetailMethod = "GetAccountDetail"
        t_Param = {
            "book_id" : t_Bookid,
            "sdid" : "976030482"
        }
        ret = GoodsAPI(t_GetAccountDetailMethod,t_Param)
        logger.info("test_GetAccountDetail:")
        logger.info("result:%s",ret )
        self.assertEqual(ret[0],0)

        t_Result = json.read(ret[1])
        self.assertEqual(t_Result["book_id"],t_Bookid)

        value = t_Result
        self.assertEqual(value["game_id"],89)
        self.assertEqual(value["area_id"],10005)
        self.assertEqual(value["group_id"],10001)
        self.assertEqual(value["sdpt"],"w195438178")
        self.assertEqual(value["sdid"],"976030482")
        self.assertEqual(value["product_type"],10)
        self.assertEqual(value["trade_mode"],4)
        self.assertEqual(value["p_name"], "unit test title")
        self.assertEqual(value["p_tips"], "unit test content")
        self.assertEqual(value["p_account"], "wzjtestc2c1")
        self.assertEqual(value["p_pw"], "wzjtestc2c1")
        self.assertEqual(value["total_amount"],100)
        self.assertEqual(value["total_amount"],100)
        self.assertEqual(value["count"],1)
        self.assertEqual(value["price"],100)
        self.assertEqual(value["total_amount"],100)
        self.assertEqual(value["state"],2)
        self.assertTrue(type(value["create_time"]) is types.StringType)

        #购买商品
        t_BuyGoodsMethod = "BuyGoods"
        t_Param = {
            "book_id" : t_Bookid,
            "sdpt" : "gz00098991526.pt",
            "sdid" : "1974048456",
            "game_id" : 89,
            "area_id" : 10005,
            "group_id" : 10001,
            "game_name" : "龙之谷",
            "area_name" : "5区",
            "group_name" : "5组",
            "mid_account" : "",
            "client_ip" : "127.0.0.1",
            "src_code" : 2,
            }
        ret = TradeAPI(t_BuyGoodsMethod,t_Param)
        logger.info("test_BuyGoods:")
        logger.info("result:%s",ret )
        self.assertEqual(ret[0],0)

        t_Result = json.read(ret[1])
        t_OrderId = t_Result["order_id"]

        value = t_Result
        self.assertEqual(value["order_type"],5)
        self.assertEqual(t_Result["book_id"],t_Bookid)
        self.assertEqual(value["total_price"],"100.00")
        self.assertEqual(value["price"],"100.00")
        self.assertEqual(value["num"],"1")
        self.assertEqual(value["b_matrix_id"],"89-10005-10001")
        self.assertEqual(value["s_matrix_id"],"89-10005-10001")
        self.assertEqual(value["buyer_ptaccount"],"gz00098991526.pt")
        self.assertEqual(value["seller_ptaccount"],"w195438178")
        self.assertEqual(value["product_name"], "unit test title")
        self.assertEqual(value["goods_type"],10)
        self.assertEqual(value["product_tips"], "unit test content")
        self.assertTrue(type(value["create_time"]) is types.StringType)
        self.assertEqual(value["status"],"1")

        #手动更改状态为已付款
        ret = SimulatePayConfrim(t_OrderId)
        self.assertEqual(ret,1)

        #后台通过认证
        t_JudgeGoodsBuyMethod = "JudgeGoodsBuy"
        t_Param = {
            "judge_result" : 1,
            "user_name" : "weizijun",
            "order_id" : t_OrderId,
            }
        ret = TradeAPI(t_JudgeGoodsBuyMethod,t_Param)
        logger.info("test_JudgeGoodsOnBuy:")
        logger.info("result:%s",ret )
        self.assertEqual(ret[0],0)

        #买家确认收货
        t_ConfirmBuyMethod = "ConfirmBuy"
        t_Param = {
            "order_id" : t_OrderId,
            "sdid" : "1974048456"
        }
        ret = TradeAPI(t_ConfirmBuyMethod,t_Param)
        logger.info("test_ConfirmBuy:")
        logger.info("result:%s",ret )
        self.assertEqual(ret[0],0)

        t_Result = json.read(ret[1])
        self.assertEqual(t_Result["book_id"],t_Bookid)

        value = t_Result
        self.assertEqual(value["game_id"],89)
        self.assertEqual(value["area_id"],10005)
        self.assertEqual(value["group_id"],10001)
        self.assertEqual(value["sdpt"],"w195438178")
        self.assertEqual(value["sdid"],"976030482")
        self.assertEqual(value["product_type"],10)
        self.assertEqual(value["trade_mode"],4)
        self.assertEqual(value["p_name"], "unit test title")
        self.assertEqual(value["p_tips"], "unit test content")
        self.assertEqual(value["p_account"], "wzjtestc2c1")
        self.assertEqual(value["p_pw"], "wzjtestc2c1")
        self.assertEqual(value["p_sdpt"], "za00098991226.pt")
        self.assertEqual(value["p_sdid"], "1974048156")
        self.assertEqual(value["total_amount"],100)
        self.assertEqual(value["total_amount"],100)
        self.assertEqual(value["count"],1)
        self.assertEqual(value["price"],100)
        self.assertEqual(value["total_amount"],100)
        self.assertEqual(value["state"],4)
        self.assertTrue(type(value["create_time"]) is types.StringType)

        #修改账号密码信息

    def test_TradeList(self):
        t_TradeListMethod = "TradeList"
        t_Param = {
            "buy_type" : 1,
            "game_id" : 89,
            "result_type" : "all",
            #"sdid" : "gz00098991526.pt"
            "sdid" : "1974048456"
        }
        ret = TradeAPI(t_TradeListMethod,t_Param)
        logger.info("test_TradeList:")
        logger.info("result:%s",ret )
        self.assertEqual(ret[0],0)

    def test_CollectFavorite(self):
        t_TradeListMethod = "CollectFavorite"
        t_Param = {
            "book_id" : "3CB7FB7F-23FF-4ECD-9970-B55E2ACEAD08",
            "sdpt" : "gz00098991526.pt",
            "sdid" : "1974048456",
        }
        ret = GoodsAPI(t_TradeListMethod,t_Param)
        logger.info("test_CollectFavorite:")
        logger.info("result:%s",ret )
        self.assertEqual(ret[0],0)

    def test_QueryFavorite(self):
        t_TradeListMethod = "QueryFavorite"
        t_Param = {
            "sdid" : "1974048456",
            }
        ret = GoodsAPI(t_TradeListMethod,t_Param)
        logger.info("test_CollectFavorite:")
        logger.info("result:%s",ret )
        self.assertEqual(ret[0],0)

    def test_QueryIsFavorite(self):
        t_TradeListMethod = "QueryIsFavorite"
        t_Param = {
            "book_id" : "3CB7FB7F-23FF-4ECD-9970-B55E2ACEAD08",
            "sdid" : "1974048456",
            }
        ret = GoodsAPI(t_TradeListMethod,t_Param)
        logger.info("test_QueryIsFavorite:")
        logger.info("result:%s",ret )
        self.assertEqual(ret[0],0)

    def test_DeleteFavorite(self):
        t_TradeListMethod = "DeleteFavorite"
        t_Param = {
            "book_id" : "EF51EDAC-8FB2-4C5C-AA2F-C88935FBE15D",
            "sdid" : "1974048456",
            }
        ret = GoodsAPI(t_TradeListMethod,t_Param)
        logger.info("test_DeleteFavorite:")
        logger.info("result:%s",ret )
        self.assertEqual(ret[0],0)

    def test_ProcessFavorite(self):
        if self._TestFlag["test_Favorite"] == False :
            return

        #通过列表查看商品
        t_SearchGoodsListMethod = "SearchGoodsList"
        t_Param = {
            "state" : 2,
        }
        ret = GoodsAPI(t_SearchGoodsListMethod,t_Param)
        logger.info("test_SearchGoodsList:")
        logger.info("result:%s",ret )
        self.assertEqual(ret[0],0)

        t_Result = json.read(ret[1])
        t_BookId = ""
        data = t_Result["list"]
        for value in data :
            if value["sdid"] != "1974048456" :
                t_BookId = value["book_id"]

        #收藏商品
        t_TradeListMethod = "CollectFavorite"
        t_Param = {
            "book_id" : t_BookId,
            "sdpt" : "gz00098991526.pt",
            "sdid" : "1974048456",
            }
        ret = GoodsAPI(t_TradeListMethod,t_Param)
        logger.info("test_CollectFavorite:")
        logger.info("result:%s",ret )
        self.assertEqual(ret[0],0)

        #查询收藏列表
        t_TradeListMethod = "QueryFavorite"
        t_Param = {
            "sdid" : "1974048456",
        }
        ret = GoodsAPI(t_TradeListMethod,t_Param)
        logger.info("test_CollectFavorite:")
        logger.info("result:%s",ret )
        self.assertEqual(ret[0],0)

        t_Result = json.read(ret[1])
        t_BookIdFlag = False
        data = t_Result["list"]
        for value in data :
            if value["book_id"] == t_BookId :
                t_BookIdFlag = True
                self.assertEqual(value["state"],2)
                self.assertTrue(type(value["create_time"]) is types.StringType)

        self.assertTrue(t_BookIdFlag)

        #查询是否收藏了该物品
        t_TradeListMethod = "QueryIsFavorite"
        t_Param = {
            "book_id" : t_BookId,
            "sdid" : "1974048456",
            }
        ret = GoodsAPI(t_TradeListMethod,t_Param)
        logger.info("test_QueryIsFavorite:")
        logger.info("result:%s",ret )
        self.assertEqual(ret[0],0)

        t_Result = json.read(ret[1])
        self.assertTrue(t_Result["favorite_flag"] == 1)

        #删除收藏
        t_TradeListMethod = "DeleteFavorite"
        t_Param = {
            "book_id" : t_BookId,
            "sdid" : "1974048456",
            }
        ret = GoodsAPI(t_TradeListMethod,t_Param)
        logger.info("test_DeleteFavorite:")
        logger.info("result:%s",ret )
        self.assertEqual(ret[0],0)



if __name__ == '__main__':
    #TestGoodsTrade.main()
    TestAPI.main()

