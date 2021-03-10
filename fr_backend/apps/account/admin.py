# Django
from django.contrib import admin

# Self
from .models import *


class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'name', 'phone', 'email', 'is_active', 'date_joined')
    list_filter = ['is_active', 'date_joined']


class AuthTokenAdmin(admin.ModelAdmin):
    list_display = ('user', 'key', 'expires', 'request_hash', 'reason')
    list_filter = ['expires']

    list_display_links = None  # 禁用编辑链接

    def has_add_permission(self, request):
        # 禁用添加按钮
        return False

    def has_delete_permission(self, request, obj=None):
        # 禁用删除按钮
        return False

    def get_actions(self, request):
        # 在actions中去掉 删除 操作
        actions = super(AuthTokenAdmin, self).get_actions(request)
        if request.user.username[0].upper() != 'J':
            if 'delete_selected' in actions:
                del actions['delete_selected']
        return actions


admin.site.register(User, UserAdmin)
admin.site.register(AuthToken, AuthTokenAdmin)
