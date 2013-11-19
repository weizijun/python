#encoding=utf-8

from settings import *
from common import *

import sys
import urllib
import HTMLParser

class CListHTMLParser(HTMLParser.HTMLParser):
    m_ulFlag = False
    m_listData = []

    def handle_starttag(self, tag, attrs):
        #设置列表
        if tag == "ul" :
            for attr in attrs:
                if attr[0] == "class" and attr[1] == "new_ul" :
                    self.m_ulFlag = True

        #设置详情
        if tag == "a" and self.m_ulFlag == True :
            for attr in attrs:
                if attr[0] == "href":
                    self.m_listData.append(attr[1])

    def handle_endtag(self, tag):
        #设置列表
        if self.m_ulFlag == True and tag == "ul" :
            self.m_ulFlag = False
    def get_content(self) :
        return self.m_listData


class CDetailHTMLParser(HTMLParser.HTMLParser):
    m_titleFlag = False
    m_dateFlag = False
    m_contentFlag = False
    m_otherDivFlag = False
    m_content = {
        "title"     : "",
        "date"      : "",
        "content"   : "",
        "real_content" : ""
    }

    def __init__(self):
        HTMLParser.HTMLParser.__init__(self)
        self.m_titleFlag = False
        self.m_dateFlag = False
        self.m_contentFlag = False
        self.m_otherDivFlag = False
        self.m_content = {
            "title"     : "",
            "date"      : "",
            "content"   : ""
        }

    def handle_starttag(self, tag, attrs):
        if tag == "div" :
            for attr in attrs:
                #设置标题
                if attr[0] == "class" and attr[1] == "article_title" :
                    self.m_titleFlag = True
                #设置时间
                elif attr[0] == "class" and attr[1] == "article_date" :
                    self.m_dateFlag = True
                #设置内容
                elif attr[0] == "class" and attr[1] == "article_content" :
                    self.m_contentFlag = True

        if self.m_contentFlag == True and tag == "div" :
            self.m_otherDivFlag = True

        if self.m_contentFlag == True :
            property = ""
            for attr in attrs:
                property += " "+attr[0]+"=\""+attr[1]+"\""
            self.m_content["content"] += "<"+tag+property+" >"



    def handle_endtag(self, tag):
        if self.m_contentFlag == True:
            self.m_content["content"] += "</"+tag+">"

        if self.m_titleFlag == True and tag == "div" :
            self.m_titleFlag = False
        elif self.m_dateFlag == True and tag == "div"  :
            self.m_dateFlag = False
        elif self.m_otherDivFlag == True and tag == "div"  :
            self.m_otherDivFlag = False
        elif self.m_contentFlag == True and tag == "div" :
            self.m_contentFlag = False

    def handle_data(self, data):
        #设置标题
        if self.m_titleFlag == True :
            if  data.strip() :
                self.m_content["title"]  = data
        #设置时间
        elif self.m_dateFlag == True :
            if  data.strip() :
                self.m_content["date"]  = data.strip()
        #设置内容
        elif self.m_contentFlag == True :
            if  data.strip() :
                self.m_content["content"]  += data.strip()
        else :
            pass

    def get_content(self) :
        return self.m_content

def parseList(type) :
    if type == 1 :
        t_url = 'http://cm.sdo.com/web1/news/news_list.asp?CategoryID=3060'
    elif type == 2:
        t_url = 'http://cm.sdo.com/web1/news/news_list.asp?CategoryID=3061'
    elif type == 3 :
        t_url = 'http://cm.sdo.com/web1/news/news_list.asp?CategoryID=3062'
    t_listContent = urllib.urlopen(t_url).read()

    try :
        parser = CListHTMLParser()
        parser.feed(t_listContent)
    except :
        logger.error("parseList error,url:"+t_url)

    for attr in parser.get_content():
        parseDetail(attr,type)

def parseDetail(url,type) :
    t_pos = url.find("../")
    if t_pos != -1 :
        url = url.replace('../','http://cm.sdo.com/web1/')
    else :
        return False

    t_detailContent = urllib.urlopen(url).read()

    try :
        parser = CDetailHTMLParser()
        parser.feed(t_detailContent)
        t_content = parser.get_content()
        insertDetail(t_content,type)
    except :
        logger.error( sys.exc_info())

def insertDetail(content,type) :
    select_sql = "select * from TradeAdmin.newsNotify where title='%s'" % content["title"]
    result = ExecuteSqlQuery(select_sql,GetAdminDbConn())

    if len(result) == 0:
        insert_sql = "REPLACE INTO TradeAdmin.newsNotify (type,title,content,game_id,create_time) VALUES(%d,'%s','%s',%d,'%s')"%(type,content["title"],content["content"],100001700,content["date"]);
        logger.info(insert_sql)
        affected  = ExecuteSql(insert_sql,GetAdminDbConn())
        logger.info("affected: " + str(affected))

if __name__ == "__main__" :
    parseList(1)
    parseList(2)
    parseList(3)



