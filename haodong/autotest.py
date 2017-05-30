# -*- coding:utf-8 -*-
# FileName: autotest.py
# Author: 沈永亮
# Data: 2017/5/27

import requests
import json

headers={'User-agent':'Mozilla/5.0 (Linux; U; Android 2.3.7; en-us; Nexus One Build/FRF91) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1'}
login_url="http://appsrv.ihodoo.com/login"
init_exam_url="http://appsrv.ihodoo.com/auth/exam/enterIndex"
get_exampaper_url="http://appsrv.ihodoo.com/auth/exam/start/"
problem_submit_url="http://appsrv.ihodoo.com/auth/exam/select"
exampaper_submit_url="http://appsrv.ihodoo.com/auth/exam/submit"
data={}


def login(username,password):
    """登录函数"""
    payload={"username":username,"password":password}
    r=requests.post(login_url,data=payload,headers=headers)
    data['token']=r.json()["token"]
    data["uid"]=r.json()["uid"]
    data["sno"]=r.json()["sno"]
    data['name']=r.json()["bindDto"]["name"]

def init_exam():
    payload={"uid":data["uid"],"token":data["token"]}
    r=requests.get(init_exam_url,params=payload)
    data["id"]=r.json()["id"]
    data["examPaperId"]=r.json()["examPaperId"]
    data["totalSubCount"]=r.json()["totalSubCount"]

def get_exampaper():
    payload={"uid":data["uid"],"token":data["token"],"totalSubCount":data["totalSubCount"]}
    r=requests.get(get_exampaper_url+"/"+data["id"]+"/"+data["examPaperId"],params=payload)
    get_subid_answer(r.json()["dtos"])

def get_subid_answer(problem_list):
    for problem_item in problem_list:
        answers=[]
        subid=str(problem_item['subid'])
        for ans in problem_item['answers']:
            answers.append(ans['optionValue'])
        ",".join(answers)
        problem_item_submit(subid,answers)

def problem_item_submit(subid,answers):
    payload={'selectOptions':answers,"token":data["token"]}
    r=requests.get(problem_submit_url+"/"+data["examPaperId"]+"/"+subid,params=payload)

def exampaper_submit():
    payload={"token":data["token"],"uid":data["uid"]}
    r=requests.get(exampaper_submit_url+"/"+data["examPaperId"],params=payload)
    return str(r.json()["score"])