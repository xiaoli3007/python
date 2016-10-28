import os
basedir = os.path.abspath(os.path.dirname(__file__))

CSRF_ENABLED = True
SECRET_KEY = 'sunli3007'
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_RECORD_QUERIES = True #数据库性能分析
# slow database query threshold (in seconds)
DATABASE_QUERY_TIMEOUT = 0.5
OPENID_PROVIDERS = [
    { 'name': 'Google', 'url': 'https://www.google.com/accounts/o8/id' },
    { 'name': 'Yahoo', 'url': 'https://me.yahoo.com' },
    { 'name': 'AOL', 'url': 'http://openid.aol.com/<username>' },
    { 'name': 'Flickr', 'url': 'http://www.flickr.com/<username>' },
    { 'name': 'MyOpenID', 'url': 'https://www.myopenid.com' }]

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')


# mail server settings
MAIL_SERVER = 'smtp.163.com'
MAIL_PORT = 25
#MAIL_USE_TLS = False
#MAIL_USE_SSL = True
MAIL_USERNAME = 'xiaoli3007'
MAIL_PASSWORD = 'sunli83021726'

# administrator list
ADMINS = ['xiaoli3007@163.com']
