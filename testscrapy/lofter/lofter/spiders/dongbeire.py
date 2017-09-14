# -*- coding: utf-8 -*-
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor as sle
from hashlib import md5
from lofter.items import LofterItem
from scrapy.exceptions import CloseSpider
import re,os


class DongbeireSpider(CrawlSpider):
    name = "dongbeire"
    allowed_domains = ["dongbeire.wordpress.com"]
    start_urls = ['https://dongbeire.wordpress.com/']

    start_urls = [u'https://dongbeire.wordpress.com/page/%d/' % d for d in range(1, 15)]

    rules = [
        Rule(sle(allow=(u'dongbeire.wordpress.com/[0-9]*/[0-9]*/[0-9]*/.+/')), callback='parse_detail')
    ]

    def parse_detail(self, response):
        items = []
        sel = Selector(response)
        sites = sel.xpath('/html')
        for site in sites:
            item = LofterItem()
            item['title'] = site.xpath('//title/text()').extract()
            item['source_url'] = response.url
            # item['link_url'] = site.xpath('//a[@class="postblk"]/@href').extract()
            # item['remote_images_paths'] = site.xpath(
            #         '//div[@class="img"]/a[@class="imgclasstag"]/img/@src').re('(.*)\?*')

            midle_remote_images = site.xpath(
                    '//div[@class="entry-content"]/p/img/@src').extract()
            midle_remote_images2 = []
            for it in midle_remote_images:
                wenhao = it.find("?")
                if wenhao != -1:
                    midle_remote_images2.append(it[0:wenhao])
                else:
                    midle_remote_images2.append(it)
            item['remote_images_paths'] = midle_remote_images2

            if len(item['remote_images_paths']) > 0:
                item['remote_default_image'] = item['remote_images_paths'][0]

            item['user_id'] = 3

            # print(item)
            items.append(item)
        # if (len(items) > 20):
        #     raise CloseSpider('enough')
        return items
