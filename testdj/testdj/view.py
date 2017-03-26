#coding:utf-8
from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    # return HttpResponse("nnnnrdd方法rrr")
    return render(request, 'index.html')


