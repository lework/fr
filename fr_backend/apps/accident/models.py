# Django
from django.db import models
from django.utils.translation import gettext as _

# Project
from common.models import CommonModelNameNotUnique, PrimordialModel

STATE_CHOICES = [
    (0, _('打开')),
    (1, _('定位中')),
    (2, _('线上已恢复')),
    (3, _('解决中')),
    (4, _('上线中')),
    (5, _('观察中')),
    (6, _('结束')),
]

LEVEL_CHOICES = [
    (0, _('紧急')),
    (1, _('中等')),
    (2, _('一般'))
]


class Event(CommonModelNameNotUnique):
    sn = models.CharField(unique=True, max_length=64, verbose_name=_('编号'), help_text=_('编号'))
    level = models.IntegerField(choices=LEVEL_CHOICES, default=2, verbose_name=_('级别'), help_text=str(LEVEL_CHOICES))
    current_state = models.IntegerField(choices=STATE_CHOICES, default=0, verbose_name=_('当前状态'),
                                        help_text=str(STATE_CHOICES))
    current_operator = models.CharField(max_length=64, blank=True, default='', verbose_name=_('当前操作人'), help_text=_('当前操作人'))
    related_resources = models.CharField(max_length=512, blank=True, default='', verbose_name=_('相关资源'), help_text=_('相关资源'))
    occurrence_date = models.DateTimeField(verbose_name=_('发生时间'), help_text=_('发生时间'))

    class Meta:
        verbose_name = '事件表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.sn + '_' + self.name


class Record(PrimordialModel):
    event = models.ForeignKey(Event, related_name='%s(class)s_event+', on_delete=models.CASCADE, verbose_name=_('事件'),
                              help_text=_('事件'))
    title = models.CharField(max_length=256, verbose_name=_('标题'), help_text=_('标题'))
    state = models.IntegerField(choices=STATE_CHOICES, default=0, verbose_name=_('当前状态'), help_text=str(STATE_CHOICES))
    current_operator = models.CharField(max_length=64, blank=True, default='', verbose_name=_('当前操作人'), help_text=_('当前操作人'))

    class Meta:
        verbose_name = '事件记录表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.event.sn + '_' + self.title
