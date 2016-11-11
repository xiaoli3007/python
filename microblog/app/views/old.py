#coding=utf-8
import json
from datetime import datetime

from app.emails import send_email
from app.security import ts
from flask import render_template, flash, redirect, session, url_for, request, g, make_response ,send_from_directory
from flask_login import login_user, logout_user, current_user, login_required
from flask_sqlalchemy import get_debug_queries
from werkzeug.utils import secure_filename

import os
import re
from app import app, db, lm, oid
from app.common.string import sting_utf8
from app.forms.forms import LoginForm, EditForm,PostForm,RegForm,SearchForm
from app.models.models import User, Post
from config import DATABASE_QUERY_TIMEOUT
from uploader import Uploader

# pagination
POSTS_PER_PAGE = 5

@lm.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.before_request
def before_request():
    g.user = current_user
    if g.user.is_authenticated:
        g.user.last_seen = datetime.utcnow()
        db.session.add(g.user)
        db.session.commit()
        g.search_form = SearchForm()

#请求后的数据库分析
@app.after_request
def after_request(response):
    for query in get_debug_queries():
        if query.duration >= DATABASE_QUERY_TIMEOUT:
            app.logger.warning("SLOW QUERY: %s\nParameters: %s\nDuration: %fs\nContext: %s\n" % (query.statement, query.parameters, query.duration, query.context))
    return response

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@app.route('/index/<int:page>', methods = ['GET', 'POST'])
@login_required
def index(page = 1):
    pagination = g.user.followed_posts().paginate(page, POSTS_PER_PAGE, False)
    #pagination = Post.query.order_by(Post.timestamp.desc()).paginate(page, POSTS_PER_PAGE, False)
    return render_template('content/index.html',
                           title = 'Home',
                           pagination = pagination)

@app.route('/search', methods = ['POST'])
@login_required
def search():
    if not g.search_form.validate_on_submit():
        return redirect(url_for('index'))
    return redirect(url_for('search_results', query = g.search_form.search.data))

@app.route('/search_results/<query>', methods=['GET'])
@login_required
def search_results(query):
    flash(query)
    results = Post.query.whoosh_search(query, 50).all()
    flash(results)
    return render_template('content/search_results.html',
                           query = query,
                           results = results)

@app.route('/login', methods = ['GET', 'POST'])
@oid.loginhandler
def login():
    if g.user is not None and g.user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first_or_404()
        session['remember_me'] = form.remember_me.data

        if user.is_correct_password(form.password.data):
            login_user(user)
            return  redirect(url_for('member_center',nickname=user.nickname))
        else:
            flash(sting_utf8('登录失败！'))
            return  redirect(url_for('login'))

    return render_template('member/login.html',
                           title = sting_utf8('登录'),
                           form = form,
                           providers = app.config['OPENID_PROVIDERS'])

@app.route('/reg', methods = ['GET', 'POST'])
def reg():
    if g.user is not None and g.user.is_authenticated:
        return redirect(url_for('index'))
    form = RegForm()
    if form.validate_on_submit():
        respemail = form.email.data
        respepassword = form.password.data

        nickname = ""
        if nickname is None or nickname == "":
            nickname = respemail.split('@')[0]
        nickname = User.make_valid_nickname(nickname)
        nickname = User.make_unique_nickname(nickname)
        user = User(nickname=nickname, email=respemail, password=respepassword)
        db.session.add(user)
        db.session.commit()
        newuser = User.query.filter_by(email=respemail).first_or_404()
        db.session.add(newuser.follow(newuser))  # 关注自己
        db.session.commit()
        # 发送邮件
        subject = sting_utf8("确认你的邮箱")

        token = ts.dumps(newuser.email, salt='email-confirm-key')

        confirm_url = url_for(
                'confirm_email',
                token=token,
                _external=True)

        txt = render_template(
                'member/email_confirm.txt',
                confirm_url=confirm_url)

        html = render_template(
                'member/email_confirm.html',
                confirm_url=confirm_url)

        send_email(subject, '', [newuser.email], txt, html)

        remember_me = False
        if 'remember_me' in session:
            remember_me = session['remember_me']
            session.pop('remember_me', None)
        login_user(user, remember=remember_me)

        return redirect(request.args.get('next') or url_for('index'))

    return render_template('member/reg.html',
                           title = sting_utf8('注册'),
                           form = form,
                           providers = app.config['OPENID_PROVIDERS'])

#url_for的使用  是用def 的名字 解析出来是路由
@app.route('/test')
def test():
    #pagination = user.posts.order_by(Post.timestamp.desc()).paginate(page, POSTS_PER_PAGE, False)
    kwargs = {"nickname": "dddd","aaa": "ffff"}
    path = {'nickname': '286895933'};
    page = 2
    path['page'] = page
    return render_template('content/test.html', kwargs=kwargs, path=path, page=page)

#邮箱确认
@app.route('/confirm/<token>')
def confirm_email(token):
    try:
        email = ts.loads(token, salt="email-confirm-key", max_age=86400)
    except:
        return render_template('404.html')

    user = User.query.filter_by(email=email).first_or_404()

    user.email_confirmed = True

    db.session.add(user)
    db.session.commit()

    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/user/<nickname>')
