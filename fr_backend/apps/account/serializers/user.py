# Python
import re
import logging

# Django
from django.contrib.auth import authenticate
from django.utils.translation import gettext as _

# Django REST framework
from rest_framework import serializers

# Account APP
from apps.account.models import User

logger = logging.getLogger('fr.main.middleware')


class UserListSerializer(serializers.ModelSerializer):
    """
    用户列表的序列化
    """
    class Meta:
        model = User
        fields = ['id', 'username', 'name', 'phone', 'email', 'is_active', 'is_superuser', 'last_login', 'date_joined']


class UserModifySerializer(serializers.ModelSerializer):
    """
    用户编辑的序列化
    """
    phone = serializers.CharField(max_length=11, required=False, allow_null=True, allow_blank=True)
    password = serializers.CharField(write_only=True, label=_('用户密码'), help_text=_('密码'), required=False,
                                     allow_null=True, allow_blank=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'name', 'password', 'phone', 'email', 'is_active', 'is_superuser', 'last_login', 'date_joined']

    def validate_username(self, username):
        if User.objects.filter(username=username).exclude(id=self.context['request'].data.get('id')):
            raise serializers.ValidationError(username + ' 账号已存在')
        return username

    def validate_phone(self, phone):
        if phone:
            REGEX_phone = "^1[358]\d{9}$|^147\d{8}$|^176\d{8}$"
            if not re.match(REGEX_phone, phone):
                raise serializers.ValidationError("手机号码不合法")
        return phone

    def update(self, instance, validated_data):
        new_password = validated_data.pop('password', None)
        instance = super(UserModifySerializer, self).update(instance, validated_data)

        if new_password:
            instance.set_password(new_password)
            instance.save(update_fields=['password'])

        return instance

    def create(self, validated_data):
        new_password = validated_data.pop('password', None)
        instance = super(UserModifySerializer, self).create(validated_data)
        if new_password:
            instance.set_password(new_password)
            instance.save(update_fields=['password'])
        elif not instance.password:
            instance.set_unusable_password()
            instance.save(update_fields=['password'])

        return instance


class AuthTokenSerializer(serializers.Serializer):
    """
    用于验证用户名和密码的正确性
    """
    username = serializers.CharField(help_text=_('用户名'))
    password = serializers.CharField(help_text=_('密码'))

    def validate(self, attrs):
        username = attrs.get('username', '')
        password = attrs.get('password', '')

        if username and password:
            user = authenticate(request=self.context.get('request'),
                                username=username, password=password)
            if not user:
                logger.warning("用户名:%s 或密码:%s 错误", username, password)
                raise serializers.ValidationError(_('用户名或密码错误.'), code='authorization')
        else:
            raise serializers.ValidationError(_('需要用户名和密码信息.'), code='authorization')

        attrs['user'] = user
        return attrs
