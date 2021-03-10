# Python
from urllib import parse

# Django
from django.conf import settings
from django.db.models import Q
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.utils.timezone import now as tz_now
from django.utils.translation import ugettext_lazy as _

# Django REST framework
from rest_framework import authentication
from rest_framework import exceptions
from rest_framework import HTTP_HEADER_ENCODING

# Self
from .models import AuthToken


UserModel = get_user_model()


class CustomBackend(ModelBackend):
    """
    自定义登录认证，使其支持username，phone，email登录
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None:
            username = kwargs.get(UserModel.USERNAME_FIELD)
        if username is None or password is None:
            return
        try:
            user = UserModel._default_manager.get(Q(username=username) | Q(phone=username) | Q(email=username))
        except UserModel.DoesNotExist:
            # Run the default password hasher once to reduce the timing
            # difference between an existing and a nonexistent user (#20760).
            UserModel().set_password(password)
        else:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user


class TokenAuthentication(authentication.TokenAuthentication):
    """
     自定义令牌验证，使其支持过期时间
    """
    model = AuthToken

    # 获取header中的token
    @staticmethod
    def _get_x_auth_token_header(request):
        auth = request.META.get('HTTP_X_AUTH_TOKEN', '')
        if isinstance(auth, type('')):
            auth = auth.encode(HTTP_HEADER_ENCODING)
        return auth

    # 获取cookie中的token
    @staticmethod
    def _get_auth_token_cookie(request):
        token = request.COOKIES.get('token', '')
        if token:
            token = parse.unquote(token).strip('"')
            return 'token %s' % token
        return ''

    # 获取token
    def authenticate(self, request):
        self.request = request
        auth = TokenAuthentication._get_x_auth_token_header(request).split()
        if not auth or auth[0].lower() != b'token':
            auth = authentication.get_authorization_header(request).split()
            if auth and auth[0].lower() == b'basic':
                return None
            if not auth or auth[0].lower() != b'token':
                auth = TokenAuthentication._get_auth_token_cookie(request).split()
                if not auth or auth[0].lower() != b'token':
                    return None
        if len(auth) == 1:
            msg = _('Invalid token header. No credentials provided.')
            raise exceptions.AuthenticationFailed(msg)
        elif len(auth) > 2:
            msg = _('Invalid token header. Token string should not contain spaces.')
            raise exceptions.AuthenticationFailed(msg)
        return self.authenticate_credentials(auth[1].decode('utf-8'))

    # 验证token
    def authenticate_credentials(self, key):
        now = tz_now()
        try:
            request_hash = self.model.get_request_hash(self.request)
            token = self.model.objects.select_related('user').get(key=key, request_hash=request_hash)
        except self.model.DoesNotExist:
            raise exceptions.AuthenticationFailed(AuthToken.reason_long('invalid_token'))

        # 检查token是否有失效原因
        if token.invalidated:
            raise exceptions.AuthenticationFailed(AuthToken.reason_long(token.reason))
        # 检查token是否过期
        if token.is_expired(now=now):
            token.invalidate(reason='timeout_reached')
            raise exceptions.AuthenticationFailed(AuthToken.reason_long('timeout_reached'))
        # 检查用户的token数量限制
        if settings.AUTH_TOKEN_PER_USER != -1:
            if not token.in_valid_tokens(now=now):
                token.invalidate(reason='limit_reached')
                raise exceptions.AuthenticationFailed(AuthToken.reason_long('limit_reached'))
        # 检查用户状态是否为激活
        if not token.user.is_active:
            raise exceptions.AuthenticationFailed(_('User inactive or deleted'))
        # 刷新token的失效时间
        token.refresh(now=now)
        return token.user, token
