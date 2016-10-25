#from flask_wtf import Form
from flask_wtf import FlaskForm
from wtforms import TextField, BooleanField, TextAreaField,StringField,PasswordField
from wtforms.validators import Required, Length,DataRequired, Email
from app.models import User
from app.util import Unique
class LoginForm(FlaskForm):
    openid = StringField('openid', validators = [DataRequired()])
    remember_me = BooleanField('remember_me', default = False)

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