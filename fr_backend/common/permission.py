# Django Rest Framework
from rest_framework.permissions import BasePermission


class IsSuperUser(BasePermission):
    """
    超级管理员.
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_superuser


class UnauthenticatedGet(BasePermission):
    """
    允许GET方式
    """
    def has_permission(self, request, view):
        return request.method in ['GET']
