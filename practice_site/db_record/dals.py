# coding=utf-8
import MySQLdb
from pytagcloud import create_tag_image, create_html_data, make_tags, \
    LAYOUT_HORIZONTAL
from pytagcloud.colors import COLOR_SCHEMES
from pytagcloud.lang.counter import get_tag_counts
from string import Template
import os
import time


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


class CloudTagDAL(object):
    def __init__(self, content):
        self.content = content

    def create_html_data(self):
        """
        HTML code sample
        """
        tags = make_tags(get_tag_counts(self.content), maxsize=120, colors=COLOR_SCHEMES['audacity'])
        # FIXME 存在segmentfault bug
        data = create_html_data(tags, (840,1000), layout=LAYOUT_HORIZONTAL, fontname='PT Sans Regular')

        template_file = open(os.path.join('templates/', 'web/template.html'), 'r')
        html_template = Template(template_file.read())

        context = {}

        tags_template = '<li class="cnt" style="top: %(top)dpx; left: %(left)dpx; height: %(height)dpx;"><a class="tag %(cls)s" href="#%(tag)s" style="top: %(top)dpx;\
        left: %(left)dpx; font-size: %(size)dpx; height: %(height)dpx; line-height:%(lh)dpx;">%(tag)s</a></li>'

        context['tags'] = ''.join([tags_template % link for link in data['links']])
        context['width'] = data['size'][0]
        context['height'] = data['size'][1]
        context['css'] = "".join("a.%(cname)s{color:%(normal)s;}\
        a.%(cname)s:hover{color:%(hover)s;}" %
                                  {'cname':k,
                                   'normal': v[0],
                                   'hover': v[1]}
                                 for k,v in data['css'].items())

        html_text = html_template.substitute(context)

        html_file = open('templates/cloud.html', 'w')
        html_file.write(html_text.encode('utf-8'))
        html_file.close()