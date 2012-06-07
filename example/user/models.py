# coding=utf-8

import hashlib
from datetime import datetime
from flaskext.sqlalchemy import BaseQuery
from ..extensions import db


class UserQ(BaseQuery):
    """User.query.xxx方法乱入
    """
    def get_by_account(self, input):
        return self.filter_by(account=input).first()

class User(db.Model):
    """通用用户帐号，可根据项目需要做调整
    """
    __tablename__ = 'user'
    
    query_class = UserQ
    
    id = db.Column(db.Integer, primary_key=True)
    account = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(32), nullable=False)
    reg_at = db.Column(db.DateTime, default=datetime.now, nullable=False)

    __mapper_args__ = {
        'order_by': id.desc(),
    }

    def __init__(self, *args, **kwargs):
        super(User, self).__init__(*args, **kwargs)
        
    def __unicode__(self):
        return '(account: %s | id: %d)' % (self.account, self.id)

    def is_active(self):
        return True
    
    def is_authenticated(self):
        return True
    
    def is_anonymous(self):
        return False
    
    def get_id(self):
        return unicode(self.id)
        
    def set_password(self, password):
        self.password = hashlib.md5(password).hexdigest()

    def check_password(self, password):
        if self.password is None:
            return False
        return self.password == hashlib.md5(password).hexdigest()
        
        
class UserRole(db.Model):
    """用户角色，一个用户可拥有多个角色
    """
    __tablename__ = 'user_role'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(10), nullable=False)
    
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    user = db.relationship(User, backref='role_list')
    
    def __init__(self, *args, **kwargs):
        super(UserRole, self).__init__(*args, **kwargs)
    






    
    
    