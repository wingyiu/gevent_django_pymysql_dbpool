# uncompyle6 version 2.14.1
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.10 (default, Oct 23 2015, 19:19:21) 
# [GCC 4.2.1 Compatible Apple LLVM 7.0.0 (clang-700.0.59.5)]
# Embedded file name: ./esb/common/djmysql_pool.py
# Compiled at: 2017-11-16 15:44:28
import logging
from sqlalchemy import exc
from sqlalchemy import event
from sqlalchemy.pool import manage
from sqlalchemy.pool import Pool
POOL_PESSIMISTIC_MODE = False
POOL_SETTINGS = {}
POOL_SETTINGS.setdefault('recycle', 3600)
logger = logging.getLogger('djmysql_pool.pool')

@event.listens_for(Pool, 'checkout')
def _on_checkout(dbapi_connection, connection_record, connection_proxy):
    logger.debug('connection retrieved from pool')
    if POOL_PESSIMISTIC_MODE:
        cursor = dbapi_connection.cursor()
        try:
            cursor.execute('SELECT 1')
        except:
            raise exc.DisconnectionError()
        finally:
            cursor.close()


@event.listens_for(Pool, 'checkin')
def _on_checkin(*args, **kwargs):
    logger.debug('connection returned to pool')


@event.listens_for(Pool, 'connect')
def _on_connect(*args, **kwargs):
    logger.debug('connection created')


def patch_mysql(pool_options={}):

    class hashabledict(dict):

        def __hash__(self):
            return hash(tuple(sorted(self.items())))

    class hashablelist(list):

        def __hash__(self):
            return hash(tuple(sorted(self)))

    class ManagerProxy(object):

        def __init__(self, manager):
            self.manager = manager

        def __getattr__(self, key):
            return getattr(self.manager, key)

        def connect(self, *args, **kwargs):
            if 'conv' in kwargs:
                conv = kwargs['conv']
                if isinstance(conv, dict):
                    items = []
                    for k, v in conv.items():
                        if isinstance(v, list):
                            v = hashablelist(v)
                        items.append((k, v))

                    kwargs['conv'] = hashabledict(items)
            if 'ssl' in kwargs:
                ssl = kwargs['ssl']
                if isinstance(ssl, dict):
                    items = []
                    for k, v in ssl.items():
                        if isinstance(v, list):
                            v = hashablelist(v)
                        items.append((k, v))

                    kwargs['ssl'] = hashabledict(items)
            return self.manager.connect(*args, **kwargs)

    from django.db.backends.mysql import base as mysql_base
    POOL_SETTINGS = pool_options
    if not hasattr(mysql_base, '_Database'):
        mysql_base._Database = mysql_base.Database
        mysql_base.Database = ManagerProxy(manage(mysql_base._Database, **POOL_SETTINGS))