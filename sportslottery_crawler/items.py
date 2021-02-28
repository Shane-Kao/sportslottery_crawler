# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class SportslotteryCrawlerItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    alliance = scrapy.Field()
    game_date = scrapy.Field()
    game_time = scrapy.Field()
    home_score = scrapy.Field()
    away_score = scrapy.Field()
    home_team = scrapy.Field()
    away_team = scrapy.Field()

