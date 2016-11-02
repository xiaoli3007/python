#coding=utf-8
import os
import unittest
from datetime import datetime, timedelta
from config import basedir
from app import app, db
from app.models import Photo,PhotoData
class TestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'test2.db')
        db.create_all()

    def tearDown(self):

        db.session.remove()
        #db.drop_all()

    def mysql_test(self):
        basedir = os.path.abspath(os.path.dirname(__file__))
        UPLOAD_FOLDER = basedir + 'uploads\/'
        print(UPLOAD_FOLDER)
        assert 1 == 1

    def test_make_user(self):
        # create a user and write it to the database
        u = Photo(title = '1111', timestamp = datetime.utcnow() + timedelta(seconds=1))
        db.session.add(u)
        u2 = PhotoData(thumb='aaaaaaaaaaaaaa.jpg', author=u)
        db.session.add(u2)
        db.session.commit()


if __name__ == '__main__':
    unittest.main()