#coding:utf-8
from django.conf import settings
import django.http as http
import sys
from django.views.debug import technical_500_response
import logging

LOG_LEVEL_DICT = {'debug': logging.DEBUG,
                  'info': logging.INFO,
                  'warning': logging.WARNING,
                  'error': logging.ERROR,
                  'critical': logging.CRITICAL}
log_file_path = 'log/testdj.log'


class BlockedIpMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.


    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        # 调用 view 之前的代码

        self.log_console_show_flag = 1
        logger = logging.getLogger()
        logger.setLevel(LOG_LEVEL_DICT['info'])
        formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')

        file_log_handle = logging.FileHandler(log_file_path)
        file_log_handle.setFormatter(formatter)
        file_log_handle.setLevel(LOG_LEVEL_DICT['debug'])
        logger.addHandler(file_log_handle)

        if self.log_console_show_flag:
            console_log_handle = logging.StreamHandler()
            console_log_handle.setFormatter(formatter)
            console_log_handle.setLevel(LOG_LEVEL_DICT['warning'])
            logger.addHandler(console_log_handle)

        self.logger_object = logger

        response = self.get_response(request)
        # self.logger_object.info("信息： %s" % ( request.META ))
        if request.META['REMOTE_ADDR'] in getattr(settings, "BLOCKED_IPS", []):
            return http.HttpResponseForbidden('<h1>Forbidden</h1>')
        # Code to be executed for each request/response after
        # the view is called.
        # 调用 view 之后的代码

        return response

# 管理员看的到
class UserBasedExceptionMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.
    def __call__(self, request):
        response = self.get_response(request)
        if request.user.is_superuser:
            return technical_500_response(request, *sys.exc_info())
        return response
