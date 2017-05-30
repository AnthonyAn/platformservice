import requests
import json

headers={
'User-Agent': 'okhttp/3.3.1',
'Content-Type': 'application/json; charset=utf-8',
'Content-Length': "138",
'Host': '42.244.42.160',
'Connection': 'Keep-Alive',
'Accept-Encoding': 'gzip',
}

login_url="http://42.244.42.160/university-facade/Murp/sdLogin"
globledata={}


def login():
    """登录函数"""
    payload={
    "u":"1527406047",
    "tec":"android:5.1",
    "type":"110",
    "p":"8f551eeae06774d8b4f33d0a267a2491",
    "ver":110,
    "uuid":"868773020177369"}
    r=requests.post(login_url,data=json.dumps(payload),headers=headers)
    print(r.text)

login()