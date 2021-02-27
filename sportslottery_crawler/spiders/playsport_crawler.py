import re
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
        doc = pq(response.body)
        alliance = doc('.tag-chosen').text()
        row_ = doc('tr[gameid]').remove('.vsicon')
        assert not len(row_) % 2
        game_time = [j.find('.td-gameinfo h4').text() for i, j in enumerate(row_.items()) if not i % 2]
        scores = [j.find('.scores').text().split() for i, j in enumerate(row_.items()) if not i % 2]
        home_score = [i[1] if i else None for i in scores]
        away_score = [i[0] if i else None for i in scores]
        teams = re.sub(r'\d', '', doc('.td-teaminfo').remove('p').text()).split()
        home_team = teams[1::2]
        away_team = teams[::2]
        print([SportslotteryCrawlerItem(
            game_time=i[0],
            home_score=i[1],
            away_score=i[2],
            home_team=i[3],
            away_team=i[4],
        ) for i in zip(game_time, home_score, away_score, home_team, away_team)])
        return [SportslotteryCrawlerItem(
            game_time=i[0],
            home_score=i[1],
            away_score=i[2],
            home_team=i[3],
            away_team=i[4],
        ) for i in zip(game_time, home_score, away_score, home_team, away_team)]