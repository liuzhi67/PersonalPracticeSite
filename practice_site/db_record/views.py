# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import time
from django.shortcuts import render, render_to_response
from django.http import JsonResponse
import requests
from lxml import etree
import urllib
import urllib2
import cookielib

from dals import DBDAL, CloudTagDAL

# Create your views here.
# 模拟浏览器访问
cookie=cookielib.CookieJar()
handler=urllib2.HTTPCookieProcessor(cookie)
opener=urllib2.build_opener(handler)
resp=opener.open('http://book.douban.com')
for item in cookie:
    print 'Name = ' + item.name
    print 'Value = ' + item.value


connection=r'keep-alive'
agent=r'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'

headers={'User-Agent':agent, 'Connection':connection}
opener=urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
opener.addheaders.append(headers)


def get_html(uid):
    url = 'https://book.douban.com/people/{}/collect'.format(uid)
    url_page = 'https://book.douban.com/people/{}/collect?start={}&sort=time&rating=all&filter=all&mode=grid'

    resp = opener.open(url)
    content = resp.read()

    print('url:{}'.format(url))
    html = etree.HTML(content)
    return html


def book_list(request):
    uid = request.GET.get('uid', '')
    url_page = 'https://book.douban.com/people/{}/collect?start={}&sort=time&rating=all&filter=all&mode=grid'
    html = get_html(uid)
    page_cnt = get_page_cnt(html)
    _get_tags(html)
    book_list = []
    for idx in range(page_cnt)[:3]:
        time.sleep(0.1)
        resp = opener.open(url_page.format(uid, idx*15))
        content = resp.read()
        html = etree.HTML(content)
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
    pages = html.xpath('/html/body/div/div/div/div/div/a')
    for p in pages:
        print('page: {}'.format(p.text))
    pcnt = int(pages[-1].text)
    return pcnt


def _get_tags(html):
    tags = html.xpath('/html/body/div/div/div/div/ul[@class="tag-list mb10"]/li/a')
    cnts = html.xpath('/html/body/div/div/div/div/ul[@class="tag-list mb10"]/li/span')
    rs = []
    for t, c in zip(tags, cnts)[:33]:
        print('tag: {} cnt:{}'.format(t.text, c.text))
        rs.append(' '.join([t.text] * int(c.text)))
    return ' '.join(rs)


def get_tags(request):
    uid = request.GET.get('uid', '')
    html = get_html(uid)
    content = _get_tags(html)
    print('ctype:{}'.format(type(content)))
    print('content:{}'.format(content))
    cloud_tag_dal = CloudTagDAL(content)
    cloud_tag_dal.create_html_data()
    return render_to_response('cloud.html')
