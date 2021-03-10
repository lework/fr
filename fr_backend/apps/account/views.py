# Python
import re
import json

# Django
from django.conf import settings
from django.utils.timezone import now
from django.contrib.auth.hashers import check_password
from django.views.decorators.cache import never_cache
# User App.

from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.schemas import AutoSchema
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action

# Project
from common.response import Response
from common.pagination import BasePageNumberPagination

# API APP
from apps.api.generics import APIView

# Self
from .models import AuthToken, User
from .serializers.user import AuthTokenSerializer, UserListSerializer, UserModifySerializer


class UserViewSet(ModelViewSet, APIView):
    """
    用户管理：增删改查
    """
    perms_name = 'user'

    queryset = User.objects.all()
    serializer_class = UserListSerializer
    pagination_class = BasePageNumberPagination
    ordering_fields = ('id',)
    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        # 根据请求类型动态变更serializer
        if self.action in ('list', 'retrieve'):
            return UserListSerializer
        else:
            return UserModifySerializer

    def create(self, request, *args, **kwargs):
        # # 创建用户默认添加密码
        # if request.data.get('password', '') == '':
        #     request.data['password'] = '123456'
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def destroy(self, request, *args, **kwargs):
        # 删除用户时删除其他表关联的用户
        instance = self.get_object()
        id = str(kwargs['pk'])
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=['POST'], detail=True, permission_classes=[IsAuthenticated],
            url_path='change_password', url_name='change_password')
    def set_password(self, request, pk=None):
        old_password = request.data['old_password']
        new_password = request.data['new_password']
        new_password_confirm = request.data['new_password_confirm']

        if old_password == new_password:
            return Response('新旧密码需不一致!', status=status.HTTP_400_BAD_REQUEST)

        if new_password != new_password_confirm:
            return Response('新密码两次输入不一致!', status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.filter(id=pk, is_active=True).first()
        if not user:
            return Response('用户错误!', status=status.HTTP_400_BAD_REQUEST)

        if check_password(old_password, user.password):
            user.set_password(new_password_confirm)
            user.save()
            return Response('密码修改成功!')
        else:
            return Response('旧密码错误!', status=status.HTTP_400_BAD_REQUEST)


class AuthTokenView(APIView):
    """
    获取token
    权限: 非登录用户也可访问
    """

    # schema = AutoSchema(
    #     manual_fields={
    #         coreapi.Field(name="username", required=True, location='form',
    #                       schema=coreschema.String(title='用户名', description="必填, 指定用户名")),
    #         coreapi.Field(name="password", required=True, location='form',
    #                       schema=coreschema.String(title='密码', description="必填, 指定用户密码")),
    #     }
    # )

    authentication_classes = ()
    permission_classes = (AllowAny,)
    serializer_class = AuthTokenSerializer
    model = AuthToken

    def get_serializer(self, *args, **kwargs):
        serializer = self.serializer_class(*args, **kwargs)
        if hasattr(self, '_raw_data_form_marker'):
            for name, field in serializer.fields.items():
                if getattr(field, 'read_only', None):
                    del serializer.fields[name]

            serializer._data = self.update_raw_data(serializer.data)
        return serializer

    @never_cache
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            request_hash = AuthToken.get_request_hash(self.request)
            # data = {'user': serializer.validated_data['user'].id,
            #         'ip': self.request.META.get('HTTP_X_FORWARDED_FOR', '')}
            # if data['ip']:
            #     data['ip'] = data['ip'].split(',')[0]
            # else:
            #     data['ip'] = self.request.META.get('REMOTE_ADDR', '')
            #
            # data['ua'] = self.request.META.get('HTTP_USER_AGENT', '')
            # data['os'] = self.request.META.get('OS', '')
            # data['name'] = self.request.META.get('USERNAME', '')
            # data['domain'] = self.request.META.get('USERDOMAIN', '')
            # user_log = UserLoginLogListSerializer(data=data)

            try:
                # 查询token
                token = AuthToken.objects.filter(user=serializer.validated_data['user'], request_hash=request_hash,
                                                 expires__gt=now(), reason='')[0]
                token.refresh()
            except IndexError:
                # 创建token
                token = AuthToken.objects.create(user=serializer.validated_data['user'], request_hash=request_hash)
                # 将超出限制数量的token设置不可用
                invalid_tokens = AuthToken.get_tokens_over_limit(serializer.validated_data['user'])
                for t in invalid_tokens:
                    t.invalidate(reason='limit_reached')

            # 设置headers
            headers = {'Auth-Token-Timeout': int(settings.AUTH_TOKEN_EXPIRATION),
                       'Pragma': 'no-cache'}

            return Response({'username': serializer.data['username'], 'token': token.key, 'expires': token.expires},
                            headers=headers)

        # 验证失败
        if 'username' in request.data:
            pass
        return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)

    def delete(self, request, *args, **kwargs):
        if 'HTTP_AUTHORIZATION' in request.META:
            token_match = re.match('Token\\s(.+)', request.META['HTTP_AUTHORIZATION'])
            if token_match:
                filter_tokens = AuthToken.objects.filter(key=token_match.groups()[0], reason="")
                if filter_tokens:
                    filter_tokens[0].invalidate(reason='logout_reached')
        return Response(status=status.HTTP_204_NO_CONTENT)