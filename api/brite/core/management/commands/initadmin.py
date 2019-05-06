import logging

from django.conf import settings
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand


class Command(BaseCommand):

    def handle(self, *args, **options):
        if User.objects.count() == 0:
            for email in settings.ADMINS:
                username = email.split('@')[0]
                password = 'Admin007!'
                logging.info(f'Creating account for ${username} (${email})')
                User.objects.create_superuser(username, email, password)
        else:
            print('Admin accounts are only initialized if no account exist')
