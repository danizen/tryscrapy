# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from medlineplus.items import PageItem


class NlmnewsSpider(CrawlSpider):
    name = 'nlmnews'
    allowed_domains = ['www.nlm.nih.gov']
    start_urls = ['https://www.nlm.nih.gov/about/newsevents.html']

    rules = [
        Rule(LinkExtractor(allow=r'news/'), callback='parse_item', follow=True),
    ]

    dcmetadata = {
        'date_issued': "//head/meta[@name='DC.Date.Issued']/@content",
        'date_modified': "//head/meta[@name='DC.Date.Modified']/@content",
        'title': "//head//meta[@name='DC.Title']/@content"
    }

    def parse_item(self, response):
        i = { 'url': response.url }
        for key, xpath in self.dcmetadata.items():
            i[key] = response.xpath(xpath).extract_first()
        if i['title'] is None:
            i['title'] = response.xpath('//head/title/@value').extract_first()
        return PageItem(**i)
