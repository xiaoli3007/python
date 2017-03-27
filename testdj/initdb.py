#coding:utf-8

from __future__ import unicode_literals
import random
from testdj.wsgi import *

from calc.models import Blog,User,Photo,PhotoData
import os, sys, getopt

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

def update_photo_data():

    user1 = User.objects.get(id=1)
    ppp = Photo.objects.filter(user=user1)
    # print(user1)
    for item in ppp:
       item.title = "张三的博客 %d" % item.id
       item.save()
       print(item.id)
    # http: //127.0.0.1:8001/media/photo/zhangsan/1/51edbf498243b6c8da024d69ab3c1985.jpg
    return  True


def update_photo(file_dir):
    print(file_dir)
    g = os.walk(file_dir)
    user1 = User.objects.get(id=2)

    # author = Photo(title='aaa2', user=user1)
    # author.save()
    #
    # author2 = PhotoData(thumb='thumb222', filepath='thumb222', photo=author)
    # author2.save()
    #
    # print(author2.id)
    # for path, d, filelist in g:
    #     # print path
    #     for item in d:
    #
    #         author = Photo(title='李四的博客%s' % item, user=user1)
    #         author.save()
    #
    #         dir_name = os.path.join(path, item)
    #         # print(item.encode('utf-8'))
    #         dirs = os.listdir(dir_name)
    #         for file in dirs:
    #             print file
    #             author2 = PhotoData(thumb='thumb_%s' % file, filepath=file, photo=author)
    #             author2.save()
            # break
            # new_name =int(item.encode('utf-8'))+739
            # print(type(new_name))
            # print(new_name)
            # os.rename(os.path.join(path, item), os.path.join(path, '%d'%new_name ))
        # for filename in filelist:
        #     print os.path.join(path, filename)

    return True


def main():
    # create_authors()
    photo_dir = 'media/photo/lisi'
    photo_file = ''
    print("%s" % sys.argv[0])
    process_path = os.path.dirname(sys.argv[0])
    if not process_path:
        process_path = os.getcwd()
    os.chdir(process_path)

    try:
        opts, args = getopt.getopt(sys.argv[1:], "f:d:n:", ["file=", 'dir='])
    except getopt.GetoptError, err:
        print 'getopt except %s' % err
        sys.exit(1)
    for o, a in opts:
        if o in ("-f", "--file"):
            photo_file = a
        elif o in ("-d", "--dir"):
            photo_dir = a

    # update_photo(photo_dir)
    update_photo_data()

if __name__ == '__main__':
    main()
    print("Done!")
