#coding=utf-8


from flask import render_template, flash, redirect, session, url_for, request

from app.models import Photo,PhotoData
from flask import Blueprint

# pagination
POSTS_PER_PAGE = 10

mod = Blueprint('find', __name__, url_prefix='/find')

@mod.route('/', methods=['GET', 'POST'])
@mod.route('/<int:page>')
def index(page=1):
    # 获取pagination对象
    pagination = Photo.query.order_by(Photo.id.asc()).paginate(page, per_page=POSTS_PER_PAGE, error_out=False)
    list_left=[]
    list_right=[]
    for i, v in enumerate(pagination.items):
        item = {}
        item['id'] = v.id
        item['title'] = v.title
        detail = v.photodatas.first()
        if detail is not None:
            item['filepath']=detail.filepath
            if i < 5:
                list_left.append(item)
            else:
                list_right.append(item)
    #return render_template('content/test.html', page=page)
    return render_template('find/index.html',
                           pagination=pagination,list_left=list_left,list_right=list_right
                           )

@mod.route('/detail', methods=['GET', 'POST'])
@mod.route('/detail/<int:id>')
def detail(id):
    detail = Photo.query.filter_by(id=id).first_or_404()
    detail_list = detail.photodatas.all()

    list_left = []
    list_right = []
    for i, v in enumerate(detail_list):
        item = {}
        item['photo_id'] = v.photo_id
        item['filepath'] = v.filepath
        if item['filepath'] != '':
            if i < len(detail_list)/2:
                list_left.append(item)
            else:
                list_right.append(item)
    #flash(list_left)
    #return render_template('content/test.html')
    return render_template('find/detail.html',
                           detail=detail,list_left=list_left,list_right=list_right
                           )

