#-*- coding: utf-8 -*-
'''
Created by yoonju on 2017. 7. 24.
'''
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.conf import settings


class Command(BaseCommand):
    help = "Create superuser."
    def handle(self, *args, **options):
        # User = settings.AUTH_USER_MODEL
        print("check admin ----")
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'neojjang@gmail.com', 'pathf1nder!234')
            print("complete to create superuser...")
        else:
            print("Already exist admin user")
