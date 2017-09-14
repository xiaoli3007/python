# -*- coding: utf-8 -*-
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor as sle
from hashlib import md5
from lofter.items import LofterItem
from scrapy.exceptions import CloseSpider
import re,os


class NvshenlofterSpider(CrawlSpider):
    name = "nvshenlofter"
    allowed_domains = ["lisi3007.lofter.com"]
    start_urls = [u'http://lisi3007.lofter.com/?page=%d' % d for d in range(1, 19)]
    # start_urls = [u'http://ada86t.lofter.com/?page=2']

    rules = [
        Rule(sle(allow=(u'lisi3007.lofter.com/post/.+')), callback='parse_lisi3007')
    ]

    # def parse(self, response):
    #     pass

    def parse_lisi3007(self, response):
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
                    '//div[@class="img"]/a/img/@src').extract()
            midle_remote_images2 = []
            for it in midle_remote_images:
                wenhao = it.find("?")
                if wenhao != -1:
                    midle_remote_images2.append(it[0:wenhao])
                else:
                    midle_remote_images2.append(it)
            item['remote_images_paths'] = midle_remote_images2
            # local_images_paths =[]
            # for itemimage in item['remote_images_paths']:
            #     local_images_paths.append("%s.%s" % (md5(itemimage).hexdigest(), os.path.basename(itemimage)))
            #
            # item['local_images_paths'] = local_images_paths

            if len(item['remote_images_paths']) > 0:
                item['remote_default_image'] = item['remote_images_paths'][0]
                # item['local_default_image'] = "%s.%s" % (md5(item['remote_default_image'][0]).hexdigest(), os.path.basename(item['remote_default_image']))

            item['user_id'] = 2

            # print(item)
            items.append(item)
        # if (len(items) > 20):
        #     raise CloseSpider('enough')
        return items