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

    # filepath222 = "%s" % (urlquote(fstr))
    # print(urlquote(fstr))
    #
    # return True
    g = os.walk(file_dir)

    user1 = User.objects.get(id=1)

    for path, d, filelist in g:
        # print path
        for item in d:

            dir_name = os.path.join(path, item)
            dirs = os.listdir(dir_name)
            for file in dirs:
                name = get_filename(file, ".")
                filepath = "%s\%s" % (dir_name, file)
                xiangduifilepath = "%s/%s" % (item, file)
                # print (type(filepath))
                guid  = md5s(sting_utf82(filepath))
                # print (guid)
                try:
                    is_exit = Video.objects.get(guid=guid)
                except ObjectDoesNotExist:
                    print(xiangduifilepath)
                    # print(filepath)
                    # print(type(name))
                    blogphoto = Video(title=sting_utf82(name), filepath=sting_utf82(xiangduifilepath), guid=guid, add_time=timezone.now(), user=user1)
                    blogphoto.save()
                # break
            # new_name =int(item.encode('utf-8'))+739
            # print(type(new_name))
            # print(new_name)
            # os.rename(os.path.join(path, item), os.path.join(path, '%d'%new_name ))
        # for filename in filelist:
        #     print os.path.join(path, filename)

    return True

def remove_files(file_dir):
    # filepath222 = "%s" % (urlquote(file_dir))
    # print(urlquote(file_dir))

    g = os.walk(file_dir)
    for path, d, filelist in g:
        # print path
        for item in d:

            dir_name = os.path.join(path, item)
            dirs = os.listdir(dir_name)
            for file in dirs:
                name = get_filename(file, ".")
                # filepath = "%s\%s" % (dir_name, file)
                filepath = "%s/%s" % (dir_name, file)
                mudidir = "%s\\20171211\\%s" % (file_dir, file)
                mudiflvdir = "%s\\flv\\%s" % (file_dir, file)

                mudi100flvdir = "%s\\100flv\\%s" % (file_dir, file)
                mudi100mp4dir = "%s\\100mp4\\%s" % (file_dir, file)

                # splitext = os.path.splitext(file)
                filesize = get_FileSize(filepath)
                # print (mudidir)

                file_path = os.path.split(filepath)  # 分割出目录与文件
                lists = file_path[1].split('.')  # 分割出文件与文件扩展名
                file_ext = lists[-1]  # 取出后缀名(列表切片操作)
                # img_ext = ['mp4', 'flv', 'avi', 'MP4']
                img_ext2 = ['bmp', 'jpeg', 'gif', 'psd', 'png', 'jpg']
                img_ext3 = ['mp4', 'avi', 'MP4']
                img_ext4 = ['flv']
                img_ext5 = ['mp4']

                if file_ext in img_ext2:
                    print ("%s-->%f" % (filepath, filesize))
                    # os.remove(filepath)

                # if file_ext in img_ext5:
                #     print ("%s-->%f" % (filepath, filesize))
                #     shutil.move(filepath, mudidir)
                # else:
                #     print ("%s-->%f" % (filepath, filesize))
                #     shutil.move(filepath, mudiflvdir)

                # if file_ext in img_ext3:
                #     if filesize < 100:
                #         print ("%s-->%f" % (filepath, filesize))
                #         shutil.move(filepath, mudi100mp4dir)
                #     else:
                #         print ("%s-->%f" % (filepath, filesize))
                #         shutil.move(filepath, mudidir)
                #
                # if file_ext in img_ext4:
                #     if filesize < 100:
                #         print ("%s-->%f" % (filepath, filesize))
                #         shutil.move(filepath, mudi100flvdir)
                #     else:
                #         print ("%s-->%f" % (filepath, filesize))
                #         shutil.move(filepath, mudiflvdir)

                    # os.remove(filepath)
                    # shutil.move(filepath, mudiflvdir)

                # try:
                #     is_exit = Video.objects.get(guid=guid)
                # except ObjectDoesNotExist:
                #     print(name)
                #     print(type(name))

    return True

def main():
    # create_authors()
    photo_dir = 'G:\\vdcilad'
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

    remove_files(photo_dir)
    # update_photo(photo_dir)

if __name__ == '__main__':
    main()
    print("Done!")
