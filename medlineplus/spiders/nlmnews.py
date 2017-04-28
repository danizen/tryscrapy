# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.utils.project import get_project_settings
from medlineplus.items import PageItem
import requests


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

    def __init__(self, *args, **kwargs):
        super(NlmnewsSpider, self).__init__(*args, **kwargs)
        self.settings = get_project_settings()

    def _get_tika_url(self):
        if 'TIKA_SERVER_URL' in self.settings:
            url = '%s/tika' % self.settings['TIKA_SERVER_URL']
            return url
        return None

    def _extract_content(self, response):
        content = ''
        tikaurl = self._get_tika_url()
        if tikaurl is not None:
            headers = {
                'Content-Type': response.headers['Content-Type'],
                'Accept': 'text/plain; charset=utf-8',
            }
            r = requests.put(tikaurl, headers=headers, data=response.body)
            if r.ok:
                content = r.content.decode('utf-8')
        return content

    def parse_item(self, response):
        i = { 'url': response.url }
        i['content'] = self._extract_content(response)
        for key, xpath in self.dcmetadata.items():
            i[key] = response.xpath(xpath).extract_first()
        if i['title'] is None:
            i['title'] = response.xpath('//head/title/@value').extract_first()
        return PageItem(**i)
