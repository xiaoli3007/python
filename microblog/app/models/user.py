#coding=utf-8
from app import app, bcrypt, db
import re
from sqlalchemy.ext.hybrid import hybrid_property

# enable_search = True
# import flask_whooshalchemy as whooshalchemy

ROLE_USER = 0
ROLE_ADMIN = 1


def __repr__(self):
    return '<Post %r>' % (self.body)


followers = db.Table('followers',
                     db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
                     db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
                     )

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(64), unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    about_me = db.Column(db.String(140))
    avatar = db.Column(db.String(120))
    last_seen = db.Column(db.DateTime)
    _password = db.Column(db.String(128))
    email_confirmed = db.Column(db.SmallInteger, default=0)
    @hybrid_property
    def password(self):
        return self._password

    @password.setter
    def _set_password(self, plaintext):
        self._password = bcrypt.generate_password_hash(plaintext)

    followed = db.relationship('User',
                               secondary=followers,
                               primaryjoin=(followers.c.follower_id == id),
                               secondaryjoin=(followers.c.followed_id == id),
                               backref=db.backref('followers', lazy='dynamic'),
                               lazy='dynamic')


    # 验证密码
    def is_correct_password(self, plaintext):
        return bcrypt.check_password_hash(self._password, plaintext)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)

    def get_avatar(self):
        if self.avatar is None:
            return  ''
        else:
            return '/uploads/' + self.avatar.encode('utf-8')

    # ...用户昵称的重复处理
    @staticmethod
    def make_unique_nickname(nickname):
        if User.query.filter_by(nickname=nickname).first() == None:
            return nickname
        version = 2
        while True:
            new_nickname = nickname + str(version)
            if User.query.filter_by(nickname=new_nickname).first() == None:
                break
            version += 1
        return new_nickname

    @staticmethod
    def make_valid_nickname(nickname):
        return re.sub('[^a-zA-Z0-9_\.]', '', nickname)
    # ...
    def __repr__(self):
        return '<User %r>' % (self.nickname)

    # ...
    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)
            return self

    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)
            return self

    def is_following(self, user):
        return self.followed.filter(followers.c.followed_id == user.id).count() > 0
    #...
    def followed_posts(self):
        return Post.query.join(followers, (followers.c.followed_id == Post.user_id)).filter(followers.c.follower_id == self.id).order_by(Post.timestamp.desc())


class Post(db.Model):
    # __tablename__ = 'post'
    # __searchable__ = ['title', 'body']
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(255))
    description = db.Column(db.String(255))
    body = db.Column(db.Text)
    timestamp = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


# if enable_search:
#     whooshalchemy.whoosh_index(app, Post)