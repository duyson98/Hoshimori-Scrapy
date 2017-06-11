from twisted.internet import reactor, defer
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging

from hoshimori.spiders.extra_card_database_spider import ExtraCardDatabaseSpider
from hoshimori.spiders.normal_card_database_spider import NormalCardDatabaseSpider
from hoshimori.spiders.sub_card_database_spider import SubCardDatabaseSpider

configure_logging()
runner = CrawlerRunner()

@defer.inlineCallbacks
def crawl():
    yield runner.crawl(NormalCardDatabaseSpider)
    yield runner.crawl(ExtraCardDatabaseSpider)
    yield runner.crawl(SubCardDatabaseSpider)
    reactor.stop()

crawl()
reactor.run() # the script will block here until the last crawl call is finished