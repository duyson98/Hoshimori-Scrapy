import os
from xml.dom import minidom

import scrapy

from utils import get_raw_image


class ZhWeaponDatabaseSpider(scrapy.Spider):
    name = "zhweapondatabase"
    allowed_domains = ["wikia.com"]
    custom_settings = {
        'FEED_FORMAT': 'csv',
        'FEED_URI': 'results/zh_weapon_database.csv',
        'FEED_EXPORT_FIELDS': ['weapon_name', 'weapon_image', 'weapon_type',
                               'rarity', 'rhythm', 'beat1', 'beat2', 'beat3',
                               'basic_atk', 'max_atk', 'material', 'coins_required', 'obtain_method',
                               'main_effects', 'sub_effects', 'weapon_prototype'],
        'ITEM_PIPELINES': {'hoshimori.pipelines.zh_weapon_csv_pipeline.ZhWeaponCSVPipeline': 300},
    }

    @classmethod
    def start_requests(self):
        urls = [
            #sword list
            # 'http://zh.battlegirl.wikia.com/wiki/%E5%8A%8D',
            #lance list
            # 'http://zh.battlegirl.wikia.com/wiki/%E7%9F%9B',
            #hammer list
            # 'http://zh.battlegirl.wikia.com/wiki/%E6%A7%8C',
            #gun list
            # 'http://zh.battlegirl.wikia.com/wiki/%E6%A7%8D',
            #rod list
            # 'http://zh.battlegirl.wikia.com/wiki/%E6%9D%96',
            #blade canon list
            # 'http://zh.battlegirl.wikia.com/wiki/%E5%8A%8D%E6%A7%8D',
            #double handgun list
            'http://zh.battlegirl.wikia.com/wiki/%E9%9B%99%E6%A7%8D',

        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    @classmethod
    def parse(self, response):
        weapon_table = response.css('table')[1]

        count = 0
        for weapon in weapon_table.css('tr'):
            if count == 0:
                count += 1
                continue
            # if count > 13:
            #     break
            url = 'http://zh.battlegirl.wikia.com'
            weapon_type = weapon.css('td')[2].css('::text').extract_first()
            type_icon = get_raw_image(weapon.css('td')[2].css('noscript').css('img::attr(src)').extract_first())
            yield scrapy.Request(url=(url + weapon.css('td')[1].css('a::attr(href)').extract_first()), callback=self.parseMore,
                                 meta={'weapon_type': weapon_type, 'type_icon': type_icon})
            count += 1

    @classmethod
    def parseMore(self, response):
        tables = response.css('table')

        overview_table = tables[0]

        count = 2
        while count < len(tables):
            variant_table = tables[count]

            result = {}

            result['weapon_type']   = response.meta['weapon_type']
            result['weapon_name']   = overview_table.css('tr')[count].css('td')[0].css('::text').extract()
            result['rarity']        = overview_table.css('tr')[count].css('td')[1].css('::text').re("[0-9,]+")
            result['main_effects']  = overview_table.css('tr')[count].css('td')[3].css('::text').extract()
            result['sub_effects']   = overview_table.css('tr')[count].css('td')[4].css('::text').extract()
            result['rhythm']        = overview_table.css('tr')[count].css('td')[5].css('::text').extract_first()
            result['beat1'] = ""
            result['beat2'] = ""
            result['beat3'] = ""
            result['basic_atk'] = variant_table.css('tr')[0].css('th')[1].css('span')[0].css('::text').re("[0-9,]+")
            result['max_atk'] = variant_table.css('tr')[0].css('th')[1].css('span')[1].css('::text').extract_first()
            if count == 2:
                result['weapon_image'] = variant_table.css('tr')[0].css('th').css('img::attr(src)').extract_first()
            else:
                result['weapon_image'] = variant_table.css('tr')[0].css('th').css('noscript').css('img::attr(src)').extract_first()
            result['material'] = variant_table.css('tr')[3].css('td').css('::text').extract()
            result['coins_required'] = variant_table.css('tr')[4].css('td').css('::text').extract_first()
            result['obtain_method'] = tables[2].css('tr')[5].css('td').css('::text').extract()
            if count == 2:
                result['weapon_prototype'] = ""
            else:
                result['weapon_prototype'] = overview_table.css('tr')[2].css('td')[0].css('::text').extract()

            yield result

            count += 1