# coding=utf-8
'''
Created on May 26, 2017

@author: Koko
'''
import csv
import os

import scrapy
from utils import get_raw_image, get_lazy_image


class ZhCardDatabaseSpider(scrapy.Spider):
    name = "database_zh"
    allowed_domains = ["wikia.com"]
    custom_settings = {
        'FEED_FORMAT': 'csv',
        'FEED_URI': 'results/zh_card_database.csv',
        'FEED_EXPORT_FIELDS': ['id', 'japanese_name', 'character', 'i_rarity', 'i_weapon', 'obtain_method', 'image',
                               'special_icon', 'art', 'special_front', 'front_top', 'front_bottom', 'front_name',
                               'front_rarity', 'front_weapon', 'subcard_effect', 'hp_1', 'sp_1', 'atk_1', 'def_1',
                               'hp_50', 'sp_50', 'atk_50', 'def_50', 'hp_70', 'sp_70', 'atk_70', 'def_70',
                               'japanese_skill_name', 'skill_SP', 'skill_range', 'skill_affinity',
                               'action_skill_effects', 'action_skill_combo', 'action_skill_damage',
                               'evolved_action_skill_combo', 'evolved_action_skill_damage', 'japanese_nakayoshi_title',
                               'nakayoshi_skill_effect', 'nakayoshi_skill_target', 'evolved_nakayoshi_skill_effect',
                               'evolved_nakayoshi_skill_target', ],
    }
    middle_file = 'results/zhcardlist.csv'

    @classmethod
    def start_requests(self):
        url = 'http://zh.battlegirl.wikia.com'
        with open(self.middle_file) as f:
            reader = csv.reader(f)
            # Skip first line
            next(f)
            for row in reader:
                yield scrapy.Request(url + row[2], callback=self.parse,
                                     meta={'id': row[0], 'japanese_name': row[1], 'image': row[3],
                                           'special_icon': row[4]})

    @classmethod
    def parse(self, response):
        # Initialization
        result = {}

        # ID and icons
        result['id'] = response.meta['id']
        result['japanese_name'] = response.meta['japanese_name']
        result['image'] = response.meta['image']
        result['special_icon'] = response.meta['special_icon']

        # Images
        images = response.css('#mw-content-text > div:nth-child(1)')
        result['art'] = get_raw_image(get_lazy_image(images.css('div:nth-child(1) > img')[-1]))

        if images.css('div:nth-child(3) > img').__len__() > 0:
            if int(images.css('div:nth-child(3) > img')[0].xpath('@height').extract_first()) > 300:
                result['special_front'] = get_raw_image(get_lazy_image(images.css('div:nth-child(3) > img')[0]))
                result['front_top'] = get_raw_image(get_lazy_image(images.css('div:nth-child(4) > img')[0]))
                result['front_bottom'] = get_raw_image(get_lazy_image(images.css('div:nth-child(5) > img')[0]))
                result['front_name'] = get_raw_image(get_lazy_image(images.css('div:nth-child(6) > img')[0]))
                result['front_rarity'] = get_raw_image(get_lazy_image(images.css('div:nth-child(7) > img')[0]))
                result['front_weapon'] = get_raw_image(get_lazy_image(images.css('div:nth-child(8) > img')[0]))
            else:
                result['front_top'] = get_raw_image(get_lazy_image(images.css('div:nth-child(3) > img')[0]))
                result['front_bottom'] = get_raw_image(get_lazy_image(images.css('div:nth-child(4) > img')[0]))
                result['front_name'] = get_raw_image(get_lazy_image(images.css('div:nth-child(5) > img')[0]))
                result['front_rarity'] = get_raw_image(get_lazy_image(images.css('div:nth-child(6) > img')[0]))
                result['front_weapon'] = get_raw_image(get_lazy_image(images.css('div:nth-child(7) > img')[0]))

        # Subcard effect
        result['subcard_effect'] = response.css(
            '#mw-content-text > table:nth-child(7) ::text').extract_first() == u'副卡牌效果'

        # Tables
        tables = response.css('table')

        # Name
        name_table = tables[0]
        result['i_rarity'] = name_table.css('tr:nth-child(3)>td::text').extract_first()
        result['i_weapon'] = name_table.css('tr:nth-child(4)>td::text').extract_first()
        result['character'] = response.css(
            '#PageHeader > div.page-header__main > div.page-header__categories > div > a:nth-child(2) ::text').extract_first().split(
            u'\uff1a')[-1]

        # Parameter
        parameter_table = tables[1]
        result['hp_1'] = parameter_table.css('tr:nth-child(2) > td:nth-child(2) ::text').extract_first()
        result['sp_1'] = parameter_table.css('tr:nth-child(3) > td:nth-child(2) ::text').extract_first()
        result['atk_1'] = parameter_table.css('tr:nth-child(4) > td:nth-child(2) ::text').extract_first()
        result['def_1'] = parameter_table.css('tr:nth-child(5) > td:nth-child(2) ::text').extract_first()
        result['hp_50'] = parameter_table.css('tr:nth-child(2) > td:nth-child(3) ::text').extract_first()
        result['sp_50'] = parameter_table.css('tr:nth-child(3) > td:nth-child(3) ::text').extract_first()
        result['atk_50'] = parameter_table.css('tr:nth-child(4) > td:nth-child(3) ::text').extract_first()
        result['def_50'] = parameter_table.css('tr:nth-child(5) > td:nth-child(3) ::text').extract_first()
        result['hp_70'] = parameter_table.css('tr:nth-child(2) > td:nth-child(4) ::text').extract_first()
        result['sp_70'] = parameter_table.css('tr:nth-child(3) > td:nth-child(4) ::text').extract_first()
        result['atk_70'] = parameter_table.css('tr:nth-child(4) > td:nth-child(4) ::text').extract_first()
        result['def_70'] = parameter_table.css('tr:nth-child(5) > td:nth-child(4) ::text').extract_first()

        # Obtain method
        obtain_table = tables[2]
        result['obtain_method'] = "".join(obtain_table.css('tr > td ::text').extract())

        # Action skill
        if tables[3].css('::text').extract_first() != u'副卡牌專用':
            action_skill_table = tables[3]
            result['japanese_skill_name'] = action_skill_table.css(
                'tr:nth-child(1) > td:nth-child(3) > b ::text').extract_first()
            result['skill_SP'] = action_skill_table.css('tr:nth-child(2) > td ::text').extract_first()
            result['skill_range'] = '\n'.join(action_skill_table.css('tr:nth-child(4) > td ::text').extract())

            skill_hits = action_skill_table.css('tr:nth-child(3) > td ::text').extract_first()
            if skill_hits.split(u'\uFF0F').__len__() == 2:
                result['skill_affinity'] = skill_hits.split(u'\uFF0F')[-1]

            skill_combo = action_skill_table.css('tr:nth-child(1) > td:nth-child(5) ::text').extract()
            # Change in skill combo after evolution
            if skill_combo.__len__() == 2:
                result['action_skill_combo'] = skill_combo[0].split(u'\uff1a')[-1]
                result['evolved_action_skill_combo'] = skill_combo[1].split(u'\uff1a')[-1]
            else:
                result['action_skill_combo'] = result['evolved_action_skill_combo'] = skill_combo[0]

            result['action_skill_damage'] = '\n'.join(
                action_skill_table.css('tr:nth-child(5) > td ::text').extract())
            if action_skill_table.css('tr:nth-child(6) > td ::text').extract_first() != u'\uff0d':
                result['evolved_action_skill_damage'] = '\n'.join(
                    action_skill_table.css('tr:nth-child(6) > td ::text').extract())

            result['action_skill_effects'] = '\n'.join(action_skill_table.css('tr:nth-child(3) > td').xpath(
                'hr/following-sibling::text()').extract())

        # Nakayoshi
        try:
            if tables[4].css('::text').extract_first() != u'副卡牌專用':
                nakayoshi_table = tables[4]
                result['japanese_nakayoshi_title'] = nakayoshi_table.css(
                    'tr:nth-child(1) > td > b ::text').extract_first()
                unevolved_nakayoshi = nakayoshi_table.css('tr:nth-child(2) > td ::text').extract_first().split(
                    u'\uFF0F')
                result['nakayoshi_skill_target'] = unevolved_nakayoshi[0]
                result['nakayoshi_skill_effect'] = unevolved_nakayoshi[1]
                evolved_nakayoshi = nakayoshi_table.css('tr:nth-child(3) > td ::text').extract_first().split(u'\uFF0F')
                if evolved_nakayoshi[0] != u'\uff0d':
                    result['evolved_nakayoshi_skill_effect'] = evolved_nakayoshi[0]
                    result['evolved_nakayoshi_skill_target'] = evolved_nakayoshi[1]
        except IndexError as err:
            print err.args
            pass

        yield result

    @classmethod
    def closed(self, reason):
        os.remove(self.middle_file)
