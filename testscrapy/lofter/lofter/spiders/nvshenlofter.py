# -*- coding: utf-8 -*-
import scrapy


class NvshenlofterSpider(scrapy.Spider):
    name = "nvshenlofter"
    allowed_domains = ["157550323.lofter.com"]
    start_urls = ['http://157550323.lofter.com/']

    def parse(self, response):
        pass
