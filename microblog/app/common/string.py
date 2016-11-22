#coding=utf-8

from urllib import unquote
import hashlib
import types
def sting_utf8(text):
    return text.decode('utf8')

def sting_utf82(text):
    return text.encode('utf8')

def gbkutf8(text):
    _str = unquote(text)
    _str = _str.decode('gbk').encode('utf-8')
    return _str

def md5(text):
    if type(text) is types.StringType:
        m = hashlib.md5()
        m.update(text)
        return m.hexdigest()
    else:
        return ''


