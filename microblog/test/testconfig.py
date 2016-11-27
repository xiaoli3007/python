#coding=utf-8
import os
basedir = os.path.abspath(os.path.dirname(__file__))


# SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'test2.db')
SQLALCHEMY_DATABASE_URI = 'mysql://root:123123@localhost/test2'

UPLOAD_FOLDER = os.path.join(basedir, 'uploads/')
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

