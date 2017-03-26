#coding:utf-8
from django.test import TestCase
import unittest
from calc.models import Blog, User


class TestDivision(TestCase):
    def test_insert(self):

        user = User.objects.get(show=1)
        # 方法 1
        # Blog.objects.create(title="zhangsan", description="tuweizhong@163.com", user=user)
        #
        # # 方法 2
        # twz = Blog(title="lisi", description="tuweizhong@163.com", user=user)
        # twz.save()
        #
        # # 方法 3
        # twz = Blog()
        # twz.title = "wangwu"
        # twz.description = "tuweizhong@163.com"
        # twz.user = user
        # twz.save()
        #
        # # 方法 4，首先尝试获取，不存在就创建，可以防止重复
        # Blog.objects.get_or_create(title="zhaoliu", description="tuweizhong@163.com", user=user)
        # 返回值(object, True/False)

    # def test_int2(self):
    #     self.assertEqual(division_funtion(9, 4), 2.25)
    #
    # def test_float(self):
    #     self.assertEqual(division_funtion(4.2, 3), 1.4)


if __name__ == '__main__':
    unittest.main()
