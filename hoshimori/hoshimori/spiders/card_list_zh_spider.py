# -*- coding: utf-8 -*-

'''
Created on May 26, 2017

@author: Koko
'''

import scrapy

from utils import get_raw_image


class ZhCardlistSpider(scrapy.Spider):
    name = "zhcardlist"
    allowed_domains = ["zh.battlegirl.wikia.com"]
    start_urls = (
        'http://zh.battlegirl.wikia.com/wiki/%E5%8D%A1%E7%89%87%E4%B8%80%E8%A6%BD',
    )
    custom_settings = {
        'FEED_FORMAT': 'csv',
        'FEED_URI': 'results/zhcardlist.csv',
        'FEED_EXPORT_FIELDS': ['id', 'card_name', 'relative_url', 'image', 'special_icon'],
    }

    @classmethod
    def parse(self, response):
        for row in response.xpath("//tr")[2:]:
            # Initialize dictionary
            result = {}

            result['id'] = row.xpath('td[1]/text()').extract_first()
            result['card_name'] = row.xpath('td[3]/a/@title').extract_first()
            result['relative_url'] = row.xpath('td[3]/a/@href').extract_first()

            # Get icons
            icons = row.css('td:nth-child(2)').xpath('.//@src').extract()
            for icon in icons:
                if icon.startswith('d'): # Or 'data'
                    icons.remove(icon)

            result['image'] = get_raw_image(icons[0])
            if icons.__len__() == 2:
                result['special_icon'] = get_raw_image(icons[1])

            yield result
