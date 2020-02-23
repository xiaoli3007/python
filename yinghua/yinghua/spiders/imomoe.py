# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
# from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor as sle
from hashlib import md5
from yinghua.items import imomoe_videoItem,imomoe_video_dataItem , imomoe_video_data_jsItem
from scrapy.exceptions import CloseSpider
import re,os
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

class ImomoeSpider(scrapy.Spider):
    name = 'imomoe'
    allowed_domains = ['imomoe.in']
    base_url = "http://imomoe.in"
    # start_urls = ['http://imomoe.in/']
    # start_urls = ['http://www.imomoe.in/so.asp?page=%d&fl=0&dq=%C8%D5%B1%BE&pl=hit' % d for d in range(1, 10)]

    # http://www.imomoe.in/so.asp?page=1&fl=0&dq=%C8%D5%B1%BE&pl=hit
    # rules = (
    #     # Extract links matching 'category.php' (but not matching 'subsection.php')
    #     # and follow links from them (since no callback means follow=True by default).
    #     Rule(LinkExtractor(allow=('category\.php',), deny=('subsection\.php',))),
    #
    #     # Extract links matching 'item.php' and parse them with the spider's method parse_item
    #     Rule(LinkExtractor(allow=('item\.php',)), callback='parse_item'),
    # )

    def start_requests(self):

        for uid in range(1, 2):
            yield scrapy.Request(url='http://www.imomoe.in/so.asp?page=%d&pl=hit&dq=%%C8%%D5%%B1%%BE' % uid, callback=self.parse_cat)


    def parse_cat(self, response):

        # print(response.xpath('//div[@class="fire l"]/div[@class="pics"]/ul/li/h2/a/@href').getall())
        liurls=response.xpath('//div[@class="fire l"]/div[@class="pics"]/ul/li/h2/a/@href').getall()
        for it in liurls:
            # print(it)
            yield scrapy.Request(self.base_url + it,callback=self.parse_item)
        # for title in response.xpath('//title').getall():
        #     yield YinghuaItem(title=title)

        # yield Request(self.base_url + '/u/{}'.format(information_item['_id']),
        #               callback=self.parse_further_information,
        #               meta=request_meta, dont_filter=True, priority=1)

        # for href in response.xpath('//a/@href').getall():
        #     yield scrapy.Request(response.urljoin(href), self.parse)

    def parse_item(self, response):
        # print(response.xpath('//title').get())
        # self.logger.info('Hi, this is an item page! %s', response.url)
        catitem = imomoe_videoItem()
        catitem['title'] = response.xpath('//div[@class="area title"]/h1/span[@class="names"]/text()').get()
        catitem['url'] = response.url
        # print(item)
        video_liurls1 = response.xpath('//div[@id="play_0"]/ul/li/a/@href').getall()
        # print(len(video_liurls1))
        request_meta = response.meta
        request_meta['catitem'] = catitem
        yield catitem
        if len(video_liurls1)<20:
            for it in video_liurls1:
                # print(it)
                yield scrapy.Request(self.base_url + it, callback=self.parse_video_item ,meta=request_meta)
        # item['description'] = response.xpath('//td[@id="item_description"]/text()').get()
        # videoid = scrapy.Field()
        # title = scrapy.Field()
        # url = scrapy.Field()
        # thumb = scrapy.Field()
        # thumb_url = scrapy.Field()
        # description = scrapy.Field()
        # bieming = scrapy.Field()
        # diqu = scrapy.Field()
        # leixing = scrapy.Field()
        # niandai = scrapy.Field()
        # tag = scrapy.Field()



    def parse_video_item(self, response):
        # print(response.xpath('//title').get())
        catitem = response.meta['catitem']

        video_item = imomoe_video_dataItem()
        video_item['videourl'] = catitem['url']
        video_item['title'] = response.xpath('//div[@class="ptitle l"]/h1/a/text()').get()+response.xpath('//div[@class="ptitle l"]/h1/span/text()').get()
        video_item['url'] = response.url
        video_item['source_js'] = self.base_url + response.xpath('//div[@class="player"]/script/@src')[0].get()
        # source_js = response.xpath('//div[@class="player"]/script')[1].get()
        # print(self.base_url + item['source_js'])
        request_meta = response.meta
        request_meta['video_item'] = video_item
        # yield scrapy.Request( video_item['source_js'], callback=self.parse_video_item_js,meta=request_meta)
        # print(video_item)
        yield video_item

    def parse_video_item_js(self, response):
        # print(response.xpath('//title').get())
        video_item = response.meta['video_item']
        item = imomoe_video_data_jsItem()
        item['jsurl'] = response.url
        item['url'] = video_item['url']
        item['source_text'] = response.text
        # print(item)
        return item
