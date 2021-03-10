# Django
from django.conf.urls import url, include

# Account app
from apps.account.views import AuthTokenView
from apps.account.urls import urlpatterns as user_urls
from apps.accident.urls import urlpatterns as accident_urls

# Self
from .views import ApiRootView, ApiV1RootView

v1_urls = [
    url('^$', ApiV1RootView.as_view(), name='api_v1_root_view'),
    url('^login/$', AuthTokenView.as_view(), name='login'),
    url('users/', include(user_urls)),
    url('accidents/', include(accident_urls)),
]

urlpatterns = [
    url('^$', ApiRootView.as_view(), name='api_root_view'),
    url('^(?P<version>(v1))/', include(v1_urls))
]
