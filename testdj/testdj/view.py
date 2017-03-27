#coding:utf-8
from django.shortcuts import render
from django.http import HttpResponse
from calc.models import User,PhotoData,Photo


def index(request):
    # return HttpResponse("nnnnrdd方法rrr")
    columns = User.objects.all()
    return render(request, 'index.html', {'columns': columns})


