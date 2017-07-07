# -*- coding: utf-8 -*-

'''
Created on May 26, 2017

@author: Koko
'''
import os

import scrapy


class SubCardlistSpider(scrapy.Spider):
    name = "subcardlist"
    allowed_domains = ["wiki.dengekionline.com"]
    start_urls = (
        # Subcards
        'https://wiki.dengekionline.com/battlegirl/%E3%82%B5%E3%83%96%E3%82%AB%E3%83%BC%E3%83%89%E5%B0%82%E7%94%A8%E3%82%AB%E3%83%BC%E3%83%89%E4%B8%80%E8%A6%A7',
    )
    custom_settings = {
        'FEED_FORMAT': 'xml',
        'FEED_URI': 'results/subcardlist.xml',
    }

    @classmethod
    def parse(self, response):
        card_table = response.xpath("//*[@id='rendered-body']/div/div/div/div/div/table")

        for card in card_table.xpath("//tbody/tr"):
            yield {
                'relative_url': card.css("a::attr(href)").extract_first(),
                'type': 'sub',
            }
