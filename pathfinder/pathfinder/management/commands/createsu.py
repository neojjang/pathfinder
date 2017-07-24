#-*- coding: utf-8 -*-
'''
Created by yoonju on 2017. 7. 24.
'''
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.conf import settings


class Command(BaseCommand):
    def handle(self, *args, **options):
        # User = settings.AUTH_USER_MODEL
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'neojjang@gmail.com', 'pathf1nder!234')
