#coding=utf-8
from flask import Flask
from flask_login import LoginManager
from flask_openid import OpenID
from flask_sqlalchemy import SQLAlchemy
import os
from config import basedir

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app, use_native_unicode="utf8")
lm = LoginManager()
lm.init_app(app)
lm.login_view = 'member.login'
oid = OpenID(app, os.path.join(basedir, 'tmp'))

from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)        #加密类

from flask_mail import Mail
mail = Mail(app)

if not app.debug:
    import logging
    from logging.handlers import RotatingFileHandler
    file_handler = RotatingFileHandler('tmp/microblog.log', 'a', 1 * 1024 * 1024, 10)
    file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('microblog startup')



from app.views import index
from app.views import member
app.register_blueprint(member.mod)


from app.models import user,photo

if __name__ == "__main__":
    app.run(host='0.0.0.0')
    # app.run(host='192.168.1.103', port=5000, debug=True)