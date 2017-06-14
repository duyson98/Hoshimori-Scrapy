import scrapy
from xml.dom import minidom


class StageListSpider(scrapy.Spider):
    name = "stagelist"
    allowed_domains = ["wiki.dengekionline.com"]
    custom_settings = {
        'FEED_FORMAT': 'xml',
        'FEED_URI': 'results/stagelist.xml',
        'CONCURRENT_REQUESTS': 1,
    }
    def start_requests(self):
        url = 'https://wiki.dengekionline.com'
        grouplist = minidom.parse("stagegrouplist.xml")
        urls = grouplist.getElementsByTagName("relative_url")
        for node in urls:
            yield scrapy.Request(url + node.firstChild.data, self.parse)

    def parse(self, response):
        table = response.xpath("//*[@id='rendered-body']/div[2]/div/table/tbody/tr/td[2]")

        for stage in table:
            stage_url = stage.css("a::attr(href)")
            if stage_url:
                yield {
                    'relative_url': stage_url.extract_first()
                }


        def spider_closed(self, spider):
            spider.logger.info('Spider closed: %s', spider.name)
