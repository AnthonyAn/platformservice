# -*- coding:utf-8 -*-
# FileName: handle.py
# Author: 沈永亮
# Data: 2017/5/27

import web
from wechatmsg import receive,reply
import psycopg2
import global_data
import re
from myfuncs import myfunc,campus
import hashlib


class Handle(object):
    def POST(self):
        webdata = web.data()
        print webdata
        recMsg = receive.parse_xml(webdata)
        toUser = recMsg.FromUserName
        fromUser = recMsg.ToUserName
        conn = psycopg2.connect(
            host="localhost", user="postgres", database="wechat")
        cur = conn.cursor()
        cur.execute("SELECT * FROM student WHERE userid=(%s)", (toUser,))
        userdata = cur.fetchone()
        cur.close()
        conn.close()

        if recMsg.MsgType == 'text':
            '''绑定账号'''
            if recMsg.Content.startswith('绑定'):
                if userdata != None:
                    replycontent = "【已经绑定账号】"
                    return reply.TextMsg(toUser, fromUser, replycontent).send()
                try:
                    data = re.split('-|—| |–|－',recMsg.Content)
                    m = hashlib.md5()
                    m.update(data[4].encode("gbk"))
                    password = m.hexdigest()
                    conn = psycopg2.connect(
                        host="localhost", user="postgres", database="wechat")
                    cur = conn.cursor()
                    cur.execute("INSERT INTO student (userid,name,id,phone,password) VALUES (%s, %s, %s, %s,%s)",(toUser,data[1].decode("utf-8"),data[2],data[3],password))
                    conn.commit()
                    replycontent = "【账号绑定成功】\n姓名："+data[1]+"\n学号："+data[2]+"\n手机："+data[3]
                    return reply.TextMsg(toUser, fromUser, replycontent).send()
                except Exception,e:
                    replycontent = "【绑定失败】\n错误信息："+e.message
                    return reply.TextMsg(toUser, fromUser, replycontent).send()

            '''获取用户数据'''
            if userdata == None:
                replycontent = '''【尚未绑定账号】\n回复 [绑定-姓名-学号-手机-统一认证密码] 完成绑定，体验全部功能。(请你放心，密码已做加密处理)
[早安] 做早起的鸟儿~
[排名] 谁能坚持到底~
[坚持] 查看早起记录~
[今天] 查看今日课程~
\n更多功能,来体验吧！'''
                return reply.TextMsg(toUser, fromUser, replycontent).send()
            else:
                global_data.set_data('stu_id', userdata[2])
                global_data.set_data('name', userdata[1])
                global_data.set_data('password', userdata[6])
                global_data.set_data('phone', userdata[3])
                global_data.set_data('issign', userdata[5])
                global_data.set_data('count', userdata[4])


            '''被动回复逻辑处理'''
            if recMsg.Content=="你好":
                replycontent="你也好"
                return reply.TextMsg(toUser,fromUser,replycontent).send()



            if recMsg.Content=='早安':
                return myfunc.signin(toUser, fromUser)

            if recMsg.Content=='排名':
                return myfunc.rankinfo(toUser, fromUser)

            if recMsg.Content=='坚持':
                return myfunc.signininfo(toUser, fromUser)

            if recMsg.Content.startswith('好动'):
                data = re.split('-|—| |–|－',recMsg.Content)
                return myfunc.haodongtest(data[1],toUser, fromUser)

            if recMsg.Content.startswith('密码'):
                data = re.split('-|—| |–|－',recMsg.Content)
                return myfunc.updatepwd(data[1],toUser, fromUser)

            if recMsg.Content=='今天':
                return campus.today_schedule(toUser, fromUser)

            if recMsg.Content=="每日一图":
                return myfunc.daypic(toUser,fromUser)

            replycontent = '''【WAKEUPCLUB】
[早安] 做早起的鸟儿~
[排名] 谁能坚持到底~
[坚持] 查看早起记录~
[今天] 查看今日课程~
\n更多功能,来体验吧！'''
            return reply.TextMsg(toUser, fromUser, replycontent).send()
