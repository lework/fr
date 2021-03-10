# Django
from django.urls import include
from django.conf.urls import url

# Django REST framework
from rest_framework import routers

# Self
from .views import EventViewSet, RecordViewSet


router = routers.SimpleRouter()
router.register(r'event', EventViewSet, basename="event")
router.register(r'record', RecordViewSet, basename="record")


urlpatterns = [
    url(r'', include(router.urls)),
]
