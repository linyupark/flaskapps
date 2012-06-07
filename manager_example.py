# coding=utf-8

from flaskext.script import Manager, Server, Shell, prompt_bool
from example import app
from example.extensions import db

# 脚本管理
script_manager = Manager(app)
script_manager.add_command('runserver', Server('0.0.0.0', port=5000))

def _make_context():
    return { 'db':db }
script_manager.add_command("shell", Shell(make_context=_make_context))

@script_manager.command
def createall():
    "Creates database tables"
    db.create_all()

@script_manager.command
def dropall():
    "Drops all database tables"
    if prompt_bool("Are you sure ? You will lose all your data !"):
        db.drop_all()

if __name__ == '__main__':
    script_manager.run()