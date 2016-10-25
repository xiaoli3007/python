"""
WSGI config for helloword project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/howto/deployment/wsgi/
"""

'''
from django.http import HttpResponse

def hello(request):
    return HttpResponse("Hello world ! 222222222222222222222")
'''
from django.shortcuts import render

def hello(request):
    context          = {}
    context['hello'] = 'Hello World!'
    return render(request, 'hello.html', context)