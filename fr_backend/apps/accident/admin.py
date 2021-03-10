# Django
from django.contrib import admin

# APP
from .models import *


class EventAdmin(admin.ModelAdmin):
    list_display = ('sn', 'name', 'level', 'current_state', 'current_operator','related_resources', 'created', 'modified', 'created_by', 'modified_by')
    list_filter = ['level', 'current_state', 'created']


class RecordAdmin(admin.ModelAdmin):
    list_display = ('event', 'title', 'state', 'created', 'modified', 'created_by', 'modified_by')
    list_filter = ['created']


admin.site.register(Event, EventAdmin)
admin.site.register(Record, RecordAdmin)
