#coding:utf-8
from django.shortcuts import render
from django.http import HttpResponse
import json,os
from django.conf import settings
from calc.models import User,PhotoData,Photo
from django.core.paginator import Paginator,InvalidPage,EmptyPage,PageNotAnInteger

BASE_DIR = settings.BASE_DIR  # 项目目录
MEDIA_ROOT = settings.MEDIA_ROOT  # 媒体目录



#个人主页
def home(request,id,page=1):
    user = User.objects.get(id=id)
    # column = Photo.objects.filter(user=user)
    page = int(page)
    pagesize = 30
    # 以下是另一种方法 未实现
    # offset = pagesize * (page - 1)
    # endsize = offset + pagesize
    # column = Photo.objects.filter(user=user).order_by('-id')[offset:endsize]
    column = Photo.objects.filter(user=user).order_by('-id')
    paginator = Paginator(column,pagesize)
    try:
        column = paginator.page(page)
    except (EmptyPage, InvalidPage, PageNotAnInteger):
        column = paginator.page(1)
    after_range_num = 5
    before_range_num = 4
    # if page >= after_range_num:
    #     page_range = paginator.page_range[page - after_range_num:page + before_range_num]
    # else:
    #     page_range = paginator.page_range[0:page + before_range_num]

    return render(request, 'calc/home.html', {'column': column, 'user': user,  'page': page})


#相册详情
def photo(request,id):

    photo = Photo.objects.get(id=id)
    user = photo.user
    column = PhotoData.objects.filter(photo=photo)
    return render(request, 'calc/photo.html', {'column': column,'photo': photo,'user': user})





#个人主页
def applist(request):
    page = request.GET.get('page', 1)
    pagesize = 30
    # 以下是另一种方法 未实现
    # offset = pagesize * (page - 1)
    # endsize = offset + pagesize
    # column = Photo.objects.filter(user=user).order_by('-id')[offset:endsize]
    column = Photo.objects.filter().order_by('-id')
    paginator = Paginator(column,pagesize)
    try:
        column = paginator.page(page)
    except (EmptyPage, InvalidPage, PageNotAnInteger):
        column = paginator.page(1)


    result_dict_all = []

    for item in column.object_list:
        p_datas = PhotoData.objects.filter(photo=item).order_by('-id')
        item_result = []
        for item_data in p_datas:
            item_result.append("/media/photo/%s/%d/%s" % (item.user.name, item.id,item_data.filepath) )

        result_dict = dict()
        result_dict['title'] = item.title.encode('utf-8')
        result_dict['addtime'] = item.addtime
        result_dict['item_result'] = item_result
        result_dict_all.append(result_dict)

    tinydict = {'name': 'john', 'code': 6734, 'dept': 'sales'}
    return HttpResponse(json.dumps(result_dict_all))
    # return HttpResponse( json.dumps(result_list), content_type='application/json')


def test2(request):

    return render(request, 'calc/test2.html')

def add(request):
    # a = request.GET.get('a', 0)
    b = request.GET['b']
    a = request.GET['a']
    c = int(a)+int(b)
    return HttpResponse(str(c))

def get_pic(request):

    # 假设图片放在static/pics/里面
    PICS = os.listdir(os.path.join(BASE_DIR, 'common_static/pics'))
    color = request.GET.get('color')
    number = request.GET.get('number')
    name = '{}_{}'.format(color, number)

    # 过滤出符合要求的图片，假设是以输入的开头的都返回
    result_list = filter(lambda x: x.startswith(name), PICS)

    print 'result_list', result_list

    return HttpResponse(
            json.dumps(result_list),
            content_type='application/json')