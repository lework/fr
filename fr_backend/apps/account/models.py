# Python
import uuid
import datetime
import hashlib
import hmac

# Django
from django.db import models, connection
from django.contrib.auth.models import AbstractUser
from django.utils.timezone import now as tz_now
from django.utils.translation import gettext as _

# Project
from common.models import CreatedModifiedModel
from fr_backend import settings

# __all__ = ['User', 'AuthToken']

REASON_CHOICES = [('', _('令牌有效')),
                  ('timeout_reached', _('令牌过期')),
                  ('limit_reached', _('已超过此用户允许的最大会话数')),
                  ('logout_reached', _('登出')),
                  ('invalid_token', _('令牌无效'))]


class User(AbstractUser):
    """
    用户表
    """
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    name = models.CharField(max_length=64, null=True, blank=True, verbose_name="姓名")
    phone = models.CharField(max_length=11, null=True, blank=True, verbose_name="手机号码")
    email = models.EmailField(max_length=32, blank=True, default='', verbose_name="邮箱")

    class Meta:
        db_table = 'user'
        verbose_name = "用户信息"
        verbose_name_plural = verbose_name
        ordering = ['id']

    def __str__(self):
        return self.name if self.name else self.username

    def get_short_name(self):
        return self.username

    def get_alias_name(self):
        return self.name


class AuthToken(CreatedModifiedModel):
    """
    用户的令牌信息
    """
    key = models.CharField(max_length=40, primary_key=True, verbose_name=_('令牌'), help_text=_('令牌'))
    user = models.ForeignKey(User, related_name='auth_tokens', on_delete=models.CASCADE,
                             verbose_name=_('用户'), help_text=_('用户'))
    expires = models.DateTimeField(default=tz_now, verbose_name=_('失效时间'), help_text=_('失效时间'))
    request_hash = models.CharField(max_length=128, blank=True, default='',
                                    verbose_name=_('浏览器标识'), help_text=_('浏览器user-agent'))
    reason = models.CharField(max_length=1024, blank=True, default='', help_text=_('令牌失效的原因'))

    class Meta:
        db_table = 'user_token'
        verbose_name = _("令牌信息")
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.user.username

    # 返回令牌失效的原因
    @staticmethod
    def reason_long(reason):
        for x in REASON_CHOICES:
            if x[0] == reason:
                return x[1]

        return None

    # 获取请求的hash值
    @classmethod
    def get_request_hash(cls, request):
        h = hashlib.sha1()
        h.update(settings.SECRET_KEY.encode('utf-8'))
        for header in settings.REMOTE_HOST_HEADERS:
            value = request.META.get(header, '').split(',')[0].strip()
            if value:
                h.update(value.encode('utf-8'))
                break

        h.update(request.META.get('HTTP_USER_AGENT', '').encode('utf-8'))
        return h.hexdigest()

    def save(self, *args, **kwargs):
        if not self.pk:
            self.refresh(save=False)
        if not self.key:
            self.key = self.generate_key()
        return super(AuthToken, self).save(*args, **kwargs)

    def refresh(self, now=None, save=True):
        if not now:
            now = tz_now()
        if not self.pk or not self.is_expired(now=now):
            self.expires = now + datetime.timedelta(seconds=settings.AUTH_TOKEN_EXPIRATION)
            if save:
                connection.on_commit(lambda: self.save(update_fields=['expires']))

    def invalidate(self, reason='timeout_reached', save=True):
        if not AuthToken.reason_long(reason):
            raise ValueError(_('指定的原因无效'))
        self.reason = reason
        if save:
            self.save()
        return reason

    @staticmethod
    def get_tokens_over_limit(user, now=None):
        if now is None:
            now = tz_now()
        invalid_tokens = AuthToken.objects.none()
        if settings.AUTH_TOKEN_PER_USER != -1:
            invalid_tokens = AuthToken.objects.filter(user=user, expires__gt=now, reason='').order_by('-created')[
                             settings.AUTH_TOKEN_PER_USER:]
        return invalid_tokens

    def generate_key(self):
        unique = uuid.uuid4()
        return hmac.new(unique.bytes, digestmod=hashlib.sha1).hexdigest()

    def is_expired(self, now=None):
        if not now:
            now = tz_now()
        return bool(self.expires < now)

    @property
    def invalidated(self):
        return bool(self.reason != '')

    def in_valid_tokens(self, now=None):
        if not now:
            now = tz_now()
        valid_n_tokens_qs = self.user.auth_tokens.filter(expires__gt=now, reason='').order_by('-created')
        if settings.AUTH_TOKEN_PER_USER != -1:
            valid_n_tokens_qs = valid_n_tokens_qs[0:settings.AUTH_TOKEN_PER_USER]
        valid_n_tokens = valid_n_tokens_qs.values_list('key', flat=True)
        return bool(self.key in valid_n_tokens)
