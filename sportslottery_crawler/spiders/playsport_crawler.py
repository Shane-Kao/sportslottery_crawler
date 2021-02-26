from datetime import datetime, timedelta

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from pyquery import PyQuery as pq

from sportslottery_crawler.items import SportslotteryCrawlerItem

# >scrapy crawl playsport
today = datetime.now().strftime(format="%Y%m%d")
yesterday = (datetime.now() - timedelta(days=1)).strftime(format="%Y%m%d")

class PlaysportCrawler(CrawlSpider):
    name = 'playsport'
    start_urls = ["https://www.playsport.cc/predictgame.php?action=scale&allianceid=4"]

    rules = [
        Rule(
            link_extractor=LinkExtractor(
                allow="predictgame.php\?action=scale\&allianceid=((?!90|4)\d+)\&sid=0&gametime={}$".format(today),
                process_value=lambda x: x + '&gametime={}'.format(today)
            ),
            callback="get_alliance",
        ),
        Rule(
            link_extractor=LinkExtractor(
                allow="predictgame.php\?action=scale\&allianceid=((?!90|4)\d+)\&sid=0&gametime={}$".format(yesterday),
                process_value=lambda x: x + '&gametime={}'.format(yesterday)
            ),
            callback="get_alliance",
        ),
    ]

    def get_alliance(self, response):
        sportslottery_crawler_item = SportslotteryCrawlerItem()
        doc = pq(response.body)
        alliance = doc('.tag-chosen').text()
        row_ = doc('tr[gameid]')
        assert not len(row_) % 2
        game_time = [j.find('.td-gameinfo h4').text() for i, j in enumerate(row_.items()) if not i % 2]
        # game_records = [doc('tr[gameid]')[i: i + 2] for i in range(0, len(doc('tr[gameid]')), 2)]

        # for i in doc('.td-gameinfo h4').text().split():
        #     sportslottery_crawler_item['date_time'] = i
        # print(doc('.td-gameinfo h4').text())
        # print(doc('.tag-chosen').text())
        return alliance, sportslottery_crawler_item