@app.route('/user/<nickname>/<int:page>')
@login_required
def user(nickname, page=1):
    user = User.query.filter_by(nickname=nickname).first()
    if user is None:
        flash('User %s not found.' % nickname)
        return redirect(url_for('index'))
    path = {'nickname': user.nickname}
    pagination = user.posts.order_by(Post.timestamp.desc()).paginate(page, POSTS_PER_PAGE, False)
    return render_template('member/user.html',
                           user=user,
                           pagination=pagination, path=path
                           )

@app.route('/member_center', methods=['GET', 'POST'])
@login_required
def member_center():
    user = User.query.filter_by(nickname=g.user.nickname).first()
    if user is None:
        flash('User %s not found.' % g.user.nickname)
        return redirect(url_for('index'))
    return render_template('member/member_center.html',
                           user=user
                           )

@app.route('/member_post_list', methods=['GET', 'POST'])
@app.route('/member_post_list/<int:page>')
@login_required
def member_post_list(page=1):
    user = User.query.filter_by(nickname=g.user.nickname).first()
    if user is None:
        flash('User %s not found.' % g.user.nickname)
        return redirect(url_for('index'))
    # 从get方法中取得页码
    #page = request.args.get('page', 1, type=int)
    #flash(page)
    pagination = user.posts.order_by(Post.timestamp.desc()).paginate(page, POSTS_PER_PAGE, False)
    # 获取pagination对象
    #pagination = Post.query.order_by(Post.timestamp.desc()).paginate(page, per_page=5, error_out=False)
    return render_template('member/member_post_list.html',
                           user=user,
                           pagination=pagination
                           )

@app.route('/post_detail', methods=['GET', 'POST'])
@app.route('/post_detail/<int:id>')
def post_detail(id):
    # 从get方法中取得页码
    detail = Post.query.filter_by(id=id).first_or_404()
    return render_template('content/post_detail.html',
                           detail=detail
                           )

@app.route('/member_post', methods=['GET', 'POST'])
@login_required
def member_post():
    user = User.query.filter_by(nickname=g.user.nickname).first()
    if user is None:
        flash('User %s not found.' % g.user.nickname)
        return redirect(url_for('index'))
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, body=form.body.data, timestamp=datetime.utcnow(), author=g.user)
        db.session.add(post)
        db.session.commit()
        flash('Your post is now live!')
        return redirect(url_for('member_post_list'))
    return render_template('member/member_post.html', user=user, form = form)


@app.route('/post_edit/<int:id>', methods=['GET', 'POST'])
@login_required
def post_edit(id):
    form = PostForm()
    detail = Post.query.filter_by(id=id).first_or_404()
    if form.validate_on_submit():
        #post = Post( title=form.title.data, body=form.body.data, timestamp=datetime.utcnow(), author=g.user)
        #Post.query.filter(Post.id == detail.id).update(post)
        detail.title = form.title.data
        detail.body = form.body.data
        detail.author = g.user
        db.session.add(detail)
        db.session.commit()
        flash('Your post is now live!')
        return redirect(url_for('member_post_list'))
    else:
        form.title.data = detail.title
        form.body.data = detail.body
    return render_template('member/member_post.html', user=user, form = form)


@app.route('/post_delete/<int:id>', methods=['GET'])
@login_required
def post_delete(id):
    detail = Post.query.filter_by(id=id).first_or_404()
    if detail is None:
        redirect(url_for('member_post_list'))
    else:
        db.session.delete(detail)
        db.session.commit()
    flash(detail.title+'delete success!')
    return redirect(url_for('member_post_list'))


@app.route('/edit', methods=['GET', 'POST'])
@login_required
def edit():
    #form = EditForm(g.user.nickname)
    form = EditForm()
    if form.validate_on_submit():

        filename = secure_filename(form.avatar.data.filename)
        form.avatar.data.save(app.config['UPLOAD_FOLDER'] + filename)

        g.user.nickname = form.nickname.data
        g.user.about_me = form.about_me.data
        g.user.avatar = filename
        # g.user.nickname = User.make_unique_nickname(form.nickname.data)
        db.session.add(g.user)
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('edit'))
    else:
        form.nickname.data = g.user.nickname
        form.about_me.data = g.user.about_me
    return render_template('member/edit.html', form=form)

@app.route('/follow/<nickname>')
@login_required
def follow(nickname):
    user = User.query.filter_by(nickname=nickname).first()
    if user is None:
        flash('User %s not found.' % nickname)
        return redirect(url_for('index'))
    if user == g.user:
        flash('You can\'t follow yourself!')
        return redirect(url_for('user', nickname=nickname))
    u = g.user.follow(user)
    if u is None:
        flash('Cannot follow ' + nickname + '.')
        return redirect(url_for('user', nickname=nickname))
    db.session.add(u)
    db.session.commit()
    flash('You are now following ' + nickname + '!')
    # ...
    #follower_notification(user, g.user)
    return redirect(url_for('user', nickname=nickname))

