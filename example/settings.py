# coding=utf-8

import os

class Base(object):
    APPROOT = os.path.abspath(os.path.dirname(__file__))
    SECRET_KEY = 'example_secret_key'
    
    # upload
    UPLOADS_DEFAULT_DEST = 'example/static/uploads/'
    UPLOADS_DEFAULT_URL = 'uploads/'
    UPLOADS_MAXSIZE = 8*1024*1024

class Dev(Base):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///%s/example.db' % Base.APPROOT

class Prd(Base):
    DEBUG = False