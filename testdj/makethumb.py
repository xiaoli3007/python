#coding:utf-8
from __future__ import unicode_literals
import random
from testdj.wsgi import *
import json
from urllib import unquote
import hashlib  ,types
import os, sys, getopt
from django.utils import timezone
from calc.models import Video,User
from django.core.exceptions import ObjectDoesNotExist
from django.utils.http import urlquote
import shutil
from guanfu_video_thumbnail import *
import Queue
import threading
import time



LOG_LEVEL_DICT = {'debug': logging.DEBUG,
                  'info': logging.INFO,
                  'warning': logging.WARNING,
                  'error': logging.ERROR,
                  'critical': logging.CRITICAL}
log_file_path = 'log/testdj.log'

exitFlag = 0

queueLock = threading.Lock()

def sting_utf8(text):
    return text.decode('utf8')

def sting_utf82(text):
    return text.encode('utf8')
def gbkutf8(text):
    _str = unquote(text)
    _str = _str.decode('gbk').encode('utf-8')
    return _str

def file_charset_to_utf8(fstr):
    """本地字符集到utf8"""
    return fstr.decode('gbk', 'ignore').encode('utf-8', 'ignore')

def make_file_thumb(file,file_dir):

    if file_dir=='':
       file_dir = os.path.dirname(file)

    # print (file)
    # print (file_dir)
    ret = functhumb(file, file_dir)
    # print (ret)
    return ret


class myThread (threading.Thread):   #继承父类threading.Thread
    def __init__(self, threadID, name, q):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.thread_stop = False
        self.q = q  #线程接的任务
        # self.log_console_show_flag = 1
        # logger = logging.getLogger()
        # logger.setLevel(LOG_LEVEL_DICT['info'])
        # formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
        #
        # file_log_handle = logging.FileHandler(log_file_path)
        # file_log_handle.setFormatter(formatter)
        # file_log_handle.setLevel(LOG_LEVEL_DICT['info'])
        # logger.addHandler(file_log_handle)
        #
        # if self.log_console_show_flag:
        #     console_log_handle = logging.StreamHandler()
        #     console_log_handle.setFormatter(formatter)
        #     console_log_handle.setLevel(LOG_LEVEL_DICT['info'])
        #     logger.addHandler(console_log_handle)
        #
        # self.logger_object = logger

    def run(self):
        print "Starting 线程开始" + str(self.threadID)
        # process_data(self.name, self.q)
        self.process_data()
        print "Exiting 线程结束" + str(self.threadID)

    def process_data(self):

        global exitFlag
        global queueLock

        print("任务开始的exitFlag %d" % exitFlag)

        # while not self.thread_stop:
        while not exitFlag:
            queueLock.acquire()
            if not self.q.empty():

                print("队列的大小 %d" % self.q.qsize())
                task = self.q.get()
                print "%d===> %s 干的活-->视频路径：%s  图片路径：%s -->exitFlag:%d" % (task[2], self.name, task[0], task[1],exitFlag)
                make_file_thumb(task[0], task[1])
                # time.sleep(4)
                self.q.task_done()
                # logger_object.info(" %s 干的活-->视频路径：%s  图片路径：%s" % (name, task[0], task[1]))
            # else:
            #     self.stop()
            queueLock.release()
            time.sleep(20)

    def stop(self):
        self.thread_stop = True


# def process_data(name, q):
#     print("队列的大小 %d" % q.qsize())
#     global exitFlag
#     while not exitFlag:
#         # if not q.empty():
#             task = q.get()
#             print "%d===> %s 干的活-->视频22路径：%s  图片路径：%s  -->exitFlag:%d" % (task[2], name, task[0], task[1], exitFlag)
#             # make_file_thumb(task[0], task[1])
#             q.task_done()
#             # time.sleep(4)

def print_time(threadName, delay):
    print "%s: %s" % (threadName, time.ctime(time.time()))

def make_file_dir(file_dir, outimagedir):
    # filepath222 = "%s" % (urlquote(file_dir))
    # print(urlquote(file_dir))

    # if outimagedir != '':
    #     wenjian = os.path.basename(item)
    #     outimage = "%s\\%s" % (outimagedir, wenjian)
    # else:
    #     outimage =  item

    phtots = []

    # imagedir = "%s\\imagedir" % (file_dir)

    g = os.walk(file_dir)
    for path, d, filelist in g:
        # print path
        for item in d:

            dir_name = os.path.join(path, item)
            dirs = os.listdir(dir_name)
            for file in dirs:
                filepath = "%s/%s" % (dir_name, file)
                # fileimage_dir = os.path.dirname(filepath)
                # print (filepath)
                # print (fileimage_dir)
                # print (imagedir)
                file_path = os.path.split(filepath)  # 分割出目录与文件
                lists = file_path[1].split('.')  # 分割出文件与文件扩展名
                file_ext = lists[-1]  # 取出后缀名(列表切片操作)
                img_ext5 = ['mp4']

                if file_ext in img_ext5:
                    phtots.append(filepath)
                # ret = functhumb(file, file_dir)
    # print(phtots)



    workQueue = Queue.Queue(len(phtots))
    threads = []
    size = len(phtots) / 100
    # size = 20
    # print(size)
    # return phtots;

    global queueLock
    # 填充队列
    queueLock.acquire()
    wnums = 0
    for item in phtots:
        if outimagedir != '':
            outimage = "%s/%s" % (outimagedir, os.path.basename(item))
        else:
            outimage = item
        workQueue.put([item, outimage, wnums])
        wnums += 1
    queueLock.release()

    # 开启线程
    num = 1;
    for j in xrange(size):
        # 创建新线程
        thread1 = myThread(num, '工人' + str(num), workQueue)
        # 开启线程
        # thread1.setDaemon(True)
        thread1.start()
        threads.append(thread1)
        num += 1

    #单线程
    # thread1 = myThread(num, '工人' + str(num), workQueue)
    # thread1.start()

    print '等待队列清空: ' + time.strftime('%H:%M:%S') + "\n"

    # 等待队列清空
    while not workQueue.empty():
        pass

    global exitFlag
    exitFlag = 1

    print 'exitFlag %d' % ( exitFlag )

    # thread1.join()
    for a in threads:
        a.join()

    print '任务结束: ' + time.strftime('%H:%M:%S') + "\n"

    return True

def main():
    # create_authors()

    photo_file = 'G:\\vdcilad\\hanju\\韩国三级禁止想象【公众号：资源菌】.mp4'
    photo_dirimagefile = 'G:\\vdcilad\\imagedir\\韩国三级禁止想象【公众号：资源菌】.mp4'

    photo_dir = ''
    photo_outdirimage = ''

    print("%s" % sys.argv[0])
    process_path = os.path.dirname(sys.argv[0])
    if not process_path:
        process_path = os.getcwd()
    os.chdir(process_path)

    try:
        opts, args = getopt.getopt(sys.argv[1:], "f:d:n:o:", ["file=", 'dir=', 'outdir='])
    except getopt.GetoptError, err:
        print 'getopt except %s' % err
        sys.exit(1)
    for o, a in opts:
        if o in ("-f", "--file"):
            photo_file = a
        elif o in ("-d", "--dir"):
            photo_dir = a
        elif o in ("-n", "--outdir"):
            photo_outdirimage = a

    if photo_dir == '':
        sys.exit(-1)

    # print(photo_dir)
    # print(photo_outdirimage)
    make_file_dir(photo_dir, photo_outdirimage)
    # make_file_thumb(photo_file, photo_dirimagefile)


if __name__ == '__main__':
    main()
    print("Done!")
