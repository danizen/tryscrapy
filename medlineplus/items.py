# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
import uuid
from time import gmtime, strftime


class PageItem(scrapy.Item):
    url = scrapy.Field()
    content = scrapy.Field()
    title = scrapy.Field()
    publisher = scrapy.Field()
    date_issued = scrapy.Field()
    date_modified = scrapy.Field()
    description = scrapy.Field()
    uuid = scrapy.Field()
    date_crawled = scrapy.Field()

    def __init__(self, *args, **kwargs):
        super(PageItem, self).__init__(*args, **kwargs)
        self['uuid'] = uuid.uuid1()
        self['date_crawled'] = strftime("%Y-%m-%dT%H:%M:%SZ", gmtime())

