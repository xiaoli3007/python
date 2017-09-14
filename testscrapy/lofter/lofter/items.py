# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

# import scrapy
from scrapy.item import Item, Field

class LofterItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    source_url = Field()
    title = Field()
    local_default_image = Field()
    remote_default_image = Field()
    local_images_paths = Field()
    remote_images_paths = Field()
    user_id = Field()
