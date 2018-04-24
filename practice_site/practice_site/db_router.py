# coding=utf-8


class DBRouter(object):
    def db_for_read(self, model, **kargs):
        if model._meta.db_table in ['user', 'site']:
            return 'test'
        return 'default'

    def db_for_write(self, model, **kargs):
        if model._meta.db_table in ['user', 'site']:
            return 'test'
        return 'default'
