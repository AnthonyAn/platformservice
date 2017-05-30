# -*- coding:utf-8 -*-
# FileName: campus.py
# Author: 沈永亮
# Data: 2017/5/27

import sys
sys.path.append("..")
import global_data
from wechatmsg import receive, reply
import time
import requests
import json

login_url="http://42.244.42.160/university-facade/Murp/sdLogin"
get_schedule_url="http://42.244.42.160/university-facade/Schedule/ScheduleList"
data={}

def init():
    global stuid,password,name,phone,count,issign
    stuid=global_data.get_data('stu_id')
    name=global_data.get_data('name')
    password=global_data.get_data('password')
    phone=global_data.get_data('phone')
    issign=global_data.get_data('issign')
    count=global_data.get_data('count')

def login(toUser, fromUser):
    """登录函数"""
    init()
    payload={"u":stuid,"tec":"android:5.1","type":"110","p":password,"ver":110,"uuid":"868773020177369"}
    try:
        r=requests.post(login_url,data=json.dumps(payload),headers={'User-Agent': 'okhttp/3.3.1','Content-Type': 'application/json; charset=utf-8','Content-Length': "138",'Host': '42.244.42.160','Connection': 'Keep-Alive','Accept-Encoding': 'gzip'})
        data['token']=r.json()['data']['token']
        data['status']=True

    except Exception as e:
        data['status']=False

def get_schedule(toUser, fromUser):
    login(toUser, fromUser)
    try:
        payload={"token":data['token']}
        r=requests.get(get_schedule_url,params=payload)
        data['slist']=r.json()['data']['slist']
        data['wlist']=r.json()['data']['wlist']
    except Exception as e:
        return

def today_schedule(toUser, fromUser):
    get_schedule(toUser, fromUser)
    if(data['status']==False):
        content = "学号和密码不匹配，请发送 [密码-你的密码] 修正！"
        replyMsg = reply.TextMsg(
            toUser, fromUser, content)
        return replyMsg.send()
    kc=[]
    if(data.has_key('slist')):

        if len(data['slist'])==0:
            content = "【今日课程】\n无"
            replyMsg = reply.TextMsg(
                toUser, fromUser, content)
            return replyMsg.send()
        for s in data['slist']:
            try:
                if s['kcmc'].encode("utf-8") not in kc:
                    kc.append(s['kcmc'].encode("utf-8"))
            except:
                pass
        content = "【今日课程】\n"+"\n".join(kc)
        replyMsg = reply.TextMsg(
            toUser, fromUser, content)
        return replyMsg.send()