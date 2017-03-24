#coding:utf-8
from django.shortcuts import render
from django.http import HttpResponse

def add(request):
    # a = request.GET.get('a', 0)
    b = request.GET['b']
    a = request.GET['a']
    c = int(a)+int(b)
    return HttpResponse(str(c))
