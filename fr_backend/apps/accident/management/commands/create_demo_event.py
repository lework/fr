# Django
from django.core.management.base import BaseCommand

# APP
from apps.accident.models import Event, Record
from apps.account.models import User


class Command(BaseCommand):
    help = 'Create demo event'

    def handle(self, *args, **kwargs):
        user_obj = User.objects.all().first()
        if not user_obj:
            self.stdout.write(self.style.ERROR('未找到系统用户，请先创建用户'))
            return

        event_data = {
            'sn': 'SJ20210307100200',
            'name': "测试事件: APP端登录出现500错误",
            'level': 0,
            'current_state': 6,
            'description': "经监控报警和验证发现，APP端登录的时候，随机出现登录500的错误。",
            'current_operator': '超级管理员',
            'related_resources': 'APP后端系统，认证系统',
            'occurrence_date': '2021-03-07 10:00:00',
            'created_by': user_obj,
            'modified_by': user_obj,
            'created': '2021-03-07 10:02:00',
            'modified': '2021-03-07 11:12:00',
        }

        record_data = [{
            'title': '事件新建',
            'description': "第一条事件记录！",
            'state': 0,
            'current_operator': '系统创建',
            'created_by': user_obj,
            'modified_by': user_obj,
            'created': '2021-03-07 10:02:00',
            'modified': '2021-03-07 10:02:00',
        },
            {
            'title': '查找问题中',
            'description': "已联系开发，测试一起查找问题中",
            'state': 1,
            'current_operator': '超级管理员',
            'created_by': user_obj,
            'modified_by': user_obj,
            'created': '2021-03-07 10:03:00',
            'modified': '2021-03-07 10:03:00',
        }, {
            'title': '线上已临时回滚',
            'description': "经查看最近变更记录，主要是更新代码，已回滚至上一版代码",
            'state': 2,
            'current_operator': '超级管理员',
            'created_by': user_obj,
            'modified_by': user_obj,
            'created': '2021-03-07 10:03:00',
            'modified': '2021-03-07 10:03:00',
        }, {
            'title': '已找到代码中的问题，修复中',
            'description': "已找到代码中的问题，开发在修复中",
            'state': 3,
            'current_operator': '超级管理员',
            'created_by': user_obj,
            'modified_by': user_obj,
            'created': '2021-03-07 10:06:00',
            'modified': '2021-03-07 10:06:00'
        }, {
            'title': '修正代码已测试完成，准备发布',
            'description': "修正代码已测试完成，准备发布",
            'state': 4,
            'current_operator': '超级管理员',
            'created_by': user_obj,
            'modified_by': user_obj,
            'created': '2021-03-07 10:09:00',
            'modified': '2021-03-07 10:09:00'
        }, {
            'title': '代码已上线',
            'description': "代码已上线，预计观察线上1小时情况",
            'state': 5,
            'current_operator': '超级管理员',
            'created_by': user_obj,
            'modified_by': user_obj,
            'created': '2021-03-07 10:10:00',
            'modified': '2021-03-07 10:10:00'
        }, {
                'title': '事件结束',
                'description': "此事件已结束！",
                'state': 6,
                'current_operator': '系统创建',
                'created_by': user_obj,
                'modified_by': user_obj,
                'created': '2021-03-07 11:12:00',
                'modified': '2021-03-07 11:12:00',
            },
        ]

        self.stdout.write(self.style.SUCCESS('############ 创建Demo事件: %s ###########' % event_data['name']))
        event_obj = None
        try:
            event_obj = Event.objects.create(**event_data)
        except Exception as e:
            self.stdout.write(self.style.ERROR('创建Demo事件错误 %s' % str(e)))
        if event_obj:
            for item in record_data:
                self.stdout.write(self.style.SUCCESS('创建Demo记录: %s' % item['title']))
                try:
                    Record.objects.create(event=event_obj, **item)
                except Exception as e:
                    self.stdout.write(self.style.ERROR('创建Demo记录错误 %s' % str(e)))

        self.stdout.write(self.style.SUCCESS('############ 完成Demo事件 ###########'))
