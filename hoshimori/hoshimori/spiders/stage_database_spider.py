import csv
import os

import scrapy


class StageDatabaseSpider(scrapy.Spider):
    name = "stagedatabase"
    allowed_domains = ["wiki.dengekionline.com"]
    custom_settings = {
        'FEED_FORMAT': 'csv',
        'FEED_URI': 'results/stage_database.csv',
        'FEED_EXPORT_FIELDS': ['stage_name', 'episode', 'stage_number', 'story_part', 'story_chapter',
                               'small_irous', 'large_irous',
                               # 'easy_level', 'easy_exp', 'easy_coins', 'easy_cheerpoint', 'easy_objectives',
                               # 'normal_level', 'normal_exp', 'normal_coins', 'normal_cheerpoint', 'normal_objectives',
                               # 'hard_level', 'hard_exp', 'hard_coins', 'hard_cheerpoint', 'hard_objectives', 'drops',
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
                yield scrapy.Request(url + row[2], callback=self.parse,
                                     meta={'story_part': row[0], 'story_chapter': row[1]})
                count += 1

    @classmethod
    def parse(self, response):
        data_table = response.xpath("//*[@id='rendered-body']/div[2]/div[1]/div[1]/table/tbody")
        if not data_table:
            data_table = response.xpath("//*[@id='rendered-body']/div/div[1]/div[1]/table/tbody")

        small_irous_table = response.xpath("//*[@id='rendered-body']/div[2]/div[1]/ul[1]/li[1]/div/table")
        if not small_irous_table:
            small_irous_table = response.xpath("//*[@id='rendered-body']/div/div[1]/ul[1]/li[1]/div/table")

        large_irous_table = response.xpath("//*[@id='rendered-body']/div[2]/div[1]/ul[1]/li[2]/div/table")
        if not large_irous_table:
            large_irous_table = response.xpath("//*[@id='rendered-body']/div/div[1]/ul[1]/li[2]/div/table")
            if not large_irous_table:
                large_irous_table = response.xpath("//*[@id='rendered-body']/div/div[1]/ul[2]/li/div/table")

        if data_table:
            yield {
                # stage
                'stage_name': response.xpath("//*[@id='page-main-title']/text()").extract_first(),
                'story_part': response.meta['story_part'],
                'story_chapter': response.meta['story_chapter'],
                'small_irous': small_irous_table.xpath(".//text()").extract(),
                'large_irous': large_irous_table.xpath(".//text()").extract(),
            }

    @classmethod
    def closed(self, reason):
        os.remove(self.middle_file)
