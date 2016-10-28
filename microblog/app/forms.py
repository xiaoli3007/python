from flask_wtf import FlaskForm
from wtforms import TextField, BooleanField, TextAreaField,StringField,PasswordField
from wtforms.validators import Required, Length,DataRequired, Email,EqualTo
from app.models import User
from app.util import Unique

class RegForm(FlaskForm):
    email = StringField('email', validators = [DataRequired(), Email('邮箱格式不对！'),
                                               Unique(
                                                       User,
                                                       User.email,
                                                       message='There is already an account with that nickname.')
                                               ])
    #password = StringField('password', validators = [DataRequired()])
    password = PasswordField('password', [
        DataRequired(),
        EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('confirmpassword')
    accept_tos = BooleanField('I accept the TOS', [DataRequired()])


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = StringField('password', validators=[DataRequired()])

class EditForm(FlaskForm):
    about_me = TextAreaField('about_me', validators = [Length(min = 0, max = 140)])
    nickname = StringField('nickname', validators=[DataRequired(),
                                             Unique(
                                                     User,
                                                     User.nickname,
                                                     message='There is already an account with that nickname.')])
'''
    def __init__(self, original_nickname, *args, **kwargs):
        FlaskForm.__init__(self, *args, **kwargs)
        self.original_nickname = original_nickname

    def validate(self):
        if not FlaskForm.validate(self):
            return False
        if self.nickname.data == self.original_nickname:
            return True
        if self.nickname.data != User.make_valid_nickname(self.nickname.data):
            self.nickname.errors.append('This nickname has invalid characters. Please use letters, numbers, dots and underscores only.')
            return False
        user = User.query.filter_by(nickname = self.nickname.data).first()
        if user != None:
            self.nickname.errors.append('This nickname is already in use. Please choose another one.')
            return False
        return True
'''
'''
        def validate_nickname(self, field):
                if field.data == 'jhon':
                    # 抛出的异常提示可作为提示显示
                    self.nickname.errors.append('This nickname is already in use. Please choose another one.')
                    return False
 '''
class PostForm(FlaskForm):
    post = StringField('post', validators=[DataRequired()])