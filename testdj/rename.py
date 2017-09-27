#coding:utf-8
import random
import json
from urllib import unquote
import hashlib  ,types
import os, sys, getopt
db_charset = 'utf8'
file_charset = 'utf8'

def utf8_to_file_charset(u8str):
    """utf8到本地文件字符集"""
    # 数据库编目和代码相同,不用转换
    if file_charset == 'utf8':
        return u8str
    else:
        return u8str.decode('utf-8', 'ignore').encode(file_charset, 'ignore')


def file_charset_to_utf8(fstr):
    """本地字符集到utf8"""
    if file_charset == 'utf8':
        return fstr
    else:
        return fstr.decode('gbk', 'ignore').encode('utf-8', 'ignore')


def utf8_to_db_charset(u8str):
    """utf8到本地文件字符集"""
    # 数据库编目和代码相同,不用转换
    if db_charset == 'utf8':
        return u8str
    else:
        return u8str.decode('utf-8', 'ignore').encode(file_charset)


def db_charset_to_utf8(dbstr):
    """本地字符集到utf8"""
    if db_charset == 'utf8':
        return dbstr.encode('utf8')
    else:
        return dbstr.decode('gbk', 'ignore').encode('utf-8')

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
    wenhao = photo.find(fuhao, -1)
    if wenhao != -1:
        address = photo[0:wenhao]
    else:
        address = photo

    return address

def safe_rename(src_file_path, dst_file_path):
    try:
        if os.path.exists(dst_file_path):
            os.remove(dst_file_path)
        os.rename(src_file_path, dst_file_path)
    except Exception, err:
        print 'safe_rename except: ', err
        rv = False
    else:
        rv = True
    finally:
        if os.path.exists(src_file_path):
            rv = False
            # os.remove(utf8_to_file_charset(b64_file_path))
    return rv

def file_rename(file):

    # filepath222 = "%s" % (file)

    # basename = get_filename(file, "\\")
    basename = os.path.basename(file)
    dir = os.path.dirname(file)

    src_file_path = "%s\%s" % (dir, basename)
    dst_file_path = file_charset_to_utf8("%s\%s" % (dir, basename))

    # safe_rename(src_file_path, dst_file_path)
    print(dst_file_path)

    return True

def directory_rename(dir):

    # filepath222 = "%s" % (dir)
    # print(filepath222)
    g = os.walk(dir)

    # dirs2 = os.listdir(dir)
    # for file1 in dirs2:
    #     filepath1 = "%s\%s" % (dir, file1)
    #     if os.path.isfile(filepath1):
    #         print (gbkutf8(file1))
    #         safe_rename(filepath1, gbkutf8(filepath1))

    for path, d, filelist in g:
        for item in d:

            dir_name = os.path.join(path, item)
            dirs = os.listdir(dir_name)
            for file in dirs:
                filepath = "%s" % (dir_name)
                filepath2 = "%sggg" % (gbkutf8(dir_name))
                print (filepath)
                print (filepath2)
                # os.rename(filepath, filepath2)
                # safe_rename(filepath,filepath2 )
                # print (gbkutf8(file))
    return True

def main():
    # create_authors()
    dir = 'G:\\aaa\\'
    file = None
    # file = 'G:\\aaa\\广东小鲜肉微信约炮童颜小网红第5期屌到死去活来720P无水印完整版 - 成人视频 成人.flv'
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
            file = a
        elif o in ("-d", "--dir"):
            dir = a
    if file is None and dir is None:
        print('请输入参数')
        sys.exit(1)
    if file is not None:
        file_rename(file)
    if dir is not None:
        directory_rename(dir)

if __name__ == '__main__':
    main()
    print("Done!")
