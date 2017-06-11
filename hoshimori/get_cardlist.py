from twisted.internet import reactor, defer
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging

from hoshimori.spiders.extracardlist_spider import ExtraCardlistSpider
from hoshimori.spiders.normalcardlist_spider import NormalCardlistSpider
from hoshimori.spiders.subcardlist_spider import SubCardlistSpider

configure_logging()
runner = CrawlerRunner()

@defer.inlineCallbacks
def crawl():
    yield runner.crawl(NormalCardlistSpider)
    yield runner.crawl(ExtraCardlistSpider)
    yield runner.crawl(SubCardlistSpider)
    reactor.stop()

crawl()
reactor.run() # the script will block here until the last crawl call is finished