# -*- coding: utf-8 -*-
from scrapy.pipelines.files import FilesPipeline
import os
from urllib.parse import urlparse
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
import datetime
import logging
HOST = '122.226.111.10'
USER = 'mock_baike'
PASSWORD = 'molbase1010'
DB = 'baike'

class ExamplePipeline(object):

    def __init__(self):
        self.conn = pymysql.Connect(host=HOST, port=3306, user=USER, db=DB, password=PASSWORD, charset='utf8')  # 创建连接
        self.cursor = self.conn.cursor()  # 创建游标
        self.cat_num_set = set()

    def open_spider(self, spider):
        pass

    def close_spider(self, spider):
        self.cursor.close()
        self.conn.close()

    def process_item(self, item, spider):
        # if item['cat_num'] not in self.cat_num_set:
        #     self.cat_num_set.add(item['cat_num'])
        pass
        # else:
        #     print("数据库已存在***************************")
        #     return item


# class SelfDefineFilePipline(FilesPipeline):
#     """
#     继承FilesPipeline，更改其存储文件的方式
#     """
#     # def __init__(self, *args, **kwargs):
#     #     super().__init__(*args, **kwargs)
#
#     def file_path(self, request, response=None, info=None):
#         # parse_result = urlparse(request.url)
#         # path = parse_result.path
#         # basename = os.path.basename(path)
#         basename = os.path.basename(request.url)
#         return basename
#         # path = urlparse(request.url).path
#         # return join(basename(dirname(path)), basename(path))