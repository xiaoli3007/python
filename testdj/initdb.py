#coding:utf-8
# @Date    : 2016-11-26 19:10:14
# @Author  : Weizhong Tu (mail@tuweizhong.com)
# @Link    : http://www.tuweizhong.com
# @Version : 0.0.1
from __future__ import unicode_literals
import random
from testdj.wsgi import *

from calc.models import Blog,User

author_name_list = ['WeizhongTu', 'twz915', 'dachui', 'zhe', 'zhen']
article_title_list = ['Django 教程', 'Python 教程', 'HTML 教程']


def create_authors():

    user1 = User.objects.get(id=1)
    # print(user1)
    for author_name in author_name_list:
        author, created = Blog.objects.get_or_create(title=author_name,user=user1)
        # 随机生成9位数的QQ，
        author.body = ''.join(
            str(random.choice(range(10))) for _ in range(9)
        )
        author.description = 'addr_%s' % (random.randrange(1, 3))
        author.save()

def update_authors():

    pass


def main():
    create_authors()


if __name__ == '__main__':
    main()
    print("Done!")
