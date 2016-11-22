#!/usr/bin/env python
# -*- coding: utf-8 -*-

# -*- coding: utf-8 -*-

"""
    config.py
    ~~~~~~~~~~~

    basic configuration

    :copyright: (c) 2013.
    :license: BSD, see LICENSE for more details.
"""


DEBUG = True

# configuration page num
PER_PAGE = 10

# configuration mysql
SQLALCHEMY_DATABASE_URI = "mysql://%s:%s@%s/%s" % ('root', 'root', '127.0.0.1', 'test')

SECRET_KEY = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
USERNAME = 'admin'
PASSWORD = 'admin'

UPLOAD_FOLDER = './static/upload/'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

RECAPTCHA_PUBLIC_KEY = '6LeJTt8SAAAAACuSjRrt3a2jgGX-xQBREEAXw9Rs'
RECAPTCHA_PRIVATE_KEY = '6LeJTt8SAAAAACjz_N65vlf9yuscktZZjOIEISFA'