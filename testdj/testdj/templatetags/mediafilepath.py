#coding:utf-8
from django import template
from django.utils.html import format_html
import platform
register = template.Library()
# from django.conf import settings
# MEDIA_IMAGE_URL = settings.MEDIA_IMAGE_URL  # 媒体目录
@register.filter
def myupper(value):
    return value.upper()


@register.simple_tag
def page_guess(current_page, loop_num):
    offset = abs(current_page - loop_num)
    if offset < 3:
        if current_page == loop_num:
            page_element = '<li class="active"><a href="?page=%s">%s</a></li>' % (loop_num, loop_num)

        else:
            page_element = '<li class=""><a href="?page=%s">%s</a></li>' % (loop_num, loop_num)

        return format_html(page_element)
    else:
        return ''

@register.simple_tag
def urlfilepath(filepath, size, filetype):

    sysstr = platform.system()

    if size!='0':
        ext = '_tposter_%s_0.jpg' % (size)
    else:
        ext = '_poster.jpg'

    if filetype ==0:
        ext = ''

    if (sysstr == "Windows"):
        returnpath = "/static/%s%s" % (filepath, ext)
    else:
        returnpath = "/mediafile/%s%s" % (filepath, ext)


    return  returnpath


