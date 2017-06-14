# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-06-05 04:01
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('school_name', models.CharField(blank=True, default='', max_length=20, verbose_name='학교')),
                ('grade', models.IntegerField(choices=[(1, '중1학년'), (2, '중2학년'), (3, '중3학년'), (4, '고1학년'), (5, '고2학년'), (6, '고3학년'), (7, '졸업'), (0, '모름')], default=0, verbose_name='학년')),
                ('level', models.IntegerField(choices=[(1, '중1초급'), (2, '중1중급'), (3, '중1상급'), (4, '중2초급'), (5, '중2중급'), (6, '중2상급'), (7, '중3초급'), (8, '중3중급'), (9, '중3상급'), (10, '고1초급'), (12, '고1중급'), (13, '고1상급'), (14, '고2초급'), (15, '고2중급'), (16, '고2상급'), (17, '고3초급'), (18, '고3중급'), (19, '고3상급'), (20, '수능'), (0, '모름')], default=0, verbose_name='학생 레벨')),
                ('is_activated', models.BooleanField(default=True)),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('update_date', models.DateTimeField(auto_now=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '학생 정보',
                'verbose_name_plural': '학생 정보',
            },
        ),
    ]
