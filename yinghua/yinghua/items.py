# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class imomoe_videoItem(scrapy.Item):
    # define the fields for your item here like:
    # srouceid = scrapy.Field()
    title = scrapy.Field()
    url = scrapy.Field()
    thumb = scrapy.Field()
    thumb_url = scrapy.Field()
    description = scrapy.Field()
    bieming = scrapy.Field()
    diqu = scrapy.Field()
    leixing = scrapy.Field()
    niandai = scrapy.Field()
    tag = scrapy.Field()
    guid = scrapy.Field()

class imomoe_video_dataItem(scrapy.Item):
    # define the fields for your item here like:
    # videoid = scrapy.Field()
    videourl = scrapy.Field()
    title = scrapy.Field()
    url = scrapy.Field()
    source_js = scrapy.Field()
    source_text = scrapy.Field()
    video_play_url1 = scrapy.Field()
    video_play_url2 = scrapy.Field()
    guid = scrapy.Field()

class imomoe_video_data_jsItem(scrapy.Item):
    # define the fields for your item here like:
    jsurl = scrapy.Field()
    url = scrapy.Field()
    source_text = scrapy.Field()
    guid = scrapy.Field()



