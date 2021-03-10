# Python
import six

# Django Rest Framework
from rest_framework import response
from rest_framework.serializers import Serializer


class Response(response.Response):
    """
    自定义json返回体
    """
    def __init__(self, data=None, status=200, msg="success",
                 template_name=None, headers=None,
                 exception=False, content_type=None):

        super(Response, self).__init__(None, status=status)

        if isinstance(data, Serializer):
            msg = (
                'You passed a Serializer instance as data, but '
                'probably meant to pass serialized `.data` or '
                '`.error`. representation.'
            )
            raise AssertionError(msg)

        resp_data = {
            "code": status,
            "msg": msg,
            "data": {}
        }

        if status >= 400:
            resp_data['statue'] = 'failure'

        resp_data['data'] = data

        self.data = resp_data
        self.template_name = template_name
        self.exception = exception
        self.content_type = content_type

        if headers:
            for name, value in six.iteritems(headers):
                self[name] = value

