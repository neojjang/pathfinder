# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-22 13:55
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0004_auto_20170422_0838'),
    ]

    operations = [
        migrations.AlterField(
            model_name='explanations',
            name='question',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='quiz.Question'),
        ),
    ]
