# -*- coding: utf-8 -*-
import json
import redis
KEY = "FluSpider"

# import pymysql
# # 和数据库建立链接
# conn = pymysql.connect(host="122.226.111.10", user="db_rw", password="molbase1010", database="baike", port=3306)
# # 游标
# cursor = conn.cursor()
#
#
# # 数据库查询
# query_sql = "SELECT * FROM book_test_info;"
# cursor.execute(query_sql)
# query_res = cursor.fetchall()
# # print(query_res)
# for i in query_res:
#     print(i)
#
# cursor.close()
# conn.close()



def main():
    redis_client = redis.Redis(host='192.168.2.11', port=6379)
    raw_urls = ['http://www.fluorochem.co.uk/Products/Products?Page={}'.format(i) for i in range(1, 20 + 1)]
    for url in raw_urls:
        print(url)
        redis_client.lpush("{}:start_urls".format(KEY), url)
    redis_client.close()


if __name__ == '__main__':
    main()
