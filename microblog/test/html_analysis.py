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

import requests
from app.common.stringfiler import  fliter_n_r
from bs4 import BeautifulSoup

import os
from config import basedir

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
    reload(sys)
    sys.setdefaultencoding('utf-8')

    webUrl = 'http://shajia3007.lofter.com/'
    singurl = 'http://shajia3007.lofter.com/post/2a928a_cd3b114'
    list = getweblist(webUrl)
    # q = Queue.Queue(len(list))
    # queueLock = threading.Lock()
    # worker = worker(q,queueLock)
    # worker.start()
    # queueLock.acquire()

    num=1
    for page in list:
        imagetitle=getfiletitle(page)
        imagelist=getfilelist(page)

        aaa = imagetitle.strip().encode('utf-8')
        print(type(aaa))
        path = os.path.join(basedir, 'uploads3\\')
        filepath = path + aaa + "\\"
        os.makedirs(filepath)
        # yuanzu =(imagetitle,imagelist,num)
        # q.put(yuanzu, block=True, timeout=None)  # 产生任务消息
        # num += 1
        break
    # queueLock.release()
    # print("***************leader:等待完成!")
    # q.join()  # 等待所有任务完成
    # print("***************leader:所有任务完成!")
