import scrapy


class SportslotteryCrawlerItem(scrapy.Item):
    alliance = scrapy.Field()
    game_date = scrapy.Field()
    game_time = scrapy.Field()
    away_score = scrapy.Field()
    home_score = scrapy.Field()
    away_team = scrapy.Field()
    home_team = scrapy.Field()
    tw_diff = scrapy.Field()
    tw_total = scrapy.Field()
    tw_away_odds = scrapy.Field()
    tw_home_odds = scrapy.Field()
    tw_diff_away_odds = scrapy.Field()
    tw_diff_home_odds = scrapy.Field()
    tw_under_odds = scrapy.Field()
    tw_over_odds = scrapy.Field()
    tw_home_count = scrapy.Field()
    tw_diff_home_count = scrapy.Field()
    tw_over_count = scrapy.Field()
    oversea_diff = scrapy.Field()
    oversea_diff_home_count = scrapy.Field()
    oversea_total = scrapy.Field()
    oversea_over_count = scrapy.Field()
