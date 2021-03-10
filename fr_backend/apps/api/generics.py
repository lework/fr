# Python
import re
import time

# Django
from django.conf import settings
from django.db import connection
from django.utils.translation import ugettext_lazy as _

# Django REST framework
from rest_framework import views, generics
from rest_framework.exceptions import PermissionDenied, AuthenticationFailed, ParseError, UnsupportedMediaType


def camelcase_to_underscore(s):
    """
    Convert CamelCase names to lowercase_with_underscore.
    """
    s = re.sub(r'(((?<=[a-z])[A-Z])|([A-Z](?![A-Z]|$)))', '_\\1', s)
    return s.lower().strip('_')


class APIView(views.APIView):
    # schema = get_default_schema()
    # versioning_class = URLPathVersioning

    def initialize_request(self, request, *args, **kwargs):
        """
        Django 初始化请求，在这里记录请求开始时间
        """

        self.time_started = time.time()
        if getattr(settings, 'SQL_DEBUG', False):
            self.queries_before = len(connection.queries)

        drf_request = super(APIView, self).initialize_request(request, *args, **kwargs)
        request.drf_request = drf_request
        try:
            request.drf_request_user = getattr(drf_request, 'user', False)
        except AuthenticationFailed:
            request.drf_request_user = None
        except (PermissionDenied, ParseError) as exc:
            request.drf_request_user = None
            self.__init_request_error__ = exc
        except UnsupportedMediaType as exc:
            exc.detail = _('You did not use correct Content-Type in your HTTP request. '
                           'If you are using our REST API, the Content-Type must be application/json')
            self.__init_request_error__ = exc
        return drf_request

    def finalize_response(self, request, response, *args, **kwargs):
        """
        记录400请求的警告日志, 在header中添加api请求时间。
        """
        if response.status_code >= 400:
            status_msg = "status %s received by user %s attempting to access %s from %s" % \
                         (response.status_code, request.user, request.path, request.META.get('REMOTE_ADDR', None))
            if hasattr(self, '__init_request_error__'):
                response = self.handle_exception(self.__init_request_error__)
            if response.status_code == 401:
                response.data["data"]['detail'] = ' To establish a login session, visit /api/login/.'
            else:
                pass
        response = super(APIView, self).finalize_response(request, response, *args, **kwargs)
        time_started = getattr(self, 'time_started', None)
        if time_started:
            time_elapsed = time.time() - self.time_started
            response['X-API-Time'] = '%0.3fs' % time_elapsed
        if getattr(settings, 'SQL_DEBUG', False):
            queries_before = getattr(self, 'queries_before', 0)
            q_times = [float(q['time']) for q in connection.queries[queries_before:]]
            response['X-API-Query-Count'] = len(q_times)
            response['X-API-Query-Time'] = '%0.3fs' % sum(q_times)
        # response["Access-Control-Allow-Origin"] = "*"
        # response["Access-Control-Allow-Headers"] = "*"
        if getattr(self, 'deprecated', False):
            response[
                'Warning'] = '299 awx "This resource has been deprecated and will be removed in a future release."'  # noqa
        return response


class GenericAPIView(generics.GenericAPIView, APIView):
    pass


class ListAPIView(generics.ListAPIView, GenericAPIView):
    pass


class ListCreateAPIView(ListAPIView, generics.ListCreateAPIView):
    pass


class RetrieveAPIView(generics.RetrieveAPIView, GenericAPIView):
    pass


class RetrieveUpdateAPIView(RetrieveAPIView, generics.RetrieveUpdateAPIView):
    pass


class RetrieveDestroyAPIView(RetrieveAPIView, generics.DestroyAPIView):
    pass


class RetrieveUpdateDestroyAPIView(RetrieveUpdateAPIView, generics.DestroyAPIView):
    pass
