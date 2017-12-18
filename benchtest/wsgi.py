"""
WSGI config for benchtest project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/howto/deployment/wsgi/
"""

# from gevent import monkey
# monkey.patch_all()

try:
    import pymysql
    pymysql.install_as_MySQLdb()
except:
    pass

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "benchtest.settings")

application = get_wsgi_application()
