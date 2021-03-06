# Generated by Django 3.1.7 on 2021-03-09 15:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accident', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='record',
            name='created_by',
            field=models.ForeignKey(default=None, editable=False, help_text='创建者', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="{'class': 'record', 'model_name': 'record', 'app_label': 'accident'}(class)s_created+", to=settings.AUTH_USER_MODEL, verbose_name='创建者'),
        ),
        migrations.AddField(
            model_name='record',
            name='event',
            field=models.ForeignKey(help_text='事件', on_delete=django.db.models.deletion.CASCADE, related_name="{'class': 'record', 'model_name': 'record', 'app_label': 'accident'}(class)s_event+", to='accident.event', verbose_name='事件'),
        ),
        migrations.AddField(
            model_name='record',
            name='modified_by',
            field=models.ForeignKey(default=None, editable=False, help_text='修改者', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="{'class': 'record', 'model_name': 'record', 'app_label': 'accident'}(class)s_modified+", to=settings.AUTH_USER_MODEL, verbose_name='修改者'),
        ),
        migrations.AddField(
            model_name='event',
            name='created_by',
            field=models.ForeignKey(default=None, editable=False, help_text='创建者', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="{'class': 'event', 'model_name': 'event', 'app_label': 'accident'}(class)s_created+", to=settings.AUTH_USER_MODEL, verbose_name='创建者'),
        ),
        migrations.AddField(
            model_name='event',
            name='modified_by',
            field=models.ForeignKey(default=None, editable=False, help_text='修改者', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="{'class': 'event', 'model_name': 'event', 'app_label': 'accident'}(class)s_modified+", to=settings.AUTH_USER_MODEL, verbose_name='修改者'),
        ),
    ]
