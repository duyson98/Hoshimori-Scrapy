from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from twisted.internet import reactor, defer

from hoshimori.spiders.stage_database_spider import StageDatabaseSpider
from hoshimori.spiders.stage_list_group_spider import StageGroupListSpider
from hoshimori.spiders.stage_list_spider import StageListSpider

configure_logging()
runner = CrawlerRunner()


@defer.inlineCallbacks
def crawl():
    yield runner.crawl(StageGroupListSpider)
    yield runner.crawl(StageListSpider)
    yield runner.crawl(StageDatabaseSpider)
    reactor.stop()


crawl()
reactor.run()  # the script will block here until the last crawl call is finished
