# -*- coding: utf-8 -*-
import scrapy
from collections import defaultdict


class GdprinfoSpider(scrapy.Spider):
    name = 'gdprinfo'
    allowed_domains = [
        'gdpr-info.eu',
    ]
    start_urls = [
        'http://gdpr-info.eu/',
    ]
    custom_settings = {
        'ITEM_PIPELINES': {}
    }

    def parse(self, response):

        for link in response.xpath('//table[@id="tablepress-12"]/tbody/tr/td[3]/a'):
            article_index = int(link.xpath('./text()').extract_first())
            yield scrapy.Request(
                url=link.xpath('./@href').extract_first(),
                callback=self.parse_article,
                meta={
                    'article_index': article_index
                }
            )

    def parse_article(self, response):
        article_index = response.meta['article_index']

        suitable_recitals = response.xpath(
            '//div[@class="empfehlung-erwaegungsgruende"]//span[@class="bold-number"]/text()'
        ).extract()

        suitable_recitals = map(int, suitable_recitals)

        yield {
            'index': article_index,
            'recitals': list(suitable_recitals)
        }

