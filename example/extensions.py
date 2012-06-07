# coding=utf-8

# 数据库
from flaskext.sqlalchemy import SQLAlchemy
db = SQLAlchemy()

# 上传组件
from flaskext.uploads import UploadSet, IMAGES
photos = UploadSet('photos', IMAGES)

# Roles
from flaskext.principal import Permission, RoleNeed
admin_permission = Permission(RoleNeed('admin'))
staff_permission = Permission(RoleNeed('staff'))
user_permission = Permission(RoleNeed('user'))