@app.route('/unfollow/<nickname>')
@login_required
def unfollow(nickname):
    user = User.query.filter_by(nickname=nickname).first()
    if user is None:
        flash('User %s not found.' % nickname)
        return redirect(url_for('index'))
    if user == g.user:
        flash('You can\'t unfollow yourself!')
        return redirect(url_for('user', nickname=nickname))
    u = g.user.unfollow(user)
    if u is None:
        flash('Cannot unfollow ' + nickname + '.')
        return redirect(url_for('user', nickname=nickname))
    db.session.add(u)
    db.session.commit()
    flash('You have stopped following ' + nickname + '.')
    return redirect(url_for('user', nickname=nickname))

@app.route('/upload/', methods=['GET', 'POST', 'OPTIONS'])
def upload():
    """UEditor文件上传接口

    config 配置文件
    result 返回结果
    """
    mimetype = 'application/json'
    result = {}
    action = request.args.get('action')

    # 解析JSON格式的配置文件
    with open(os.path.join(app.static_folder, 'ueditor', 'php',
                           'config.json')) as fp:
        try:
            # 删除 `/**/` 之间的注释
            CONFIG = json.loads(re.sub(r'\/\*.*\*\/', '', fp.read()))
        except:
            CONFIG = {}

    if action == 'config':
        # 初始化时，返回配置文件给客户端
        result = CONFIG

    elif action in ('uploadimage', 'uploadfile', 'uploadvideo'):
        # 图片、文件、视频上传
        if action == 'uploadimage':
            fieldName = CONFIG.get('imageFieldName')
            config = {
                "pathFormat": CONFIG['imagePathFormat'],
                "maxSize": CONFIG['imageMaxSize'],
                "allowFiles": CONFIG['imageAllowFiles']
            }
        elif action == 'uploadvideo':
            fieldName = CONFIG.get('videoFieldName')
            config = {
                "pathFormat": CONFIG['videoPathFormat'],
                "maxSize": CONFIG['videoMaxSize'],
                "allowFiles": CONFIG['videoAllowFiles']
            }
        else:
            fieldName = CONFIG.get('fileFieldName')
            config = {
                "pathFormat": CONFIG['filePathFormat'],
                "maxSize": CONFIG['fileMaxSize'],
                "allowFiles": CONFIG['fileAllowFiles']
            }

        if fieldName in request.files:
            field = request.files[fieldName]
            uploader = Uploader(field, config, app.static_folder)
            result = uploader.getFileInfo()
        else:
            result['state'] = '上传接口出错'

    elif action in ('uploadscrawl'):
        # 涂鸦上传
        fieldName = CONFIG.get('scrawlFieldName')
        config = {
            "pathFormat": CONFIG.get('scrawlPathFormat'),
            "maxSize": CONFIG.get('scrawlMaxSize'),
            "allowFiles": CONFIG.get('scrawlAllowFiles'),
            "oriName": "scrawl.png"
        }
        if fieldName in request.form:
            field = request.form[fieldName]
            uploader = Uploader(field, config, app.static_folder, 'base64')
            result = uploader.getFileInfo()
        else:
            result['state'] = '上传接口出错'

    elif action in ('catchimage'):
        config = {
            "pathFormat": CONFIG['catcherPathFormat'],
            "maxSize": CONFIG['catcherMaxSize'],
            "allowFiles": CONFIG['catcherAllowFiles'],
            "oriName": "remote.png"
        }
        fieldName = CONFIG['catcherFieldName']

        if fieldName in request.form:
            # 这里比较奇怪，远程抓图提交的表单名称不是这个
            source = []
        elif '%s[]' % fieldName in request.form:
            # 而是这个
            source = request.form.getlist('%s[]' % fieldName)

        _list = []
        for imgurl in source:
            uploader = Uploader(imgurl, config, app.static_folder, 'remote')
            info = uploader.getFileInfo()
            _list.append({
                'state': info['state'],
                'url': info['url'],
                'original': info['original'],
                'source': imgurl,
            })

        result['state'] = 'SUCCESS' if len(_list) > 0 else 'ERROR'
        result['list'] = _list

    else:
        result['state'] = '请求地址出错'

    result = json.dumps(result)

    if 'callback' in request.args:
        callback = request.args.get('callback')
        if re.match(r'^[\w_]+$', callback):
            result = '%s(%s)' % (callback, result)
            mimetype = 'application/javascript'
        else:
            result = json.dumps({'state': 'callback参数不合法'})

    res = make_response(result)
    res.mimetype = mimetype
    res.headers['Access-Control-Allow-Origin'] = '*'
    res.headers['Access-Control-Allow-Headers'] = 'X-Requested-With,X_Requested_With'
    return res

@app.route('/uploads/<filename>', methods=['GET', 'POST'])
def uploads(filename):
    # flash(send_from_directory(app.config['UPLOAD_FOLDER'],filename))
    return send_from_directory(app.config['UPLOAD_FOLDER'],filename, as_attachment=True)

@app.errorhandler(404)
def internal_error(error):
    return render_template('404.html')

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('505.html')