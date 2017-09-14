#coding:utf-8
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Testse(models.Model):
    thumb = models.CharField(u'缩略图网址11', max_length=255)
    filepath = models.CharField(u'缩略图网址2222', max_length=255,null=True)
    app_name = models.CharField(u'应用名', max_length=32, db_column='app_name2', default='')
    app_name3 = models.SmallIntegerField(u'应用名222',  default=0)
    app_name4 = models.BooleanField(u'应用名333', max_length=2, default=0)
    app_name5 = models.EmailField(u'邮箱', max_length=80, default=0)
    app_name6 = models.DecimalField(u'积分',  max_digits=5, decimal_places=2, default=0.00)
    app_name7 = models.SlugField(u'邮箱222', max_length=50, default=0)

    class Meta:
        db_table = "testse"
        verbose_name = '信息统计111'
        verbose_name_plural = '信息统计222'