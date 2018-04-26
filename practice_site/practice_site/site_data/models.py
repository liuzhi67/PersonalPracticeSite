# coding=utf-8

from __future__ import unicode_literals

from django.db import models


class Site(models.Model):
    id = models.PositiveIntegerField(primary_key=True, blank=True, verbose_name=u'自增id(留空自动生成)')
    name = models.CharField(max_length=32, verbose_name=u'网站名称')
    url = models.CharField(max_length=255, verbose_name=u'网址')
    mtime = models.DateTimeField(auto_now=True, verbose_name=u'修改时间')
    ctime = models.DateTimeField(auto_now=True,  verbose_name=u'创建时间')

    class Meta:
        db_table = 'site'


def get_site_choices():
    rcs = Site.objects.all()
    choices = [(x.id, x.name) for x in rcs]
    return choices

class User(models.Model):
    id = models.PositiveIntegerField(primary_key=True, blank=True, verbose_name=u'自增id(留空自动生成)')
    site_id = models.PositiveIntegerField(verbose_name=u'网站', choices=get_site_choices())
    user_id = models.CharField(max_length=32, verbose_name=u'用户id')
    name = models.CharField(max_length=128, verbose_name=u'用户名')
    description = models.TextField(verbose_name=u'备注')
    mtime = models.DateTimeField(auto_now=True, verbose_name=u'修改时间')
    ctime = models.DateTimeField(auto_now=True,  verbose_name=u'创建时间')

    def __init__(self, *args, **kargs):
        super(User, self).__init__(*args, **kargs)
        self._meta.get_field('site_id').choices = get_site_choices()

    class Meta:
        db_table = 'user'
