import scrapy
from xml.dom import minidom


class StageDatabaseSpider(scrapy.Spider):
    name = "stagedatabase"
    allowed_domains = ["wiki.dengekionline.com"]
    custom_settings = {
        'FEED_FORMAT': 'csv',
        'FEED_URI': 'stage_database.csv',
        'FEED_EXPORT_FIELDS': ['stage_type', 'stage_name', 'easy_dangerLv', 'easy_expPt', 'easy_coins', 'easy_bondPt', 'easy_objectives',
                               'normal_dangerLv', 'normal_expPt', 'normal_coins', 'normal_bondPt', 'normal_objectives',
                               'hard_dangerLv', 'hard_expPt', 'hard_coins', 'hard_bondPt', 'hard_objectives', 'items',
        ],
        'ITEM_PIPELINES': {'hoshimori.pipelines.stage_csv_pipeline.StageCSVPipeline': 300},
        'CONCURRENT_REQUESTS': 1,
    }
    def start_requests(self):
        url = 'https://wiki.dengekionline.com'
        stagelist = minidom.parse("stagelist.xml")
        urls = stagelist.getElementsByTagName("relative_url")
        count = 0
        for node in urls:
            if count == 3: break
            yield scrapy.Request(url + node.firstChild.data, self.parse)
            count += 1


    def parse(self, response):
        data_table = response.xpath("//*[@id='rendered-body']/div[2]/div[1]/div[1]/table/tbody")
        item_table = response.xpath("//*[@id='rendered-body']/div[2]/div[1]/div[2]/table/tbody")

        if not data_table:
            yield {
                'stage_type': 'Story',
                'stage_name': response.xpath(".//*[@id='page-main-title']/text()").extract_first(),
                'items': '',
            }
        else:
            objective_list = response.xpath("//*[@id='rendered-body']/div[2]/div[1]/p[1]//text()").extract()

            yield {
                #stage
                'stage_type': 'Quest',
                'stage_name': response.xpath(".//*[@id='page-main-title']/text()").extract_first(),

                #easy
                'easy_dangerLv':    data_table.xpath("./tr[2]/td[2]/text()").extract_first(),
                'easy_expPt':       data_table.xpath("./tr[3]/td[2]/text()").extract_first(),
                'easy_coins':       data_table.xpath("./tr[4]/td[2]/text()").extract_first(),
                'easy_bondPt':      data_table.xpath("./tr[5]/td[2]/text()").extract_first(),
                'easy_objectives':  (objective_list[1], objective_list[2], objective_list[3],),

                #normal
                'normal_dangerLv':    data_table.xpath("./tr[2]/td[3]/text()").extract_first(),
                'normal_expPt':       data_table.xpath("./tr[3]/td[3]/text()").extract_first(),
                'normal_coins':       data_table.xpath("./tr[4]/td[3]/text()").extract_first(),
                'normal_bondPt':      data_table.xpath("./tr[5]/td[3]/text()").extract_first(),
                'normal_objectives':  (objective_list[5], objective_list[6], objective_list[7],),

                #hard
                'hard_dangerLv':    data_table.xpath("./tr[2]/td[4]/text()").extract_first(),
                'hard_expPt':       data_table.xpath("./tr[3]/td[4]/text()").extract_first(),
                'hard_coins':       data_table.xpath("./tr[4]/td[4]/text()").extract_first(),
                'hard_bondPt':      data_table.xpath("./tr[5]/td[4]/text()").extract_first(),
                'hard_objectives':  (objective_list[9], objective_list[10], objective_list[11],),

                'items': item_table.xpath("./tr[2]/td/strong/text()").extract(),
            }