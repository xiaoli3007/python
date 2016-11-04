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
import os
import urllib2,cookielib,requests
import threading
from bs4 import BeautifulSoup
import re
from config import basedir
"""
Description    : 将网页图片保存本地
@param imgUrl  : 待保存图片URL
@param imgName : 待保存图片名称
@return 无
"""
def saveImage( imgUrl,imgName ="default.jpg" ):
    '''
    response = requests.get(imgUrl, stream=True)
    image = response.content
    '''
    cj = cookielib.LWPCookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    urllib2.install_opener(opener)
    req = urllib2.Request(imgUrl)
    operate = opener.open(req)
    image = operate.read()

    DstDir = os.path.join(basedir, 'uploads2\\')

    print("保存文件"+DstDir+imgName+"\n")
    try:
        with open(DstDir+imgName ,"wb") as jpg:
            jpg.write( image)
            return
    except IOError:
        print("IO Error\n")
        return
    finally:
        jpg.close

"""
Description    : 开启多线程执行下载任务
@param filelist:待下载图片URL列表
@return 无
"""

def downImageViaMutiThread( filelist ):
    task_threads=[]  #存储线程
    count=1
    for file in filelist:
        filename = file.replace("/","-")
        if 'com-' in filename:
            p = re.compile(r'com-')
            filename = p.split(filename)[1]
            t = threading.Thread(target=saveImage,args=(file,filename))
            count = count+1
            task_threads.append(t)
    for task in task_threads:
        task.start()
    for task in task_threads:
        task.join()

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
    webUrl = 'http://shajia3007.lofter.com/'
    singurl = 'http://shajia3007.lofter.com/post/2a928a_cd3b114'
    list = getweblist(webUrl)
    # downImageViaMutiThread(list)
    for page in list:
        imagelist=getfilelist(page)
        downImageViaMutiThread(imagelist)