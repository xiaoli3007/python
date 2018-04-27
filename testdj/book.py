#coding:utf-8
from __future__ import unicode_literals
import random
from testdj.wsgi import *
import json
from urllib import unquote
import hashlib  ,types
import os, sys, getopt
from django.utils import timezone
from calc.models import Video,User,Book
from django.core.exceptions import ObjectDoesNotExist
from django.utils.http import urlquote
import shutil

import sys
reload(sys)
sys.setdefaultencoding("utf-8")

def sting_utf8(text):
    return text.decode('utf8')

def sting_utf82(text):
    return text.encode('utf8')
def gbkutf8(text):
    _str = unquote(text)
    _str = _str.decode('gbk').encode('utf-8')
    return _str

def md5s(text):
    if type(text) is types.StringType:
        m = hashlib.md5()
        m.update(text)
        return m.hexdigest()
    else:
        return ''

def get_filename(photo,fuhao):
    wenhao = photo.find(fuhao)
    if wenhao != -1:
        address = photo[0:wenhao]
    else:
        address = photo

    return address

def get_FileSize(filePath):

    # filePath = unicode(filePath, 'utf8')
    fsize = os.path.getsize(filePath)
    fsize = fsize/float(1024*1024)

    return round(fsize, 2)

def update_photo(file_dir):

    file = open(file_dir)  # 返回一个文件对象
    for line in file:
        # print line,
        line = line.strip('\n')
        guid = md5s(sting_utf82(line))
        print (guid)
        title = sting_utf82(line)
        print (title)
        filepath = '20180328/'+title
        print (filepath)
        try:
            is_exit = Book.objects.get(guid=guid)
        except ObjectDoesNotExist:
            blogphoto = Book(title=title, filepath=filepath, guid=guid)
            blogphoto.save()
        # do something
    file.close()



    return True


def main():
    # create_authors()
    photo_dir = 'G:/vdcilad/mulu.txt'
    photo_file = ''
    print("%s" % sys.argv[0])
    process_path = os.path.dirname(sys.argv[0])
    if not process_path:
        process_path = os.getcwd()
    os.chdir(process_path)

    try:
        opts, args = getopt.getopt(sys.argv[1:], "f:d:n:", ["file=", 'dir='])
    except getopt.GetoptError, err:
        print 'getopt except %s' % err
        sys.exit(1)
    for o, a in opts:
        if o in ("-f", "--file"):
            photo_file = a
        elif o in ("-d", "--dir"):
            photo_dir = a

    if photo_dir == '':
        sys.exit(-1)
    # remove_files(photo_dir)
    update_photo(photo_dir)

if __name__ == '__main__':
    main()
    print("Done!")
