'''
Created on May 26, 2017

@author: Koko
'''
import scrapy


class CardlistSpider(scrapy.Spider):
    name = "cardlist"
    allowed_domains = ["wiki.dengekionline.com"]
    start_urls = (
        'https://wiki.dengekionline.com/battlegirl/%E3%82%AB%E3%83%BC%E3%83%89%E4%B8%80%E8%A6%A7',
        )

    def parse(self, response):
        card_table = response.xpath("//*[@id='rendered-body']/div/div/div/div/div/table")
        
        for card in card_table.xpath("//tbody/tr"):
            yield {
                'relative_url': card.css("a::attr(href)").extract_first(),
            }
