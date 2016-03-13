# coding=utf-8

from flask import Flask
# 请求上下文，封装了客户端发出的HTTP请求中的内容
from flask import request
# 初始化，把接收自客户端的所有请求都转交给这个对象处理
app = Flask(__name__)

# 路由，处理URL和函数之间关系的程序
@app.route('/')
# 视图函数
def index():
    return '<h1>Hello World!</h1>'

# “<>”中的内容为动态部分，内容会作为参数传入到视图函数中
@app.route('/user/<name>')
def user(name):
    return '<h1>Hello,%s!' % name

@app.route('/request')
def _request():
    '''获取http请求头部中UA部分的内容'''

    user_agent = request.headers.get('User-Agent')
    return '<p>You browser is %s</p>' % user_agent

# 启动服务器
if __name__ == '__main__':
    app.run(debug=True)
