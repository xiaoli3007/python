#coding:utf-8
from django.shortcuts import render
from django.http import HttpResponse
import json,os
from django.conf import settings


BASE_DIR = settings.BASE_DIR  # 项目目录
# 假设图片放在static/pics/里面
PICS = os.listdir(os.path.join(BASE_DIR, 'common_static/pics'))

def add(request):
    # a = request.GET.get('a', 0)
    b = request.GET['b']
    a = request.GET['a']
    c = int(a)+int(b)
    return HttpResponse(str(c))

def home(request):
    return render(request, 'calc/home.html')

def get_pic(request):
    color = request.GET.get('color')
    number = request.GET.get('number')
    name = '{}_{}'.format(color, number)

    # 过滤出符合要求的图片，假设是以输入的开头的都返回
    result_list = filter(lambda x: x.startswith(name), PICS)

    print 'result_list', result_list

    return HttpResponse(
            json.dumps(result_list),
            content_type='application/json')