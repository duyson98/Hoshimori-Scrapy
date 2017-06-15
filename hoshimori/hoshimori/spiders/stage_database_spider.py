import os
from xml.dom import minidom

import scrapy


class StageDatabaseSpider(scrapy.Spider):
    name = "stagedatabase"
    allowed_domains = ["wiki.dengekionline.com"]
    custom_settings = {
        'FEED_FORMAT': 'csv',
        'FEED_URI': 'results/stage_database.csv',
        'FEED_EXPORT_FIELDS': ['stage_name', 'episode', 'stage_number',
                               'easy_level', 'easy_exp', 'easy_coins', 'easy_cheerpoint', 'easy_objectives',
                               'normal_level', 'normal_exp', 'normal_coins', 'normal_cheerpoint', 'normal_objectives',
                               'hard_level', 'hard_exp', 'hard_coins', 'hard_cheerpoint', 'hard_objectives', 'drops', ],
        'ITEM_PIPELINES': {'hoshimori.pipelines.stage_csv_pipeline.StageCSVPipeline': 300},
    }
    middle_file = 'results/stagelist.xml'

    @classmethod
    def start_requests(self):
        url = 'https://wiki.dengekionline.com'
        stagelist = minidom.parse(self.middle_file)
        urls = stagelist.getElementsByTagName("relative_url")
        for node in urls:
            yield scrapy.Request(url + node.firstChild.data, self.parse)

    @classmethod
    def parse(self, response):
        data_table = response.xpath("//*[@id='rendered-body']/div[2]/div[1]/div[1]/table/tbody")
        if not data_table:
            data_table = response.xpath("//*[@id='rendered-body']/div/div[1]/div[1]/table/tbody")

        if data_table:
            item_table = response.xpath("//*[@id='rendered-body']/div[2]/div[1]/div[2]/table/tbody")
            if not item_table:
                item_table = response.xpath("//*[@id='rendered-body']/div/div[1]/div[2]/table/tbody")

            objective_list = response.xpath("//*[@id='rendered-body']/div[2]/div[1]/p[1]//text()").extract()
            if not objective_list:
                objective_list = response.xpath("//*[@id='rendered-body']/div/div[1]/p[1]//text()").extract()

            yield {
                # stage
                'stage_name': response.xpath("//*[@id='page-main-title']/text()").extract_first(),

                # easy
                'easy_level': data_table.xpath("./tr[2]/td[2]/text()").extract_first(),
                'easy_exp': data_table.xpath("./tr[3]/td[2]/text()").extract_first(),
                'easy_coins': data_table.xpath("./tr[4]/td[2]/text()").extract_first(),
                'easy_cheerpoint': data_table.xpath("./tr[5]/td[2]/text()").extract_first(),
                'easy_objectives': (objective_list[1], objective_list[2], objective_list[3],),

                # normal
                'normal_level': data_table.xpath("./tr[2]/td[3]/text()").extract_first(),
                'normal_exp': data_table.xpath("./tr[3]/td[3]/text()").extract_first(),
                'normal_coins': data_table.xpath("./tr[4]/td[3]/text()").extract_first(),
                'normal_cheerpoint': data_table.xpath("./tr[5]/td[3]/text()").extract_first(),
                'normal_objectives': (objective_list[6], objective_list[7], objective_list[8],),

                # hard
                'hard_level': data_table.xpath("./tr[2]/td[4]/text()").extract_first(),
                'hard_exp': data_table.xpath("./tr[3]/td[4]/text()").extract_first(),
                'hard_coins': data_table.xpath("./tr[4]/td[4]/text()").extract_first(),
                'hard_cheerpoint': data_table.xpath("./tr[5]/td[4]/text()").extract_first(),
                'hard_objectives': (objective_list[11], objective_list[12], objective_list[13],),

                'drops': item_table.xpath("./tr[2]/td/strong/text()").extract(),
            }

    @classmethod
    def closed(self, reason):
        os.remove(self.middle_file)
