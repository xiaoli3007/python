#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import time
import sys
import atexit
import ConfigParser
import MySQLdb
import datetime
import urllib
import urllib2
import json
import platform
import getopt
import logging
import  settings as setting

# 错误报告
# 使用方法: guanfu_error_log.py -f task.ini

# unix时间戳转换为字符串
# timestamp_str(1447257600)
def timestamp_str(value):
    format = '%Y-%m-%d %H:%M:%S'
    # value为传入的值为时间戳(整形)，如：1332888820
    value = time.localtime(value)
    ## 经过localtime转换后变成
    ## time.struct_time(tm_year=2012, tm_mon=3, tm_mday=28, tm_hour=6, tm_min=53, tm_sec=40, tm_wday=2, tm_yday=88, tm_isdst=0)
    # 最后再经过strftime函数转换为正常日期格式。
    dt = time.strftime(format, value)
    return dt

# 字符串转换为unix时间戳
# str_timestamp('2015-11-12 00:00:00')
def str_timestamp(dt):
    #dt为字符串
    #中间过程，一般都需要将字符串转化为时间数组
    time.strptime(dt, '%Y-%m-%d %H:%M:%S')
    ## time.struct_time(tm_year=2012, tm_mon=3, tm_mday=28, tm_hour=6, tm_min=53, tm_sec=40, tm_wday=2, tm_yday=88, tm_isdst=-1)
    #将"2012-03-28 06:53:40"转化为时间戳
    s = time.mktime(time.strptime(dt, '%Y-%m-%d %H:%M:%S'))
    return int(s)

class ErrorLogTask():
    def __init__(self):
        self.logger_object = None
        self.log_level = logging.DEBUG
        self.log_file_path = 'log/mysql.log'
        self.log_console_show_flag = 1
        self.conn = None;
        self.cur  = None;

    def __init_logger(self):
        logger = logging.getLogger()
        logger.setLevel(self.log_level)
        formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')

        file_log_handle = logging.FileHandler(self.log_file_path)
        file_log_handle.setFormatter(formatter)
        file_log_handle.setLevel(self.log_level)
        logger.addHandler(file_log_handle)

        if self.log_console_show_flag:
            console_log_handle = logging.StreamHandler()
            console_log_handle.setFormatter(formatter)
            console_log_handle.setLevel(self.log_level)
            logger.addHandler(console_log_handle)
        self.logger_object = logger

    def init(self):

        db_host = setting.MYSQL_HOST
        db_name = setting.MYSQL_DBNAME
        db_socket = ''
        db_user = setting.MYSQL_USER
        db_password = setting.MYSQL_PASSWD
        db_port = 3306
        # print 'host=%s,user=%s,passwd=%s,port=%s,db=%s,unix_socket=%s' % (db_host,db_user,db_password,db_port,db_name,db_socket)
        self.__init_logger()
        try:
            self.conn=MySQLdb.connect(host=db_host,user=db_user,passwd=db_password,port=db_port,db=db_name,unix_socket=db_socket,charset="utf8")
            self.cur=self.conn.cursor()
            if self.conn is None:
                return False

        except Exception, err:
            print "connect mysql Exception:%s", err
            self.logger_object.exception('init database failed!')
            return False
        else:
            return True

    def get_db_data(self):

        try:

            guid = 'aasfasfasf'
            title = '45345345'
            source_url = '45345345'
            user_id =1

            sql = "INSERT INTO calc_blogphoto  (guid,title,source_url,user_id) VALUES ('%s','%s','%s',%d)" % (guid,title, source_url,user_id)

            print(sql)
            self.cur.execute(sql)
            # # 获取网站标题及域名
            # count=self.cur.execute('select media_dir,site_title,domain from v9_site where siteid=1')
            # result=self.cur.fetchone()
            # site_title = result[1]
            # domain = result[2]
            #
            # product_code = self.get_product_code()
            # # print 'product_code = %s' % product_code
            #
            # count=self.cur.execute("select id,msg,log_time from v9_error_log where had_read=0")
            # results = self.cur.fetchall()
            # error_array = [];
            # for r in results:
            #     dict = {'msg':r[1],'log_time':r[2]};
            #     error_array.append(dict)
            #
            #     # 将已发送的数据设置为已读
            #     update_sql = "update v9_error_log set had_read=1 where id="+str(r[0]);
            #     self.cur.execute(update_sql)

            self.cur.close()
            self.conn.commit()
            self.conn.close()
            return True

        except MySQLdb.Error,e:
            self.logger_object.exception( "Error %d: %s" % (e.args[0], e.args[1]))

        return False

def main():
    my_task = ErrorLogTask()
    my_task.init()
    my_task.get_db_data()

if __name__ == '__main__':
    main()

