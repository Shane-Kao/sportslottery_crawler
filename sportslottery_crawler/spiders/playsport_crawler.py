import re
from datetime import datetime, timedelta

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from pyquery import PyQuery as pq

from sportslottery_crawler.items import SportslotteryCrawlerItem

# >scrapy crawl playsport
# TODO:crawl for certain day
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
        m_ = re.match(r'.+gametime=(\d+)$', response.url)
        game_date = m_.group(1)
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
        tw_diff_info = [i.find('.td-bank-bet01').text() for i in row_.items()]
        tw_diff_home_odds = [i.split(',')[-1].strip() if i else None for i in tw_diff_info[1::2]]
        tw_diff_away_odds = [i.split(',')[-1].strip() if i else None for i in tw_diff_info[::2]]
        tw_diff = [float(i.split(',')[0][1:]) if i else None for i in tw_diff_info[1::2]]
        tw_diff_cnt_info = [i.find('.td-bank-bet01').next().text() for i in row_.items()][1::2]
        tw_diff_home_count = [int(i.split('%')[0])/100 if i else None for i in tw_diff_cnt_info]
        tw_away_odds = [i.find('.td-bank-bet03').text()[1:] if i.find('.td-bank-bet03').text()
                        else None for i in row_.items()][::2]
        tw_home_odds = [i.find('.td-bank-bet03').text()[1:] if i.find('.td-bank-bet03').text()
                        else None for i in row_.items()][1::2]
        tw_home_count=[int(i.find('.td-bank-bet03').next().text().split('%')[0]) / 100 if i.find(
            '.td-bank-bet03').next().text() else None
         for i in row_.items()][1::2]
        tw_total_info = [i.find('.td-bank-bet02').text() for i in row_.items()]
        tw_under_odds = [i.split(',')[-1].strip() if i else None for i in tw_total_info[1::2]]
        tw_over_odds = [i.split(',')[-1].strip() if i else None for i in tw_total_info[::2]]
        tw_total = [float(i.split(',')[0][1:]) if i else None for i in tw_total_info[1::2]]
        tw_total_cnt_info = [i.find('.td-bank-bet02').next().text() for i in row_.items()][::2]
        tw_over_count = [int(i.split('%')[0])/100 if i else None for i in tw_total_cnt_info]
        return SportslotteryCrawlerItem(
            alliance=alliance,
            game_date=game_date,
            game_time=game_time,
            away_score=away_score,
            home_score=home_score,
            away_team=away_team,
            home_team=home_team,
            tw_diff=tw_diff,
            tw_diff_away_odds=tw_diff_away_odds,
            tw_diff_home_odds=tw_diff_home_odds,
            tw_diff_home_count=tw_diff_home_count,
            tw_away_odds=tw_away_odds,
            tw_home_odds=tw_home_odds,
            tw_home_count=tw_home_count,
            tw_total=tw_total,
            tw_under_odds=tw_under_odds,
            tw_over_odds=tw_over_odds,
            tw_over_count=tw_over_count,
        )