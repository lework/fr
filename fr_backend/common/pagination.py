# Python
from collections import OrderedDict

# Django Rest Framework
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination


class BasePageNumberPagination(PageNumberPagination):
    """
    分页设置
    """
    page_size = 10
    page_size_query_param = 'size'
    page_query_param = 'page'
    max_page_size = 1000

    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('count', self.page.paginator.count),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('results', data)
        ]))
