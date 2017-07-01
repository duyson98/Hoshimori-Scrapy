'''
Created on May 26, 2017

@author: Koko
'''
import csv
import os

import scrapy


class ZhCardDatabaseSpider(scrapy.Spider):
    name = "database_zh"
    allowed_domains = ["wikia.com"]
    custom_settings = {
        'FEED_FORMAT': 'csv',
        'FEED_URI': 'results/zh_database.csv',
        'FEED_EXPORT_FIELDS': ['id', 'card_name', 'icon', 'special_icon',
                               'image_0', 'image_1', 'image_2', 'image_3', 'image_4',
                               'image_5', 'image_6', 'image_7', 'image_8'],
    }
    middle_file = 'results/zhcardlist.csv'

    @classmethod
    def start_requests(self):
        url = 'http://zh.battlegirl.wikia.com'
        with open(self.middle_file) as f:
            reader = csv.reader(f)
            count = 0
            for row in reader:
                if count > 3:
                    break
                yield scrapy.Request(url + row[2], callback=self.parse,
                                     meta={'id': row[0], 'icon': row[3], 'special_icon': row[4]})
                count += 1

    @classmethod
    def parse(self, response):
        # Initialization
        result = {}

        # ID and icons
        result['id'] = response.meta['id']
        result['card_name'] = response.meta['card_name']
        result['icon'] = response.meta['icon']
        result['special_icon'] = response.meta['special_icon']

        # Tables
        tables = response.css('table')

        name_table = tables[0]
        parameter_table = tables[1]
        source_table = tables[2]
        action_skill_table = tables[3]
        nakayoshi_table = tables[4]
        if len(tables) > 5:
            subcard_effect_table = tables[5]



        # Images
        images = response.xpath('//*[@id="mw-content-text"]/div[1]//img')
        count = 0
        for image in images:
            # If lazy load
            if image.xpath('@src').extract_first().startswith('data'):
                result['image_{}'.format(count)] = image.xpath('@data-src').extract_first()
            else:
                result['image_{}'.format(count)] = image.xpath('@src').extract_first()
            count += 1

        yield result

    # @classmethod
    # def closed(self, reason):
    #     os.remove(self.middle_file)
