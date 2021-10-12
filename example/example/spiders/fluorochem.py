# -*- coding: utf-8 -*-

from scrapy_redis.spiders import RedisSpider

from example.items import ExampleItem


class BookSpider(RedisSpider):
    name = 'FluSpider'
    # redis_key = "book:start_urls"
    custom_settings = {
        'DEFAULT_REQUEST_HEADERS': {
            'User-Agent': ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                           'Chrome/77.0.3865.120 Safari/537.36'),
        },
        "DOWNLOAD_DELAY": 2,
        # "SCHEDULER": "scrapy_redis.scheduler.Scheduler",
        # "DUPEFILTER_CLASS": "scrapy_redis.dupefilter.RFPDupeFilter",
        "REDIS_URL": 'redis://@192.168.2.11:6379',
        # "SCHEDULER_PERSIST": True,
        # "SCHEDULER_QUEUE_CLASS": 'scrapy_redis.queue.SpiderPriorityQueue',
        # "DUPEFILTER_DEBUG": True
    }

    def parse(self, response):
        trs = response.xpath('//table[@id="tblSearchResults"]//tr')
        for tr in trs[1:]:
            cat_num = tr.xpath('./td[1]/text()').get()
            pdt_name = tr.xpath('./td[2]/text()').get()
            cas_number = tr.xpath('./td[3]/text()').get()
            href = tr.xpath('./td[4]/a/@href').get()
            href = response.urljoin(href)
            crawled_url = response.url
            yield {
                "cat_num": cat_num,
                "pdt_name": pdt_name,
                "cas_number": cas_number,
                "href": href,
                "crawled_url": crawled_url,
                "easyspider": {
                    "mysql_config": {
                        "db": "zhongyi",
                        "table": "book_test_info"
                    }
                }
            }