from datetime import datetime, timedelta

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from pyquery import PyQuery as pq

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
        doc = pq(response.body)
        print(doc('.tag-chosen').text())