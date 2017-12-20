#!/bin/bash

PATH = $PATH:/guanfu/server/mysql/bin:/guanfu/server/nginx/sbin:/guanfu/server/php/sbin:/guanfu/server/php/bin
LD_LIBRARY_PATH = /guanfu/server/mediaserver/lib/:/usr/local/lib:/guanfu/server/mysql/lib

i = 1
cd /guanfu/server/script

while [ $i < 20 ] ; do
python /guanfu/server/script/guanfu_import_course.py
sleep 5 
$i = $i+1
done
cd -