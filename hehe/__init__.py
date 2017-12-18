from common.djmysql_pool import patch_mysql
from django.conf import settings
patch_mysql(pool_options=settings.DJMYSQL_POOL_OPTIONS)