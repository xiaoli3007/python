# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-17 08:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calc', '0007_auto_20170417_1039'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogphoto',
            name='guid',
            field=models.CharField(default='', max_length=255, verbose_name='guid'),
        ),
    ]
