# Django
from django.urls import include, path
from django.conf.urls import url

# Django REST framework
from rest_framework import routers

# Self
from .views import AuthTokenView, UserViewSet


router = routers.SimpleRouter()
router.register(r'', UserViewSet, basename="users")


urlpatterns = [
    path('token', AuthTokenView.as_view(), name='token'),
    url(r'', include(router.urls)),
]
