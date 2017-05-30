# -*- coding:utf-8 -*-
# FileName: signin.py
# Author: 沈永亮
# Data: 2017/5/27

import sys
sys.path.append("..")
import global_data
from wechatmsg import receive, reply
import psycopg2
import time
import requests
import hashlib
from haodong import autotest


def init():
    global stuid,password,name,phone,count,issign
    stuid=global_data.get_data('stu_id')
    name=global_data.get_data('name')
    password=global_data.get_data('password')
    phone=global_data.get_data('phone')
    issign=global_data.get_data('issign')
    count=global_data.get_data('count')

def connectdb(dbname='wechat'):
    global conn,cur
    conn = psycopg2.connect(
        host="localhost", user="postgres", database=dbname)
    cur = conn.cursor()


def signin(toUser, fromUser):
    init()

    if issign == "1":
        content = name + "同学，你是不是傻啦？你不是已经找过床小协签了到了么？赶紧学习去，别调戏我啦~"
        replyMsg = reply.TextMsg(toUser, fromUser, content)
        return replyMsg.send()
    if( int(time.strftime("%H")) > 7 ):
        content = name+"同学，我很严肃地告诉你，现在是白天，好好学习，不要来调戏床小协啦~记得明天早晨来找我~"
        replyMsg = reply.TextMsg(toUser, fromUser, content)
        return replyMsg.send()
    if (int(time.strftime("%H")) == 7 and int(time.strftime("%M")) > 20 ):
        content = name+"同学，我很严肃地告诉你，现在是白天，好好学习，不要来调戏床小协啦~记得明天早晨来找我~"
        replyMsg = reply.TextMsg(toUser, fromUser, content)
        return replyMsg.send()
    if( int(time.strftime("%H")) < 6 ):
        content = name+"同学，天还早，再睡一会吧！养足精神，才有干劲！"
        replyMsg = reply.TextMsg(toUser, fromUser, content)
        return replyMsg.send()

    connectdb()
    cur.execute("UPDATE student SET count=(%s),issign=(%s) WHERE userid=(%s)",(count+1,"1",toUser))
    conn.commit()
    cur.close()
    conn.close()
    title = "打卡成功 | "+"new！绑定网关密码体验更多功能！输入 密码+'网关密码' 即可绑定。"
    descri = "已获得阳光：" + \
        "☀" * count
    Picurl = "http://www.suda.edu.cn/upload/scene/201705/20170517104218.jpg"
    url = "http://www.wxhand.com/addon/MessageBoard/WapMessageBoard/lists/hmp/67c3b1d0dad251173d1f2127ef7e26d4.html"
    replyMsg = reply.NewsMsg(
        toUser, fromUser, Picurl, title, descri, url)
    return replyMsg.send()

def rankinfo(toUser, fromUser):

    class rank():
        name=''
        count=0
        def __init__(self,name,count):
            self.name=name
            self.count=count
        def __str__(self):
            return "/:rose {0:^11} --> {1:3d}\n".format(self.name,self.count)

    ranklist=[]
    connectdb()
    cur.execute("SELECT * FROM student ORDER BY count desc")
    rows=cur.fetchall()
    
    content="🌟 早睡早起的床小协~\n🌟 21天早起榜单~\n\n"
    cur.close()
    conn.close()

    connectdb("wakeup")
    cur.execute("SELECT name,count FROM(SELECT user_phone,COUNT(*) FROM (SELECT user_phone FROM sign_in WHERE sign_in_time > timestamp '2017-4-24') temp GROUP BY(user_phone) ORDER BY count DESC) t,users WHERE user_phone=phone")
    rows2=cur.fetchall()
    cur.close()
    conn.close()

    for row in rows:
      ranki=rank(row[1], row[4])
      ranklist.append(ranki)

    for row in rows2:
      ranki=rank(row[0], row[1])
      ranklist.append(ranki)

    ranklist.sort(key=lambda obj:obj.count, reverse=True) 
    for item in ranklist:
      if item.count<2:
          continue
      content+=str(item)
    content+="\n🌟 愿你不辜负每一个清晨！"
    replyMsg = reply.TextMsg(toUser, fromUser, content)
    return replyMsg.send()

def signininfo(toUser, fromUser):
    init()
    para = {'format': 'js', 'idx': -1, 'n': 1}
    pho = requests.get("http://cn.bing.com/HPImageArchive.aspx", params=para)
    print pho.json()
    Picurl = "http://s.cn.bing.net" + \
        pho.json()['images'][0]['url']
    connectdb()
    cur.close()
    conn.close()
    title = "MORNING | 最最棒的"+name+"，请继续加油！"
    descri = pho.json()['images'][0]['copyright'].encode("utf-8").split('(')[1].strip(')')+"\n\n打卡天数："+str(count)+"\n已经获得阳光：" + \
        "☀" * count
    url = "http://www.wxhand.com/addon/MessageBoard/WapMessageBoard/lists/hmp/67c3b1d0dad251173d1f2127ef7e26d4.html"
    replyMsg = reply.NewsMsg(
        toUser, fromUser, Picurl, title, descri, url)
    return replyMsg.send()

def haodongtest(hdpwd,toUser, fromUser):
    init()
    try:
        autotest.login(phone,hdpwd)
    except:
        return reply.TextMsg(
            toUser, fromUser,"密码与账号不匹配，请核实好动校园密码！\n账号："+phone+"\n密码："+hdpwd).send()
    try:
        autotest.init_exam() 
        autotest.get_exampaper()
        autotest.exampaper_submit()
        replyMsg = reply.TextMsg(
            toUser, fromUser, "【考试成功】"+"\n最终得分："+autotest.exampaper_submit())
        return replyMsg.send()
    except:
        return reply.TextMsg(
            toUser, fromUser,"考试未开始！").send()

def updatepwd(data,toUser, fromUser):
    m = hashlib.md5()
    m.update(data.encode("gbk"))
    psw = m.hexdigest()
    connectdb()
    cur.execute("UPDATE student SET password=(%s) WHERE userid=(%s)",(psw,toUser))
    conn.commit()
    cur.close()
    conn.close()
    content = "【修改成功】"
    replyMsg = reply.TextMsg(
        toUser, fromUser, content)
    return replyMsg.send()

def daypic(toUser,fromUser):
    para = {'format': 'js', 'idx': -8, 'n': 1}
    pho = requests.get("http://cn.bing.com/HPImageArchive.aspx", params=para)
    Picurl = "http://s.cn.bing.net" + \
        pho.json()['images'][0]['url']
    title = "每日一图 | " + \
        pho.json()['images'][0]['copyright'].encode("utf-8").split('(')[0]
    url = Picurl
    descri = pho.json()['images'][0]['copyright'].encode("utf-8").split('(')[1].strip(')')

    replyMsg = reply.NewsMsg(
        toUser, fromUser, Picurl, title, descri, url)
    return replyMsg.send()