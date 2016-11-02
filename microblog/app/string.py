#coding=utf-8

from urllib import unquote


def sting_utf8(text):
    return text.decode('utf8')

def gbkutf8(text):
    _str = unquote(text)
    _str = _str.decode('gbk').encode('utf-8')
    return _str

