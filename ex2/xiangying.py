# coding=utf-8
from flask import Flask
from flask import make_response
# 重定向函数
from flask import redirect
from flask import abort
app = Flask(__name__)

@app.route('/')
def index():
    '''视图函数返回的响应状态码默认为200，表明这个代码已经被成功处理

    此处函数设定返回状态码为400，表示请求失败'''
    return '<h1>Bad Request</h1>', 400

@app.route('/response')
def _response():
    response = make_response('<h1>This document carries a cookie!</h1>')
    response.set_cookie('answer', '42')
    return response

@app.route('/redirect')
def _redirect():
    '''url重定向'''
    return redirect('http://www.baidu.com')

@app.route('/user/<id>')
def get_user(id):
    user = load_user(id)
    if not user:
        abort(404)
    return '<h1>Hello,%s</h1>' % user.name

if __name__ == '__main__':
    app.run(debug=True)