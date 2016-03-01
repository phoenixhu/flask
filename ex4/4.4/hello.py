# coding=utf-8
# 导入Flask及jinja2模板
from flask import Flask, render_template
# 导入命令行解析器
from flask.ext.script import Manager
# 导入前端框架
from flask.ext.bootstrap import Bootstrap
# 导入时间戳
from flask.ext.moment import Moment
# 导入跨站请求伪造保护
from flask.ext.wtf import Form
# 导入文本字段和提交按钮
from wtforms import StringField, SubmitField
# 导入验证函数，确保提交的字段不为空
from wtforms.validators import Required

# 初始化
app = Flask(__name__)
# 设置跨站请求伪造保护密钥
app.config['SECRET_KEY'] = 'hard to guess string'

# 实例化
manager = Manager(app)
bootstrap = Bootstrap(app)
moment = Moment(app)

# 定义表单类
class NameForm(Form):
    # 定义文本字段对象，验证函数Required()确保输入的内容不为空
    name = StringField('What is your name?', validators=[Required()])
    # 定义提交按钮对象
    submit = SubmitField('Submit')

# 定义404页面
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

# 定义500页面
@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

# 的定义首页路由，支持GET及POST请求方法
@app.route('/', methods=['GET', 'POST'])
# 定义首页视图函数
def index():
    # 存放表单中输入的数据，如果没有输入其值为None
    name = None
    # 定义表单类的实例化
    form = NameForm()
    # 如果表单中输入的数据能被验证函数接受（不为空），返回值为True，否则为Flase，当返回值为True开始处理表单提交的数据
    if form.validate_on_submit():
        # 获取用户输入的数据
        name = form.name.data
        # 清空表单中数据
        form.name.data = ''
    # 渲染模板
    return render_template('index.html', form=form, name=name)

if __name__ == '__main__':
    manager.run()