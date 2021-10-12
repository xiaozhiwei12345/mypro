# coding=utf-8
from importlib import import_module
from bs4 import UnicodeDammit


class DBService(object):

    def __getattr__(self, key):
        return eval("super(DBService, self).__getattribute__('server').%s" % key)


class MysqlService(DBService):

    # 将字典item拼接成sql插入语句
    @classmethod
    def join_sql_from_map(cls, insert_table, args_map, db_name=None):
        sql_template = "insert into %s(%s) values(%s);"
        dict_list = args_map.items()

        fields = ",".join(map(lambda x: "%s" % x[0], dict_list))
        value = map(lambda x: '"%s"' % (
                    not isinstance(x[1], str) and str(x[1]).replace("\\", "\\\\").replace('"', '\\"') or x[1].replace(
                "\\", "\\\\").replace('"', '\\"')), dict_list)
        value = ",".join(value)
        if not db_name:
            return sql_template % (insert_table, fields, value)
        sql = sql_template % ("%s.%s" % (db_name, insert_table), fields, value)
        sql = sql.replace('"None"', "null")
        return sql

    @classmethod
    def update_sql_from_map(cls, table_name, update_target, update_dict, db_name=None):
        if not db_name:
            header = "update %s set " % table_name
        else:
            header = "update %s.%s set " % (db_name, table_name)
        content, footer = [], []
        for k, v in update_dict.items():
            content.append('`%s`="%s"' % (k, str(v).replace("\\", "\\\\").replace('"', '\\"')))
        for k, v in update_target.items():
            footer.append('`%s`="%s"' % (k, str(v).replace("\\", "\\\\").replace('"', '\\"')))
        _content = ",".join(content).replace('"None"', "null")
        _footer = "and".join(footer).replace('"None"', "null")
        return "%s%s where %s" % (header, _content, _footer)

    @classmethod
    def join_query_map(self, query_map, item_join_symbol="=", multi_join_symbol=" and "):
        return multi_join_symbol.join(map(lambda item: '`%s`%s%s' % (self.mysql_escape(item[0]), item_join_symbol,
                                                                     '"%s"' % self.mysql_escape(
                                                                         item[1]) if self.mysql_escape(
                                                                         item[1]) is not None else "null"),
                                          query_map.items())).replace("=null", " is null")

    @classmethod
    def mysql_escape(self, s):
        return s.replace("\\", "\\\\").replace('"', '\\"').replace("%", "%%") if isinstance(s, str) else s

    @classmethod
    def join_sql_from_map_with_s(cls, insert_table, args_map):
        sql_template = "insert into %s(%s) value(%s);"
        dict_list = args_map.items()

        fields = ",".join(map(lambda x: "`%s`" % x[0], dict_list))
        value = []
        for item in dict_list:
            x = item[1]
            x = str(x)
            print("%s encoding %s" % (x, UnicodeDammit(x).original_encoding))
            e = UnicodeDammit(x).original_encoding
            if e:
                x = x.decode(e)
            value.append(x)
        tmp_value = ['%s' for i in range(len(value))]
        tmp_value = ",".join(tmp_value)
        print("\n\n\n tmp_value %s \n\n" % tmp_value)
        return sql_template % (insert_table, fields, tmp_value), value

    # 和数据库建立链接
    def __init__(self, host, user, password, port):
        self.sqlalchemy = import_module("sqlalchemy")
        self.server = self.sqlalchemy.create_engine("mysql+pymysql://{}:{}@{}:{}/?charset=utf8".format(user, password, host, port))

    # 查询数据库，返回数据字典组成的列表
    def query(self, sql):
        query_result = self.execute(sql)
        return [dict(i) for i in query_result]

    # 执行sql函数
    def execute(self, sql):
        result = self.server.execute(sql)
        return result

    # 执行没有完全拼接的sql
    def execute_with_argument(self, sql, argument=None):
        result = self.server.execute(sql, argument)
        return result

    # 选择数据库
    def select_db(self, db):
        self.execute("use %s;" % db)