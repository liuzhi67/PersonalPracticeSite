# coding=utf-8
import os
import time
import logging
import random
import MySQLdb
from pytagcloud import create_tag_image, create_html_data, make_tags, \
    LAYOUT_HORIZONTAL
from pytagcloud.colors import COLOR_SCHEMES
from pytagcloud.lang.counter import get_tag_counts
from string import Template


api_logger = logging.getLogger('api')


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
        template_file.close()

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

    def generate_html_elements(self, tag_cnter, width=1000, height=1000):
        margin_w = int(width / 10)
        margin_h = int(height / 10)
        colors = ['#ff8939', '#b52841', '#ffc051', '#e85f4d', '#590051']
        sum_cnt = 0
        for t, c in tag_cnter.items():
            sum_cnt += c
        # 归一化
        norm_tags = {t: {'size': c*2.0/sum_cnt} for t, c in tag_cnter.items()}
        for t, c in norm_tags.items():
            norm_size = c['size'] * height
            norm_tags[t]['tag'] = t
            norm_tags[t]['size'] = norm_size
            norm_tags[t]['font-size'] = norm_size
            norm_tags[t]['height'] = norm_size + 1
            norm_tags[t]['color'] = colors[random.randint(0, len(colors)-1)]

        #norm_tags = {}
        #tags = make_tags(tag_cnter.items(), maxsize=120, colors=COLOR_SCHEMES['audacity'])
        #for x in tags:
        #    x['font-size'] = x['size']
        #    x['height'] = x['size']
        #    norm_tags[x['tag']] = x
        #    print('-----tag:{} norm_tag:{}'.format(x['tag'].encode('utf-8'), norm_tags[x['tag']]))

        # 按指定width*height空间根据尺寸随机生成标签云
        area_map = [[0] * width] * height
        for t, c in norm_tags.items():
            radius = int(max(c['font-size']/2, 1))
            w = random.randint(radius+margin_w, width-radius-margin_w)
            h = random.randint(radius+margin_h, height-radius-margin_h)
            step = 2
            try_cnt = max(height, width)/step
            while True:
                if try_cnt <= 0:
                    break
                try_cnt -= 1
                h = (h + step) % height
                w = (w + step) % width
                if h - radius < 0 or h + radius > height:
                    continue
                if w - radius < 0 or w + radius >width:
                    continue
                last_validh = h
                last_validw = w
                step *= 2
                used_cnt = 0
                for _h in range(h-radius, h+radius):
                    for _w in range(w-radius, w+radius):
                        used_cnt += area_map[_h][_w]
                total_cnt = 2 * radius * 2 * radius
                if used_cnt <= total_cnt/2.0:
                    for _h in range(h-radius, h+radius):
                        for _w in range(w-radius, w+radius):
                            area_map[_h][_w] = 1
                    c['left'] = w - radius
                    c['top'] = h - radius
                    break
            if 'top' not in c:
                for _h in range(last_validh-radius, last_validh+radius):
                    for _w in range(last_validw-radius, last_validw+radius):
                        area_map[_h][_w] = 1
                c['left'] = last_validw - radius
                c['top'] = last_validh - radius
        used_cnt = 0
        for _h in range(0, height):
            for _w in range(0, width):
                used_cnt += area_map[_h][_w]
        api_logger.info('width:{}|height:{}|used_cnt:{}'.format(width, height, used_cnt))
        return norm_tags

    def create_simple_html_data(self, tag_cnter, width=1000, height=1000):
        """
        HTML code sample
        """
        norm_tags = self.generate_html_elements(tag_cnter, width, height)

        template_file = open(os.path.join('templates/', 'web/simple_template.html'), 'r')
        html_template = Template(template_file.read())
        template_file.close()

        context = {}

        tags_template = '<li class="cnt" style="top: %(top)dpx; left: %(left)dpx; height: %(height)dpx; font-size: %(size)dpx; color: %(color)s;">%(tag)s</li>'

        context['tags'] = ''.join([tags_template % v for _, v in norm_tags.items()])
        context['width'] = width
        context['height'] = height
        context['css'] = ""

        html_text = html_template.substitute(context)

        html_file = open('templates/simple_cloud.html', 'w')
        html_file.write(html_text.encode('utf-8'))
        html_file.close()
