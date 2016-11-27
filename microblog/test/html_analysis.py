# -*- coding:UTF-8 -*-
#!/usr/bin/python3

'''
Script Name     : downLoadImage.py
Author          : svoid
Created         : 2015-03-14
Last Modified   :
Version         : 1.0
Modifications   :
Description     : 网站爬取图片
'''
import sys
import threading
import requests
from app.common.stringfiler import fliter_n_r
from bs4 import BeautifulSoup

import os
from testconfig import UPLOAD_FOLDER
import Queue
from work_test6 import workers
"""
Description    : 获取图片地址
@param pageUrl : 网页URL
@return : 图片地址列表
"""

def getfilelist(pageUrl):
    web = requests.get(pageUrl)
    soup = BeautifulSoup(web.text)
    filelist=[]
    for photos in soup.find_all('div',{'class':'cont'}):
        for photo in photos.find_all('img'):
            wenhao = photo.get('src').find("?")
            if wenhao != -1:
                address = photo.get('src')[0:wenhao]
            else:
                address = photo.get('src')
            filelist.append(address)
    #        filelist.append(photo.get('data-original'))
    return filelist

"""
Description    : 获取图片标题
@param pageUrl : 网页URL
@return : 图片标题
"""

def getfiletitle(pageUrl):
    web = requests.get(pageUrl)
    soup = BeautifulSoup(web.text)
    title= soup.title.string
    return fliter_n_r(title)

def getweblist(webUrl):
    web = requests.get(webUrl)
    soup = BeautifulSoup(web.text)
    weblist=[]
    for pagelist in soup.find_all('div',{'class':'g-mn'}):
        for link in pagelist.find_all('a',{'class':'indexlink'}):
            if link.get('href') != '#':
                address = link.get('href')
                weblist.append(address)
    return weblist

if __name__ == "__main__":
    # reload(sys)
    # sys.setdefaultencoding('utf-8')

    webUrl = 'http://shajia3007.lofter.com/'
    singurl = 'http://shajia3007.lofter.com/post/2a928a_cd3b114'
    list = getweblist(webUrl)
    queueLock = threading.Lock()
    q = Queue.Queue(len(list))
    threads = []
    threadID = 1

    # 创建新线程
    for _ in xrange(1):
        worker = workers(q,queueLock)
        worker.start()
        threads.append(worker)
        threadID += 1

    queueLock.acquire()
    num=1
    for page in reversed(list):
        imagetitle=getfiletitle(page)
        imagelist=getfilelist(page)
        # aaa = imagetitle.strip().encode('utf-8')
        # aaa = aaa.decode('utf-8')
        # print(type(aaa))
        # filepath = UPLOAD_FOLDER + aaa + "/"
        # print(filepath)
        # os.makedirs(filepath)
        # print(imagetitle)
        yuanzu =(imagetitle,imagelist,num)
        q.put(yuanzu, block=True, timeout=None)  # 产生任务消息
        num += 1
    queueLock.release()
    print("***************leader:等待完成!")

    # 等待所有线程完成
    for t in threads:
        t.join()
    print("***************leader:所有任务完成!")
