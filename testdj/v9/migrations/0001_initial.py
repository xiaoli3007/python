# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-27 02:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Testse',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('thumb', models.CharField(max_length=255, verbose_name='\u7f29\u7565\u56fe\u7f51\u574011')),
                ('filepath', models.CharField(max_length=255, null=True, verbose_name='\u7f29\u7565\u56fe\u7f51\u57402222')),
                ('app_name', models.CharField(db_column='app_name2', default='', max_length=32, verbose_name='\u5e94\u7528\u540d')),
                ('app_name3', models.SmallIntegerField(default=0, verbose_name='\u5e94\u7528\u540d222')),
                ('app_name4', models.BooleanField(default=0, max_length=2, verbose_name='\u5e94\u7528\u540d333')),
                ('app_name5', models.EmailField(default=0, max_length=80, verbose_name='\u90ae\u7bb1')),
                ('app_name6', models.DecimalField(decimal_places=2, default=0.0, max_digits=5, verbose_name='\u79ef\u5206')),
                ('app_name7', models.SlugField(default=0, verbose_name='\u90ae\u7bb1222')),
            ],
            options={
                'db_table': 'testse',
                'verbose_name': '\u4fe1\u606f\u7edf\u8ba1111',
                'verbose_name_plural': '\u4fe1\u606f\u7edf\u8ba1222',
            },
        ),
    ]
