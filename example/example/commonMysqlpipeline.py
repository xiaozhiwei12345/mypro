# -*- coding: utf-8 -*-

import time
import json
import logging
import hashlib
from example.DBService import MysqlService
from twisted.internet.threads import deferToThread
import copy
logger = logging.getLogger(__name__)

# 将字典加密


def md5_from_dict(item):
    sort_list = sorted(item.items(), key=lambda x: x[0])
    # 全部统一成str
    sort_list = list(map(lambda s: list(map(str, s)), sort_list))
    return hashlib.md5(str(sort_list).encode('utf-8')).hexdigest()


def current_time():
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))


class commonpipeline(object):
    """通过继承 commonpipeline 来保证

    1. pipeline 是异步同时进行的
    2. 一旦出错，能及时汇报上去，汇报到 failed_urls

    注意, commonpipeline 调用的都是 _process_item  前面有一个 _ 下划线
    """

    def process_item(self, item, spider):
        d = deferToThread(self._process_item, item, spider)

        def error_back(err):
            pass
        d.addErrback(error_back)
        return d


MYSQL_HOST = "192.168.2.11"
MYSQL_USER = "root"
MYSQL_PASSWORD = "123456"
MYSQL_PORT = 3306
MYSQL_DB = "zhongyi"
MYSQL_TABLE = "book_test_info"


class commonMysqlpipeline(commonpipeline):

    def __init__(self, settings):
        self.mysql_host = MYSQL_HOST
        self.mysql_user = MYSQL_USER
        self.mysql_password = MYSQL_PASSWORD
        self.mysql_port = MYSQL_PORT
        self.mysql_db = MYSQL_DB
        self.mysql_table = MYSQL_TABLE

        self.server = MysqlService(
            self.mysql_host, self.mysql_user, self.mysql_password, self.mysql_port)
        self.server.select_db(self.mysql_db)

    @classmethod
    def from_settings(cls, settings):
        return cls(settings)

    @classmethod
    def from_crawler(cls, crawler):
        return cls.from_settings(crawler.settings)

    def _process_item(self, item, spider):

        config_dict = item.pop("easyspider")
        hash_value = md5_from_dict(item)
        query_map = 'hash_check="%s"' % hash_value

        unique_key = "id"
        current_db = config_dict.get("mysql_config").get("db")
        current_table = config_dict.get("mysql_config").get("table")
        check_sql = "select %s from %s.%s where %s;" % (unique_key, current_db, current_table, query_map)
        check_result = self.server.query(check_sql)
        if check_result:
            # 找到记录，那么后续的操作就是update更新
            unique_key_item = check_result[0].get(unique_key)
            item["last_checktime"] = current_time()
            update_sql = self.server.update_sql_from_map(
                current_table, {unique_key: unique_key_item}, item, current_db).replace("%", "%%")
            logger.debug(
                "already have record, update last_checktime, running sql is %s" % update_sql)
            self.server.execute(update_sql)
        else:
            # 找不到记录，那么就是直接插入
            item["hash_check"] = hash_value
            item["last_checktime"] = current_time()
            item["created_time"] = current_time()
            sql = self.server.join_sql_from_map(
                current_table, item, current_db).replace("%", "%%")
            logger.debug("find a new record, insert sql is %s" % sql)
            self.server.execute(sql)
        return item