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

def update_photo(file_dir):
    print(file_dir)
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
                # print (type(filepath))
                guid  = md5s(sting_utf82(filepath))
                # print (guid)

                try:
                    is_exit = Video.objects.get(guid=guid)
                except ObjectDoesNotExist:
                    print(name)
                    print(type(name))
                    blogphoto = Video(title=sting_utf82(name), filepath=sting_utf82(filepath), guid=guid, add_time=timezone.now(), user=user1)
                    blogphoto.save()
                # break
            # new_name =int(item.encode('utf-8'))+739
            # print(type(new_name))
            # print(new_name)
            # os.rename(os.path.join(path, item), os.path.join(path, '%d'%new_name ))
        # for filename in filelist:
        #     print os.path.join(path, filename)

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

    update_photo(photo_dir)

if __name__ == '__main__':
    main()
    print("Done!")
