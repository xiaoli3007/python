# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import codecs
import json
from datetime import datetime
from hashlib import md5
from scrapy import log
from twisted.enterprise import adbapi

import scrapy
from scrapy.contrib.pipeline.images import ImagesPipeline
from scrapy.exceptions import DropItem
from function import *
from utils.mysqldriver import MySQL



class LofterPipeline(object):
    def process_item(self, item, spider):
        return item


class JsonWriterPipeline(object):

    def __init__(self):
        self.file = codecs.open('lofter.json', 'wb', encoding='utf-8')

    def process_item(self, item, spider):
        line = json.dumps(dict(item), ensure_ascii=False) + "\n"
        self.file.write(line)
        return item

    def spider_closed(self, spider):
        self.file.close()

class MyImagesPipeline(ImagesPipeline):

    def get_media_requests(self, item, info):
        # if len(item['remote_images_paths']) > 0:
           for image_url in item['remote_images_paths']:
                yield scrapy.Request(image_url)

    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem("Item contains no images")


        item['local_images_paths'] = image_paths
        if len(item['local_images_paths'])> 0:
            item['local_default_image'] = image_paths[0]
        else:
            item['local_default_image'] = ''

        # print('============================')
        # print(results)
        # print(type(image_paths))
        # print(image_paths)
        # print(image_paths[0])
        # print(item['local_default_image'])
        # print('============================')
        return item


class SportPipeline(object):

    _db = None
    def __init__(self):
        dbconfig = {
            'host':'localhost',
            'port': 3306,
            'user':'root',
            'passwd':'123123',
            'db':'testdj',
            'charset':'utf8'
        }

        self._db = MySQL(dbconfig)

    def process_item(self, item, spider):
        insert_sql =  "INSERT INTO calc_blogphoto  (guid,title,source_url,user_id,remote_images_paths,local_images_paths,remote_default_image,local_default_image) VALUES ('%s','%s','%s',%d,'%s','%s','%s','%s')" % (
            'aaaa', item['title'][0], item['source_url'], item['user_id'], '3', '33', '22', '13')

        id = self._db.insert(insert_sql)
        print('============================')
        print(id)
        print('============================')
        return item



class MySQLStorePipeline(object):
    """A pipeline to store the item in a MySQL database.

    This implementation uses Twisted's asynchronous database API.
    """

    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        dbargs = dict(
                host=settings['MYSQL_HOST'],
                db=settings['MYSQL_DBNAME'],
                user=settings['MYSQL_USER'],
                passwd=settings['MYSQL_PASSWD'],
                charset='utf8',
                use_unicode=True,
        )
        dbpool = adbapi.ConnectionPool('MySQLdb', **dbargs)
        return cls(dbpool)

    def process_item(self, item, spider):
        # run db query in the thread pool
        d = self.dbpool.runInteraction(self._do_upsert, item, spider)
        d.addErrback(self._handle_error, item, spider)
        # at the end return the item in case of success or failure
        d.addBoth(lambda _: item)
        # return the deferred instead the item. This makes the engine to
        # process next item (according to CONCURRENT_ITEMS setting) after this
        # operation (deferred) has finished.
        return d

    def _do_upsert(self, conn, item, spider):
        """Perform an insert or update."""
        guid = self._get_guid(item)
        now = datetime.utcnow().replace(microsecond=0).isoformat(' ')

        conn.execute("""SELECT EXISTS(
            SELECT 1 FROM calc_blogphoto WHERE guid = %s
        )""", (guid, ))
        ret = conn.fetchone()[0]

        if ret:

            # upsql = "UPDATE  calc_blogphoto SET   title='%s', source_url='%s', remote_images_paths='%s', local_images_paths='%s', remote_default_image='%s', local_default_image='%s' WHERE guid='%s'" % (
            #     item['title'][0], item['source_url'],  json.dumps(item['remote_images_paths']),  json.dumps(item['local_images_paths']),item['remote_default_image'],item['local_default_image'],guid
            # )
            # conn.execute(upsql)
            spider.log("Item updated in db: %s %r" % (guid, item))
        else:

            # print('============================')
            # print(item)
            # print(item['title'][0].decode('utf8').encode('gbk'))
            # print(type(item['title'][0].decode('utf8').encode('gbk')))
            # print('============================')
            sql = "INSERT INTO calc_blogphoto  (guid,title,source_url,user_id,remote_images_paths,local_images_paths,remote_default_image,local_default_image) VALUES ('%s','%s','%s',%d,'%s','%s','%s','%s')" % (
            guid, item['title'][0], item['source_url'], item['user_id'], json.dumps(item['remote_images_paths']), json.dumps(item['local_images_paths']), item['remote_default_image'], item['local_default_image'])

            # print(sql)
            conn.execute(sql)


    def _handle_error(self, failure, item, spider):
        """Handle occurred on db interaction."""
        # do nothing, just log
        log.err(failure)

    def _get_guid(self, item):
        """Generates an unique identifier for a given item."""
        # hash based solely in the url field
        return md5(item['source_url']).hexdigest()