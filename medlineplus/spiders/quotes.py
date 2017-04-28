# -*- coding: utf-8 -*-
import scrapy
import uuid


class QuotesSpider(scrapy.Spider):
    name = "quotes"

    allowed_domains = ["quotes.toscrape.com"]

    start_urls = [
        'http://quotes.toscrape.com/page/1/',
    ]

    # def start_requests(self):
    #    urls = [
    #        'http://quotes.toscrape.com/page/1/',
    #        'http://quotes.toscrape.com/page/2/',
    #    ]
    #    for url in urls:
    #        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for q in response.css('div.quote'):
            yield {
                'uuid':     str(uuid.uuid1()),
                'text':     q.css('span.text::text').extract_first(),
                'author':   q.css('small.author::text').extract_first(),
                'tags':     q.css('div.tags a.tag::text').extract(),
            }

        next_page = response.css('li.next a::attr(href)').extract_first()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(url=next_page, callback=self.parse)
