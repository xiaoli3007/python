# -*- coding: utf-8 -*-
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor as sle
from hashlib import md5
from lofter.items import LofterItem
from scrapy.exceptions import CloseSpider
import re,os
from lofter.function import *


class BianmaSpider(CrawlSpider):
    name = "bianma"
    allowed_domains = ["lisi3007.lofter.com"]
    start_urls = ['http://lisi3007.lofter.com/post/1eb0f412_e361d69']

    def parse(self, response):
        items = []
        sel = Selector(response)
        sites = sel.xpath('/html')
        for site in sites:
            item = LofterItem()
            item['title'] = site.xpath('//title/text()').extract()
            item['source_url'] = response.url

            item['user_id'] = 22
            print(type(db_charset_to_utf8(item['title'][0])))
            # print(item['title'][0])
            # print(item)
            items.append(item)

        # if (len(items) > 20):
        #     raise CloseSpider('enough')
        return items
