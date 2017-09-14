# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-17 09:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calc', '0009_blogphoto_source_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogphoto',
            name='local_default_image',
            field=models.CharField(default='', max_length=255, verbose_name='\u9ed8\u8ba4\u56fe\u7247\u672c\u5730'),
        ),
        migrations.AlterField(
            model_name='blogphoto',
            name='local_images_paths',
            field=models.TextField(default='', verbose_name='\u672c\u5730\u56fe\u7247\u8def\u5f84\u6c47\u603b'),
        ),
        migrations.AlterField(
            model_name='blogphoto',
            name='remote_default_image',
            field=models.CharField(default='', max_length=255, verbose_name='\u9ed8\u8ba4\u56fe\u7247\u8fdc\u7a0b'),
        ),
        migrations.AlterField(
            model_name='blogphoto',
            name='remote_images_paths',
            field=models.TextField(default='', verbose_name='\u8fdc\u7a0b\u56fe\u7247\u8def\u5f84\u6c47\u603b'),
        ),
    ]