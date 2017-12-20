#!/bin/sh
export LD_LIBRARY_PATH=/guanfu/server/mediaserver/lib/:/usr/local/lib:/guanfu/server/mysql/lib
/guanfu/server/sphinx/bin/indexer -c /guanfu/server/sphinx/etc/sphinx.conf delta --rotate

if [ -f /guanfu/server/sphinx/data/delta.sph ]; then
    /guanfu/server/sphinx/bin/indexer -c /guanfu/server/sphinx/etc/sphinx.conf --merge main delta --merge-dst-range deleted 0 0 --rotate
fi
