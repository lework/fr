# Django
from django.db import models
from django.utils.translation import gettext as _
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.utils.timezone import now

# Django-CRUM
from crum import get_current_user


class BaseModel(models.Model):
    """
    所有Model的基础类。
    """

    class Meta:
        abstract = True

    def __str__(self):
        if 'name' in self.__dict__:
            return u'%s-%s' % (self.name, self.pk)
        else:
            return u'%s-%s' % (self._meta.verbose_name, self.pk)


class CreatedModifiedModel(BaseModel):
    """
    具有添加修改日期的通用基础类，如果没有指定值则默认添加。
    """

    class Meta:
        abstract = True

    created = models.DateTimeField(default=None, editable=False, verbose_name=_('创建时间'), help_text=_('创建时间'))
    modified = models.DateTimeField(default=None, editable=False, verbose_name=_('更新时间'), help_text=_('更新时间'))

    def save(self, *args, **kwargs):
        update_fields = list(kwargs.get('update_fields', []))
        # 实现 auto_now_add 和 auto_now 逻辑.
        # not self.pk and
        if not self.created:
            self.created = now()
            if 'created' not in update_fields:
                update_fields.append('created')
        if 'modified' not in update_fields or not self.modified:
            self.modified = now()
            update_fields.append('modified')
        super(CreatedModifiedModel, self).save(*args, **kwargs)


class PrimordialModel(CreatedModifiedModel):
    """
    通用模型, 增加创建者和修改者, 还有描述字段
    """

    class Meta:
        abstract = True

    description = models.TextField(blank=True, default='', verbose_name=_("描述"), help_text=_("描述"))
    created_by = models.ForeignKey('account.User', related_name='%s(class)s_created+', default=None,
                                   null=True, editable=False, on_delete=models.SET_NULL,
                                   verbose_name=_("创建者"), help_text=_('创建者'))
    modified_by = models.ForeignKey('account.User', related_name='%s(class)s_modified+', default=None,
                                    null=True, editable=False, on_delete=models.SET_NULL,
                                    verbose_name=_("修改者"), help_text=_('修改者'))

    def save(self, *args, **kwargs):
        update_fields = kwargs.get('update_fields', [])
        user = get_current_user()
        # print(user)
        if user and not user.id:
            user = None

        if not self.pk and not self.created_by:
            self.created_by = user
            if 'created_by' not in update_fields:
                update_fields.append('created_by')

        if not self.pk and not self.modified_by:
            self.modified_by = user
            if 'modified_by' not in update_fields:
                update_fields.append('modified_by')

        super(PrimordialModel, self).save(*args, **kwargs)
        return

    def validate_unique(self, exclude=None):
        super(PrimordialModel, self).validate_unique(exclude=exclude)
        model = type(self)
        if not hasattr(model, 'SOFT_UNIQUE_TOGETHER'):
            return
        errors = []
        for ut in model.SOFT_UNIQUE_TOGETHER:
            kwargs = {}
            for field_name in ut:
                kwargs[field_name] = getattr(self, field_name, None)
            try:
                obj = model.objects.get(**kwargs)
            except ObjectDoesNotExist:
                continue
            if not (self.pk and self.pk == obj.pk):
                errors.append(
                    '%s with this (%s) combination already exists.' % (
                        model.__name__,
                        ', '.join(set(ut) - {'polymorphic_ctype'})
                    )
                )
        if errors:
            raise ValidationError(errors)


class CommonModel(PrimordialModel):
    """
    基本模型: 名称唯一
    """

    class Meta:
        abstract = True

    name = models.CharField(max_length=128, unique=True, verbose_name=_("名称"), help_text=_("名称"))


class CommonModelNameNotUnique(PrimordialModel):
    """
    基本模型: 名称不唯一
    """

    class Meta:
        abstract = True

    name = models.CharField(max_length=128, unique=False, verbose_name=_("名称"), help_text=_("名称"))
