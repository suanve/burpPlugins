#!/usr/bin/env python
# -*- coding: utf-8 -*-


'''
    BurpSuite插件开发指南之 Python 篇
'''

import base64
import re
import getpass
import os
import time
from dbexts import dbexts
from burp import IBurpExtender   # 导入 burp 接口
from burp import IProxyListener 
from burp import IHttpListener  # http流量监听类
from java.net import URL    # 导入 Java 库

res_host = re.compile(r'Host: ([^,]*)')
res_path = re.compile(r'(GET|POST) ([^ ]*) HTTP/')

# 按照 Python 类继承的方式实现相关接口
class BurpExtender(IBurpExtender, IProxyListener,IHttpListener):

    def connect(self):
        try:
            dbcfg = os.getcwd()+'/jdbc.ini' 
            # print dbcfg
            self.db = dbexts(cfg=dbcfg)
            self.db.isql("select * from info where id =1")
            return "数据库连接成功"
        except:
            return "数据库连接失败"


    def info_add(self,info):

        sql = "insert info (`datetime`,`username`,`request_body`,`method`,`domain`,`type`) values('{0}','{1}','{2}','{3}','{4}','{5}')".format(info[0],info[1],info[2],info[3],info[4],info[5])
        print sql
        self.db.isql(sql)


    def registerExtenderCallbacks(self, callbacks):
        # code here
        self._callbacks = callbacks
        self._helpers = callbacks.getHelpers() # 通用函数
        self._callbacks.setExtensionName("Hisql")
        print "成功加载插件!"
        print "="*20
        print self.connect()
        print ""
        # register ourselves as an HTTP listener
        callbacks.registerHttpListener(self)
    

        pass

    def processProxyMessage(self, messageIsRequest, message):
        pass

    def processHttpMessage(self, toolFlag, messageIsRequest, messageInfo):
        request = messageInfo.getRequest()
        analyzedRequest = self._helpers.analyzeResponse(request)
        request_header = analyzedRequest.getHeaders()   #请求包的结构
        username = getpass.getuser()
        
        try:
            method, path = res_path.findall(request_header[0])[0]
            host = res_host.findall(request_header[1])[0]
            url = method+" "+host+path
        except:
            url = ""

        info = [
            time.time(),
            username,
            base64.b64encode(request),
            method,
            host,
            toolFlag
        ]
        self.info_add(info)
