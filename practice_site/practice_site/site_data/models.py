# coding=utf-8

from __future__ import unicode_literals

from django.db import models


class Site(models.Model):
    id = models.PositiveIntegerField(primary_key=True, blank=True)
    name = models.CharField(max_length=32, verbose_name=u'网站名称')
    url = models.CharField(max_length=255, verbose_name=u'网址')
    mtime = models.DateTimeField(auto_now=True, verbose_name=u'修改时间')
    ctime = models.DateTimeField(auto_now=True,  verbose_name=u'创建时间')

    class Meta:
        db_table = 'site'


def get_area_choices():
    rcs = Site.objects.all()
    choices = [(x.id, x.name) for x in rcs]
    return choices

class User(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    name = models.CharField(max_length=32, verbose_name=u'用户名', choices=get_area_choices())
    description = models.TextField(verbose_name=u'备注', choices=get_area_choices())
    mtime = models.DateTimeField(auto_now=True, verbose_name=u'修改时间')
    ctime = models.DateTimeField(auto_now=True,  verbose_name=u'创建时间')

    class Meta:
        db_table = 'user'
