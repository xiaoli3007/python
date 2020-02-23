# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

from yinghua.utils.mysqldriver import  MysqldbHelper
from yinghua.items import imomoe_videoItem,imomoe_video_dataItem , imomoe_video_data_jsItem

class YinghuaPipeline(object):
    def process_item(self, item, spider):
        return item

class MysqlDBPipeline(object):
    def __init__(self):
        self.Tweets = MysqldbHelper()

    def process_item(self, item, spider):
        """ 判断item的类型，并作相应的处理，再入数据库 """
        if isinstance(item, imomoe_videoItem):
            self.insert_item(self.Tweets, item,'imomoe_video')
        elif isinstance(item, imomoe_video_dataItem):
            self.insert_item(self.Tweets, item,'imomoe_video_data')
        # elif isinstance(item, imomoe_video_data_jsItem):
        #     self.insert_item(self.Tweets, item,'imomoe_video_data_js')
        return item

    @staticmethod
    def insert_item(collection, item,table_name):
        # print(dict(item))
        collection.insert(table_name, dict(item))
        # collection.insert(dict(item))
