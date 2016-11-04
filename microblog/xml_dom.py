#!/usr/bin/python
# -*- coding: UTF-8 -*-

from xml.dom.minidom import parse
import xml.dom.minidom
from app.stringfiler import  filter_tags
import json

# 使用minidom解析器打开 XML 文档
DOMTree = xml.dom.minidom.parse("photo.xml")
collection = DOMTree.documentElement
if collection.hasAttribute("shelf"):
    print "Root element : %s" % collection.getAttribute("shelf")
# 在集合中获取所有电影
lists = collection.getElementsByTagName("PostItem")
# 打印每部电影的详细信息
num =1
for info in lists:

    print "*****Movie*****"
    if info.hasAttribute("title"):
        print "Title: %s" % info.getAttribute("title")

    if info.getElementsByTagName('tag'):
        tag = info.getElementsByTagName('tag')[0]
        print "tag: %s" % tag.childNodes[0].data
    if info.getElementsByTagName('caption'):
        caption = info.getElementsByTagName('caption')[0]
        if  caption.childNodes:
            print "caption: %s" % filter_tags(caption.childNodes[0].data)
    if info.getElementsByTagName('photoLinks'):
        photoLinks = info.getElementsByTagName('photoLinks')[0]
        jsonlist = json.loads(photoLinks.childNodes[0].data)
        for item in jsonlist:
            #print "photoLinks: %s" % item['orign']
            wenhao = item['orign'].find("?")
            if  wenhao != -1:
                print item['orign'][0:wenhao]
    publishTime = info.getElementsByTagName('publishTime')[0]
    print "publishTime: %s" % publishTime.childNodes[0].data
    #print(num)
    num = num+1
