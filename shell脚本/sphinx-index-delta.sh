#!/bin/sh
export LD_LIBRARY_PATH=/guanfu/server/mediaserver/lib/:/usr/local/lib:/guanfu/server/mysql/lib
cd /guanfu/server/sphinx/bin
/guanfu/server/sphinx/bin/indexer -c /guanfu/server/sphinx/etc/sphinx.conf delta --rotate
