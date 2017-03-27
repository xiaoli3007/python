#coding:utf-8
from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
from django.core.urlresolvers import reverse
# Create your models here.
import datetime

class User(models.Model):
    name = models.CharField(u'姓名', max_length=100)
    url = models.CharField(u'网址', max_length=255)
    blognums = models.IntegerField(u'博客数目', default=11)
    show = models.BooleanField(u'是否显示', default=True)
    pub_date = models.DateTimeField(u'添加时间', auto_now=True, editable=True)

    def __unicode__(self):
        # 在Python3中使用 def __str__(self)
        return self.name

    def get_absolute_url(self):
        return reverse('home', args=(self.id,1,))

    class Meta:
        verbose_name = '用户管理'
        verbose_name_plural = '用户管理'

class Blog(models.Model):
    title = models.CharField(u'标题', max_length=255)
    description = models.CharField(u'描述', max_length=255)
    body = models.TextField(u'内容')
    pub_date = models.DateTimeField('发表时间', auto_now_add=True, editable=True)
    update_time = models.DateField('更新时间', auto_now=True, null=True)
    test_time = models.DateTimeField('测试时间', default=timezone.now)
    user = models.ForeignKey(User)
    def __unicode__(self):
        # 在Python3中使用 def __str__(self)
        return self.title

    class Meta:
        verbose_name = '博客管理'
        verbose_name_plural = '博客管理'

class Photo(models.Model):
    title = models.CharField(u'图片标题', max_length=255)
    addtime = models.IntegerField(u'发布时间', default=0)
    user = models.ForeignKey(User)
    def __unicode__(self):
        # 在Python3中使用 def __str__(self)
        return self.title

    def get_absolute_url(self):
        return reverse('photo', args=(self.id,))

    class Meta:
        verbose_name = '相册管理'
        verbose_name_plural = '相册管理'

class PhotoData(models.Model):
    thumb = models.CharField(u'缩略图网址', max_length=255)
    filepath = models.CharField(u'缩略图网址', max_length=255,null=True)
    photo = models.ForeignKey(Photo)

    class Meta:
        verbose_name = '照片管理'
        verbose_name_plural = '照片管理'