__author__ = 'weizijun.mike'


import requests
import sys
import random
import unittest
from settings import *
from common import *
import json
import types
import time

def Login(num) :
    s = requests.Session()
    url = 'http://m.souzhuangbei.com/api/accountapi/gamelogin?num=%d' % num
    s.get(url)
    return s

def GoodsAPI(session,method,param) :
    url = "http://m.souzhuangbei.com/api/accountapi/goods?method="
    url += method
    url += "&params="+json.write(param)

    session.get(url)
    return session.text

def TradeAPI(session,method,param) :
    url = "http://m.souzhuangbei.com/api/accountapi/trade?method="
    url += method
    url += "&params="+json.write(param)

    session.get(url)
    return session.text

def HpsAPI(session,method,param) :
    url = "http://m.souzhuangbei.com/api/accountapi/hps?method="
    url += method
    url += "&params="+json.write(param)

    session.get(url)
    return session.text

def ConfigAPI(session,method,param) :
    url = "http://m.souzhuangbei.com/api/accountapi/config?method="
    url += method
    url += "&params="+json.write(param)

    session.get(url)
    return session.text

class TestAPI(unittest.TestCase) :
    def setUp(self):
        self._TestFlag = {
            'test_SendVerifySms' : False,
            'test_SendVerifySms2' : False,
            'test_FreezeAccount' : False,
            'test_TradeAccount' : False,
            }

    def test_RealInfoPhone(self):
        t_Method = "RealInfoPhone"
        t_Param = {
            "sdid" : self._TestAccount_wei["sdid"],
            "client_ip" : self._client_ip,
            }
        ret = HpsAPI(t_Method,t_Param)

        logger.info("test_RealInfoPhone:")
        logger.info("result:%s",ret )

        self.assertEqual(ret[0],0)

    def test_QueryAllGameAccount(self):
        t_Method = "QueryAllGameAccount"
        t_Param = {
            "sdid" : self._TestAccount_wei["sdid"],
            "client_ip" : self._client_ip,
            }
        ret = HpsAPI(t_Method,t_Param)
        logger.info("test_QueryAllGameAccount:")
        logger.info("result:%s",ret )
        self.assertEqual(ret[0],0)

    def test_FreezeAccount(self):
        if self._TestFlag['test_FreezeAccount'] == False :
            return
        t_Method = "FreezeAccount"
        t_Param = {
            "sdid" : self._TestAccount_wei["sdid"],
            "client_ip" : self._client_ip,
            }
        ret = HpsAPI(t_Method,t_Param)
        logger.info("test_FreezeAccount:")
        logger.info("result:%s",ret )
        self.assertEqual(ret[0],0)

        t_Method = "UnfreezeAccount"
        t_Param = {
            "sdid" : self._TestAccount_wei["sdid"],
            "client_ip" : self._client_ip,
            }
        ret = HpsAPI(t_Method,t_Param)
        logger.info("test_UnFreezeAccount:")
        logger.info("result:%s",ret )
        self.assertEqual(ret[0],0)

    def test_TradeAccount(self):
        if self._TestFlag['test_TradeAccount'] == False :
            return
        t_Method = "FreezeAccount"
        t_Param = {
            "sdid" : self._TestAccount_wei["sdid"],
            "client_ip" : self._client_ip,
            }
        ret = HpsAPI(t_Method,t_Param)
        logger.info("test_TradeAccount test_FreezeAccount:")
        logger.info("result:%s",ret )
        self.assertEqual(ret[0],0)

        t_Method = "TradeAccount"
        t_Param = {
            "sdid" : self._TestAccount_wei["sdid"],
            "client_ip" : self._client_ip,
            "phone" : "18501735725",
            "pass_word" : "abc123456789",
            "customer_acc" : "weizijuntestc2c",
            }
        ret = HpsAPI(t_Method,t_Param)
        logger.info("test_TradeAccount:")
        logger.info("result:%s",ret )
        self.assertEqual(ret[0],0)

    def test_SoldAccountVerify(self):
        t_Method = "SoldAccountVerify"
        t_Param = {
            "sdid" : "976030482",#self._TestAccount_wei["sdid"],
            "client_ip" : self._client_ip,
            }
        ret = HpsAPI(t_Method,t_Param)
        logger.info("test_SoldAccountVerify:")
        logger.info("result:%s",ret )
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
        logger.info("test_SendVerifySms:")
        logger.info("result:%s",ret )
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
        logger.info("test_SendVerifySms2:")
        logger.info("result:%s",ret )
        self.assertEqual(ret[0],0)

    def test_QuerySndaId(self):
        t_Method = "QuerySndaId"
        t_Param = {
            "type" :"2",
            "value" : self._TestAccount_wei["sdpt"],
            }
        ret = HpsAPI(t_Method,t_Param)
        logger.info("test_QuerySndaId:")
        logger.info("result:%s",ret )
        self.assertEqual(ret[0],0)

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

if __name__ == '__main__':
    pass