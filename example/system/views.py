# coding=utf-8

import random, time
from datetime import datetime
from flask import Blueprint, render_template, redirect, request, url_for, \
                  current_app, abort
from ..extensions import photos

sys = Blueprint('sys', __name__)


@sys.route('/upload/', methods=['GET', 'POST'])
def upload():
    """系统内统一的文件上传入口
    """
    now = datetime.now()
    sub_folder = '%s/%s/%s' % (now.year, now.month, now.day)
    filename = None
    
    if request.method == 'POST' and 'photo' in request.files:
        
        filename = photos.save(
            request.files['photo'],
            folder=sub_folder,
            name='%d_%d.' % (time.time(), random.randint(0, 99))
        )
        
    return photos.url(filename)


@sys.route('/demo/')
def demo():
    """系统功能演示地址
    """
    return render_template('demo/upload.html')
    
    
@sys.route('/fetch/<file_type>')
def fetch(file_type):
    """系统统一文件获取
    """
    pass
