# coding=utf-8

from models import User
from flaskext.wtf import Form, BooleanField, PasswordField, SelectField, \
                         TextField, DateField, required, email, equal_to, \
                         ValidationError



class LoginForm(Form):
    
    account = TextField(u'帐号', validators=[required(message=u'请填写帐号')])
    password = PasswordField(u'密码', validators=[required(message=u'请填写密码')])
    remember = BooleanField(u'自动登录')
    
    def validate_account(self, field):
        user = User.query.get_by_account(field.data)
        if user is None:
            raise ValidationError(u'此帐号不存在')



class RegisterForm(LoginForm):
    
    account = TextField(u'帐号',
        validators=[
            required(message=u'请填写帐号'),
            email(message=u'请确认帐号格式为电子邮箱')])
    
    repeat_password = PasswordField(u'确认密码',
        validators=[equal_to('password', message=u'确认密码需要跟密码一致')])
    
    def validate_account(self, field):
        user = User.query.get_by_account(field.data)
        if user is not None:
            raise ValidationError(u'此帐号已经存在')
