# Python
import time
import threading

# Django
from django.utils.deprecation import MiddlewareMixin


class TimingMiddleware(threading.local, MiddlewareMixin):
    """
    中间件，计算API总消耗时间
    """

    def process_request(self, request):
        self.start_time = time.time()

    def process_response(self, request, response):
        if not hasattr(self, 'start_time'):  # some tools may not invoke process_request
            return response
        total_time = time.time() - self.start_time
        response['X-API-Total-Time'] = '%0.3fs' % total_time

        return response

