'''
Created on May 26, 2017

@author: Koko
'''
import scrapy
from xml.dom import minidom

class CardDatabaseSpider(scrapy.Spider):
    name = "database"
    allowed_domains = ["wiki.dengekionline.com"]
    
    def start_requests(self):
        url = 'https://wiki.dengekionline.com/'
        count = 0
        cardlist = minidom.parse("cardlist.xml")
        urls = cardlist.getElementsByTagName("relative_url")
        while count < 3:
            yield scrapy.Request(url + urls[count].firstChild.data, self.parse)
            count += 1

    def parse(self, response):
        yield {
            'card_name': response.xpath('//*[@id="rendered-body"]/div[2]/div/div[1]/table/tbody/tr[2]/td[2]/text()').extract_first()
        }
