# -*- coding:utf-8 -*-
# Title:autopackage


try:
    import os
    import re
    import sys
    import json
    import thread
    import traceback
    import inspect
    import random
    from burp import IBurpExtender, IContextMenuFactory, IScannerCheck, IScanIssue
    from burp import IHttpListener, IHttpRequestResponse
    from array import array
    from javax.swing import JMenu
    from javax.swing import JMenuItem
except ImportError:
    print "Failed to load dependencies. This issue may be caused by using the unstable Jython 2.7 beta."


reload(sys)
sys.setdefaultencoding('utf-8')


VERSION = "0.1"
Auther = "suanve"
Blog = "http://xiaokou.top"
helpers = None
callbacks = None
extension_enable = False
DEBUG = True



class BurpExtender(IBurpExtender, IContextMenuFactory, IHttpListener, IHttpRequestResponse):
    def registerExtenderCallbacks(self, this_callbacks):
        global callbacks, helpers
        self.messages = []
        self.menusConf = {}
        callbacks = this_callbacks
        helpers = callbacks.getHelpers()
        callbacks.setExtensionName('AutoPackage')
        callbacks.registerContextMenuFactory(self)  

    def getBodyFromBytes(self, isRequest, rawBytes):
        """Extracts the body bytes from a request or response raw bytes.
        Returns a byte[] containing the body of the request or response.

        Args:
        * isRequest (bool): Set to true if rawBytes is a request. false if it's a
            response.
        * rawBytes (byte[]): Raw bytes containing the request or response.
        """
        info = self.getInfoFromBytes(isRequest, rawBytes)
        print info
        return rawBytes[info.getBodyOffset()]

    

    def createMenuItems(self, invocation):
        self.invocation = invocation
        ctx = invocation.getToolFlag()
        if ctx in [64]:
            self.menus = []
            self.menus.append(
                JMenuItem("Change body encoding to json", actionPerformed=self.bodytojson))
            self.menus.append(JMenuItem(
                "Change body encoding to multipart", actionPerformed=self.bodytomultipart))

            return self.menus if self.menus else None

    

    def bodytomultipart(self, bu):
        
        currentRequest = self.invocation.getSelectedMessages()[0]
        requestInfo = helpers.analyzeRequest(
            currentRequest)  
        self.headers = list(requestInfo.getHeaders())
        message = currentRequest.getRequest().tostring()
        data = message.split("\n")
        for x in range(len(data)):
            if "Content-Type" in data[x]:
                data[x] = "Content-Type: multipart/form-data; boundary=---------------------------3628390971530629446582491509"

        Body = """

-----------------------------3628390971530629446582491509
Content-Disposition: form-data; name="file"; filename="a.png"
Content-Type: image/png
        
PNG 

-----------------------------3628390971530629446582491509
Content-Disposition: form-data; name="submit"

提交
-----------------------------3628390971530629446582491509--       
"""

        newMessage = "\n".join(data)
        newMessage += Body
        currentRequest.setRequest(newMessage)

    def bodytojson(self, bu):
        currentRequest = self.invocation.getSelectedMessages()[0]
        requestInfo = helpers.analyzeRequest(
            currentRequest)  
        self.headers = list(requestInfo.getHeaders())
        message = currentRequest.getRequest().tostring()
        Type = re.findall(
            r"(application\/json|application\/x-www-form-urlencoded)", message)[0]
        print(Type)
        if Type == 'application/json':
            data = message.split("\n")

            print data
            DataFlag = 0
            for x in range(len(data)):
                if "Content-Type" in data[x]:
                    data[x] = "Content-Type: application/x-www-form-urlencoded"

                if re.compile(r'\{.*\:.*\}').match(data[x]):
                    post_data = data[x]
                    DataFlag = x

            PostData = ""

            a = {}
            for p in post_data[1:-1].split(","):
                a[p.split(":")[0]] = p.split(":")[
                    1][1:-1] if re.match("^[\"\'].*[\"\']$", p.split(":")[1]) else p.split(":")[1]

            for k in a.keys():
                PostData += "{0}={1}&".format(k[1:-1], a[k])

            data[DataFlag] = str(PostData)[:-1]
            newMessage = "\n".join(data)
            
            currentRequest.setRequest(newMessage)

        elif Type == 'application/x-www-form-urlencoded':
            data = message.split("\n")
            print message

            DataFlag = 0
            for x in range(len(data)):
                if "Content-Type" in data[x]:
                    data[x] = "Content-Type: application/json"

                if re.compile(r'\S+\=\S+').match(data[x]):
                    post_data = data[x]
                    DataFlag = x

            PostData = {}
            s = ['{']
            for post_key_value in post_data.split("&"):
                if post_key_value == '':
                    continue
                post_k_v = post_key_value.split('=')
                s.append('"{0}":"{1}",'.format(post_k_v[0], post_k_v[1]))
            s.append("}")
            data[DataFlag] = str("".join(s)).replace(",}", "}")
            newMessage = "\n".join(data)
            
            currentRequest.setRequest(newMessage)

