# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-22 08:38
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0002_auto_20170417_1551'),
    ]

    operations = [
        migrations.RenameField(
            model_name='question',
            old_name='time',
            new_name='limit_time',
        ),
    ]
