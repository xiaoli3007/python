# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-26 12:25
from __future__ import unicode_literals

import DjangoUeditor.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0002_auto_20150728_1232'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='content',
            field=DjangoUeditor.models.UEditorField(blank=True, default='', verbose_name='\u5185\u5bb9'),
        ),
    ]