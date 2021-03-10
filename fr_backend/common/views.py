# Django Rest Framework
from rest_framework import views


def exception_handler(exc, context):
    """
    自定义 drf 的 异常处理
    :param exc:
    :param context:
    :return:
    """
    response = views.exception_handler(exc, context)
    if response is not None:
        msg = 'failure' if response.status_code >= 400 else 'success'
        notification_response = {'code': response.status_code, 'msg': msg, 'data': response.data}
        response.data = notification_response
    return response
