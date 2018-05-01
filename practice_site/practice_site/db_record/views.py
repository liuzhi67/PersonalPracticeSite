# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import time
import logging
from collections import Counter
from django.shortcuts import render, render_to_response
from django.http import JsonResponse
import requests
from lxml import etree
import urllib
import urllib2
import cookielib
import random

from dals import DBDAL, CloudTagDAL


api_logger = logging.getLogger('api')


# Create your views here.
# 模拟浏览器访问
cookie=cookielib.CookieJar()
handler=urllib2.HTTPCookieProcessor(cookie)
opener=urllib2.build_opener(handler)
# 先打开豆瓣建立cookie,否则https请求会403
resp=opener.open('http://book.douban.com')
for item in cookie:
    print 'Name = ' + item.name
    print 'Value = ' + item.value


connection=r'keep-alive'
agent=r'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'

headers={'User-Agent':agent, 'Connection':connection}
opener=urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
opener.addheaders.append(headers)


def get_html(url):
    api_logger.info('url:{} querying...'.format(url))
    resp = opener.open(url)
    api_logger.info('url:{} query finished code:{}'.format(url, resp.code))
    content = resp.read()

    html = etree.HTML(content)
    return html


def book_list(request):
    uid = request.GET.get('uid', '')
    url = 'https://book.douban.com/people/{}/collect'.format(uid)
    html = get_html(url)
    page_cnt = get_page_cnt(html)
    book_list = []
    url_page = 'https://book.douban.com/people/{}/collect?start={}&sort=time&rating=all&filter=all&mode=grid'
    for idx in range(page_cnt)[:3]:
        time.sleep(0.1)
        html = get_html(url_page.format(uid, idx*15))
        book_list.extend(get_book_infos(html))
    db_dal = DBDAL()
    [db_dal.insert(t, c, h) for (t, h, c) in book_list]

    return JsonResponse({'status': 0, 'data': {'book_infos': book_list, 'page_cnt': page_cnt}})


def get_book_infos(html):
    titles = html.xpath('/html/body/div/div/div/div/ul/li/div/h2/a')
    hrefs = html.xpath('/html/body/div/div/div/div/ul/li/div/h2/a/@href')
    comments = html.xpath('/html/body/div/div/div/div/ul/li/div/div/p')
    for t, h, c in zip(titles, hrefs, comments):
        print('t:{} h:{} c:{}'.format(t.text.strip(), h, c.text))
    book_list = [(t.text.strip(), h, c.text.strip()) for t, h, c in zip(titles, hrefs, comments)]
    return book_list


def get_page_cnt(html):
    pages = html.xpath('/html/body/div/div/div/div/div[@class="paginator"]/a')
    for p in pages:
        print('page: {}'.format(p.text))
    pcnt = int(pages[-1].text)
    return pcnt


def _get_tags(html):
    tags = html.xpath('/html/body/div/div/div/div/ul[@class="tag-list mb10"]/li/a')
    cnts = html.xpath('/html/body/div/div/div/div/ul[@class="tag-list mb10"]/li/span')
    rs = []
    tag_cnter = Counter()
    for t, c in zip(tags, cnts)[:33]:
        print('tag: {} cnt:{}'.format(t.text, c.text))
        # 随机字符串导致的 segmentfault 出现概率低一些
        # rs.append(' '.join([len(t.text) * str(random.randint(100, 10000))] * int(c.text)))
        rs.append(' '.join([t.text] * int(c.text)))
        tag_cnter[t.text] = int(c.text)
    return tag_cnter, ' '.join(rs)


def get_tags(request):
    uid = request.GET.get('uid', '')
    channel = request.GET.get('channel', 'book')
    if channel not in ['book', 'movie']:
        channel = 'book'
    url = 'https://{}.douban.com/people/{}/collect'.format(channel, uid)
    html = get_html(url)
    _, content = _get_tags(html)
    cloud_tag_dal = CloudTagDAL(content)
    cloud_tag_dal.create_html_data()
    return render_to_response('cloud.html')


def get_simple_tags(request):
    uid = request.GET.get('uid', '')
    channel = request.GET.get('channel', 'book')
    if channel not in ['book', 'movie']:
        channel = 'book'
    url = 'https://{}.douban.com/people/{}/collect'.format(channel, uid)
    html = get_html(url)
    tag_cnter, _ = _get_tags(html)
    cloud_tag_dal = CloudTagDAL('')
    cloud_tag_dal.create_simple_html_data(tag_cnter, 800, 800)
    return render_to_response('simple_cloud.html')
