# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pandas as pd

from utils.create_dir import create_dir


class SportslotteryCrawlerPipeline:
    def process_item(self, item, spider):
        item_dict = dict(item)
        alliance = item_dict.pop('alliance')
        game_date = item_dict.pop('game_date')
        df = pd.DataFrame(item_dict)
        create_dir("data/{}".format(alliance))
        df.to_csv("data/{}/{}.csv".format(alliance, game_date), index=False)


