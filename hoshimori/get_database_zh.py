from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from twisted.internet import reactor, defer

from hoshimori.spiders.card_database_zh_spider import ZhCardDatabaseSpider
from hoshimori.spiders.card_list_zh_spider import ZhCardlistSpider

configure_logging()
runner = CrawlerRunner()


@defer.inlineCallbacks
def crawl():
    yield runner.crawl(ZhCardlistSpider)
    yield runner.crawl(ZhCardDatabaseSpider)
    reactor.stop()


crawl()
reactor.run()  # the script will block here until the last crawl call is finished
