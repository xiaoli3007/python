#!/bin/sh
/guanfu/server/mediaserver/bin/kill.sh python
sleep 1
/guanfu/server/mediaserver/bin/kill.sh ffmpeg
sleep 1
/etc/init.d/gfmediaserver stop
sleep 1
/etc/init.d/gfmediaserver start