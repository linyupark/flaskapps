# coding=utf8

from flask import Flask, jsonify, render_template, request
import settings
app = Flask(__name__)
app.config.from_object(settings.Dev)


# 模块路由 blueprint注册
from user.views import user
app.register_blueprint(user, url_prefix='/u')

from system.views import sys
app.register_blueprint(sys, url_prefix='/sys')


# DB设定
from extensions import db
db.init_app(app)


# Log
if not app.debug:
    import logging
    from logging import FileHandler
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler = FileHandler('%s/app.logger.log' % app.config['APPROOT'])
    file_handler.setLevel(logging.WARNING)
    file_handler.setFormatter(formatter)
    app.logger.addHandler(file_handler)
    
    
# Auth
from flaskext.login import LoginManager
from user.models import User
login_manager = LoginManager()
login_manager.setup_app(app)
login_manager.login_message = u'请先登录'
login_manager.login_view = 'user.login'
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)
    

# Principal 权限控制器
from user.models import User
from flaskext.principal import Principal, identity_loaded, RoleNeed, \
                               UserNeed
principals = Principal(app)

@identity_loaded.connect_via(app)
def on_identity_loaded(sender, identity):
    user = User.query.get(identity.name)
    for role in user.role_list:
        identity.provides.add(RoleNeed(role.name))
    identity.provides.add(UserNeed(user.id))


# 上传组件
from extensions import photos
from flaskext.uploads import configure_uploads, patch_request_class
configure_uploads(app, (photos, ))
patch_request_class(app, app.config['UPLOADS_MAXSIZE'])


# 自定义错误页面
@app.errorhandler(403)
def access_forbidden(error):
    if request.is_xhr:
        return jsonify(error_code='403')
    return render_template("_403.html")

@app.errorhandler(404)
def page_not_found(error):
    if request.is_xhr:
        return jsonify(error_code='404')
    return render_template("_404.html")

@app.errorhandler(500)
def server_error(error):
    if request.is_xhr:
        return jsonify(error_code='500')
    return render_template("_500.html")
    
    
    
    
    
    
    
    
    
    
    
    