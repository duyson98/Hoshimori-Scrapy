# -*- coding: utf-8 -*-

'''
Created on May 26, 2017

@author: Koko
'''
import scrapy


class ExtraCardlistSpider(scrapy.Spider):
    name = "extracardlist"
    allowed_domains = ["wiki.dengekionline.com"]
    start_urls = (
        # Extra cards
        'https://wiki.dengekionline.com/battlegirl/Extra%E3%82%AB%E3%83%BC%E3%83%89%E4%B8%80%E8%A6%A7',
    )
    custom_settings = {
        'FEED_FORMAT': 'xml',
        'FEED_URI': 'results/extracardlist.xml',
    }

    @classmethod
    def parse(self, response):
        card_table = response.xpath("//*[@id='rendered-body']/div/div/div/div/div/table")

        for card in card_table.xpath("//tbody/tr"):
            yield {
                'relative_url': card.css("a::attr(href)").extract_first(),
                'type': 'extra',
            }

    def spider_closed(self, spider):
        spider.logger.info('Spider closed: %s', spider.name)
