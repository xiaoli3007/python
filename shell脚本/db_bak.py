# -*- coding:utf-8 -*-
# usuage: db_bak passwd dbname

import sys
import os
import re
from datetime import datetime, date, time

BAK_DIR = '/guanfu/databack'
DB_NAME = 'train'
RESERVE_NUM = 10


def back_nts():
    global BAK_DIR
    global DB_NAME
    create_date = datetime.now()
    str_date = create_date.strftime('%Y-%m-%d-%H-%M-%S')
    back_filename = "guanfu_db_%s-%s.sql" % (DB_NAME, str_date)
    if len(sys.argv) > 1 and sys.argv[1]:
        password = sys.argv[1]
        cmd = 'mysqldump -uroot -p%s %s > %s && tar -zcvf %s.tar.gz %s && rm -f %s' % (
            password, DB_NAME, back_filename, back_filename, back_filename, back_filename)
    else:
        cmd = 'mysqldump -uroot %s > %s && tar -zcvf %s.tar.gz %s && rm -f %s' % (
            DB_NAME, back_filename, back_filename, back_filename, back_filename)

    os.chdir(BAK_DIR)
    print cmd
    os.system(cmd)


def clear_old_back():
    global BAK_DIR
    global RESERVE_NUM
    file_list = os.listdir(BAK_DIR)
    bak_file_list = []
    for line in file_list:
        file_path = os.path.join(BAK_DIR, line)
        if os.path.isfile(file_path):
            if re.match(r'^guanfu_db_' + DB_NAME, line) is not None:
                bak_file_list.append(file_path)

    num = len(bak_file_list)
    if num > RESERVE_NUM:
        bak_file_list.sort()
        for i in range(0, num - RESERVE_NUM):
            print bak_file_list[i]
            os.remove(bak_file_list[i])


if __name__ == '__main__':
    if len(sys.argv) > 2 and sys.argv[2]:
        DB_NAME = sys.argv[2]
    back_nts()
    clear_old_back()
