# -*- coding:utf-8 -*-
# FileName: global_data.py
# Author: 沈永亮
# Data: 2017/5/27

data={}

def get_data(key, default_value=None):
    '''获得全局变量:键值对'''
    try:
        return data[key]
    except KeyError:
        return default_value


def set_data(key, value):
    '''添加/修改全局变量:键值对'''
    global data
    data[key] = value