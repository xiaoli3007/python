# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-29 08:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calc', '0004_auto_20170329_1434'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='files',
            field=models.FileField(default='', upload_to='uploads', verbose_name='\u6587\u4ef6\u4e0a\u4f20'),
        ),
    ]
