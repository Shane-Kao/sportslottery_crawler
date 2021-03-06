# -*- coding: utf-8 -*-
__author__ = 'Shane_Kao'
from scrapy.crawler import CrawlerProcess
from apscheduler.schedulers.twisted import TwistedScheduler
from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_ERROR

from sportslottery_crawler.spiders.playsport_crawler import PlaysportCrawler
from scrapy.utils.project import get_project_settings
from utils.notifier import _notifier


def my_listener(event):
    if event.exception:
        _ = _notifier(msg='\n'.join(["Crawler Failed" , ]))
    else:
        _ = _notifier(msg='\n'.join(["Crawler Worked", ]))


def main():
    process = CrawlerProcess(get_project_settings())
    process.crawl(PlaysportCrawler)
    scheduler = TwistedScheduler()
    scheduler.add_job(process.crawl, 'interval', hours=3, args=[PlaysportCrawler])
    scheduler.add_listener(my_listener, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR)
    scheduler.start()
    process.start(False)


if __name__ == '__main__':
    main()