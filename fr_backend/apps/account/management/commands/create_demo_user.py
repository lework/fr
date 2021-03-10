# Django
from django.core.management.base import BaseCommand

# APP
from apps.account.models import User


class Command(BaseCommand):
    help = 'Create demo user'

    def handle(self, *args, **kwargs):
        data = {
            "name": "超级管理员"
        }

        try:
            User.objects.create_superuser(username='admin', email='admin@test.com', password='admin123', **data)
            self.stdout.write(self.style.SUCCESS("创建超级管理员: admin/admin123"))
        except Exception as e:
            self.stdout.write(self.style.ERROR('创建超级管理员 %s ' % str(e)))
