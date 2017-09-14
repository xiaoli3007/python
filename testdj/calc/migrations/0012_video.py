# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-09-12 07:57
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('calc', '0011_auto_20170417_1720'),
    ]

    operations = [
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='\u6807\u9898')),
                ('guid', models.CharField(default='', max_length=255, verbose_name='guid')),
                ('filepath', models.CharField(default='', max_length=255, null=True, verbose_name='\u89c6\u9891\u8def\u5f84')),
                ('addtime', models.IntegerField(default=0, null=True, verbose_name='\u53d1\u5e03\u65f6\u95f4')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='calc.User')),
            ],
            options={
                'verbose_name': '\u89c6\u9891',
                'verbose_name_plural': '\u89c6\u9891',
            },
        ),
    ]
