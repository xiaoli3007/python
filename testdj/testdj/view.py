#coding:utf-8
from django.shortcuts import render
from django.http import HttpResponse
from calc.models import User,PhotoData,Photo,BlogPhoto
import json

def index(request):
    # return HttpResponse("nnnnrdd方法rrr")
    # columns = User.objects.all()

    getcolumns = BlogPhoto.objects.filter().order_by('?')[0:20]
    columns = []
    for item in getcolumns:
        item.local_images_paths = json.loads(item.local_images_paths)
        columns.append(item)
    # return HttpResponse(columns)
    return render(request, 'index.html', {'columns': columns})


