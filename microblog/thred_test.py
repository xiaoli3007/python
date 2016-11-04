#!/usr/bin/python
# -*- coding: UTF-8 -*-

import threading
import time
from down_images import downimage

class myThread (threading.Thread):   #继承父类threading.Thread
    def __init__(self, threadID, name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
    def run(self):                   #把要执行的代码写到run函数里面 线程在创建后会直接运行run函数
        print "Starting 下载" + self.name
        #print_time(self.name, self.counter)
        downimage(self.name)
        print "Exiting 结束下载" + self.name

def print_time(threadName, delay):

        print "%s: %s" % (threadName, time.ctime(time.time()))


images = ['http://imglf1.nosdn.127.net/img/bXFZeWMrV2orbjQycDhJTHY1dElMeFhyTHc2V2t2YUFJZU5uN2pnTExIRFppUFI4bmVGWWVnPT0.jpg', 'http://imglf.nosdn.127.net/img/bXFZeWMrV2orbjQycDhJTHY1dElML0oxNElPQzB0ZDNtRHZjc090UWN6aExrWUFadjZvcTRBPT0.jpg', 'http://imglf1.nosdn.127.net/img/bXFZeWMrV2orbjQycDhJTHY1dElMOTlEV3NSbXJoRnJVNWVwWTh1cjRVL0g1RTRob0xmQmt3PT0.jpg', 'http://imglf0.nosdn.127.net/img/bXFZeWMrV2orbjQycDhJTHY1dElMMklzcnRnZ2RZbjlQc21hUlZKeGVVSVN4cE5OSHJJZnBnPT0.jpg', 'http://imglf2.nosdn.127.net/img/bXFZeWMrV2orbjQycDhJTHY1dElMNlVtRmFPN1lheTV2S2FFclFBVFpPTElMeHJVMytjVGxRPT0.jpg', 'http://imglf1.nosdn.127.net/img/bXFZeWMrV2orbjQycDhJTHY1dElMODlDOVZVNUQwWWRONXVHQU9Wd05hajJzdE1sSHpNVHpRPT0.jpg', 'http://imglf0.nosdn.127.net/img/bXFZeWMrV2orbjQycDhJTHY1dElMMEVzWlZPaG9LRmprNVRDcGp5TnVYL1Bad01GZVFqaHRnPT0.jpg', 'http://imglf2.nosdn.127.net/img/bXFZeWMrV2orbjQycDhJTHY1dElMOFBEUC9mQXNQcG5xWmE5UXU2Y3NPTlJGbXBnRTRDaWF3PT0.jpg', 'http://imglf2.nosdn.127.net/img/bXFZeWMrV2orbjQycDhJTHY1dElMNHZUVExiOEJyMnQ4RTZDc2VwYjJIRCtndERyam96SWp3PT0.jpg']
num = 1;
for item in images:
    # 创建新线程
    thread1 = myThread(num, item)
    # 开启线程
    thread1.start()
    #time.sleep(5)
    num = num+1
