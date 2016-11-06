#coding=utf-8
import os
import unittest
from datetime import datetime, timedelta
from app import app, db
from app.models import Photo,PhotoData
import xml.dom.minidom
from app.stringfiler import  fliter_html,replaceCharEntity
from app.string import  sting_utf82
import json
from pillow_image import IsValidImage

class TestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:123123@localhost/test2'
        db.create_all()

    def tearDown(self):
        db.session.remove()
        #db.drop_all()
    def imageTest(self):
        file ="E:\python_project\microblog\uploads2\photo5\\7b6caebf488be798eb483629eb2a11a2.jpg"
        assert IsValidImage(file)

    def mysql_test(self):
        # 使用minidom解析器打开 XML 文档
        DOMTree = xml.dom.minidom.parse("photo.xml")
        collection = DOMTree.documentElement
        if collection.hasAttribute("shelf"):
            print "Root element : %s" % collection.getAttribute("shelf")
        # 在集合中获取所有电影
        lists = collection.getElementsByTagName("PostItem")
        # 打印每部电影的详细信息
        num = 1
        for info in lists:
            print "*****start*****"
            if info.getElementsByTagName('tag'):
                tag = info.getElementsByTagName('tag')[0]
                title = tag.childNodes[0].data
            if info.getElementsByTagName('caption'):
                caption = info.getElementsByTagName('caption')[0]
                if caption.childNodes:
                   title = replaceCharEntity(caption.childNodes[0].data)
                   #title = 'ffff'
            if info.getElementsByTagName('photoLinks'):
                photoLinks = info.getElementsByTagName('photoLinks')[0]
                jsonlist = json.loads(photoLinks.childNodes[0].data)
                for item in jsonlist:
                    print "photoLinks: %s" % item['orign']
            publishTime = info.getElementsByTagName('publishTime')[0]
            print "publishTime: %s" % publishTime.childNodes[0].data
            if title is None:
                title = 'title+'+num
            u = Photo(title=title[0:200])
            db.session.add(u)
            if jsonlist is not None:
               for item in jsonlist:
                    print "photoLinks: %s" % item['orign']
                    wenhao = item['orign'].find("?")
                    if wenhao != -1:
                        thumb = item['orign'][0:wenhao]
                    else:
                        thumb = item['orign']
                    u2 = PhotoData(thumb=thumb, author=u)
                    db.session.add(u2)
            db.session.commit()
            num = num+1

'''
    def test_make_user(self):
        # create a user and write it to the database
        u = Photo(title = '1111', timestamp = datetime.utcnow() + timedelta(seconds=1))
        db.session.add(u)
        u2 = PhotoData(thumb='aaaaaaaaaaaaaa.jpg', author=u)
        db.session.add(u2)
        db.session.commit()
'''

if __name__ == '__main__':
    unittest.main()