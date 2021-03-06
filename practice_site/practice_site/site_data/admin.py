# coding=utf-8
from __future__ import unicode_literals

from django.contrib import admin
from models import Site, User


@admin.register(Site)
class SiteAdmin(admin.ModelAdmin):
    list_display = ('name', 'url', 'mtime', 'ctime')


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'name', 'description', 'mtime', 'ctime')
    list_editable = []
