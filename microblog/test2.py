#coding=utf-8
import os
import unittest
from datetime import datetime, timedelta
from config import basedir

basedir = os.path.abspath(os.path.dirname(__file__))

print 'sqlite:///' + os.path.join(basedir, 'app.db')

'''
class TestCase(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def mysql_test(self):

        assert 1 == 1


if __name__ == '__main__':
    unittest.main()
'''