#coding=utf-8

import threading,Queue
import time
from down_images import downimage
from app.models import Photo,PhotoData
from app.string import md5,sting_utf8,sting_utf82

exitFlag = 0

class myThread (threading.Thread):   #继承父类threading.Thread
    def __init__(self, threadID, name,q):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.thread_stop = False
        self.q = q  #线程接的任务

    def run(self):                   #把要执行的代码写到run函数里面 线程在创建后会直接运行run函数
        print "Starting 下载" + str(self.threadID)
        #threadLock.acquire()
        #print_time(self.name, self.counter)
        #downimage(self.imagelist,self.name)
        #threadLock.release()
        process_data(self.name, self.q)
        print "Exiting 结束下载" + str(self.threadID)

    def stop(self):
        self.thread_stop = True

def process_data(threadName, q):
    while not exitFlag:
        queueLock.acquire()
        if not workQueue.empty():
            task = q.get()
            print "%s 的任务 %s" % (threadName, task[1])
            downimage(task[0], task[1])
        queueLock.release()
        #time.sleep(1)

def print_time(threadName, delay):
        print "%s: %s" % (threadName, time.ctime(time.time()))

'''
images32 = ['http://imglf1.nosdn.127.net/img/bXFZeWMrV2orbjQycDhJTHY1dElMeFhyTHc2V2t2YUFJZU5uN2pnTExIRFppUFI4bmVGWWVnPT0.jpg', 'http://imglf.nosdn.127.net/img/bXFZeWMrV2orbjQycDhJTHY1dElML0oxNElPQzB0ZDNtRHZjc090UWN6aExrWUFadjZvcTRBPT0.jpg', 'http://imglf1.nosdn.127.net/img/bXFZeWMrV2orbjQycDhJTHY1dElMOTlEV3NSbXJoRnJVNWVwWTh1cjRVL0g1RTRob0xmQmt3PT0.jpg', 'http://imglf0.nosdn.127.net/img/bXFZeWMrV2orbjQycDhJTHY1dElMMklzcnRnZ2RZbjlQc21hUlZKeGVVSVN4cE5OSHJJZnBnPT0.jpg', 'http://imglf2.nosdn.127.net/img/bXFZeWMrV2orbjQycDhJTHY1dElMNlVtRmFPN1lheTV2S2FFclFBVFpPTElMeHJVMytjVGxRPT0.jpg', 'http://imglf1.nosdn.127.net/img/bXFZeWMrV2orbjQycDhJTHY1dElMODlDOVZVNUQwWWRONXVHQU9Wd05hajJzdE1sSHpNVHpRPT0.jpg', 'http://imglf0.nosdn.127.net/img/bXFZeWMrV2orbjQycDhJTHY1dElMMEVzWlZPaG9LRmprNVRDcGp5TnVYL1Bad01GZVFqaHRnPT0.jpg', 'http://imglf2.nosdn.127.net/img/bXFZeWMrV2orbjQycDhJTHY1dElMOFBEUC9mQXNQcG5xWmE5UXU2Y3NPTlJGbXBnRTRDaWF3PT0.jpg', 'http://imglf2.nosdn.127.net/img/bXFZeWMrV2orbjQycDhJTHY1dElMNHZUVExiOEJyMnQ4RTZDc2VwYjJIRCtndERyam96SWp3PT0.jpg']
'''


phtots = Photo.query.order_by(Photo.id.asc()).filter(Photo.id>350).all()
#phtots = Photo.query.order_by(Photo.id.asc()).all()
'''
for item in phtots:
    print(md5('photp'+str(item.id)))
'''
#threadLock = threading.Lock()
queueLock = threading.Lock()
workQueue = Queue.Queue(len(phtots))

threads =[]
size = len(phtots)/100
# 开启线程
num = 1;
for j in xrange(size):
    # 创建新线程
    thread1 = myThread(num, '工人' + str(num),workQueue)
    # 开启线程
    thread1.start()
    threads.append(thread1)
    num += 1

# 填充队列
queueLock.acquire()

for item in phtots:
    images = item.photodatas.order_by(PhotoData.id.asc()).all()
    #images = item.photodatas.order_by(PhotoData.id.asc()).filter(Photo.filepath=='').all()
    imagelist = []
    for i in images:
        imagelist.append(sting_utf82(i.thumb))
    t_name = "%s%s" % ('photo', str(item.id))
    workQueue.put([imagelist,t_name])
    #print(111)
    #print(imagelist)
    #time.sleep(1)
queueLock.release()


# 等待队列清空
while not workQueue.empty():
    pass

# 通知线程是时候退出
exitFlag = 1

for a in threads:
    a.join()

print '任务结束: ' + time.strftime('%H:%M:%S') + "\n"