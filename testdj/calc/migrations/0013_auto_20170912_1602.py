# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-09-12 08:02
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('calc', '0012_video'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='video',
            name='addtime',
        ),
        migrations.AddField(
            model_name='video',
            name='add_time',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='\u6d4b\u8bd5\u65f6\u95f4'),
        ),
        migrations.AddField(
            model_name='video',
            name='update_time',
            field=models.DateField(auto_now=True, null=True, verbose_name='\u66f4\u65b0\u65f6\u95f4'),
        ),
    ]
