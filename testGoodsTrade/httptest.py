__author__ = 'weizijun.mike'


import requests

s = requests.Session()

s.get("http://m.souzhuangbei.com/api/accountapi/gamelogin")
r = s.get("http://m.souzhuangbei.com/api/accountapi/config?method=QueryAccount")

print r.text
