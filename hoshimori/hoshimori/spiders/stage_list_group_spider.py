import os

import scrapy


class StageGroupListSpider(scrapy.Spider):
    name = "stagegrouplist"
    allowed_domain = ["wiki.dengekionline.com"]

    custom_settings = {
        'FEED_FORMAT': 'xml',
        'FEED_URI': 'results/stagegrouplist.xml',
    }

    start_urls = (
        'https://wiki.dengekionline.com/battlegirl/%E3%82%AF%E3%82%A8%E3%82%B9%E3%83%88',
    )
    middle_file = ''

    @classmethod
    def parse(self, response):
        all_stages = response.xpath("//*[@id='rendered-body']/div/div[1]/div")

        count = 0
        for group in all_stages:
            yield {
                'relative_url': group.css("p a::attr(href)").extract_first()
            }
            count += 1
            if count == 24: break

    def closed(self, reason):
        os.remove(self.middle_file)
