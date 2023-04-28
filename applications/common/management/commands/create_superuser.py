import os

from django.contrib.auth.models import Group
from django.core.management import BaseCommand
from django.db.transaction import atomic

from applications.user.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.create_superuser()
        self.create_groups()

    @atomic
    def create_superuser(self):

        u, is_created = User.objects.get_or_create(
            mobile_number='09123456789',
            defaults={'mobile_number': '09123456789',
                      'is_active': True,
                      'is_staff': True,
                      'is_superuser': True,
                      })
        if not is_created:
            print(f'root user already created: {u.username} ')
        else:
            u.set_password(os.getenv("ROOT_USER_PASSWORD", default="123"))
            u.save()
            print(f'root user created:{u.username}')

    @atomic()
    def create_groups(self):
        groups = [
            os.getenv('OPERATOR_GROUP', default="Operators"),
            os.getenv('ADMINISTRATE_GROUP', default="Administrate"),
            os.getenv('PLAYER_GROUP', default="Player"),
        ]
        for name in groups:
            g, is_created = Group.objects.get_or_create(name=name)
            print(f"group `{g.name}` creation status is: {is_created}")
