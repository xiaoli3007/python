from flask import render_template, flash, redirect, session, url_for, request, g
from flask_login import login_user, logout_user, current_user, login_required
from app import app, db, lm, oid
from app.forms import LoginForm, EditForm,PostForm,RegForm

from app.models import User, ROLE_USER, ROLE_ADMIN,Post
from datetime import datetime
from app.emails import follower_notification,send_email
from flask_sqlalchemy import get_debug_queries
from config import DATABASE_QUERY_TIMEOUT
from app.security import ts
# pagination
POSTS_PER_PAGE = 3

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
    #posts = g.user.followed_posts().paginate(page, POSTS_PER_PAGE, False).items
    posts = g.user.followed_posts().paginate(page, POSTS_PER_PAGE, False)
    return render_template('index.html',
                           title = 'Home',
                           posts = posts)

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
            flash('登录失败！')
            return  redirect(url_for('login'))

    return render_template('login.html',
                           title = '登录',
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
        subject = "确认你的邮箱"

        token = ts.dumps(newuser.email, salt='email-confirm-key')

        confirm_url = url_for(
                'confirm_email',
                token=token,
                _external=True)

        html = render_template(
                'email_confirm.html',
                confirm_url=confirm_url)

        send_email(subject, '', newuser.email, '', html)

        remember_me = False
        if 'remember_me' in session:
            remember_me = session['remember_me']
            session.pop('remember_me', None)
        login_user(user, remember=remember_me)

        return redirect(request.args.get('next') or url_for('index'))

    return render_template('reg.html',
                           title = '注册',
                           form = form,
                           providers = app.config['OPENID_PROVIDERS'])


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

    return redirect(url_for('signin'))

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
    posts = user.posts.paginate(page, POSTS_PER_PAGE, False)
    return render_template('user.html',
                           user=user,
                           posts=posts)

@app.route('/member_center', methods=['GET', 'POST'])
@login_required
def member_center():
    user = User.query.filter_by(nickname=g.user.nickname).first()
    if user is None:
        flash('User %s not found.' % g.user.nickname)
        return redirect(url_for('index'))
    return render_template('member_center.html',
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
    posts = user.posts.paginate(page, POSTS_PER_PAGE, False)
    return render_template('member_post_list.html',
                           user=user,
                           posts=posts
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
        post = Post(body=form.post.data, timestamp=datetime.utcnow(), author=g.user)
        db.session.add(post)
        db.session.commit()
        flash('Your post is now live!')
        return redirect(url_for('member_post_list'))
    return render_template('member_post.html', user=user, form = form)

@app.route('/edit', methods=['GET', 'POST'])
@login_required
def edit():
    #form = EditForm(g.user.nickname)
    form = EditForm()
    if form.validate_on_submit():
        g.user.nickname = form.nickname.data
        g.user.about_me = form.about_me.data
        # g.user.nickname = User.make_unique_nickname(form.nickname.data)
        db.session.add(g.user)
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('edit'))
    else:
        form.nickname.data = g.user.nickname
        form.about_me.data = g.user.about_me
    return render_template('edit.html', form=form)

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
    follower_notification(user, g.user)
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

@app.errorhandler(404)
def internal_error(error):
    return render_template('404.html')

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('505.html')