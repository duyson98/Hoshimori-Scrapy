'''
Created on May 26, 2017

@author: Koko
'''
import scrapy
from xml.dom import minidom


class ExtraCardDatabaseSpider(scrapy.Spider):
    name = "database_extra"
    allowed_domains = ["wiki.dengekionline.com"]
    custom_settings = {
        'FEED_FORMAT': 'csv',
        'FEED_URI': 'results/extra_database.csv',
        'FEED_EXPORT_FIELDS': ['card_type', 'character', 'event', 'card_name', 'card_image', 'weapon_type',
                               'weapon_image', 'rarity', 'stat1_hp', 'stat1_sp', 'stat1_atk', 'stat1_def', 'stat50_hp',
                               'stat50_sp', 'stat50_atk', 'stat50_def', 'stat70_hp', 'stat70_sp', 'stat70_atk',
                               'stat70_def', 'skill_name', 'skill_sp', 'skill_combo', 'skill_hit', 'skill_damage',
                               'skill_range', 'skill_effect', 'skill_comment', 'skill_preview', 'charge_name',
                               'charge_hit', 'charge_damage', 'charge_range', 'charge_comment', 'nakayoshi_name',
                               'nakayoshi_target_noevol', 'nakayoshi_effect_noevol', 'nakayoshi_target_evol',
                               'nakayoshi_effect_evol'],
        'ITEM_PIPELINES': {'hoshimori.pipelines.card_csv_pipeline.CardCSVPipeline': 300},
    }
    def start_requests(self):
        url = 'https://wiki.dengekionline.com'
        cardlist = minidom.parse("results/extracardlist.xml")
        urls = cardlist.getElementsByTagName("relative_url")
        for node in urls:
            yield scrapy.Request(url + node.firstChild.data, self.parse)

    def parse(self, response):
        card_front = response.xpath('//*[@id="rendered-body"]/div[2]/div/div[1]/table/tbody')
        stat_table = response.xpath('//*[@id="rendered-body"]/div[2]/div/div[2]/table/tbody')
        skill_table = response.xpath('//*[@id="rendered-body"]/div[2]/div/div[4]/table/tbody')
        charge_table = response.xpath('//*[@id="rendered-body"]/div[2]/div/div[6]/table/tbody')
        nakayoshi = response.xpath('//*[@id="rendered-body"]/div[3]/div[1]')

        yield {
            # Card
            'card_name':    card_front.xpath('tr[2]/td[2]/text()').extract_first(),
            'card_image':   card_front.xpath('tr[1]/td/a/img/@src').extract_first(),
            'card_type': 'extra',
            # Weapon
            'weapon_type':  card_front.xpath('tr[3]/td[2]/text()').extract_first(),
            'weapon_image': card_front.xpath('tr[3]/td[2]/a/@href').extract_first(),
            # Rarity
            'rarity':       card_front.xpath('tr[3]/td[4]//text()').extract_first(),
            # Parameter
            # 1
            'stat1_hp':     stat_table.xpath('tr[2]/td[2]/text()').extract_first(),
            'stat1_sp':     stat_table.xpath('tr[2]/td[3]/text()').extract_first(),
            'stat1_atk':    stat_table.xpath('tr[2]/td[4]/text()').extract_first(),
            'stat1_def':    stat_table.xpath('tr[2]/td[5]/text()').extract_first(),
            # 50
            'stat50_hp':    stat_table.xpath('tr[3]/td[2]/text()').extract_first(),
            'stat50_sp':    stat_table.xpath('tr[3]/td[3]/text()').extract_first(),
            'stat50_atk':   stat_table.xpath('tr[3]/td[4]/text()').extract_first(),
            'stat50_def':   stat_table.xpath('tr[3]/td[5]/text()').extract_first(),
            # 70
            'stat70_hp':    stat_table.xpath('tr[4]/td[2]/text()').extract_first(),
            'stat70_sp':    stat_table.xpath('tr[4]/td[3]/text()').extract_first(),
            'stat70_atk':   stat_table.xpath('tr[4]/td[4]/text()').extract_first(),
            'stat70_def':   stat_table.xpath('tr[4]/td[5]/text()').extract_first(),
            # Skill
            'skill_name' :      skill_table.xpath('tr[1]/td[2]//text()').extract(),
            'skill_sp':         skill_table.xpath('tr[2]/td[2]//text()').extract(),
            'skill_combo':      skill_table.xpath('tr[2]/td[4]//text()').extract(),
            'skill_hit':        skill_table.xpath('tr[2]/td[6]//text()').extract(),
            'skill_damage':     skill_table.xpath('tr[3]/td[2]//text()').extract(),
            'skill_range':      skill_table.xpath('tr[4]/td[2]//text()').extract(),
            'skill_effect':     skill_table.xpath('tr[5]/td[2]//text()').extract(),
            'skill_comment':    skill_table.xpath('tr[7]/td//text()').extract(),
            'skill_preview': response.xpath('//*[@id="rendered-body"]/div[2]/div/div[5]/a/img/@src').extract_first(),
            # Charge
            'charge_name':      charge_table.xpath('tr[1]/td[2]/text()').extract_first(),
            'charge_hit':       charge_table.xpath('tr[2]/td[2]/text()').extract_first(),
            'charge_damage':    charge_table.xpath('tr[3]/td[2]/text()').extract_first(),
            'charge_range':     charge_table.xpath('tr[4]/td[2]/text()').extract_first(),
            'charge_comment':   charge_table.xpath('tr[6]/td/text()').extract_first(),
            # Nakayoshi
            'nakayoshi_name':           nakayoshi.xpath('div[1]/table/tbody/tr/td[2]/text()').extract_first(),
            'nakayoshi_target_noevol':  nakayoshi.xpath('div[2]/div[1]/div[1]/table/tbody/tr[1]/td[2]/text()').extract_first(),
            'nakayoshi_effect_noevol':  nakayoshi.xpath('div[2]/div[1]/div[1]/table/tbody/tr[2]/td[2]/text()').extract_first(),

        }
