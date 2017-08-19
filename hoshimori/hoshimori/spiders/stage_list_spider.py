import os
from xml.dom import minidom

import scrapy


class StageListSpider(scrapy.Spider):
    name = "stagelist"
    allowed_domains = ["wiki.dengekionline.com"]
    custom_settings = {
        'FEED_FORMAT': 'csv',
        'FEED_URI': 'results/stagelist.csv',
        'FEED_EXPORT_FIELDS': ['story_part', 'story_chapter', 'relative_url'],
    }
    middle_file = 'stagegrouplist.xml'

    @classmethod
    def start_requests(self):
        url = 'https://wiki.dengekionline.com'
        grouplist = minidom.parse(self.middle_file)
        urls = grouplist.getElementsByTagName("relative_url")
        for node in urls:
            yield scrapy.Request(url + node.firstChild.data, self.parse)

    @classmethod
    def parse(self, response):
        table = response.xpath("//*[@id='rendered-body']/div[2]/div/table/tbody/tr/td[2]")

        for stage in table:
            stage_url = stage.css("a::attr(href)")
            if stage_url:
                yield {
                    'story_part': response.xpath("//*[@id='page-main-title']/text()").extract_first().split('/')[1].split(' ')[0],
                    'story_chapter': response.xpath("//*[@id='page-main-title']/text()").extract_first().split('/')[1].split(' ')[1],
                    'relative_url': stage_url.extract_first(),
                }

    @classmethod
    def closed(self, reason):
        os.remove(self.middle_file)
