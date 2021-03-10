# Django REST framework
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

# Project
from common.pagination import BasePageNumberPagination
from common.permission import UnauthenticatedGet

# API APP
from apps.api.generics import APIView

# Self
from .models import Event, Record
from .serializers.event import EventListSerializer, EventModifySerializer, RecordListSerializer, RecordModifySerializer


class EventViewSet(ModelViewSet, APIView):
    queryset = Event.objects.all().order_by('-id')
    pagination_class = BasePageNumberPagination
    permission_classes = [UnauthenticatedGet | IsAuthenticated]
    lookup_field = 'sn'

    def get_serializer_class(self):
        # 根据请求类型动态变更serializer
        if self.action in ('list', ):
            return EventListSerializer
        else:
            return EventModifySerializer


class RecordViewSet(ModelViewSet, APIView):
    queryset = Record.objects.all().order_by('-id')
    pagination_class = BasePageNumberPagination
    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        # 根据请求类型动态变更serializer
        if self.action in ('list',):
            return RecordListSerializer
        else:
            return RecordModifySerializer
