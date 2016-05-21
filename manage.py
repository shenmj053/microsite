#!/usr/bin/env python
#_*_coding: utf-8 _*_
import os
from app import create_app, db
from app.models import User, Role, Post, Permission, Follow
from flask.ext.script import Manager, Shell
from flask.ext.migrate import Migrate, MigrateCommand

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app,db)

def make_shell_context():
    return dict(app=app, db=db, User=User, Role=Role, Post=Post, Follow=Follow, Permission=Permission)
manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)

@manager.command  #修饰的函数名就是命令名,即test
def test():
    """Run the unit tests"""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)

@manager.command
def deploy():
    '''Run deployment tasks.'''
    from flask.ext.migrate import upgrade
    from app.models import Role, User

    upgrade()
    Role.inser_roles()
    User.add_self_follows()


if __name__ == '__main__':
    #app.run(debug=True)
    manager.run()