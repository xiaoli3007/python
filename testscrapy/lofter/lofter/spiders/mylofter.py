# -*- coding: utf-8 -*-
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor as sle
from hashlib import md5
from lofter.items import LofterItem
from scrapy.exceptions import CloseSpider
import re,os


class MylofterSpider(CrawlSpider):
    name = "mylofter"
    allowed_domains = ["ada86t.lofter.com"]
    # start_urls = ['http://ada86t.lofter.com/']
    start_urls = [u'http://ada86t.lofter.com/?page=%d' % d for d in range(1, 175)]
    # start_urls = [u'http://ada86t.lofter.com/?page=2']

    rules = [
        Rule(sle(allow=(u'ada86t.lofter.com/post/.+')), callback='parse_ada86t')
    ]

    # def parse(self, response):
    #     items = []
    #     sel = Selector(response)
    #     sites = sel.xpath('/html')
    #     for site in sites:
    #         item = LofterItem()
    #         item['product_url'] = response.url
    #         item['link_url'] = site.xpath('//a[@class="postblk"]/@href').extract()
    #         # item['image_url'] = site.xpath(
    #         #         '//div[@id="preview"]/div/img[@src]').re(r'src="(.*?)" jqimg')
    #
    #         item['title'] = site.xpath('//title/text()').extract()
    #         print(item)
    #         items.append(item)
    #         if (len(items) > 20):
    #             raise CloseSpider('enough')
    #         return items

    def parse_ada86t(self, response):
        items = []
        sel = Selector(response)
        sites = sel.xpath('/html')
        for site in sites:
            item = LofterItem()
            item['title'] = site.xpath('//title/text()').extract()
            item['source_url'] = response.url
            # item['link_url'] = site.xpath('//a[@class="postblk"]/@href').extract()
            # item['remote_images_paths'] = site.xpath(
            #         '//div[@class="pic"]/a/img/@src').re('(.*)\?')

            item['remote_images_paths'] = site.xpath(
                    '//div[@class="pic"]/a/img/@src').extract()

            # local_images_paths =[]
            # for itemimage in item['remote_images_paths']:
            #     local_images_paths.append("%s.%s" % (md5(itemimage).hexdigest(), os.path.basename(itemimage)))
            #
            # item['local_images_paths'] = local_images_paths
            item['remote_default_image'] = ''
            if len(item['remote_images_paths']) > 0:
                item['remote_default_image'] = item['remote_images_paths'][0]
                # item['local_default_image'] = "%s.%s" % (md5(item['remote_default_image'][0]).hexdigest(), os.path.basename(item['remote_default_image']))

            item['user_id'] = 1

            # print(item)
            items.append(item)
        # if (len(items) > 20):
        #     raise CloseSpider('enough')
        return items

