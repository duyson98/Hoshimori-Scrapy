import csv
import os

import scrapy


class StageDifficultyDatabaseSpider(scrapy.Spider):
    name = "stagedifficultydatabase"
    allowed_domains = ["wiki.dengekionline.com"]
    custom_settings = {
        'FEED_FORMAT': 'csv',
        'FEED_URI': 'results/stage_difficulty_database.csv',
        'FEED_EXPORT_FIELDS': ['episode', 'stage_number', 'difficulty',
                               'level', 'exp', 'coins', 'cheerpoint', 'drops', 'objectives',
                               ],
        'ITEM_PIPELINES': {'hoshimori.pipelines.stage_csv_pipeline.StageCSVPipeline': 300},
    }
    middle_file = 'stagelist.csv'

    @classmethod
    def start_requests(self):
        url = 'https://wiki.dengekionline.com'
        with open(self.middle_file) as f:
            reader = csv.reader(f)
            # Skip first line
            next(f)
            count = 0
            for row in reader:
                if count == 815: break
                yield scrapy.Request(url + row[2], callback=self.parse)
                count += 1

    @classmethod
    def parse(self, response):
        data_table = response.xpath("//*[@id='rendered-body']/div[2]/div[1]/div[1]/table/tbody")
        if not data_table:
            data_table = response.xpath("//*[@id='rendered-body']/div/div[1]/div[1]/table/tbody")

        item_table = response.xpath("//*[@id='rendered-body']/div[2]/div[1]/div[2]/table/tbody")
        if not item_table:
            item_table = response.xpath("//*[@id='rendered-body']/div/div[1]/div[2]/table/tbody")

        objective_list = response.xpath("//*[@id='rendered-body']/div[2]/div[1]/p[1]//text()").extract()
        if not objective_list:
            objective_list = response.xpath("//*[@id='rendered-body']/div/div[1]/p[1]//text()").extract()

        if data_table:
            if len(objective_list) == 16:
                yield {
                    'stage_name': response.xpath("//*[@id='page-main-title']/text()").extract_first(),
                    # easy
                    'difficulty': "Easy",
                    'level': data_table.xpath("./tr[2]/td[2]/text()").extract_first(),
                    'exp': data_table.xpath("./tr[3]/td[2]/text()").extract_first(),
                    'coins': data_table.xpath("./tr[4]/td[2]/text()").extract_first(),
                    'cheerpoint': data_table.xpath("./tr[5]/td[2]/text()").extract_first(),
                    'drops': response.xpath("//*[@id='rendered-body']/div/div[1]/div[2]/table/tbody/tr[2]//text()").extract(),
                    'objectives': "%s,%s,%s" % (objective_list[1].split('\n')[1], objective_list[2].split('\n')[1], objective_list[3].split('\n')[1]),
                }

                yield {
                    'stage_name': response.xpath("//*[@id='page-main-title']/text()").extract_first(),
                    # normal
                    'difficulty': "Normal",
                    'level': data_table.xpath("./tr[2]/td[3]/text()").extract_first(),
                    'exp': data_table.xpath("./tr[3]/td[3]/text()").extract_first(),
                    'coins': data_table.xpath("./tr[4]/td[3]/text()").extract_first(),
                    'cheerpoint': data_table.xpath("./tr[5]/td[3]/text()").extract_first(),
                    'drops': response.xpath("//*[@id='rendered-body']/div/div[1]/div[3]/table/tbody/tr[2]//text()").extract(),
                    'objectives': "%s,%s,%s" % (objective_list[5].split('\n')[1], objective_list[6].split('\n')[1], objective_list[7].split('\n')[1]),
                }

                yield {
                    'stage_name': response.xpath("//*[@id='page-main-title']/text()").extract_first(),
                    # hard
                    'difficulty': "Hard",
                    'level': data_table.xpath("./tr[2]/td[4]/text()").extract_first(),
                    'exp': data_table.xpath("./tr[3]/td[4]/text()").extract_first(),
                    'coins': data_table.xpath("./tr[4]/td[4]/text()").extract_first(),
                    'cheerpoint': data_table.xpath("./tr[5]/td[4]/text()").extract_first(),
                    'drops': response.xpath("//*[@id='rendered-body']/div/div[1]/div[4]/table/tbody/tr[2]//text()").extract(),
                    'objectives': "%s,%s,%s" % (objective_list[9].split('\n')[1], objective_list[10].split('\n')[1], objective_list[11].split('\n')[1]),
                }

                yield {
                    'stage_name': response.xpath("//*[@id='page-main-title']/text()").extract_first(),
                    # ex
                    'difficulty': "Ex",
                    'level': data_table.xpath("./tr[2]/td[5]/text()").extract_first(),
                    'exp': data_table.xpath("./tr[3]/td[5]/text()").extract_first(),
                    'coins': data_table.xpath("./tr[4]/td[5]/text()").extract_first(),
                    'cheerpoint': data_table.xpath("./tr[5]/td[5]/text()").extract_first(),
                    'drops': response.xpath("//*[@id='rendered-body']/div/div[1]/div[5]/table/tbody/tr[2]//text()").extract(),
                    'objectives': "%s,%s,%s" % (objective_list[13].split('\n')[1], objective_list[14].split('\n')[1], objective_list[15].split('\n')[1]),
                }
            else:
                yield {
                    'stage_name': response.xpath("//*[@id='page-main-title']/text()").extract_first(),
                    # easy
                    'difficulty': "Easy",
                    'level': data_table.xpath("./tr[2]/td[2]/text()").extract_first(),
                    'exp': data_table.xpath("./tr[3]/td[2]/text()").extract_first(),
                    'coins': data_table.xpath("./tr[4]/td[2]/text()").extract_first(),
                    'cheerpoint': data_table.xpath("./tr[5]/td[2]/text()").extract_first(),
                    'drops': item_table.xpath(".//text()").extract(),
                    'objectives': "%s,%s,%s" % (objective_list[1].split('\n')[1], objective_list[2].split('\n')[1], objective_list[3].split('\n')[1]),
                }

                yield {
                    'stage_name': response.xpath("//*[@id='page-main-title']/text()").extract_first(),
                    # normal
                    'difficulty': "Normal",
                    'level': data_table.xpath("./tr[2]/td[3]/text()").extract_first(),
                    'exp': data_table.xpath("./tr[3]/td[3]/text()").extract_first(),
                    'coins': data_table.xpath("./tr[4]/td[3]/text()").extract_first(),
                    'cheerpoint': data_table.xpath("./tr[5]/td[3]/text()").extract_first(),
                    'drops': item_table.xpath(".//text()").extract(),
                    'objectives': "%s,%s,%s" % (objective_list[5].split('\n')[1], objective_list[6].split('\n')[1], objective_list[7].split('\n')[1]),
                }

                yield {
                    'stage_name': response.xpath("//*[@id='page-main-title']/text()").extract_first(),
                    # hard
                    'difficulty': "Hard",
                    'level': data_table.xpath("./tr[2]/td[4]/text()").extract_first(),
                    'exp': data_table.xpath("./tr[3]/td[4]/text()").extract_first(),
                    'coins': data_table.xpath("./tr[4]/td[4]/text()").extract_first(),
                    'cheerpoint': data_table.xpath("./tr[5]/td[4]/text()").extract_first(),
                    'drops': item_table.xpath(".//text()").extract(),
                    'objectives': "%s,%s,%s" % (objective_list[9].split('\n')[1], objective_list[10].split('\n')[1], objective_list[11].split('\n')[1]),
                }

    @classmethod
    def closed(self, reason):
        os.remove(self.middle_file)
