# -*- coding:utf-8 -*-
"""
 3. 一些常用函数
"""
import os
import sqlobject
import logging
import sqlobject.main
from sqlobject.sqlbuilder import *
import time
from datetime import datetime
import glob
import hashlib
import MySQLdb
import json

db_charset = 'utf8'
file_charset = 'utf8'
local_name = ''
LOG_LEVEL_DICT = {'debug': logging.DEBUG,
                  'info': logging.INFO,
                  'warning': logging.WARNING,
                  'error': logging.ERROR,
                  'critical': logging.CRITICAL}

filename_filter_dict = {'?': '', ':': '', '*': '', '\\': '', '/': '', '<': '', '>': '', '|': '', '"': ''}

###########################################################################################
#  数据库定义
###########################################################################################

#######################################################################################
# tool function
#######################################################################################

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


def safe_makedirs(dirname):
    try:
        if not os.path.isdir(dirname):
            os.makedirs(dirname)
    except Exception, err:
        print "makedir except:%s", err
        return False
    else:
        return True


def safe_unicode(body, enc):
    try:
        bd = body.decode(enc)
    except UnicodeDecodeError, e:
        #        print e
        return None
    else:
        return bd


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


def safe_remove(file_path):
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
            return True
    except Exception, err:
        print 'safe_rename except: %s ', err
        return False


def files(curr_dir='.', ext='*.*'):
    """当前目录下的文件"""
    for i in glob.glob(os.path.join(curr_dir, ext)):
        yield i


def all_files(rootdir, ext):
    """当前目录下以及子目录的文件"""
    for name in os.listdir(rootdir):
        if os.path.isdir(os.path.join(rootdir, name)):
            try:
                for i in all_files(os.path.join(rootdir, name), ext):
                    yield i
            except:
                pass
    for i in files(rootdir, ext):
        yield i


def remove_files(rootdir, ext, show=False):
    """删除rootdir目录下的符合的文件"""
    for i in files(rootdir, ext):
        if show:
            print i
        os.remove(i)


def save_ont_filter_file(input_filepath, filter_list):
    filter_list.append(input_filepath)


def get_filter_list(rootdir, ext, filter_list, show=False):
    filter_all_files(rootdir, ext, save_ont_filter_file, filter_list, show)


def filter_all_files(rootdir, ext, filter_func, param, show=False):
    """删除rootdir目录下以及子目录下符合的文件"""
    for i in all_files(rootdir, ext):
        if show:
            print i
        filter_func(i, param)


def remove_all_files(rootdir, ext, show=False):
    """删除rootdir目录下以及子目录下符合的文件"""
    for i in all_files(rootdir, ext):
        if show:
            print i
        os.remove(i)


def safe_getone(r):
    try:
        row = r.getOne(None)
    except sqlobject.main.SQLObjectIntegrityError:
        print "multi record"
    return row


def read_file_by_chunks(filename, chunksize=1024 * 1024):
    file_object = open(filename, 'rb')
    while True:
        chunk = file_object.read(chunksize)
        if not chunk:
            break
        yield chunk
    file_object.close()

def check_file_occupy(file_name):
    try:
        f_test = open(file_name, 'a')
    except:
        return True
    f_test.close()
    return False

def multiple_replace(text):
    rx = re.compile('|'.join(map(re.escape, filename_filter_dict)))

    def one_xlat(match):
        return filename_filter_dict[match.group(0)]

    return rx.sub(one_xlat, text)


def check_file_exist(filepath):
    if os.path.isfile(utf8_to_file_charset(filepath)) and os.path.getsize(utf8_to_file_charset(filepath)) > 0:
        return True
    else:
        return False


def get_int_createdate(createdate):
    if createdate:
        fix_createdate = createdate.replace('/', '-')
        if len(fix_createdate) < 14:
            fix2_createdate = fix_createdate + "  00:00:00"
        else:
            fix2_createdate = fix_createdate
        timearray = time.strptime(fix2_createdate, '%Y-%m-%d %H:%M:%S')
        return int(time.mktime(timearray))
    else:
        return datetime.now()


def get_md5(filepath):
    m = hashlib.md5()
    with open(filepath, 'rb') as fp:
        while True:
            blk = fp.read(4096)  # 4KB per block
            if not blk:
                break
            m.update(blk)
    return m.hexdigest()


# unix时间戳转换为字符串
# timestamp_str(1447257600)
def timestamp_str(value):
    tm_fmt = '%Y-%m-%d %H:%M:%S'
    # value为传入的值为时间戳(整形)，如：1332888820
    value = time.localtime(value)
    # 经过localtime转换后变成
    # time.struct_time(tm_year=2012, tm_mon=3, tm_mday=28, tm_hour=6, tm_min=53, tm_sec=40, tm_wday=2, tm_yday=88, tm_isdst=0)
    # 最后再经过strftime函数转换为正常日期格式。
    dt = time.strftime(tm_fmt, value)
    return dt


# 字符串转换为unix时间戳
# str_timestamp('2015-11-12 00:00:00')
def str_timestamp(dt):
    # dt为字符串
    # 中间过程，一般都需要将字符串转化为时间数组
    time.strptime(dt, '%Y-%m-%d %H:%M:%S')
    # time.struct_time(tm_year=2012, tm_mon=3, tm_mday=28, tm_hour=6, tm_min=53, tm_sec=40, tm_wday=2, tm_yday=88, tm_isdst=-1)
    # 将"2012-03-28 06:53:40"转化为时间戳
    s = time.mktime(time.strptime(dt, '%Y-%m-%d %H:%M:%S'))
    return int(s)

def get_second_by_str(duration_str):
    if not duration_str:
        return 0
    item_list = duration_str.split(':')
    if not item_list:
        return 0
    return int(item_list[0]) * 3600 + int(item_list[1]) * 60 + int(item_list[2])


if __name__ == '__main__':
    pass
