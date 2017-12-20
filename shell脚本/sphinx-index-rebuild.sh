#!/bin/sh
export LD_LIBRARY_PATH=/guanfu/server/mediaserver/lib/:/usr/local/lib:/guanfu/server/mysql/lib
/guanfu/server/sphinx/bin/indexer -c /guanfu/server/sphinx/etc/sphinx.conf main --rotate
