"""minicms URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin

from DjangoUeditor import urls as DjangoUeditor_urls
from news import views as new_views
from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [
    url(r'^$', new_views.index, name='index'),
    url(r'^column/(?P<column_slug>[^/]+)/$', new_views.column_detail, name='column'),
    url(r'^news/(?P<article_slug>[^/]+)/$', new_views.article_detail, name='article'),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^ueditor/', include(DjangoUeditor_urls)),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)