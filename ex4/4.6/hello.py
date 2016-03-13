# coding=utf-8
# 导入flask，jinja2模板，用户回话，http重定向，urk映射，flash消息
from flask import Flask, render_template, session, redirect, url_for, flash
from flask.ext.script import Manager
from flask.ext.bootstrap import Bootstrap
from flask.ext.moment import Moment
from flask.ext.wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import Required

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'

manager = Manager(app)
bootstrap = Bootstrap(app)
moment = Moment(app)

# 定义表单类
class NameForm(Form):
    # 存储在表单中输入的数据，表单被提交后，这个变量会存在用户回话中，即seesion['name']
    name = StringField('What is your name?', validators=[Required()])
    # 提交按钮
    submit = SubmitField('Submit')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


@app.route('/', methods=['GET', 'POST'])
def index():
    # 定义表单类的实例化
    form = NameForm()
    # 如果表单输入不为空，开始处理表单提交的数据
    if form.validate_on_submit():
        # 从用户会话中读取‘name’键的值，如果该键不存在会返会返回None
        old_name = session.get('name')
        # 存储在用户会话中的数据和表单提交中的数据进行比较，如果两个名字不一样，调用flash函数
        if old_name is not None and old_name != form.name.data:
            # 响应一段消息（此消息需要通过模板渲染，模板中使用get_flashed_messages()函数）
            flash('Looks like you have changed your name!')
        # 将表单提交的数据保存在用户会话中
        session['name'] = form.name.data
        # http重定向响应到index函数
        return redirect(url_for('index'))
    return render_template('index.html', form=form, name=session.get('name'))

# 调试模式，当代码改动自动刷新浏览器，脚本加入“dev”参数
@manager.command
def dev():
    from livereload import Server
    live_server = Server(app.wsgi_app)
    live_server.watch('**/*.*')
    live_server.serve(open_url=True)

if __name__ == '__main__':
    manager.run()