#! /bin/sh
# chkconfig: 2345 55 25
# Description: Startup script for uwsgi webserver on Debian. Place in /etc/init.d and
# run 'update-rc.d -f uwsgi defaults', or use the appropriate command on your
# distro. For CentOS/Redhat run: 'chkconfig --add uwsgi'

### BEGIN INIT INFO
# Provides:          uwsgid
# Required-Start:    $all
# Required-Stop:     $all
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Short-Description: starts the uwsgi web server
# Description:       starts uwsgi using start-stop-daemon
### END INIT INFO

# Author:   licess
# website:  http://lnmp.org

PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin
DESC="uwsgi daemon"
NAME=uwsgi
DAEMON=/usr/bin/uwsgi
CONFIGFILE=/data/web/python/microblog/$NAME.ini
PIDFILE=/var/run/$NAME.pid
SCRIPTNAME=/etc/init.d/uwsgid

set -e
[ -x "$DAEMON" ] || exit 0

do_start() {
    $DAEMON $CONFIGFILE || echo -n "uwsgi already running"
}

do_stop() {
    $DAEMON --stop $PIDFILE || echo -n "uwsgi not running"
    rm -f $PIDFILE
    echo "$DAEMON STOPED."
}

do_reload() {
    $DAEMON --reload $PIDFILE || echo -n "uwsgi can't reload"
}

do_status() {
    ps aux|grep $DAEMON | grep -v grep
}

case "$1" in
 status)
    echo -en "Status $NAME: \n"
    do_status
 ;;
 start)
    echo -en "Starting $NAME: \n"
    do_start
 ;;
 stop)
    echo -en "Stopping $NAME: \n"
    do_stop
 ;;
 reload|graceful)
    echo -en "Reloading $NAME: \n"
    do_reload
 ;;
 *)
    echo "Usage: $SCRIPTNAME {start|stop|reload}" >&2
    exit 3
 ;;
esac

exit 0