import scrapy


class SportslotteryCrawlerItem(scrapy.Item):
    alliance = scrapy.Field()
    game_date = scrapy.Field()
    game_time = scrapy.Field()
    home_score = scrapy.Field()
    away_score = scrapy.Field()
    home_team = scrapy.Field()
    away_team = scrapy.Field()

