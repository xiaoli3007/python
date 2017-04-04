#coding:utf-8
from django.shortcuts import render
from django.http import HttpResponse
import json,os
from django.conf import settings
from calc.models import User,PhotoData,Photo
from django.core.paginator import Paginator,InvalidPage,EmptyPage,PageNotAnInteger
from django.core.exceptions import ObjectDoesNotExist

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

    try:
        photo = Photo.objects.get(id=id)
    except ObjectDoesNotExist:
        return HttpResponse("Either the entry or blog doesn't exist.")

    # return HttpResponse(photo);
    user = photo.user
    column = PhotoData.objects.filter(photo=photo)
    return render(request, 'calc/photo.html', {'column': column,'photo': photo,'user': user})





#个人主页
def applist(request):
    page = request.GET.get('page', 1)
    pagesize = 5
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
        result_dict['id'] = item.id
        result_dict['item_result'] = item_result
        result_dict_all.append(result_dict)

    tinydict = {'name': 'john', 'code': 6734, 'dept': 'sales'}

    callback = request.GET.get('callback', '')

    # result = "%s(%s)" % (callback, json.dumps(result_dict_all))
    result = "%s" % ( json.dumps(result_dict_all))

    # return HttpResponse( json.dumps(result_list), content_type='application/json')
    # response = HttpResponse(json.dumps({"key": "value", "key2": "value"}))
    # response["Access-Control-Allow-Origin"] = "*"
    # response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
    # response["Access-Control-Max-Age"] = "1000"
    # response["Access-Control-Allow-Headers"] = "*"

    response = HttpResponse(result, content_type='application/json')
    response["Access-Control-Allow-Origin"] = "*"
    return response

#个人主页
def app_photo_show(request):

    id = request.GET.get('id', 1)
    # photo = Photo.objects.get(id=id)
    try:
        photo = Photo.objects.get(id=id)
    except ObjectDoesNotExist:
        return HttpResponse("Either the entry or blog doesn't exist.")

    p_datas = PhotoData.objects.filter(photo=photo).order_by('-id')
    item_result = []
    for item in p_datas:
        if(item.filepath is  not None):
            item_result.append("/media/photo/%s/%d/%s" % (photo.user.name, photo.id, item.filepath) )

    result_dict = dict()
    result_dict['title'] = photo.title.encode('utf-8')
    result_dict['item_result'] = item_result

    callback = request.GET.get('callback', '')
    # result = "%s(%s)" % (callback, json.dumps(result_dict))
    result = "%s" % ( json.dumps(result_dict))
    response = HttpResponse(result, content_type='application/json')
    response["Access-Control-Allow-Origin"] = "*"
    return response



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