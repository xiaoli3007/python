# -*- coding:UTF-8 -*-
import Queue
import cookielib
import threading
import time
import urllib2

import os
from app.common.string import md5
from config import basedir
from pillow_image import IsValidImage


#队列的列子

class worker(threading.Thread):

    def __init__(self, queue,queueLock):
     threading.Thread.__init__(self)
     self.queue = queue
     self.thread_stop = False
     self.queuelock = queueLock
    def run(self):
        while not self.thread_stop:
            print("thread%d %s: 等待任务" % (self.ident, self.name))
            try:
                task = self.queue.get(block=True, timeout=20)  # 接收消息
            except Queue.Empty:
                print("没事儿了回家了")
                self.thread_stop = True
                break
            self.queuelock.acquire()
            print("task recv:%s ,task No:%s" % (task[0], task[1]))
            print("我在工作")
            for url in task[1]:
                path = os.path.join(basedir, 'uploads3\\')
                filepath = path + str(task[2]) + "\\"
                if os.path.exists(filepath) is False:
                    os.makedirs(filepath)
                name = md5(url) + ".jpg"
                imgaefile = filepath + name
                '''
                response = requests.get(url, stream=True)
                data = response.content
                '''
                if os.path.exists(imgaefile) is False or IsValidImage(imgaefile) is False:
                    try:
                        # 保存文件时候注意类型要匹配，如要保存的图片为jpg，则打开的文件的名称必须是jpg格式，否则会产生无效图片
                        cj = cookielib.LWPCookieJar()
                        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
                        urllib2.install_opener(opener)
                        req = urllib2.Request(url)
                        operate = opener.open(req)
                        data = operate.read()
                    except:
                        print('网络发生异常' + imgaefile)
                        continue
                    else:
                        f = open(imgaefile, 'wb')
                        f.write(data)
                        f.close()
            print("工作完成!")
            self.queue.task_done()  # 完成一个任务
            res = self.queue.qsize()  # 判断消息队列大小
            if res > 0:
                print("fuck!There are still %d tasks to do" % (res))
            self.queuelock.release()
            time.sleep(3)

    def stop(self):
        self.thread_stop = True

if __name__ == "__main__":
    pass
    # q = Queue.Queue(3)
    # worker = worker(q)
    # worker.start()
    # q.put(["produce one cup!", 1], block=True, timeout=None)  # 产生任务消息
    # q.put(["produce one desk!", 2], block=True, timeout=None)
    # q.put(["produce one apple!", 3], block=True, timeout=None)
    # q.put(["produce one banana!", 4], block=True, timeout=None)
    # q.put(["produce one bag!", 5], block=True, timeout=None)
    # print("***************leader:等待完成!")
    # q.join()  # 等待所有任务完成
    # print("***************leader:所有任务完成!")