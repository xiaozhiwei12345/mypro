# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ExampleItem(scrapy.Item):
    # define the fields for your item here like:
    cat_num = scrapy.Field()
    pdt_name = scrapy.Field()
    cas_number = scrapy.Field()
    href = scrapy.Field()
