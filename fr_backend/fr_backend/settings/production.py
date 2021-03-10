from .defaults import *

APP_ENV = 'production'

SECRET_KEY = '-nq(f9ar0s@qsr%1dnw-4o3!-86^9z%dpi93z*^5wsm&&xpbo9'

ALLOWED_HOSTS = ['*']

DEBUG = False
TEMPLATE_DEBUG = DEBUG
SQL_DEBUG = DEBUG

# # mysql
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': 'one',
#         'USER': 'root',
#         'PASSWORD': '123456',
#         'HOST': 'localhost',
#         'OPTIONS': {
#             "init_command": "SET foreign_key_checks=0;",
#         }
#     }
# }

AUTH_TOKEN_EXPIRATION = 60 * 60 * 24  # 用户token的失效时间，单位秒
