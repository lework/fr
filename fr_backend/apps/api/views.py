# Python
from collections import OrderedDict

# Django
from django.utils.translation import gettext as _
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie

# Django Rest framework
from rest_framework.reverse import reverse
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

# Self
from .generics import APIView


class ApiRootView(APIView):
    permission_classes = (AllowAny,)
    name = _('REST API')

    @method_decorator(ensure_csrf_cookie)
    def get(self, request, format=None, *args, **kwargs):
        """ 列出支持的api版本 """

        v1 = reverse('api:api_v1_root_view', request=request, format=format, args=args, kwargs={'version': 'v1'})

        data = OrderedDict()
        data['description'] = _('REST API')
        data['current_version'] = v1
        data['available_versions'] = dict(v1=v1)

        return Response(data)


class ApiVersionRootView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, format=None, *args, **kwargs):
        """
        列出所有的的api接口
        :param request:
        :param format:
        :param args:
        :param kwargs:
        :return:
        """
        data = OrderedDict()
        data['login'] = reverse('api:login', request=request, format=format, args=args, kwargs=kwargs)
        data['users'] = reverse('api:users-list', request=request, format=format, args=args, kwargs=kwargs)
        data['event'] = reverse('api:event-list', request=request, format=format, args=args, kwargs=kwargs)
        data['record'] = reverse('api:record-list', request=request, format=format, args=args, kwargs=kwargs)
        return Response(data)


class ApiV1RootView(ApiVersionRootView):
    """
    api的v1版本
    """
    view_name = _('Version 1')
