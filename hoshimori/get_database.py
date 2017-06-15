from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from twisted.internet import reactor, defer

from hoshimori.spiders.card_database_extra_spider import ExtraCardDatabaseSpider
from hoshimori.spiders.card_database_normal_spider import NormalCardDatabaseSpider
from hoshimori.spiders.card_database_sub_spider import SubCardDatabaseSpider
from hoshimori.spiders.card_list_extra_spider import ExtraCardlistSpider
from hoshimori.spiders.card_list_normal_spider import NormalCardlistSpider
from hoshimori.spiders.card_list_sub_spider import SubCardlistSpider

configure_logging()
runner = CrawlerRunner()


@defer.inlineCallbacks
def crawl():
    yield runner.crawl(NormalCardlistSpider)
    yield runner.crawl(ExtraCardlistSpider)
    yield runner.crawl(SubCardlistSpider)
    yield runner.crawl(NormalCardDatabaseSpider)
    yield runner.crawl(ExtraCardDatabaseSpider)
    yield runner.crawl(SubCardDatabaseSpider)
    reactor.stop()


crawl()
reactor.run()  # the script will block here until the last crawl call is finished
