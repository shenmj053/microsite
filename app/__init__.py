#_*_coding: utf-8 _*_

#程序包的构造文件
from flask import Flask
from flask.ext.bootstrap import Bootstrap
from flask.ext.moment import Moment
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.mail import Mail
from flask.ext.login import LoginManager
from flask.ext.pagedown import PageDown
#从配置文件config.py中导入config字典
from config import config
#移到下面的函数中,延迟创建
#app = Flask(__name__)

bootstrap = Bootstrap()
moment = Moment()
db = SQLAlchemy()
mail = Mail()
pagedown = PageDown()
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'

def create_app(config_name):
    #将第9行的创建程序实例移过来,从而延迟创建
    app = Flask(__name__)
    #从config字典中导入配置
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    bootstrap.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    db.init_app(app)
    pagedown.init_app(app)
    login_manager.init_app(app)


    from .main import main as main_blueprint
    #注册main蓝本
    app.register_blueprint(main_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')  #路由加上指定的前缀

    from .api_1_0 import api as api_1_0_blueprint
    app.register_blueprint(api_1_0_blueprint, url_prefix='/api/v1.0')

    #工厂函数返回创建的程序实例,程序时在运行时创建的
    return app
