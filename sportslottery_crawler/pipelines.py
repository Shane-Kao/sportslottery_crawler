import pandas as pd

from utils.create_dir import create_dir
from utils.notifier import _notifier


class SportslotteryCrawlerPipeline:
    def process_item(self, item, spider):
        spider_name = spider.name
        item_dict = dict(item)
        alliance = item_dict.pop('alliance')
        game_date = item_dict.pop('game_date')
        df = pd.DataFrame(item_dict)
        if not df.empty:
            create_dir("data/{}/{}".format(spider_name, alliance))
            df.to_csv("data/{}/{}/{}.csv".format(spider_name, alliance, game_date), index=False)
            status_code = _notifier(
                msg='\n'.join(["Success", alliance, game_date])
            )
            if status_code != 200:
                raise Exception
