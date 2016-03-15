#coding=utf-8

# 导入蓝本模块
from flask import Blueprint

# 创建蓝本，参数1：蓝本的名称；参数2：蓝本所在的包或模块
main = Blueprint('main', __name__)

# 导入路由视图和错误处理模块与蓝本关联起来
from . import views, errors