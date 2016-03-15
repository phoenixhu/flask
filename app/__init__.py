#coding=utf-8
# 构造文件

from flask import Flask
from flask.ext.bootstrap import Bootstrap
from flask.ext.mail import Mail
from flask.ext.moment import Moment
from flask.ext.sqlalchemy import SQLAlchemy
from config import config

bootstrap = Bootstrap()
mail = Mail()
moment = Moment()
db = SQLAlchemy()

# 程序工厂函数
def create_app(config_name):
    app = Flask(__name__)
    # 从配置文件中导入数据库
    app.config.from_object(config[config_name])
    # 从此字典对象上调用静态函数初始化配置
    config[config_name].init_app(app)

    # 从扩展对象上调用静态函数初始化函数（此init_app与上面不同，属于扩展的内建函数）
    bootstrap.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    db.init_app(app)

    # 注册蓝本
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    # 返回创建的程序实例
    return app
