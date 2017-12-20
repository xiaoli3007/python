#!/bin/sh

/etc/init.d/nginx stop
/etc/init.d/php-fpm start
service memcached stop
/etc/init.d/searchd stop
/etc/init.d/gfmediaserver stop
/etc/init.d/mysqld stop
/etc/init.d/gflive stop

rm -rf /guanfu/www/rms/caches/error_log.php
rm -rf /guanfu/log/nginx/access/rms.log

rm -rf /guanfu/log/php/php-fpm.log
rm -rf /guanfu/log/nginx/error.log
rm -rf /guanfu/log/mysql/error.log

rm -rf /guanfu/server/sphinx/log/searchd.log
rm -rf /guanfu/server/sphinx/log/query.log
rm -rf /guanfu/server/mediaserver/logs/uploadserv*
rm -rf /guanfu/server/mediaserver/logs/uploadctrl*

rm -rf /guanfu/server/mediaserver/logs/error_log
rm -rf /guanfu/server/mediaserver/logs/error_log

rm -rf /guanfu/server/mediaserver/live/logs/access.log
rm -rf /guanfu/server/mediaserver/live/logs/error.log

rm -rf /guanfu/server/mediaserver/bin/logs/*.log

/etc/init.d/mysqld start
service memcached start
/etc/init.d/gfmediaserver start
/etc/init.d/searchd start
/etc/init.d/nginx start
/etc/init.d/php-fpm start
/etc/init.d/gflive start

