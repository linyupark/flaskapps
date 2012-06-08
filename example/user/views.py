# coding=utf-8

from flask import Blueprint, render_template, redirect, request, url_for, \
                  current_app
from flaskext.login import login_required, login_user, logout_user
from flaskext.principal import Identity, identity_changed
from forms import LoginForm, RegisterForm
from models import User
from ..extensions import db, staff_permission, admin_permission, user_permission

user = Blueprint('user', __name__)


@user.route('/')
@login_required
def index():
    """用户列表
    """
    return u'用户列表页面'
    
    
@user.route('/login/', methods=['GET', 'POST'])
def login():
    """用户登录
    """
    form = LoginForm()
    
    if form.validate_on_submit():
        user = User.query.get_by_account(form.account.data)
        login_user(user)
        identity_changed.send(current_app._get_current_object(),
                              identity=Identity(user.id))
        return redirect(request.args.get('next') or url_for('user.index'))
    
    return render_template('user/login.html', form=form)
    
    
@user.route('/register/', methods=['GET', 'POST'])
def register():
    """用户注册
    """
    form = RegisterForm()
    
    if form.validate_on_submit():
        user = User(
            account=form.account.data,
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        
    return render_template("user/register.html", form=form)
    

@user.route('/test_role/<role>')
def test_role(role):
    """测试用户角色权限
    """
    if(role == 'staff'):
        with staff_permission.require(403):
            return 'your are staff!'
    
    if(role == 'admin'):
        with admin_permission.require(403):
            return 'you are admin!'
        
    if(role == 'user'):
        with user_permission.require(403):
            return 'user!'
        
    return 'No Role Name %s!' % role
    
