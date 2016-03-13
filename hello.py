# coding=utf-8
import os
from flask import Flask, render_template, session, redirect, url_for, flash
from flask.ext.script import Manager
from flask.ext.bootstrap import Bootstrap
from flask.ext.moment import Moment
# 导入表单扩展
from flask.ext.wtf import Form
# 导入表单字段
from wtforms import StringField, SubmitField
# 导入表单验证函数
from wtforms.validators import Required
from flask.ext.sqlalchemy import SQLAlchemy

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
# 跨站伪造保护密钥
app.config['SECRET_KEY'] = 'hard to guess string'
app.config['SQLALCHEMY_DATABASE_URI'] =\
    'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True

manager = Manager(app)
bootstrap = Bootstrap(app)
moment = Moment(app)
db = SQLAlchemy(app)

# 定义模型，类中的属性对应数据库表中的列
class Role(db.Model):
    # 定义表名
    __tablename__ = 'roles'
    # 定义id主键的属性，第一参数列类型，表示普通整数；第二参数列选项，表示此列是表的主键
    id = db.Column(db.Integer, primary_key=True)
    # 定义name列的属性，第一参数64位变长字符串类型，第二参数此列不允许出现重复的值
    name = db.Column(db.String(64), unique=True)
    '''实例化将返回与角色相关联的用户组成的列表;
    第一参数,表明这个关系的另一端是哪个模型;
    第二参数,向User模型中添加反向引用;
    第三参数,不加载记录，但提供加载记录的查询'''
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __repr__(self):
        '''此方法返回一个具有可读性的字符串表示模型。可在调试和测试时使用'''
        return '<Role %r>' % self.name

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    # 第三参数为此列创建索引，提升查询效率
    username = db.Column(db.String(64), unique=True, index=True)
    # 定义外键建立起关系，第一参数普通整数类型，第二参数表明此列的值是roles表中行的id值
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def __repr__(self):
        return '<User %r>' % self.username

class NameForm(Form):
    '''定义表单类'''
    # 存储在表单中输入的数据，表单被提交后，这个变量会存在用户回话中，即seesion['name']
    name = StringField('What is your name?', validators=[Required()])
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
        # 获取用户会话name键的值，如果该键不存在会返回None
        old_name = session.get('name')
        # 存储在用户会话中的数据和表单提交的数据进行比较，如果两个数据不一样，调用flash函数
        if old_name is not None and old_name != form.name.data:
            # 响应一段消息
            flash('Looks like you have changed your name!')
        # 将表单提交的数据保存在用户会话中
        session['name'] = form.name.data
        # http重定向响应到index函数
        return redirect(url_for('index'))
    return render_template('index.html', form=form, name=session.get('name'))

if __name__ == '__main__':
    manager.run()