# coding=utf-8
import MySQLdb


class DBDAL(object):
    def __init__(self):
        self.db = MySQLdb.connect(host='127.0.0.1', port=3306, user='site', passwd='hz123456', db='test')
        self.cursor = self.db.cursor()
        self.cursor.execute('set names utf8mb4;')

    def insert(self, title, comment, url):
        sql = 'insert into db_book(title, comment, url) values ("{}", "{}", "{}");'.format(title.encode('utf-8'), comment.encode('utf-8'), url)
        print('sql:{}'.format(sql))
        res = self.cursor.execute(sql)
        self.db.commit()
        return res
