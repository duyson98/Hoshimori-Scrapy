import os
from xml.dom import minidom

import scrapy


class WeaponDatabaseSpider(scrapy.Spider):
    name = "weapondatabase"
    allowed_domains = ["wiki.dengekionline.com"]
    custom_settings = {
        'FEED_FORMAT': 'csv',
        'FEED_URI': 'results/weapon_database.csv',
        'FEED_EXPORT_FIELDS': ['weapon_type', 'weapon_name','weapon_image', 'obtain_method',
                               'rarity', 'rhythm', 'basic_atk', 'max_atk', 'additional_effects', 'coins_required',
                               'material', 'effects_as_sub_weapon'],
    }

    @classmethod
    def start_requests(self):
        urls = [
            #sword list
            'https://wiki.dengekionline.com/battlegirl/%E3%82%BD%E3%83%BC%E3%83%89%E4%B8%80%E8%A6%A7',
            #lance list
            'https://wiki.dengekionline.com/battlegirl/%E3%82%B9%E3%83%94%E3%82%A2%E4%B8%80%E8%A6%A7',
            #hammer list
            'https://wiki.dengekionline.com/battlegirl/%E3%83%8F%E3%83%B3%E3%83%9E%E3%83%BC%E4%B8%80%E8%A6%A7',
            #gun list
            'https://wiki.dengekionline.com/battlegirl/%E3%82%AC%E3%83%B3%E4%B8%80%E8%A6%A7',
            #rod list
            'https://wiki.dengekionline.com/battlegirl/%E3%83%AD%E3%83%83%E3%83%89%E4%B8%80%E8%A6%A7',
            #blade canon list
            'https://wiki.dengekionline.com/battlegirl/%E3%83%96%E3%83%AC%E3%82%A4%E3%83%89%E3%82%AB%E3%83%8E%E3%83%B3%E4%B8%80%E8%A6%A7',
            #double handgun list
            'https://wiki.dengekionline.com/battlegirl/%E3%83%84%E3%82%A4%E3%83%B3%E3%83%90%E3%83%AC%E3%83%83%E3%83%88%E4%B8%80%E8%A6%A7',

        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    @classmethod
    def parse(self, response):
        weapon_table = response.xpath("//*[@id='rendered-body']/div/div/div/div/div/table")

        for weapon in weapon_table.xpath("./tbody/tr"):
            url = 'https://wiki.dengekionline.com'
            type = response.xpath("//*[@id='rendered-body']/p[1]/a/text()").extract_first(),
            yield scrapy.Request(url=(url + weapon.xpath("./td[1]/a/@href").extract_first()), callback=self.parseMore,
                                 meta={'type': type})

    @classmethod
    def parseMore(self, response):
        data_table = response.xpath("//*[@id='rendered-body']/div/div[1]/div[1]/table")

        if data_table:
            material_table = response.xpath("//*[@id='rendered-body']/div/div[1]/div[2]/table")

            if material_table:
                yield {
                    'weapon_type': response.meta['type'],
                    'weapon_name': data_table.xpath("./tbody/tr[1]/td[1]/strong/text()").extract_first(),
                    'weapon_image': data_table.xpath("./tbody/tr[2]/td[1]/a/img/@src").extract_first(),
                    'basic_atk': data_table.xpath("./tbody/tr[2]/td[3]/text()").extract_first(),
                    'max_atk': data_table.xpath("./tbody/tr[3]/td[2]/text()").extract_first(),
                    'additional_effects': data_table.xpath("./tbody/tr[4]/td[2]/text()").extract(),
                    'coins_required': data_table.xpath("./tbody/tr[1]/td[3]/text()").extract_first(),
                    'rhythm': data_table.xpath("./tbody/tr[5]/td[2]/a/img/@src").extract_first(),
                    'material':material_table.xpath("./tbody/tr[2]/td/strong/text()").extract(),
                    'effects_as_sub_weapon': response.xpath("//*[@id='rendered-body']/div/div[1]/div[3]/div/table/tbody/tr[2]/td/text()").extract(),
                }
            else:
                yield {
                    'weapon_type': response.meta['type'],
                    'weapon_name': data_table.xpath("./tbody/tr[1]/td[1]/strong/text()").extract_first(),
                    'weapon_image': data_table.xpath("./tbody/tr[2]/td[1]/a/img/@src").extract_first(),
                    'basic_atk': data_table.xpath("./tbody/tr[2]/td[3]/text()").extract_first(),
                    'max_atk': data_table.xpath("./tbody/tr[3]/td[2]/text()").extract_first(),
                    'additional_effects': data_table.xpath("./tbody/tr[4]/td[2]/text()").extract(),
                    'coins_required': data_table.xpath("./tbody/tr[1]/td[3]/text()").extract_first(),
                    'rhythm': data_table.xpath("./tbody/tr[5]/td[2]/a/img/@src").extract_first(),
                    'effects_as_sub_weapon': response.xpath("//*[@id='rendered-body']/div/div[1]/div[2]/div/table/tbody/tr[2]/td/text()").extract(),
                }
        else:
            data_table = response.xpath("//*[@id='rendered-body']/div/div[1]/table")

            #mainly alpha and beta variants
            variant_data_list1 = response.xpath("//*[@id='rendered-body']/div/div[2]/div/div/div[1]/table/tbody/tr")
            if not variant_data_list1:
                variant_data_list1 = response.xpath("//*[@id='rendered-body']/div/div[3]/div/div/div[1]/table/tbody/tr")

            count = 1
            for variant in variant_data_list1:
                if count == 1:
                    count += 1
                    continue

                if (not variant) or (count == 6): break

                sub_effect_table = response.xpath(
                    "//*[@id='rendered-body']/div/div[2]/div/div/div[2]/div[1]/div/table")
                if not sub_effect_table:
                    sub_effect_table = response.xpath(
                        "//*[@id='rendered-body']/div/div[2]/div/div/div[2]/div/div/div[2]/div[1]/div/table")
                if not sub_effect_table:
                    sub_effect_table = response.xpath(
                        "//*[@id='rendered-body']/div/div[3]/div/div/div[2]/div/div/div[2]/div[1]/div/table")

                yield {
                    'weapon_type': response.meta['type'],
                    'weapon_name': variant.xpath("./td[1]/text()").extract_first(),
                    'weapon_image': data_table.xpath("./tbody/tr[2]/td[1]/a/img/@src").extract_first(),
                    'obtain_method': data_table.xpath("./tbody/tr[3]/td[2]/text()").extract_first(),
                    'basic_atk': variant.xpath("./td[2]/text()").extract_first(),
                    'max_atk': variant.xpath("./td[3]/text()").extract_first(),
                    'additional_effects': variant.xpath("./td[4]//text()").extract(),
                    'coins_required': variant.xpath("./td[5]/text()").extract_first(),
                    'rarity': data_table.xpath("./tbody/tr[3]/td[1]/span/text()").extract_first(),
                    'rhythm': data_table.xpath("./tbody/tr[5]/td/a/img/@src").extract_first(),
                    'material': variant.xpath("./td[6]//text()").extract(),
                    'effects_as_sub_weapon': sub_effect_table.xpath("./tbody/tr" + "[" + repr(count) + "]" + "/td[2]//text()").extract(),
                }
                count += 1

            # gamma variants
            variant_data_list2 = response.xpath(
                "//*[@id='rendered-body']/div/div[2]/div/div/div[2]/div/div/div[1]/table/tbody/tr")
            if not variant_data_list2:
                variant_data_list2 = response.xpath(
                    "//*[@id='rendered-body']/div/div[3]/div/div/div[2]/div/div/div[1]/table/tbody/tr")

            count = 1
            for variant in variant_data_list2:
                if count == 1:
                    count += 1
                    continue

                if count == 5: break

                sub_effect_table = response.xpath(
                    "//*[@id='rendered-body']/div/div[2]/div/div/div[2]/div[1]/div/table")
                if not sub_effect_table:
                    sub_effect_table = response.xpath(
                        "//*[@id='rendered-body']/div/div[2]/div/div/div[2]/div/div/div[2]/div[1]/div/table")
                if not sub_effect_table:
                    sub_effect_table = response.xpath(
                        "//*[@id='rendered-body']/div/div[3]/div/div/div[2]/div/div/div[2]/div[1]/div/table")

                yield {
                    'weapon_type': response.meta['type'],
                    'weapon_name': variant.xpath("./td[1]/text()").extract(),
                    'weapon_image': data_table.xpath("./tbody/tr[2]/td[1]/a/img/@src").extract_first(),
                    'obtain_method': data_table.xpath("./tbody/tr[3]/td[2]/text()").extract_first(),
                    'basic_atk': variant.xpath("./td[2]/text()").extract_first(),
                    'max_atk': variant.xpath("./td[3]/text()").extract_first(),
                    'additional_effects': variant.xpath("./td[4]//text()").extract(),
                    'coins_required': variant.xpath("./td[5]/text()").extract_first(),
                    'rarity': data_table.xpath("./tbody/tr[3]/td[1]/span/text()").extract_first(),
                    'rhythm': variant.xpath("./td[1]/a/img/@src").extract_first(),
                    'material': variant.xpath("./td[6]//text()").extract(),
                    'effects_as_sub_weapon': sub_effect_table.xpath("./tbody/tr[5]/td[2]//text()").extract(),
                }
                count += 1