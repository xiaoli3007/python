# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-17 08:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calc', '0008_blogphoto_guid'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogphoto',
            name='source_url',
            field=models.CharField(default='', max_length=255, verbose_name='\u6765\u6e90\u5730\u5740'),
        ),
    ]
