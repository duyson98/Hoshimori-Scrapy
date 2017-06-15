# -*- coding: utf-8 -*-

'''
Created on May 26, 2017

@author: Koko
'''
import os

import scrapy


class NormalCardlistSpider(scrapy.Spider):
    name = "normalcardlist"
    allowed_domains = ["wiki.dengekionline.com"]
    start_urls = (
        # Normal cards
        'https://wiki.dengekionline.com/battlegirl/%E3%82%AB%E3%83%BC%E3%83%89%E4%B8%80%E8%A6%A7',

    )
    custom_settings = {
        'FEED_FORMAT': 'xml',
        'FEED_URI': 'results/normalcardlist.xml',
    }
    middle_file = ''

    @classmethod
    def parse(self, response):
        card_table = response.xpath("//*[@id='rendered-body']/div/div/div/div/div/table")

        for card in card_table.xpath("//tbody/tr"):
            yield {
                'relative_url': card.css("a::attr(href)").extract_first(),
                'type': 'normal',
            }

    @classmethod
    def closed(self, reason):
        os.remove(self.middle_file)
