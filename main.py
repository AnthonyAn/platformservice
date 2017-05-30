# -*- coding:utf-8 -*-
# FileName: main.py
# Author: 沈永亮
# Data: 2017/5/27

import web
from handle import Handle

urls = (
    '/wx', 'Handle',
)

if __name__ == '__main__':
    app = web.application(urls, globals())
    app.run()