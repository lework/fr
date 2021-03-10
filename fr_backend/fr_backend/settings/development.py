from .defaults import *

APP_ENV = 'development'

SECRET_KEY = '-nq(f9ar0s@qsr%1dnw-4o3!-86^9z%dpi93z*^5wsm&&xpbo9'

ALLOWED_HOSTS = ['*']

# Disable capturing DEBUG
DEBUG = True
TEMPLATE_DEBUG = DEBUG
SQL_DEBUG = DEBUG

# django-debug-toolbar
INSTALLED_APPS += ['debug_toolbar', ]
MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware']
INTERNAL_IPS = ['127.0.0.1']

DEBUG_TOOLBAR_CONFIG = {
    'ENABLE_STACKTRACES': True,
}

AUTH_TOKEN_EXPIRATION = 60 * 60 * 7 * 24  # 用户token的失效时间，单位秒
