# -*- coding:utf-8 -*-
"""
 1. serial表,program表里数字字段的全局定义
 2. 采用sqlobject orm的数据库定义
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


# 下载模式
MODE_UPLOADSERV = 1
MODE_SFTP = 2
MODE_OFFLINE = 3


# 媒体格式类型，通过扩展名区分
URL_TYPE_VIDEO = 0  # 视音频 适用于各种视音频文件
URL_TYPE_ISO = 1  # iso映像文件
URL_TYPE_IMAGE = 2  # 图片
URL_TYPE_DOCUMENT = 4  # 文档，适用于WORD,PPT,EXCEL,PDF等支持WEB-DAV协议的文档
URL_TYPE_ONLINE_COURSE = 6  # 可以用浏览器打开的课件，标准课件
URL_TYPE_LINK = 8  # 可以用浏览器打开的各种链接，主要是http链接
URL_TYPE_AUDIO = 12  # 音频格式
URL_TYPE_ATTACH = 13  # 附件格式
URL_TYPE_PRICOURSE = 14  # 私有课件
URL_TYPE_OTHER = 200  # 其他
URL_TYPE_UNKNOW = -1  # 其他

URL_TYPE_POSTER = 3  # 海报图片
URL_TYPE_MIDDLE_CONTROL = 5  # 中控
URL_TYPE_TRURAN_COURSE = 7  # 确然课件系统制作的课件，如确然的三分屏课件
URL_TYPE_MOBILE = 9  # 移动手机点播
URL_TYPE_TABLET = 10  # 移动平板点播
URL_TYPE_PC = 12  # 嵌入式pc播放
URL_TYPE_TEXT_LIBRARY = 11  # 文库


OPT_DOC_PDF = 2  # 文档pdf
OPT_DOC_SWF = 4  # 文档swf
OPT_VIDEO_BQ = 8  # 对应字段：transcodeState 标清,表示已经转码的文件
OPT_VIDEO_GQ = 16  # 对应字段：transcodeState 高清
OPT_VIDEO_CQ = 32  # 对应字段：transcodeState 超清
OPT_VIDEO_YQ = 1024  # 对应字段：源分辨率一致
OPT_VIDEO_JQ = 2048  # 对应字段：transcodeState 极清
OPT_VIDEO_AUDIO = 4096  # 对应字段：transcodeState 音频

OPT_IMG_POSTER = 1  # 对应字段：transcodeState 海报
OPT_DOC_LIB = 2  # 对应字段：transcodeState 文库
OPT_ISO_VIRTUAL = 4  # 对应字段：transcodeState 虚拟光驱

# 返回的错误描述
ERR_PARAM = 1  # 参数不正确
ERR_CONFIG = 2  # 任务配置文件不正确
ERR_SEND_EXCEPTION = 3  # 发送出现异常
ERR_NOT_FOUND = 4  # 资源没有发现
ERR_GUID_EXIST = 5
MSG_GUID_SKIP = 1001

# 名字字典
svrname_dict = {}
dict_url = {'在线点播': 0, '映像文件': 1, '图片': 2, '文档': 4, '课件': 6, '链接': 8}

db_charset = 'utf8'
file_charset = 'utf8'
local_name = ''

LOG_LEVEL_DICT = {'debug': logging.DEBUG,
                  'info': logging.INFO,
                  'warning': logging.WARNING,
                  'error': logging.ERROR,
                  'critical': logging.CRITICAL}

filename_filter_dict = {'?': '', ':': '', '*': '', '\\': '', '/': '', '<': '', '>': '', '|': '', '"': ''}

office_ext_dict = {'Word': ['doc', 'docx', 'txt', 'rtf', 'mht', 'mhthl', 'odt', 'wps', 'wpd', 'dotm', 'dot', 'dotx', 'docm'],
                   'Excel': ['xlsx', 'xls'],
                   'PowerPoint': ['ppt', 'pptx', 'pps'],
                   'Visio': ['vsd', 'vsdx']
                   }

office_ext_list = office_ext_dict['Word'] + office_ext_dict['Excel'] + office_ext_dict['PowerPoint'] + office_ext_dict['Visio']
text_ext_list = ['pdf'] + office_ext_list

iso_ext_list = ['iso', 'cue', 'nrg', 'img']

video_ext_list = ['3gp', '3gpp', 'asf', 'asx', 'avi', 'dat', 'divx', 'f4v', 'flac', 'flv', 'rv', 'mpg', 'mpeg', 'mpv', 'm1v', 'mp4', 'mov',
                  'mkv', 'mtk', 'm2ts', 'm4v',
                  'mks', 'mac', 'm2v', 'mts', 'm2t', 'ogm', 'pva', 'qt', 'rm', 'rmvb', 'rmi', 'sdp', 'ts', 'vob', 'vqf', 'wmv', 'wm', 'xmp'
                  ]

# mp3 不用转码
audio_ext_list = ['mp3', 'ac3', 'aac', 'au', 'aiff', 'aifc', 'ape', 'apl', 'amr', 'cda', 'dts', 'flac', 'mpa', 'm4a', 'mid', 'midi', 'mka',
                  'ogg', 'ra', 'sdp', 'snd', 'wma', 'wav']

# unsupport  'jpc', 'jp2', 'svg',iff
image_ext_list = ['png', 'jpg', 'jpeg', 'bmp', 'gif', 'tif', 'tiff']

mediaformat_dict = {URL_TYPE_VIDEO: video_ext_list, URL_TYPE_ISO: iso_ext_list, URL_TYPE_DOCUMENT: text_ext_list,
                    URL_TYPE_AUDIO: audio_ext_list}

import_mediaformat_dict = {URL_TYPE_VIDEO: video_ext_list, URL_TYPE_ISO: iso_ext_list, URL_TYPE_DOCUMENT: text_ext_list,
                           URL_TYPE_AUDIO: audio_ext_list + ['mp3'], URL_TYPE_IMAGE: image_ext_list}


def add_check_mediaformat(url_type, mediaformat_list):
    mediaformat_dict[url_type].extend(mediaformat_list)


def get_media_format_from_dict(file_path, mdict):
    if file_path.startswith("http://") or file_path.startswith("ftp://"):
        return URL_TYPE_LINK

    file_title, file_ext = os.path.splitext(file_path)

    if (not file_ext) or (len(file_ext) < 2):
        # self.task_object.logger_object.info('mediaformat is unknow ext:[%s] filepath:[%s]', file_ext.decode('utf8'), file_path)
        return URL_TYPE_UNKNOW

    file_ext = file_ext[1:].lower()
    for key in mdict:
        if file_ext in mdict[key]:
            return key

    # self.task_object.logger_object.info('mediaformat is unknow ext:[%s] filepath:[%s]', file_ext.decode('utf8'), file_path)
    return URL_TYPE_UNKNOW


def get_media_format(file_path):
    global mediaformat_dict
    return get_media_format_from_dict(file_path, mediaformat_dict)


def get_media_format_import(file_path):
    global import_mediaformat_dict
    return get_media_format_from_dict(file_path, import_mediaformat_dict)


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


if __name__ == '__main__':
    pass
