# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-19 15:01
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0003_auto_20170419_1501'),
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='StudentExam',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('update_date', models.DateTimeField(auto_now=True)),
                ('quiz', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quiz.Quiz')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.Student')),
            ],
            options={
                'verbose_name_plural': '시험 관리',
                'verbose_name': '시험 관리',
            },
        ),
        migrations.CreateModel(
            name='StudentScore',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.PositiveSmallIntegerField(default=0, verbose_name='점수')),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('update_date', models.DateTimeField(auto_now=True)),
                ('exam', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.StudentExam')),
            ],
            options={
                'verbose_name_plural': '성적',
                'verbose_name': '성적',
            },
        ),
        migrations.RemoveField(
            model_name='studentresults',
            name='quiz',
        ),
        migrations.RemoveField(
            model_name='studentresults',
            name='student',
        ),
        migrations.DeleteModel(
            name='StudentResults',
        ),
    ]
