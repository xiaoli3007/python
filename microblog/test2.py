#coding=utf-8
import os
basedir = os.path.abspath(os.path.dirname(__file__))
#SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')


UPLOAD_FOLDER = basedir+'uploads\/'

print(UPLOAD_FOLDER)