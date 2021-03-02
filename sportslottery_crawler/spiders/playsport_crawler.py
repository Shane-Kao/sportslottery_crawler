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

    @staticmethod
    def _process_count(row, class_name, type_):
        cnt_info = [i.find('.{}'.format(class_name)).next().text() for i in row.items()]
        cnt_info = cnt_info[1::2] if type_ != "total" else cnt_info[::2]
        return [int(i.split('%')[0])/100 if i else None for i in cnt_info]

    @staticmethod
    def _process_tw_info(row, class_name):
        info_ = [i.find('.{}'.format(class_name)).text() for i in row.items()]
        odds1 = [i.split(',')[-1].strip() if i else None for i in info_[1::2]]
        odds2 = [i.split(',')[-1].strip() if i else None for i in info_[::2]]
        val_ = [float(i.split(',')[0][1:]) if i else None for i in info_[1::2]]
        return val_, odds1, odds2

    @staticmethod
    def _process_oversea_info(row, class_name):
        info = [i.find('.{}'.format(class_name)).text() for i in row.items()]
        info = [[info[i], info[i + 1]] for i in range(len(info)) if not i % 2]
        info = [i[0] if len(i[0]) > len(i[1]) else i[1] for i in info]
        return info

    @staticmethod
    def _process_oversea_diff():
        pass

    @staticmethod
    def _process_oversea_total():
        pass

    def get_alliance(self, response):
        doc = pq(response.body)
        m_ = re.match(r'.+gametime=(\d+)$', response.url)
        game_date = m_.group(1)
        alliance = doc('.tag-chosen').text()
        row_ = doc('tr[gameid]').remove('.vsicon').remove(".aid8-teaminfo")
        assert not len(row_) % 2
        game_time = [j.find('.td-gameinfo h4').text() for i, j in enumerate(row_.items()) if not i % 2]
        scores = [j.find('.scores').text().split() for i, j in enumerate(row_.items()) if not i % 2]
        home_score = [i[1] if i else None for i in scores]
        away_score = [i[0] if i else None for i in scores]
        teams = re.sub(r'\d', '', doc('.td-teaminfo').remove('p').text()).split()
        home_team = teams[1::2]
        away_team = teams[::2]
        tw_diff, tw_diff_home_odds, tw_diff_away_odds = self._process_tw_info(row_, "td-bank-bet01")
        tw_diff_home_count = self._process_count(row_, "td-bank-bet01", "diff")
        tw_odds = [i.find('.td-bank-bet03').text()[1:] if i.find('.td-bank-bet03').text() else None for i in
                   row_.items()]
        tw_away_odds = tw_odds[::2]
        tw_home_odds = tw_odds[1::2]
        tw_home_count = self._process_count(row_, "td-bank-bet03", "money_line")
        tw_total, tw_under_odds, tw_over_odds = self._process_tw_info(row_, "td-bank-bet02")
        tw_over_count = self._process_count(row_, "td-bank-bet02", "total")
        oversea_diff_info = self._process_oversea_info(row_, "td-universal-bet01")
        oversea_diff_home_count = self._process_count(row_, "td-universal-bet01", "diff")
        oversea_total_info = self._process_oversea_info(row_, "td-universal-bet02")
        oversea_over_count = self._process_count(row_, "td-universal-bet02", "total")
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
            oversea_diff=oversea_diff_info,
            oversea_diff_home_count=oversea_diff_home_count,
            oversea_total=oversea_total_info,
            oversea_over_count=oversea_over_count,
        )