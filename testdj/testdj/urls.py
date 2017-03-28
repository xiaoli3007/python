"""testdj URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from . import view
from calc import views as calc_views
from django.conf.urls.static import static
from django.conf import settings
import os
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^home/(\d+)/([0-9]+)$', calc_views.home, name='home'),  # new
    url(r'^photo/(\d+)$', calc_views.photo, name='photo'),  # new
    url(r'^applist/$', calc_views.applist, name='applist'),  # new

    url(r'^add/$', calc_views.add, name='add'),
    url(r'^test2/$', calc_views.test2, name='test2'),  # new
    url(r'^get_pic/$', calc_views.get_pic, name='get-pic'),
    url(r'^$', view.index),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)