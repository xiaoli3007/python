#coding=utf-8

from datetime import datetime
from app.common.emails import send_email
from app.common.security import ts
from flask import render_template, flash, redirect, session, url_for, request, g, make_response ,send_from_directory
from flask_login import login_user, logout_user, login_required
from werkzeug.utils import secure_filename
from app import app, db, lm, oid
from app.common.string import sting_utf8
from app.forms import LoginForm, EditForm,PostForm,RegForm
from app.models import User, Post
from flask import Blueprint

# pagination
POSTS_PER_PAGE = 5

mod = Blueprint('member', __name__, url_prefix='/member')


@lm.user_loader
def load_user(id):
    return User.query.get(int(id))


@mod.route('/login', methods = ['GET', 'POST'])
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
            return  redirect(url_for('member.member_center',nickname=user.nickname))
        else:
            flash(sting_utf8('登录失败！'))
            return  redirect(url_for('member.login'))

    return render_template('member/login.html',
                           title = sting_utf8('登录'),
                           form = form,
                           providers = app.config['OPENID_PROVIDERS'])

@mod.route('/reg', methods = ['GET', 'POST'])
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
                'member.confirm_email',
                token=token,
                _external=True)

        txt = render_template(
                'member/email_confirm.txt',
                confirm_url=confirm_url)

        html = render_template(
                'member/email_confirm.html',
                confirm_url=confirm_url)

        #send_email(subject, '', [newuser.email], txt, html)

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

#邮箱确认
@mod.route('/confirm/<token>')
def confirm_email(token):
    try:
        email = ts.loads(token, salt="email-confirm-key", max_age=86400)
    except:
        return render_template('404.html')

    user = User.query.filter_by(email=email).first_or_404()

    user.email_confirmed = True

    db.session.add(user)
    db.session.commit()

    return redirect(url_for('member.login'))

@mod.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@mod.route('/index', methods = ['GET'])
@mod.route('/index/<int:page>', methods = ['GET'])
@login_required
def index(page = 1):
    pagination = g.user.followed_posts().paginate(page, POSTS_PER_PAGE, False)
    return render_template('content/index.html',
                           title = 'Home',
                           pagination = pagination)

@mod.route('/center', methods=['GET', 'POST'])
@login_required
def member_center():
    user = User.query.filter_by(nickname=g.user.nickname).first()
    if user is None:
        flash('User %s not found.' % g.user.nickname)
        return redirect(url_for('index'))
    return render_template('member/member_center.html',
                           user=user
                           )

@mod.route('/post_list', methods=['GET', 'POST'])
@mod.route('/post_list/<int:page>')
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


@mod.route('/post', methods=['GET', 'POST'])
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
        return redirect(url_for('member.member_post_list'))
    return render_template('member/member_post.html', user=user, form = form)


@mod.route('/post_edit/<int:id>', methods=['GET', 'POST'])
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
        return redirect(url_for('member.member_post_list'))
    else:
        form.title.data = detail.title
        form.body.data = detail.body
    return render_template('member/member_post.html', form = form)


@mod.route('/post_delete/<int:id>', methods=['GET'])
@login_required
def post_delete(id):
    detail = Post.query.filter_by(id=id).first_or_404()
    if detail is None:
        redirect(url_for('member.member_post_list'))
    else:
        db.session.delete(detail)
        db.session.commit()
    flash(detail.title+'delete success!')
    return redirect(url_for('member.member_post_list'))


@mod.route('/edit', methods=['GET', 'POST'])
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
        return redirect(url_for('member.member_center'))
    else:
        form.nickname.data = g.user.nickname
        form.about_me.data = g.user.about_me
    return render_template('member/edit.html', form=form)

@mod.route('/follow/<nickname>')
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

@mod.route('/unfollow/<nickname>')
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

